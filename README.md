# Tally + Data Science Financial Analytics & Fraud Risk Detection System

## Project overview
A portfolio project that connects **Tally-style accounting data** with **Data Science**. It analyzes sales, purchases and ledger entries, measures profitability, detects unusual transactions and produces an explainable fraud-risk score.

The accounting files are synthetic and structured like Tally exports. They are not real company records.

## Business problem
Finance teams process many vouchers and transactions. Manual review can miss unusual patterns. This system helps answer:
- What are total sales and estimated profit?
- Which categories are most profitable?
- Which transactions need review?
- Why was a transaction flagged?

## Data flow
Tally-style vouchers → CSV → Python/Pandas → feature engineering → profitability analysis → anomaly detection → processed reports → Streamlit dashboard

## Fraud/anomaly rules
| Signal | Points |
|---|---:|
| Possible duplicate voucher | 30 |
| High transaction value | 20 |
| High discount | 20 |
| High quantity | 10 |
| Unusual unit price | 15 |
| High-value cash transaction | 15 |

Risk levels: **Low 0–29**, **Medium 30–59**, **High 60–100**.

This is an explainable risk model, not proof that a transaction is fraudulent.

## Technologies
Python, Pandas, NumPy, Streamlit, CSV accounting data, EDA, feature engineering, anomaly detection.

## Folder structure
```text
tally-data-science-financial-fraud/
├── data/raw/
│   ├── tally_sales_vouchers.csv
│   ├── tally_purchase_vouchers.csv
│   └── tally_ledger.csv
├── data/processed/
│   ├── sales_with_risk_scores.csv
│   ├── monthly_financial_summary.csv
│   ├── category_profitability.csv
│   └── fraud_risk_report.csv
├── src/analyze_financials.py
├── dashboard/app.py
├── reports/project_report.md
├── reports/resume_project_description.md
├── requirements.txt
└── README.md
```

## Run locally
```bash
pip install -r requirements.txt
python src/analyze_financials.py
streamlit run dashboard/app.py
```

## Resume project title
**Tally + Data Science Financial Analytics & Fraud Risk Detection System**

## Resume description
Built a Tally-style financial analytics system using Python and Pandas to analyze sales, purchase, and ledger data, evaluate profitability, identify transaction anomalies, and generate explainable fraud-risk scores. Developed processed financial reports and a Streamlit dashboard for financial monitoring and decision support.
