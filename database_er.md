# Database Conceptual Design (Part B)

## 1. Entity-Relationship Diagram
<img width="1263" height="870" alt="image" src="https://github.com/user-attachments/assets/39bf0536-e97a-4432-b0b5-b78b19488b0d" />

## 2. Complexity Requirements Checklist
This design demonstrates at least one example of each required item:

### Attributes
- **Identifier**: `user_id` (User), `transaction_id` (Transaction).
- **Single-value**: `amount` (Transaction), `expiry_date` (Credit_Card).
- **Optional**: `email` (User), `website` (Merchant).
- **Mandatory**: `first_name` (User), `timestamp` (Transaction).

### Entities
- **Strong Entity**: `User`, `Merchant`, `Credit_Card`.
- **Weak Entity**: `Fraud_Alert` (Depends on `Transaction` to exist).
- **Associative Entity**: `Transaction` (Bridges the M:N relationship between `Credit_Card` and `Merchant`).

### Cardinality
- **One-to-One (1:1)**: `User` to `Identity_Profile`.
- **One-to-Many (1:N)**: `User` to `Credit_Card`.
- **Many-to-Many (M:N)**: `Credit_Card` and `Merchant` via the `Transaction` associative entity.

## 3. User Groups
- **Fraud Analyst**: Investigates flagged accounts.
- **Cardholder**: Reviews personal spending and disputes charges.
- **System Admin**: Maintains database integrity and access.

## 4. Design Assumptions
1. A transaction cannot exist without both a valid Credit Card and a Merchant.
2. If a Transaction is deleted, any associated `Fraud_Alert` (Weak Entity) is automatically deleted.
3. Each Credit Card is tied to exactly one primary User.
4. The anonymized features (V1-V28) from the Kaggle source are treated as transaction-level attributes for risk scoring.
