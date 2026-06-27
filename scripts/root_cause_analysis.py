import pandas as pd
import os
import sys

OUTPUT_DIR = 'reports/insights'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_root_cause_analysis():
    print("Loading data for root cause analysis...")
    try:
        sales_df = pd.read_csv('data/sales.csv')
    except FileNotFoundError:
        print("data/sales.csv not found.")
        sys.exit(1)
        
    date_col = 'order_date' if 'order_date' in sales_df.columns else 'date'
    sales_df[date_col] = pd.to_datetime(sales_df[date_col])
    sales_df['month'] = sales_df[date_col].dt.to_period('M')
    
    # We will identify the largest drop in revenue month-over-month
    rev_col = 'sales_amount' if 'sales_amount' in sales_df.columns else 'revenue'
    
    monthly_rev = sales_df.groupby('month')[rev_col].sum().reset_index()
    monthly_rev['prev_month_rev'] = monthly_rev[rev_col].shift(1)
    monthly_rev['pct_change'] = (monthly_rev[rev_col] - monthly_rev['prev_month_rev']) / monthly_rev['prev_month_rev']
    
    # Find the worst month
    worst_month_row = monthly_rev.loc[monthly_rev['pct_change'].idxmin()]
    worst_month = worst_month_row['month']
    
    print(f"Worst performing month identified: {worst_month} with {worst_month_row['pct_change']*100:.2f}% drop.")
    
    # Drill down into regions for that month compared to previous
    curr_data = sales_df[sales_df['month'] == worst_month].groupby('region')[rev_col].sum()
    prev_data = sales_df[sales_df['month'] == (worst_month - 1)].groupby('region')[rev_col].sum()
    
    rc_df = pd.DataFrame({'curr_rev': curr_data, 'prev_rev': prev_data}).fillna(0)
    rc_df['diff'] = rc_df['curr_rev'] - rc_df['prev_rev']
    
    rc_df = rc_df.sort_values('diff') # Most negative diff is the biggest root cause
    
    rc_df.to_csv(f'{OUTPUT_DIR}/root_cause_{worst_month}.csv')
    print(f"Root cause investigation complete. Saved to {OUTPUT_DIR}/root_cause_{worst_month}.csv.")

if __name__ == "__main__":
    run_root_cause_analysis()
