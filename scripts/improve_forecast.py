import pandas as pd
import numpy as np
import os
from prophet import Prophet
import xgboost as xg
import lightgbm as lgb
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import matplotlib.pyplot as plt

# Create directory for models and reports
os.makedirs('enhanced_models', exist_ok=True)

def mape(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def get_festival_dates():
    # Approximate dates for major Indian festivals 2021-2025
    festivals = [
        ('Diwali', '2021-11-04'), ('Diwali', '2022-10-24'), ('Diwali', '2023-11-12'), ('Diwali', '2024-11-01'),
        ('Holi', '2021-03-29'), ('Holi', '2022-03-18'), ('Holi', '2023-03-08'), ('Holi', '2024-03-25'),
        ('Christmas', '2021-12-25'), ('Christmas', '2022-12-25'), ('Christmas', '2023-12-25'), ('Christmas', '2024-12-25')
    ]
    return pd.DataFrame(festivals, columns=['holiday', 'ds'])

def prepare_data():
    print("Loading data...")
    sales_df = pd.read_csv('data/sales.csv')
    campaigns_df = pd.read_csv('data/campaigns.csv')
    
    sales_df['order_date'] = pd.to_datetime(sales_df['order_date'])
    daily_rev = sales_df.groupby('order_date')['sales_amount'].sum().reset_index()
    daily_rev.columns = ['ds', 'y']
    
    # Feature Engineering
    print("Engineering features...")
    daily_rev['month'] = daily_rev['ds'].dt.month
    daily_rev['day'] = daily_rev['ds'].dt.day
    daily_rev['dayofweek'] = daily_rev['ds'].dt.dayofweek
    daily_rev['quarter'] = daily_rev['ds'].dt.quarter
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
    
    return daily_rev, festivals

def train_prophet(df, festivals):
    print("Training Prophet...")
    train = df.iloc[:-90]
    test = df.iloc[-90:]
    
    # Add festivals as holidays
    model = Prophet(holidays=festivals, daily_seasonality=True)
    # Add regressors
    model.add_regressor('campaign_active')
    model.add_regressor('is_weekend')
    model.add_regressor('is_month_end')
    
    model.fit(train)
    forecast = model.predict(test)
    
    y_true = test['y'].values
    y_pred = forecast['yhat'].values
    
    return mape(y_true, y_pred), np.sqrt(mean_squared_error(y_true, y_pred)), model

def train_tree_models(df):
    print("Training XGBoost & LightGBM...")
    # Tree models need numeric features only
    X = df.drop(['ds', 'y'], axis=1)
    y = df['y']
    
    X_train, X_test = X.iloc[:-90], X.iloc[-90:]
    y_train, y_test = y.iloc[:-90], y.iloc[-90:]
    
    # XGBoost
    xgb_model = xg.XGBRegressor(n_estimators=500, learning_rate=0.05, max_depth=6)
    xgb_model.fit(X_train, y_train)
    xgb_preds = xgb_model.predict(X_test)
    xgb_metrics = (mape(y_test, xgb_preds), np.sqrt(mean_squared_error(y_test, xgb_preds)), xgb_model)
    
    # LightGBM
    lgb_model = lgb.LGBMRegressor(n_estimators=500, learning_rate=0.05, max_depth=6, verbose=-1)
    lgb_model.fit(X_train, y_train)
    lgb_preds = lgb_model.predict(X_test)
    lgb_metrics = (mape(y_test, lgb_preds), np.sqrt(mean_squared_error(y_test, lgb_preds)), lgb_model)
    
    return xgb_metrics, lgb_metrics

def run_improvement():
    df, festivals = prepare_data()
    
    p_mape, p_rmse, p_model = train_prophet(df, festivals)
    xgb_metrics, lgb_metrics = train_tree_models(df)
    
    xgb_mape, xgb_rmse, xgb_model = xgb_metrics
    lgb_mape, lgb_rmse, lgb_model = lgb_metrics
    
    # Report
    report = f"""# Model Comparison Report
    
| Model | MAPE (%) | RMSE |
| :--- | :--- | :--- |
| **Prophet (Enhanced)** | {p_mape:.2f}% | {p_rmse:,.0f} |
| **XGBoost** | {xgb_mape:.2f}% | {xgb_rmse:,.0f} |
| **LightGBM** | {lgb_mape:.2f}% | {lgb_rmse:,.0f} |

"""
    print(report)
    with open('model_comparison_report.md', 'w') as f:
        f.write(report)
        
    # Select Best (Lowest MAPE)
    results = [('Prophet', p_mape, p_model), ('XGBoost', xgb_mape, xgb_model), ('LightGBM', lgb_mape, lgb_model)]
    best_name, best_mape, best_model = min(results, key=lambda x: x[1])
    
    print(f"Best Model: {best_name} with MAPE: {best_mape:.2f}%")
    joblib.dump(best_model, 'best_forecast_model.pkl')
    
if __name__ == "__main__":
    run_improvement()
