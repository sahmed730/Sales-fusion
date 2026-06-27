import pandas as pd
import numpy as np
import os
import lightgbm as lgb
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib

def mape(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def prepare_weekly_data():
    print("Loading data for weekly aggregation...")
    sales_df = pd.read_csv('data/sales.csv')
    sales_df['order_date'] = pd.to_datetime(sales_df['order_date'])
    
    # Aggregate to Weekly
    # 'W-MON' means week starting Monday
    weekly_rev = sales_df.resample('W-MON', on='order_date')['sales_amount'].sum().reset_index()
    weekly_rev.columns = ['ds', 'y']
    
    # Feature Engineering
    print("Engineering weekly features...")
    weekly_rev['month'] = weekly_rev['ds'].dt.month
    weekly_rev['week_of_year'] = weekly_rev['ds'].dt.isocalendar().week.astype(int)
    weekly_rev['quarter'] = weekly_rev['ds'].dt.quarter
    
    # Lag features (previous 4 weeks)
    for i in range(1, 5):
        weekly_rev[f'lag_{i}'] = weekly_rev['y'].shift(i)
    
    # Rolling mean
    weekly_rev['rolling_mean_4'] = weekly_rev['y'].shift(1).rolling(window=4).mean()
    
    weekly_rev = weekly_rev.dropna()
    return weekly_rev

def run_weekly_forecast():
    df = prepare_weekly_data()
    
    # 12-week split (~3 months)
    train = df.iloc[:-12]
    test = df.iloc[-12:]
    
    X_cols = ['month', 'week_of_year', 'quarter', 'lag_1', 'lag_2', 'lag_3', 'lag_4', 'rolling_mean_4']
    y_col = 'y'
    
    print("Training LightGBM on Weekly Data...")
    model = lgb.LGBMRegressor(n_estimators=1000, learning_rate=0.05, max_depth=5, verbose=-1)
    model.fit(train[X_cols], train[y_col])
    
    preds = model.predict(test[X_cols])
    current_mape = mape(test[y_col], preds)
    
    print(f"Weekly MAPE: {current_mape:.2f}%")
    
    if current_mape < 25:
        print("Success! MAPE is under control.")
    
    report = f"""# Weekly Revenue Forecast Report
    
| Metric | Value |
| :--- | :--- |
| **Model** | LightGBM (Weekly) |
| **MAPE** | {current_mape:.2f}% |
| **RMSE** | {np.sqrt(mean_squared_error(test[y_col], preds)):,.0f} |

"""
    with open('model_comparison_report.md', 'w') as f:
        f.write(report)
        
    joblib.dump(model, 'best_forecast_model.pkl')

if __name__ == "__main__":
    run_weekly_forecast()
