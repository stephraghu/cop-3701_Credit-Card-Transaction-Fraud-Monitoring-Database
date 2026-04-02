-- Users Table
CREATE TABLE users (
    user_id    INT PRIMARY KEY,
    first_name VARCHAR2(50),
    last_name  VARCHAR2(50),
    email      VARCHAR2(100),
    phone      VARCHAR2(20)
);

-- Merchants Table
CREATE TABLE merchants (
    merchant_id INT PRIMARY KEY,
    name        VARCHAR2(100),
    category    VARCHAR2(50)
);

-- Credit Cards Table
CREATE TABLE credit_cards (
    card_number VARCHAR2(20) PRIMARY KEY,
    user_id     INT REFERENCES users(user_id),
    expiry      DATE,
    card_type   VARCHAR2(20),
    card_limit  NUMBER(15,2)
);

-- Transactions Table
CREATE TABLE transactions (
    trans_id    INT PRIMARY KEY,
    card_num    VARCHAR2(20) REFERENCES credit_cards(card_number),
    merch_id    INT REFERENCES merchants(merchant_id),

    -- Kaggle Dataset Columns
    trans_time  NUMBER,
    v1 FLOAT, v2 FLOAT, v3 FLOAT, v4 FLOAT, v5 FLOAT,
    v6 FLOAT, v7 FLOAT, v8 FLOAT, v9 FLOAT, v10 FLOAT,
    v11 FLOAT, v12 FLOAT, v13 FLOAT, v14 FLOAT, v15 FLOAT,
    v16 FLOAT, v17 FLOAT, v18 FLOAT, v19 FLOAT, v20 FLOAT,
    v21 FLOAT, v22 FLOAT, v23 FLOAT, v24 FLOAT, v25 FLOAT,
    v26 FLOAT, v27 FLOAT, v28 FLOAT,
    amount      NUMBER(15,2),
    class       INT
);