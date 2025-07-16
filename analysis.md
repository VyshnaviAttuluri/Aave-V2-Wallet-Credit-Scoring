# 📊 Aave V2 Wallet Credit Scoring — Data Analysis & Strategic Insights

---

## 1. Executive Summary

This report summarizes the creditworthiness of DeFi wallets based on behavioral features extracted from their transaction activity on Aave V2. Wallets are scored from 0 to 1000 using a custom heuristic model. The purpose of this analysis is to identify patterns among high-risk and low-risk wallets to enable better risk management.

---

## 2. Dataset Overview

- **Source**: `transactions.json`
- **Wallets Analyzed**: 3,497
- **Transaction Count**: ~100,000
- **Fields**: wallet_address, type, amount, timestamp

---

## 3. Feature Engineering Recap

| Feature | Description |
|--------|-------------|
| `total_deposits` | Number of deposit actions by the wallet |
| `total_borrows` | Number of borrow actions |
| `repay_to_borrow_ratio` | Total repaid / total borrowed amount |
| `avg_borrow_repay_time` | Mean time delay (in seconds) between borrow and repay |
| `liquidation_count` | Number of liquidation events triggered for the wallet |
| `active_days` | Days active between first and last transaction |
| `tx_frequency` | Transactions per active day |
| `unique_tx_types` | Number of unique transaction types (e.g., deposit, borrow, repay) |

---

## 4. Credit Scoring Logic

A weighted formula is applied to engineer a raw credit score, then scaled between 0 and 1000:

```python
score = (
    total_deposits * 10 +
    repay_to_borrow_ratio * 100 +
    (1 / (avg_borrow_repay_time + 1)) * 500000 +
    tx_frequency * 200 -
    liquidation_count * 200
)
```

Scores are normalized to 0–1000 range using MinMax scaling.

---

## 5. Credit Score Distribution
<img width="859" height="547" alt="image" src="https://github.com/user-attachments/assets/937292c9-25e5-4a48-8ff0-be8aaebba4e3" />

The score range (0–1000) was split into 10 buckets:

| Score Range | Wallet Count | Risk Tier        |
|-------------|--------------|------------------|
| 0–99        | Moderate     | 🚨 Likely spam/bots, high risk |
| 100–199     | Moderate     | Low repayment, high liquidation |
| 200–299     | High         | Unstable borrowers |
| 300–399     | High         | Mixed behavior |
| 400–499     | High         | Borderline healthy |
| 500–599     | High         | Improving credit pattern |
| 600–699     | Some         | Mostly reliable |
| 700–799     | Few          | Very stable wallets |
| 800–899     | Few          | Excellent credit behavior |
| 900–1000    | Very few     | Top-tier wallets |


```python
import pandas as pd
import matplotlib.pyplot as plt

scores = pd.read_csv("scores.csv")
scores['score_bucket'] = pd.cut(scores['credit_score'], bins=range(0, 1100, 100))
scores['score_bucket'].value_counts().sort_index().plot(kind='bar', color='skyblue', edgecolor='black')
plt.title("Credit Score Distribution (0–1000)")
plt.xlabel("Score Range")
plt.ylabel("Wallet Count")
plt.grid(True)
plt.show()
```

---

## 6. Wallet Behavior Analysis
<img width="989" height="590" alt="image" src="https://github.com/user-attachments/assets/1bdf7115-f3c2-4e6a-b9bf-cf2fa54da55e" />


<img width="580" height="507" alt="image" src="https://github.com/user-attachments/assets/e0b403ca-6515-4277-9940-68a17b54b89b" />

### 🔻 Low-Scoring Wallets (0–299)
- Few deposits and limited repayment behavior
- High liquidation rate (often >1 per wallet)
- Long delays between borrow and repay
- Only 1–2 transaction types (e.g., mostly borrow/liquidation)

### 🔹 Mid-Tier Wallets (300–699)
- Reasonable number of deposits and repayments
- Moderate activity and some liquidation cases
- Average repayment times

### 🔸 High-Scoring Wallets (700–1000)
- Consistent deposit and repayment cycles
- Very low or zero liquidation
- Fast borrow-repay turnover
- High transaction diversity (4+ types)
- Frequent active days

---

## 7. Summary

- **Score skew**: Majority of users fall into 100–600 range
- **High scores**: Indicate strong on-chain lending behavior
- **Low scores**: Flags wallets with default risk or spamming behavior

Use these scores to:
- Segment wallet populations by risk
- Adjust loan terms (e.g., interest rate, collateral ratio)
- Build robust DeFi access control mechanisms

> This analysis empowers data-driven credit modeling in decentralized finance, making protocols safer and more capital-efficient.
