# Project Report

## 1. Objective
Analyze accounting voucher and ledger data and convert it into financial and risk insights.

## 2. Accounting layer
The raw dataset represents Tally-style sales vouchers, purchase vouchers, ledger entries, customers, suppliers, payment modes and tax amounts.

## 3. Data Science layer
Python performs data loading, feature engineering, aggregation, profitability analysis, anomaly detection and risk scoring.

## 4. Fraud/anomaly analysis
The system flags duplicate-like vouchers, high-value transactions, large discounts, unusual quantities, unusual unit prices and high-value cash transactions. Each alert has a score and human-readable reason.

## 5. Business value
Finance teams can monitor revenue, compare category profitability, prioritize transaction review and support management decisions.

## 6. Limitation
The data is synthetic. Risk flags require human/accounting review and do not prove fraud. A production system could later be extended with confirmed-case labels and machine-learning models.
