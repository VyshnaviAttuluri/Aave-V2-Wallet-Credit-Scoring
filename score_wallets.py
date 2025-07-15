
import pandas as pd
import json

# ---------- STEP 1: Load raw transaction JSON ----------
with open("transactions.json", "r") as f:
    raw_data = json.load(f)

df = pd.DataFrame(raw_data)

# ---------- STEP 2: Clean & Preprocess ----------
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
# Handle missing 'amount' key by filling with 0, or you could drop rows if amount is crucial
df['amount'] = df.get('amount', pd.Series([0] * len(df))).astype(float)
df = df.dropna(subset=['wallet_address', 'type']) # Changed 'user' to 'wallet_address'

# ---------- STEP 3: Feature Engineering ----------
def compute_features(df):
    # 1. Basic counts
    total_deposits = df[df['type'] == 'deposit'].groupby('wallet_address').size().rename('total_deposits') # Changed 'user' to 'wallet_address'
    total_borrows = df[df['type'] == 'borrow'].groupby('wallet_address').size().rename('total_borrows') # Changed 'user' to 'wallet_address'

    # 2. Repay-to-Borrow Ratio
    repay_sum = df[df['type'] == 'repay'].groupby('wallet_address')['amount'].sum() # Changed 'user' to 'wallet_address'
    borrow_sum = df[df['type'] == 'borrow'].groupby('wallet_address')['amount'].sum() # Changed 'user' to 'wallet_address'
    repay_ratio = (repay_sum / (borrow_sum + 1)).rename('repay_to_borrow_ratio')

    # 3. Avg. Borrow-Repay Time (sec)
    borrow_time = df[df['type'] == 'borrow'][['wallet_address', 'timestamp']].rename(columns={'timestamp': 'borrow_time'}) # Changed 'user' to 'wallet_address'
    repay_time = df[df['type'] == 'repay'][['wallet_address', 'timestamp']].rename(columns={'timestamp': 'repay_time'}) # Changed 'user' to 'wallet_address'
    merged = pd.merge(borrow_time, repay_time, on='wallet_address')
    merged['delta'] = (merged['repay_time'] - merged['borrow_time']).dt.total_seconds().abs()
    avg_repay_time = merged.groupby('wallet_address')['delta'].mean().rename('avg_borrow_repay_time') # Changed 'user' to 'wallet_address'

    # 4. Liquidation count
    liquidation_count = df[df['type'] == 'liquidationcall'].groupby('wallet_address').size().rename('liquidation_count') # Changed 'user' to 'wallet_address'

    # 5. Active days
    first_seen = df.groupby('wallet_address')['timestamp'].min() # Changed 'user' to 'wallet_address'
    last_seen = df.groupby('wallet_address')['timestamp'].max() # Changed 'user' to 'wallet_address'
    active_days = (last_seen - first_seen).dt.days.rename('active_days')

    # 6. Tx frequency
    tx_count = df.groupby('wallet_address').size().rename('total_tx') # Changed 'user' to 'wallet_address'
    tx_freq = (tx_count / (active_days + 1)).rename('tx_frequency')

    # 7. Unique tx types
    unique_tx_types = df.groupby('wallet_address')['type'].nunique().rename('unique_tx_types') # Changed 'user' to 'wallet_address'

    # 8. Combine all features
    features = pd.concat([
        total_deposits,
        total_borrows,
        repay_ratio,
        avg_repay_time,
        liquidation_count,
        active_days,
        tx_freq,
        unique_tx_types
    ], axis=1).fillna(0)

    return features

features = compute_features(df)

# ---------- STEP 4: Heuristic Scoring Logic ----------
def score_wallets(features):
    score = (
        features['total_deposits'] * 10 +
        features['repay_to_borrow_ratio'] * 100 +
        (1 / (features['avg_borrow_repay_time'] + 1)) * 500000 +
        features['tx_frequency'] * 200 -
        features['liquidation_count'] * 200
    )
    score = score.clip(lower=0)
    scaled_score = 1000 * (score - score.min()) / (score.max() - score.min() + 1e-9)
    return scaled_score

features['credit_score'] = score_wallets(features)

# ---------- STEP 5: Save output ----------
features.reset_index()[['wallet_address', 'credit_score']].rename( # Changed 'user' to 'wallet_address'
    columns={'wallet_address': 'wallet_address'}
).to_csv("scores.csv", index=False)

print("✅ All wallets scored. File 'scores.csv' generated.")
