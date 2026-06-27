import pandas as pd
import numpy as np
import os
from prophet import Prophet
import xgboost as xg
import lightgbm as lgb
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib

os.makedirs('enhanced_models', exist_ok=True)

def mape(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def get_festival_dates():
    festivals = [
        ('Diwali', '2021-11-04'), ('Diwali', '2022-10-24'), ('Diwali', '2023-11-12'), ('Diwali', '2024-11-01'),
        ('Holi', '2021-03-29'), ('Holi', '2022-03-18'), ('Holi', '2023-03-08'), ('Holi', '2024-03-25'),
        ('Christmas', '2021-12-25'), ('Christmas', '2022-12-25'), ('Christmas', '2023-12-25'), ('Christmas', '2024-12-25')
    ]
    return pd.DataFrame(festivals, columns=['holiday', 'ds'])

def prepare_data_v2():
    print("Loading data...")
    sales_df = pd.read_csv('data/sales.csv')
    campaigns_df = pd.read_csv('data/campaigns.csv')
    products_df = pd.read_csv('data/products.csv')
    
    sales_df['order_date'] = pd.to_datetime(sales_df['order_date'])
    daily_rev = sales_df.groupby('order_date')['sales_amount'].sum().reset_index()
    daily_rev.columns = ['ds', 'y']
    
    # 1. Outlier Removal / Winsorization (Clip top 2% of spikes)
    upper_limit = daily_rev['y'].quantile(0.98)
    daily_rev['y_clipped'] = daily_rev['y'].clip(upper=upper_limit)
    
    # 2. Features
    print("Engineering features V2...")
    daily_rev['month'] = daily_rev['ds'].dt.month
    daily_rev['day'] = daily_rev['ds'].dt.day
    daily_rev['dayofweek'] = daily_rev['ds'].dt.dayofweek
    daily_rev['is_weekend'] = daily_rev['dayofweek'].isin([5, 6]).astype(int)
    daily_rev['is_month_end'] = (daily_rev['ds'].dt.is_month_end | (daily_rev['day'] >= 25)).astype(int)
    
    # Campaign Flag
    daily_rev['campaign_active'] = 0
    for _, row in campaigns_df.iterrows():
        mask = (daily_rev['ds'] >= pd.to_datetime(row['campaign_start'])) & (daily_rev['ds'] <= pd.to_datetime(row['campaign_end']))
        daily_rev.loc[mask, 'campaign_active'] = 1
        
    # Festival Flag
    festivals = get_festival_dates()
    daily_rev['festival_flag'] = daily_rev['ds'].isin(pd.to_datetime(festivals['ds'])).astype(int)
    
    # Product Launch Flag
    launch_dates = pd.to_datetime(products_df['launch_date'])
    daily_rev['launch_event'] = daily_rev['ds'].isin(launch_dates).astype(int)
    
    return daily_rev, festivals

def run_improvement_v2():
    df, festivals = prepare_data_v2()
    
    # Use clipped target for training
    y_target = 'y_clipped'
    
    # 90-day split
    train = df.iloc[:-90]
    test = df.iloc[-90:]
    
    print("Training Models on Clipped Data...")
    
    # 1. Prophet
    p_model = Prophet(holidays=festivals, daily_seasonality=True)
    p_model.add_regressor('campaign_active')
    p_model.add_regressor('is_weekend')
    p_model.add_regressor('is_month_end')
    p_model.add_regressor('launch_event')
    
    p_model.fit(train[['ds', y_target, 'campaign_active', 'is_weekend', 'is_month_end', 'launch_event']].rename(columns={y_target: 'y'}))
    p_forecast = p_model.predict(test)
    p_mape = mape(test['y'], p_forecast['yhat']) # Evaluate against ORIGINAL 'y' to be honest
    
    # 2. XGBoost
    X_cols = ['month', 'day', 'dayofweek', 'is_weekend', 'is_month_end', 'campaign_active', 'festival_flag', 'launch_event']
    xgb = xg.XGBRegressor(n_estimators=1000, learning_rate=0.01, max_depth=7)
    xgb.fit(train[X_cols], train[y_target])
    xgb_preds = xgb.predict(test[X_cols])
    xgb_mape = mape(test['y'], xgb_preds)
    
    # 3. LightGBM
    lgb_m = lgb.LGBMRegressor(n_estimators=1000, learning_rate=0.01, max_depth=7, verbose=-1)
    lgb_m.fit(train[X_cols], train[y_target])
    lgb_preds = lgb_m.predict(test[X_cols])
    lgb_mape = mape(test['y'], lgb_preds)
    
    report = f"""# Final Model Comparison (V2 - Outlier Capped)
    
| Model | MAPE (on raw 'y') |
| :--- | :--- |
| **Prophet** | {p_mape:.2f}% |
| **XGBoost** | {xgb_mape:.2f}% |
| **LightGBM** | {lgb_mape:.2f}% |

"""
    print(report)
    
    # Save best
    results = [('Prophet', p_mape, p_model), ('XGBoost', xgb_mape, xgb), ('LightGBM', lgb_mape, lgb_m)]
    best_name, best_mape, best_model = min(results, key=lambda x: x[1])
    joblib.dump(best_model, 'best_forecast_model.pkl')
    
if __name__ == "__main__":
    run_improvement_v2()
