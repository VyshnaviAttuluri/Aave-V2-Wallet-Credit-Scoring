# 💼 Aave V2 Wallet Credit Scoring

## 💼 Aave V2 Wallet Credit Scoring

## 🚀 Overview
This project presents a full-stack machine learning pipeline that generates DeFi credit scores (0–1000) based solely on historical transaction behavior from Aave V2 protocol data. It aims to evaluate the creditworthiness of blockchain wallet addresses through behavioral analysis.

> **Objective:** Score each wallet between 0–1000 where higher scores imply responsible financial behavior, while lower scores suggest risky, automated, or exploitative activity.

---

## 📁 Project Structure
```
project-root/
├── notebooks/
│   ├── Aave_V2_Wallet_Credit_Scoring_EDA.ipynb    #Data Cleaning & EDA
│   ├── 2_feature_engineering.ipynb       # Feature derivation logic
├── score_wallets.py                      # ✅ One-Step scoring pipeline (production-ready)
├── scores.csv                            # ✅ Output: [wallet_address, credit_score]
├── README.md                             # ✅ You're here!
└── analysis.md                           # ✅ Summary of scoring insights and wallet behavior
```
# 🧠 Notebooks Overview

| Notebook Name | Purpose |
|---------------|---------|
| `Aave_V2_Wallet_Credit_Scoring_EDA.ipynb` | Clean & explore wallet transactions. Analyze patterns and behavior. |
| `2_feature_engineering.ipynb` | Extract behavioral features like repay ratio, liquidation count, etc. |

---

## 🧠 Methodology

### 🔹 Step 1: Data Ingestion
- JSON file loaded with transaction-level logs (deposit, borrow, repay, etc.)

### 🔹 Step 2: Feature Engineering (Wallet-Level Aggregation)
We compute the following features:
- `total_deposits` – Total deposit actions per wallet
- `total_borrows` – Total borrow actions
- `repay_to_borrow_ratio` – Ratio of amount repaid to borrowed
- `avg_borrow_repay_time` – How quickly a user repays a loan
- `liquidation_count` – Number of times a wallet was liquidated
- `active_days` – Days between first and last transaction
- `tx_frequency` – Transactions per active day
- `unique_tx_types` – Diversity of transaction types

### 🔹 Step 3: Scoring Model (Heuristic-Based)
Credit Score = Weighted combination of good and bad behavioral signals:
- 📈 Positive signals: deposits, fast repayment, frequency
- ⚠️ Negative signals: liquidation, inactivity
- Final scores scaled to 0–1000 using min-max normalization

---

## 📊 Sample Output (scores.csv)
| wallet_address | credit_score |
|----------------|---------------|
| 0x123...       | 999.99        |
| 0x456...       | 574.60        |
| 0x789...       | 241.47        |
| 0xabc...       | 0.0           |

---

## 🔧 How to Run
You can run the scoring pipeline end-to-end using:
```bash
python score_wallets.py
```
It reads `transactions.json` and outputs `scores.csv` in the same directory.

> ✅ You can also explore features in the `notebooks/` folder and retrain or enhance scoring logic.

---

## 📈 Insights (see `analysis.md`)
- 80% of wallets fall in the 200–600 score range
- Liquidated wallets have scores < 100
- High-frequency wallets show stronger repayment patterns

---

## 💡 Future Enhancements
- Integrate anomaly detection for bot behavior
- Use LSTMs or GNNs for time-aware or graph-based scoring
- Plug-in real-time blockchain streams via Infura/Moralis APIs

---

## 🧾 References
- Aave V2 Docs: https://docs.aave.com/
- Kaggle Blockchain Datasets
- Vitalik's Blog: Reputation in Web3

---

## 👩‍💻 Author
**Vyshnavi Attuluri**  
[GitHub](https://github.com/VyshnaviAttuluri) | vyshnaviathuluri5102@gmail.com

---

## 🏁 Final Note
This project demonstrates an end-to-end autonomous credit scoring system using DeFi data. The methodology is intentionally transparent, flexible, and designed to scale for future productionization or research extensions.

> *Scoring transparency ≠ simplicity. We embrace data richness while maintaining clarity for auditability.* ✅
