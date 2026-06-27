import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
import os
import sys

OUTPUT_DIR = 'reports/insights'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_region_analysis():
    print("Loading data...")
    try:
        sales_df = pd.read_csv('data/sales.csv')
    except FileNotFoundError:
        print("data/sales.csv not found.")
        sys.exit(1)
        
    date_col = 'order_date' if 'order_date' in sales_df.columns else 'date'
    rev_col = 'sales_amount' if 'sales_amount' in sales_df.columns else 'revenue'
    
    sales_df[date_col] = pd.to_datetime(sales_df[date_col])
    
    # Clustering regions based on total revenue and quantity
    region_agg = sales_df.groupby('region').agg(
        total_revenue=(rev_col, 'sum'),
        total_quantity=('quantity', 'sum'),
        avg_order_value=(rev_col, 'mean')
    ).reset_index()
    
    print("Performing K-Means Clustering on Regions...")
    kmeans = KMeans(n_clusters=3, random_state=42)
    features = region_agg[['total_revenue', 'total_quantity', 'avg_order_value']]
    region_agg['cluster'] = kmeans.fit_predict(features)
    
    region_agg.to_csv(f'{OUTPUT_DIR}/regional_clusters.csv', index=False)
    
    print("Running anomaly detection...")
    iso = IsolationForest(contamination=0.05, random_state=42)
    region_agg['is_anomaly'] = iso.fit_predict(features)
    
    anomalies = region_agg[region_agg['is_anomaly'] == -1]
    anomalies.to_csv(f'{OUTPUT_DIR}/regional_anomalies.csv', index=False)
    
    print(f"Region analysis complete. Results saved in {OUTPUT_DIR}.")

if __name__ == "__main__":
    run_region_analysis()
