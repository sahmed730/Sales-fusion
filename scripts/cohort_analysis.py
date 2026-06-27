import pandas as pd
import os

OUTPUT_DIR = 'reports/insights'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_cohort_analysis():
    print("Loading data for cohort analysis...")
    try:
        sales_df = pd.read_csv('data/sales.csv')
    except FileNotFoundError:
        print("data/sales.csv not found.")
        return
        
    date_col = 'order_date' if 'order_date' in sales_df.columns else 'date'
    customer_col = 'customer_id'
    
    if customer_col not in sales_df.columns:
        print("customer_id column not found, skipping cohort analysis.")
        return
        
    sales_df[date_col] = pd.to_datetime(sales_df[date_col])
    
    # Assign acquisition month
    sales_df['order_month'] = sales_df[date_col].dt.to_period('M')
    sales_df['cohort'] = sales_df.groupby(customer_col)[date_col].transform('min').dt.to_period('M')
    
    # Calculate cohort metrics
    cohort_data = sales_df.groupby(['cohort', 'order_month']).agg(n_customers=(customer_col, 'nunique')).reset_index()
    cohort_data['period_number'] = (cohort_data.order_month - cohort_data.cohort).apply(lambda x: x.n)
    
    cohort_pivot = cohort_data.pivot(index='cohort', columns='period_number', values='n_customers')
    cohort_size = cohort_pivot.iloc[:, 0]
    retention_matrix = cohort_pivot.divide(cohort_size, axis=0)
    
    retention_matrix.to_csv(f'{OUTPUT_DIR}/cohort_retention.csv')
    print(f"Cohort analysis complete. Saved to {OUTPUT_DIR}/cohort_retention.csv.")

if __name__ == "__main__":
    run_cohort_analysis()
