'''
COP3710 Part E by MAMSKY143 for stephraghu
(Features and UI for Credit Card Transaction Fraud Database)

Run app in terminal w/ 'streamlit run app.py'
'''

import streamlit as st
import oracledb
import pandas as pd

# --- DB CONFIG ---
## Change these to match your Oracle instance (if needed)
LIB_DIR = "instantclient_23_0"
DB_USER = "PLACEHOLDER"
DB_PASS = "PLACEHOLDER"
DB_DSN  = "PLACEHOLDER"

# --- ORACLE CLIENT INIT ---
@st.cache_resource
def init_db():
    if LIB_DIR:
        try:
            oracledb.init_oracle_client(lib_dir=LIB_DIR)
        except Exception as e:
            st.warning(f"Oracle Client init note: {e}")

init_db()

def get_connection():
    return oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)

def run_query(sql, params=None):
    """Run a SELECT and return (columns, rows). Safe for the UI layer."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
        cols = [c[0] for c in cur.description]
        rows = cur.fetchall()
        cur.close()
        return cols, rows
    finally:
        conn.close()

def show_results(cols, rows, caption=None):
    """Results as scrollable df w/ row count"""
    if not rows:
        st.info("No records matched your filter.")
        return
    df = pd.DataFrame(rows, columns=cols)
    if caption:
        st.caption(caption)
    st.write(f"**{len(df)} record(s) returned.**")
    st.dataframe(df, use_container_width=True)

# --- STREAMLIT UI ---
st.title("Credit Card Transaction Fraud Database")
st.subheader("COP3710 Part E Features And UI")

menu = ["Queries", "Read", "Create", "Update", "Delete"]
choice = st.sidebar.selectbox("Select Action", menu)

# --- QUERIES / FEATURES ---
if choice == "Queries":
    st.sidebar.markdown("---")
    query_choice = st.sidebar.radio(
        "Select Feature",
        [
            "1. Filter On Single Table",
            "2. Users And Their Credit Cards",
            "3. Credit Cards And Associated Transactions",
            "4. Transactions And Associated Merchants",
            "5. Associated Users, Credit Cards, and Transactions",
        ],
    )

    ## Query 1 Filter On Single Table
    if query_choice.startswith("1"):
        st.header("Query 1: Filter On Single Table")

        table = st.selectbox(
            "Table",
            ["Users", "Merchants", "Credit Cards", "Transactions"],
        )

        col_map = {
            "Users": [
                ("first_name", True), ("last_name", True),
                ("email", True), ("phone", True), ("user_id", False),
            ],
            "Merchants": [
                ("name", True), ("category", True), ("merchant_id", False),
            ],
            "Credit Cards": [
                ("card_type", True), ("card_number", True),
                ("user_id", False), ("card_limit", False),
            ],
            "Transactions": [
                ("CLASS", False), ("card_num", True),
                ("merch_id", False), ("amount", False), ("trans_id", False),
            ],
        }

        col_options = col_map[table]
        col_labels = [c[0] for c in col_options]
        col_choice = st.selectbox("Filter column", col_labels)
        is_text = dict(col_options)[col_choice]

        value = st.text_input(f"Value for {col_choice}")

        if st.button("Run filter"):

            base_sql = {
                "Users":        "SELECT user_id, first_name, last_name, email, phone FROM users",
                "Merchants":    "SELECT merchant_id, name, category FROM merchants",
                "Credit Cards": "SELECT card_number, user_id, card_type, card_limit, expiry FROM credit_cards",
                "Transactions": 'SELECT trans_id, card_num, merch_id, trans_time, amount, "CLASS" FROM transactions',
            }[table]

            params = {}

            if value.strip() == "":
                sql = f"{base_sql} WHERE ROWNUM <= 500"

            elif is_text:
                sql = f"{base_sql} WHERE LOWER({col_choice}) LIKE :val AND ROWNUM <= 500"
                params["val"] = f"%{value.lower()}%"

            else:
                try:
                    num_val = float(value)
                except:
                    st.error("Enter a valid number.")
                    st.stop()

                if col_choice == "CLASS":
                    sql = f'{base_sql} WHERE "CLASS" = :val'
                else:
                    sql = f"{base_sql} WHERE {col_choice} = :val"

                params["val"] = num_val

            try:
                cols, rows = run_query(sql, params)
                show_results(cols, rows)
            except Exception as e:
                st.error(f"Database error: {e}")

    ## Query 2 Users And Credit Cards
    elif query_choice.startswith("2"):
        st.header("Query 2: Users And Associated Credit Cards")

        filter_user = st.text_input("Optional user_id")

        if st.button("Run query"):
            sql = """
                SELECT u.user_id,
                       u.first_name,
                       u.last_name,
                       u.email,
                       c.card_number,
                       c.card_type,
                       c.card_limit,
                       c.expiry
                FROM users u
                JOIN credit_cards c ON u.user_id = c.user_id
            """

            params = {}

            if filter_user.strip():
                try:
                    params["user_id_val"] = int(filter_user)
                    sql += " WHERE u.user_id = :user_id_val"
                except:
                    st.error("user_id must be integer")
                    st.stop()

            sql += " ORDER BY u.user_id"

            try:
                cols, rows = run_query(sql, params)
                show_results(cols, rows)
            except Exception as e:
                st.error(f"Database error: {e}")

    ## Query 3 JOIN b/t Cards And Transactions
    elif query_choice.startswith("3"):
        st.header("Query 3: Credit Cards And Associated Transactions")

        filter_card = st.text_input("Optional card number")
        only_fraud = st.checkbox("Only fraud (CLASS = 1)")

        if st.button("Run query"):
            sql = """
                SELECT c.card_number,
                       c.card_type,
                       c.user_id,
                       t.trans_id,
                       t.trans_time,
                       t.amount,
                       t."CLASS",
                       t.merch_id
                FROM credit_cards c
                JOIN transactions t
                  ON TO_CHAR(c.card_number) = TO_CHAR(t.card_num)
            """

            conditions = []
            params = {}

            if filter_card.strip():
                conditions.append("c.card_number = :cnum")
                params["cnum"] = filter_card.strip()

            if only_fraud:
                conditions.append('t."CLASS" = 1')

            if conditions:
                sql += " WHERE " + " AND ".join(conditions)

            sql += " ORDER BY c.card_number, t.trans_id"

            try:
                cols, rows = run_query(sql, params)
                show_results(cols, rows)
            except Exception as e:
                st.error(f"Database error: {e}")

    ## Query 4 JOIN b/t Transactions And Merchants
    elif query_choice.startswith("4"):
        st.header("Query 4: Transactions And Associated Merchants")

        filter_category = st.text_input("Category (optional)")
        min_amount = st.number_input("Minimum amount", min_value=0.0)

        if st.button("Run query"):
            sql = """
                SELECT t.trans_id,
                       t.card_num,
                       t.amount,
                       t."CLASS",
                       m.merchant_id,
                       m.name,
                       m.category
                FROM transactions t
                JOIN merchants m
                  ON t.merch_id = m.merchant_id
            """

            conditions = []
            params = {}

            if filter_category.strip():
                conditions.append("LOWER(m.category) LIKE :cat")
                params["cat"] = f"%{filter_category.lower()}%"

            if min_amount > 0:
                conditions.append("t.amount >= :amt")
                params["amt"] = min_amount

            if conditions:
                sql += " WHERE " + " AND ".join(conditions)

            sql += " ORDER BY t.amount DESC"

            try:
                cols, rows = run_query(sql, params)
                show_results(cols, rows)
            except Exception as e:
                st.error(f"Database error: {e}")

    ## Query 5 JOIN b/t Users, Credit Cards, and Transactions
    elif query_choice.startswith("5"):
        st.header("Query 5: Associated Users, Credit Cards, and Transactions")

        user_id = st.text_input("User ID")

        if st.button("Run query"):
            try:
                uid = int(user_id)
            except:
                st.error("Enter a valid integer user_id")
                st.stop()

            sql = """
                SELECT u.user_id,
                       u.first_name,
                       u.last_name,
                       c.card_number,
                       c.card_type,
                       t.trans_id,
                       t.trans_time,
                       t.amount,
                       t."CLASS"
                FROM users u
                JOIN credit_cards c
                  ON u.user_id = c.user_id
                JOIN transactions t
                  ON c.card_number = t.card_num
                WHERE u.user_id = :user_id_val
                ORDER BY c.card_number, t.trans_id
            """

            try:
                cols, rows = run_query(sql, {"user_id_val": uid})

                if rows:
                    amt_idx = cols.index("AMOUNT")
                    class_idx = cols.index("CLASS")

                    total = sum(r[amt_idx] or 0 for r in rows)
                    fraud = sum(1 for r in rows if r[class_idx] == 1)

                    st.metric("Transactions", len(rows))
                    st.metric("Total Spend", f"${total:,.2f}")
                    st.metric("Fraud Count", fraud)

                show_results(cols, rows)

            except Exception as e:
                st.error(f"Database error: {e}")


# --- READ (Shows the tables and entries) ---
elif choice == "Read":
    st.write("### Database Directory")
    table_choice = st.selectbox(
        "Select Table to View",
        ["Users", "Merchants", "Credit Cards", "Transactions"],
    )
    try:
        conn = get_connection()
        cur = conn.cursor()

        if table_choice == "Users":
            query = "SELECT user_id, first_name, last_name, email FROM users"
        elif table_choice == "Merchants":
            query = "SELECT merchant_id, name, category FROM merchants"
        elif table_choice == "Credit Cards":
            query = "SELECT card_number, user_id, card_type, card_limit FROM credit_cards"
        elif table_choice == "Transactions":
            v_cols = ", ".join([f"V{i}" for i in range(1, 29)])
            query = f"SELECT trans_id, card_num, merch_id, trans_time, {v_cols}, amount, class FROM transactions"

        cur.execute(query)
        columns = [col[0] for col in cur.description]
        data = cur.fetchall()
        cur.close()
        conn.close()

        if data:
            st.write(f"Displaying {len(data)} records from **{table_choice}**")
            st.dataframe(pd.DataFrame(data, columns=columns), use_container_width=True)
        else:
            st.info(f"No records found in {table_choice}.")
    except Exception as e:
        st.error(f"Database Error: {e}")

# --- FEATURES COMING SOON... maybe ---
elif choice == "Create":
    st.write("### Create")
    st.info("This feature is coming soon.")

elif choice == "Update":
    st.write("### Update")
    st.info("This feature is coming soon.")

elif choice == "Delete":
    st.write("### Delete")
    st.info("This feature is coming soon.")

# run using: streamlit run app.py
