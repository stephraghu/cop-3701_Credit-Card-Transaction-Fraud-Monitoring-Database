# Database Conceptual Design

## 1. Entity-Relationship Diagram
<img width="1217" height="1246" alt="image" src="https://github.com/user-attachments/assets/11aee0f8-591a-4d0b-8efd-c0cbba08318d" />


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

---
## 5. Final Normalized Relational Schema
The following schema represents the translation of the E/R diagram into a relational model. All relations have been verified to be in Boyce-Codd Normal Form (BCNF).

- **User** (**user_id**, first_name, last_name, email, phone_number)
- **Identity_Profile** (**profile_id**, *user_id*, ssn_hash, last_verified)
- **Credit_Card** (**card_number**, *user_id*, expiry_date, card_type, credit_limit)
- **Merchant** (**merchant_id**, merchant_name, category, website)
- **Transaction** (**transaction_id**, *card_number*, *merchant_id*, amount, timestamp, v1, v2, v3, class)
- **Fraud_Alert** (**alert_id**, *transaction_id*, risk_score, investigation_status, created_at)

*Note: **Bold** indicates Primary Keys; *Italics* indicate Foreign Keys.*
