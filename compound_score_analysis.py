import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

# Load data
file_path = "C:/Users/shwet/OneDrive/Documents/Python Project/compound_transactions.csv"
df = pd.read_csv(file_path)

# Ensure timestamp is datetime
df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')

# Filter only valid function types
relevant_actions = ["Mint", "Borrow", "RepayBorrow", "Redeem"]
df = df[df["function"].isin(relevant_actions)]

# Clean 'amount' if it exists
if "amount" in df.columns:
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
else:
    df["amount"] = 0

# Create new column with date only (for groupby on activity)
df["date"] = df["timestamp"].dt.date

# Group by wallet and calculate features
grouped = df.groupby("wallet_id")

features = pd.DataFrame(index=grouped.size().index)

features["num_transactions"] = grouped["tx_hash"].nunique()
features["active_days"] = grouped["date"].nunique()
features["avg_tx_per_day"] = features["num_transactions"] / features["active_days"].replace(0, 1)
features["total_volume"] = grouped["amount"].sum()
features["avg_volume"] = grouped["amount"].mean()

# Normalize features
scaler = MinMaxScaler()
scaled = pd.DataFrame(scaler.fit_transform(features), columns=features.columns, index=features.index)

# Weighted scoring
weights = {
    "num_transactions": 0.25,
    "active_days": 0.20,
    "avg_tx_per_day": 0.20,
    "total_volume": 0.20,
    "avg_volume": 0.15
}

scaled["score"] = sum(scaled[col] * weight for col, weight in weights.items())
scaled["score"] = (scaled["score"] * 1000).round().astype(int)

# Output to CSV
output = scaled[["score"]].reset_index()
output_path = "C:/Users/shwet/OneDrive/Documents/Python Project/compound_credit_scores.csv"
output.to_csv(output_path, index=False)

print(f"✅ Credit scores written to: {output_path}")
