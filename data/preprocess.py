import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta


def preprocess_data():
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Created 'data/' directory.")

    print("Generating fake data for Users, Merchants, and Cards...")

    # Generate 100 Users
    users = pd.DataFrame({
        'user_id': range(100, 200),
        'first_name': [f'UserFirstName_{i}' for i in range(100)],
        'last_name': [f'UserLastName_{i}' for i in range(100)],
        'email': [f'student_{i}@floridapoly.edu' for i in range(100)],
        'phone': [f'863-555-{i:04d}' for i in range(100)]
    })

    # Generate 100 Merchants
    merchants = pd.DataFrame({
        'merchant_id': range(500, 600),
        'name': [f'Merchant_Store_{i}' for i in range(100)],
        'category': np.random.choice(['Retail', 'Food', 'Travel', 'Digital'], 100)
    })

    # Generate 100 Credit Cards
    cards = pd.DataFrame({
        'card_number': [f'4111{i:012d}' for i in range(100)],
        'user_id': users['user_id'],
        'expiry': [(datetime.now() + timedelta(days=365 * 3)).strftime('%Y-%m-%d') for _ in range(100)],
        'card_type': 'Visa',
        'card_limit': 5000.00
    })

    print("Processing first 100 rows from creditcard.csv...")
    try:
        # Load 100 rows from Kaggle
        kaggle_df = pd.read_csv('creditcard.csv', nrows=100)

        transactions = pd.DataFrame()
        transactions['trans_id'] = range(90000, 90000 + len(kaggle_df))

        # Random assign card & merchant to each Kaggle row
        transactions['card_num'] = np.random.choice(cards['card_number'], len(kaggle_df))
        transactions['merch_id'] = np.random.choice(merchants['merchant_id'], len(kaggle_df))

        transactions = pd.concat([transactions, kaggle_df], axis=1)

        # save to csv
        users.to_csv('data/users.csv', index=False)
        merchants.to_csv('data/merchants.csv', index=False)
        cards.to_csv('data/cards.csv', index=False)
        transactions.to_csv('data/transactions.csv', index=False)

        print("Preprocessing Complete!")
        print(f"Generated files in 'data/' folder:")
        print(f" - users.csv: {len(users)} rows")
        print(f" - merchants.csv: {len(merchants)} rows")
        print(f" - cards.csv: {len(cards)} rows")
        print(f" - transactions.csv: {len(transactions)} rows")

    except FileNotFoundError:
        print("Error: 'creditcard.csv' not found")


if __name__ == "__main__":
    preprocess_data()