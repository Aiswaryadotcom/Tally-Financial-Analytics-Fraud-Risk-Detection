from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
OUT = ROOT / 'data' / 'processed'
OUT.mkdir(parents=True, exist_ok=True)

sales = pd.read_csv(RAW / 'tally_sales_vouchers.csv', parse_dates=['date'])
purchases = pd.read_csv(RAW / 'tally_purchase_vouchers.csv', parse_dates=['date'])
ledger = pd.read_csv(RAW / 'tally_ledger.csv', parse_dates=['date'])

# Financial profitability features. Cost is an illustrative synthetic estimate.
rng = np.random.default_rng(42)
sales['estimated_cost'] = sales['quantity'] * sales['unit_price'] * rng.uniform(0.72, 0.90, len(sales))
sales['estimated_profit'] = sales['net_sales'] - sales['estimated_cost']
sales['profit_margin_pct'] = np.where(sales['net_sales'] > 0, sales['estimated_profit'] / sales['net_sales'] * 100, 0)

# Explainable anomaly features
sales['duplicate_key'] = (
    sales['date'].dt.strftime('%Y-%m-%d') + '|' + sales['customer_id'] + '|' +
    sales['item_id'] + '|' + sales['net_sales'].round(2).astype(str)
)
sales['duplicate_count'] = sales.groupby('duplicate_key')['duplicate_key'].transform('count')
price_median = sales.groupby('item_id')['unit_price'].transform('median')
sales['price_deviation_pct'] = np.where(price_median > 0, (sales['unit_price'] - price_median).abs() / price_median * 100, 0)
q75, q25 = sales['total_amount'].quantile(.75), sales['total_amount'].quantile(.25)
iqr = q75 - q25
sales['high_value_flag'] = sales['total_amount'] > q75 + 1.5 * iqr
sales['high_discount_flag'] = sales['discount_pct'] >= 30
sales['high_quantity_flag'] = sales['quantity'] >= sales['quantity'].quantile(.99)
sales['price_anomaly_flag'] = sales['price_deviation_pct'] >= 40
sales['duplicate_flag'] = sales['duplicate_count'] > 1
sales['cash_high_value_flag'] = (sales['payment_mode'] == 'Cash') & (sales['total_amount'] >= sales['total_amount'].quantile(.95))

sales['fraud_risk_score'] = (
    sales['duplicate_flag'].astype(int) * 30 +
    sales['high_value_flag'].astype(int) * 20 +
    sales['high_discount_flag'].astype(int) * 20 +
    sales['high_quantity_flag'].astype(int) * 10 +
    sales['price_anomaly_flag'].astype(int) * 15 +
    sales['cash_high_value_flag'].astype(int) * 15
).clip(0, 100)
sales['risk_level'] = pd.cut(sales['fraud_risk_score'], bins=[-1,29,59,100], labels=['Low','Medium','High'])

def reasons(r):
    x=[]
    if r.duplicate_flag: x.append('possible duplicate voucher')
    if r.high_value_flag: x.append('unusually high transaction value')
    if r.high_discount_flag: x.append('unusually high discount')
    if r.high_quantity_flag: x.append('unusually high quantity')
    if r.price_anomaly_flag: x.append('unusual unit price')
    if r.cash_high_value_flag: x.append('high-value cash transaction')
    return '; '.join(x) if x else 'normal pattern'
sales['risk_reasons'] = sales.apply(reasons, axis=1)

sales['month'] = sales['date'].dt.to_period('M').astype(str)
monthly = sales.groupby('month', as_index=False).agg(
    sales=('net_sales','sum'), tax=('tax','sum'), gross_billing=('total_amount','sum'),
    profit=('estimated_profit','sum'), invoices=('voucher_no','count'))
monthly['profit_margin_pct'] = monthly['profit'] / monthly['sales'] * 100

category = sales.groupby('category', as_index=False).agg(
    sales=('net_sales','sum'), profit=('estimated_profit','sum'),
    quantity=('quantity','sum'), invoices=('voucher_no','count'))
category['profit_margin_pct'] = category['profit'] / category['sales'] * 100

risk = sales[sales['fraud_risk_score'] > 0][[
    'voucher_no','date','customer_name','item_name','total_amount','payment_mode',
    'fraud_risk_score','risk_level','risk_reasons']].sort_values(
    ['fraud_risk_score','total_amount'], ascending=False)

sales.to_csv(OUT / 'sales_with_risk_scores.csv', index=False)
monthly.to_csv(OUT / 'monthly_financial_summary.csv', index=False)
category.to_csv(OUT / 'category_profitability.csv', index=False)
risk.to_csv(OUT / 'fraud_risk_report.csv', index=False)

print('Analysis completed successfully.')
print(f'Sales vouchers: {len(sales):,}')
print(f'Purchase vouchers: {len(purchases):,}')
print(f'Total sales: Rs {sales.net_sales.sum():,.2f}')
print(f'Estimated profit: Rs {sales.estimated_profit.sum():,.2f}')
print(f'Flagged transactions: {len(risk):,}')
