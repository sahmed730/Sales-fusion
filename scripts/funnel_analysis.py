import pandas as pd
import os

OUTPUT_DIR = 'reports/insights'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_funnel_analysis():
    print("Loading data for funnel analysis...")
    # Assuming we have a mock events or web traffic dataset, 
    # but since we only have sales, we'll create a mock sales funnel
    # based on unique customers.
    try:
        sales_df = pd.read_csv('data/sales.csv')
    except FileNotFoundError:
        print("data/sales.csv not found.")
        return
        
    # Mocking funnel steps based on customer purchasing frequency
    total_customers = sales_df['customer_id'].nunique()
    
    # Step 1: Any purchase
    step_1 = total_customers
    
    # Step 2: Repeat Purchase (>1 order)
    customer_counts = sales_df.groupby('customer_id').size()
    step_2 = (customer_counts > 1).sum()
    
    # Step 3: Loyal Customer (>5 orders)
    step_3 = (customer_counts > 5).sum()
    
    funnel = pd.DataFrame({
        'Step': ['1. First Purchase', '2. Repeat Purchase', '3. Loyal (>5 Purchases)'],
        'Count': [step_1, step_2, step_3]
    })
    
    funnel['Conversion_Rate'] = funnel['Count'] / funnel['Count'].shift(1).fillna(funnel['Count'][0])
    funnel['Overall_Conversion'] = funnel['Count'] / funnel['Count'][0]
    
    funnel.to_csv(f'{OUTPUT_DIR}/sales_funnel.csv', index=False)
    print(f"Funnel analysis complete. Saved to {OUTPUT_DIR}/sales_funnel.csv.")

if __name__ == "__main__":
    run_funnel_analysis()
