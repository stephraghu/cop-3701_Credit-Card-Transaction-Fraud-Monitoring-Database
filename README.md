# Credit Card Transaction Fraud Monitoring Database

## Project Description
This project involves the design and implementation of a comprehensive relational database system for monitoring credit card transactions and proactively detecting fraudulent behavior. The system manages complex relationships between cardholders, their financial instruments, merchants, and automated security alerts triggered by suspicious activity.

## Application Domain
Financial services, specifically focused on credit card lifecycle management and real-time transaction risk assessment.

## Project Goals
- **Conceptual Modeling**: Design a robust E/R diagram featuring strong, weak, and associative entities.
- **Relational Integrity**: Implement a schema in BCNF to ensure data consistency and reduce redundancy.
- **Advanced Analytics**: Utilize SQL window functions to identify rapid-fire transactions or "velocity" fraud.
- **Automated Monitoring**: Use database triggers to populate a weak entity `Fraud_Alert` table whenever a high-risk transaction is recorded.

## Unique and Difficult Aspects
- **Resolving Many-to-Many Relationships**: The `Transaction` associative entity must link millions of `Credit_Card` records to global `Merchant` records.
- **Handling Anonymized Data**: Integrating PCA-transformed features (V1-V28) from the Kaggle dataset into a structured relational format while maintaining query performance.

## Users
- **Fraud Analysts**: Monitor the `Fraud_Alert` table and investigate high-risk scores.
- **Cardholders**: Manage their `Credit_Card` profiles and review their `Transaction` history.
- **Bank Administrators**: Oversee `User` account security and system-wide configurations.

## Data Source
The transaction data is sourced from the **Kaggle Credit Card Fraud dataset**:  
https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud  
*Note: This data has been extended with fabricated User and Merchant data to meet project complexity requirements.*
