# aave_credit_scoring_problem_statement_2

# 📄 Compound Wallet Credit Scoring – Submission Write-up

## 🔍 Data Collection Method
We used the [Covalent API](https://www.covalenthq.com/docs/) to retrieve transaction-level data from the Compound protocol. Specifically, we filtered the dataset using relevant `function` types such as `Mint`, `Borrow`, `RepayBorrow`, and `Redeem` to capture core lending and borrowing behavior. The API provided rich JSON responses containing wallet addresses, transaction hashes, timestamps, function types, and amounts, which were stored and preprocessed into a structured CSV file.

## 📊 Feature Selection Rationale
To assess a wallet’s behavior and associated financial risk, we extracted and engineered the following features:

- **`num_transactions`**: Total unique transactions (proxy for engagement level).
- **`active_days`**: Count of unique active days (shows consistency of usage).
- **`avg_tx_per_day`**: Indicates wallet activity frequency and regularity.
- **`total_volume`**: Aggregate value across relevant transactions (shows exposure size).
- **`avg_volume`**: Average value per transaction (helps identify risk per transaction).

These features reflect both **quantitative activity** and **temporal consistency**, both of which are critical in risk modeling.

## 🧮 Scoring Method
We normalized the above features using **Min-Max Scaling** to bring them to a 0–1 range. A weighted sum of these normalized values was computed based on their perceived contribution to creditworthiness. The final score was scaled to a 0–1000 range and rounded to an integer.

### Weights assigned:

| Feature            | Weight |
|--------------------|--------|
| num_transactions   | 0.25   |
| active_days        | 0.20   |
| avg_tx_per_day     | 0.20   |
| total_volume       | 0.20   |
| avg_volume         | 0.15   |

## ✅ Justification of Risk Indicators
- **High transaction count** and **active days** suggest reliability and sustained engagement with Compound.
- **Frequent activity (avg_tx_per_day)** highlights discipline and habit in lending/borrowing.
- **Total and average volume** reflect the user’s financial capacity and average exposure risk.
- Wallets with **sporadic high-volume activity** but **low consistency** are penalized relative to those with **stable patterns**.

