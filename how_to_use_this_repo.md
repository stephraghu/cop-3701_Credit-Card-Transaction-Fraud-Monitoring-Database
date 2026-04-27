# How to Use This Repository

Follow the steps below to set up the database and run the application locally.

## 1. Create the Database

Run the SQL script to initialize your database schema:

`create_db.sql`

## 2. Configure Database Credentials (Data Loader)

Open `dataload.py` and update **lines 7–9** with your database credentials:

```python
DB_HOST = "PLACEHOLDER"
DB_USER = "PLACEHOLDER"
DB_PASSWORD = "PLACEHOLDER"
```

## 3. Populate the Database

Run the data loader script to insert sample (fake) data:

`
python dataload.py
`

## 4. Configure Database Credentials (App)

Open `app.py` and update **lines 15–17** with your database credentials:

```python
DB_HOST = "PLACEHOLDER"
DB_USER = "PLACEHOLDER"
DB_PASSWORD = "PLACEHOLDER"
```

## 5. Run the Application

Start the Streamlit app using the following command:

```bash
python -m streamlit run app.py
```

## Application Preview
## <img width="2736" height="1452" alt="Homepage" src="https://github.com/user-attachments/assets/758d0c6a-6580-47c7-902f-17a988d00fd1" />


Notes

* Make sure all required Python dependencies are installed before running the app.
* Ensure your database service is running and accessible.
* Double-check credentials if you encounter connection errors.
