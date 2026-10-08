from pathlib import Path
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / 'data' / 'processed'
st.set_page_config(page_title='Tally Financial Risk Analytics', layout='wide')
st.title('Tally + Data Science Financial Analytics')
st.caption('Synthetic Tally-style accounting data | profitability | anomaly detection | fraud-risk scoring')

sales = pd.read_csv(DATA / 'sales_with_risk_scores.csv')
monthly = pd.read_csv(DATA / 'monthly_financial_summary.csv')
category = pd.read_csv(DATA / 'category_profitability.csv')

c1,c2,c3,c4 = st.columns(4)
c1.metric('Total Sales', f"Rs {sales.net_sales.sum():,.0f}")
c2.metric('Estimated Profit', f"Rs {sales.estimated_profit.sum():,.0f}")
c3.metric('Profit Margin', f"{sales.estimated_profit.sum()/sales.net_sales.sum()*100:.1f}%")
c4.metric('Flagged Transactions', f"{(sales.fraud_risk_score > 0).sum():,}")

st.subheader('Monthly Financial Performance')
st.line_chart(monthly.set_index('month')[['sales','profit']])
st.subheader('Category Profitability')
st.dataframe(category.sort_values('profit', ascending=False), use_container_width=True)
st.subheader('Fraud / Anomaly Risk')
levels = st.multiselect('Risk level', ['High','Medium','Low'], default=['High','Medium'])
view = sales[sales.risk_level.isin(levels)].sort_values('fraud_risk_score', ascending=False)
st.dataframe(view[['voucher_no','date','customer_name','item_name','total_amount','payment_mode','fraud_risk_score','risk_level','risk_reasons']], use_container_width=True)
