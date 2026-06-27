import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import os
import sys

OUTPUT_DIR = 'reports/forecasts'

def load_data():
    try:
        sales_df = pd.read_csv('data/sales.csv')
        campaigns_df = pd.read_csv('data/campaigns.csv')
        return sales_df, campaigns_df
    except FileNotFoundError as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

def prepare_data(sales_df):
    try:
        # Fallback to date if order_date doesn't exist
        date_col = 'order_date' if 'order_date' in sales_df.columns else 'date'
        rev_col = 'sales_amount' if 'sales_amount' in sales_df.columns else 'revenue'
        
        sales_df[date_col] = pd.to_datetime(sales_df[date_col])
        daily_sales = sales_df.groupby(date_col)[rev_col].sum().reset_index()
        daily_sales.columns = ['ds', 'y']
        return daily_sales
    except Exception as e:
        print(f"Error preparing data: {e}")
        sys.exit(1)

def train_prophet_model(daily_sales, campaigns_df):
    try:
        holidays = pd.DataFrame({
            'holiday': campaigns_df.get('campaign_name', campaigns_df.get('name', 'campaign')),
            'ds': pd.to_datetime(campaigns_df.get('campaign_start', campaigns_df.get('start_date'))),
            'lower_window': 0,
            'upper_window': 7, # Default to 7 days if unknown
        })
        model = Prophet(holidays=holidays, daily_seasonality=True)
        model.fit(daily_sales)
        return model
    except Exception as e:
        print(f"Error training model: {e}")
        sys.exit(1)

def generate_forecast(model, periods=90):
    try:
        future = model.make_future_dataframe(periods=periods)
        forecast = model.predict(future)
        return forecast
    except Exception as e:
        print(f"Error generating forecast: {e}")
        sys.exit(1)

def run_revenue_forecast():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("Starting modular revenue forecast...")
    sales_df, campaigns_df = load_data()
    daily_sales = prepare_data(sales_df)
    model = train_prophet_model(daily_sales, campaigns_df)
    forecast = generate_forecast(model)
    
    # Save
    forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(f'{OUTPUT_DIR}/revenue_forecast.csv', index=False)
    print(f"Revenue forecast completed and saved to {OUTPUT_DIR}/revenue_forecast.csv.")

if __name__ == "__main__":
    run_revenue_forecast()
