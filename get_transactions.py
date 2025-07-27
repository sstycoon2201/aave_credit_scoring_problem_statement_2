import requests
import pandas as pd
import time

# Constants
API_KEY = "cqt_rQpm9FFTQQjvBqkbXxpvt7xh4GXw"
CHAIN_ID = "1"
BASE_URL = f"https://api.covalenthq.com/v1/{CHAIN_ID}/address"
LOCAL_EXCEL_PATH = r"C:\Users\shwet\OneDrive\Documents\Python Project\Copy of Wallet id.xlsx"
OUTPUT_FILE = r"C:\Users\shwet\OneDrive\Documents\Python Project\compound_transactions.csv"

# Load wallet addresses
wallet_df = pd.read_excel(LOCAL_EXCEL_PATH)
wallet_addresses = wallet_df.iloc[:, 0].dropna().unique().tolist()

print(f"Loaded {len(wallet_addresses)} wallet addresses.")

# Keywords for filtering Compound-related transactions
COMPOUND_KEYWORDS = [
    'compound', 'ctoken', 'ceth', 'cdai', 'cusdc', 'borrow', 'repay',
    'liquidate', 'collateral', 'mint', 'redeem', 'claimcomp'
]

def is_compound_related(event_name: str, decoded: dict) -> bool:
    if event_name and any(keyword in event_name.lower() for keyword in COMPOUND_KEYWORDS):
        return True
    if decoded and 'name' in decoded and any(keyword in decoded['name'].lower() for keyword in COMPOUND_KEYWORDS):
        return True
    return False

output_data = []

for i, wallet in enumerate(wallet_addresses, start=1):
    print(f"[{i}/{len(wallet_addresses)}] Fetching: {wallet}")
    url = f"{BASE_URL}/{wallet}/transactions_v3/?key={API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        items = data.get("data", {}).get("items", [])
        if not items:
            print(f"⚠️ No transactions found for {wallet}")
            continue

        for tx in items:
            tx_hash = tx.get("tx_hash")
            timestamp = tx.get("block_signed_at")
            log_events = tx.get("log_events", [])

            for event in log_events:
                decoded = event.get("decoded")
                event_name = decoded.get("name") if decoded else None

                if is_compound_related(event_name, decoded):
                    token_name = None
                    amount = None

                    if decoded and 'params' in decoded and decoded['params']:
                        for param in decoded['params']:
                            if param.get('name', '').lower() in ['amount', 'value']:
                                amount = param.get('value')
                            if param.get('name', '').lower() in ['token', 'asset']:
                                token_name = param.get('value')

                    output_data.append({
                        "wallet_id": wallet,
                        "tx_hash": tx_hash,
                        "timestamp": timestamp,
                        "function": event_name,
                        "token": token_name,
                        "amount": amount
                    })
        time.sleep(0.2)

    except Exception as e:
        print(f"⚠️ Exception for wallet {wallet}: {e}")
        continue

# Save to CSV
if output_data:
    output_df = pd.DataFrame(output_data)
    output_df.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Done! {len(output_data)} Compound transactions saved to {OUTPUT_FILE}")
else:
    print("⚠️ No Compound-related transactions found.")
