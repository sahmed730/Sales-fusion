import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_revenue_patterns():
    print("Loading sales and campaign data...")
    sales_df = pd.read_csv('data/sales.csv')
    campaigns_df = pd.read_csv('data/campaigns.csv')
    
    sales_df['order_date'] = pd.to_datetime(sales_df['order_date'])
    daily_rev = sales_df.groupby('order_date')['sales_amount'].sum().reset_index()
    daily_rev.columns = ['ds', 'y']
    
    # Identify Spikes (e.g., > 2 standard deviations)
    mean_val = daily_rev['y'].mean()
    std_val = daily_rev['y'].std()
    threshold = mean_val + 2 * std_val
    spikes = daily_rev[daily_rev['y'] > threshold]
    
    print(f"Mean Daily Revenue: {mean_val:,.0f}")
    print(f"Std Dev: {std_val:,.0f}")
    print(f"Number of 'Spike' Days (> Mean + 2SD): {len(spikes)}")
    
    # Plot with Campaign Overlays
    plt.figure(figsize=(15, 7))
    plt.plot(daily_rev['ds'], daily_rev['y'], label='Daily Revenue', alpha=0.6)
    plt.axhline(threshold, color='red', linestyle='--', label='Spike Threshold')
    
    # Highlight Campaigns
    for _, row in campaigns_df.iterrows():
        plt.axvspan(pd.to_datetime(row['campaign_start']), 
                    pd.to_datetime(row['campaign_end']), 
                    color='green', alpha=0.2)
    
    plt.title('Daily Revenue with Campaign Overlays (Green Shaded)')
    plt.savefig('revenue_pattern_analysis.png')
    plt.close()
    
    # Check Weekend Effect
    daily_rev['is_weekend'] = daily_rev['ds'].dt.dayofweek.isin([5, 6])
    weekend_avg = daily_rev[daily_rev['is_weekend']]['y'].mean()
    weekday_avg = daily_rev[~daily_rev['is_weekend']]['y'].mean()
    print(f"Weekend Avg: {weekend_avg:,.0f} vs Weekday Avg: {weekday_avg:,.0f}")

    # Save spikes for inspection
    spikes.to_csv('revenue_spikes_audit.csv', index=False)

if __name__ == "__main__":
    analyze_revenue_patterns()
