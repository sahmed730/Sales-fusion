import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from prophet import Prophet
from prophet.diagnostics import performance_metrics, cross_validation
import xgboost as xg
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.model_selection import train_test_split, cross_val_score, KFold
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import os

# Output directory for audit results
audit_dir = 'forecast_audit_results'
if not os.path.exists(audit_dir):
    os.makedirs(audit_dir)

def mape(y_true, y_pred): 
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

def audit_prophet():
    print("--- Auditing Prophet (Revenue) ---")
    sales_df = pd.read_csv('data/sales.csv')
    sales_df['order_date'] = pd.to_datetime(sales_df['order_date'])
    daily_sales = sales_df.groupby('order_date')['sales_amount'].sum().reset_index()
    daily_sales.columns = ['ds', 'y']

    # Backtesting: Last 90 days as test set
    train = daily_sales.iloc[:-90]
    test = daily_sales.iloc[-90:]

    model = Prophet(daily_seasonality=True)
    model.fit(train)
    
    forecast = model.predict(test)
    
    y_true = test['y'].values
    y_pred = forecast['yhat'].values

    metrics = {
        'MAE': mean_absolute_error(y_true, y_pred),
        'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
        'MAPE': mape(y_true, y_pred)
    }
    
    # Residuals
    residuals = y_true - y_pred
    
    # Plot Actual vs Predicted
    plt.figure(figsize=(12, 6))
    plt.plot(test['ds'], y_true, label='Actual', marker='o')
    plt.plot(test['ds'], y_pred, label='Predicted', linestyle='--', marker='x')
    plt.title('Prophet: Actual vs Predicted Revenue (Last 90 Days)')
    plt.legend()
    plt.savefig(f'{audit_dir}/prophet_actual_vs_pred.png')
    plt.close()

    # Residual Plot
    plt.figure(figsize=(10, 5))
    plt.scatter(y_pred, residuals)
    plt.axhline(0, color='red', linestyle='--')
    plt.xlabel('Predicted')
    plt.ylabel('Residuals')
    plt.title('Prophet: Residual Analysis')
    plt.savefig(f'{audit_dir}/prophet_residuals.png')
    plt.close()

    return metrics

def audit_xgboost():
    print("--- Auditing XGBoost (Demand) ---")
    # Using prep logic from demand_forecast.py
    sales_df = pd.read_csv('data/sales.csv')
    sales_df['order_date'] = pd.to_datetime(sales_df['order_date'])
    demand_df = sales_df.groupby(['order_date', 'product_name', 'category', 'region'])['quantity'].sum().reset_index()
    demand_df['month'] = demand_df['order_date'].dt.month
    demand_df['day'] = demand_df['order_date'].dt.day
    demand_df['dayofweek'] = demand_df['order_date'].dt.dayofweek
    demand_df['quarter'] = demand_df['order_date'].dt.quarter
    demand_df = demand_df.sort_values(by=['product_name', 'region', 'order_date'])
    demand_df['prev_demand'] = demand_df.groupby(['product_name', 'region'])['quantity'].shift(1).fillna(0)
    demand_df = pd.get_dummies(demand_df, columns=['category', 'region'])
    
    X = demand_df.drop(['order_date', 'product_name', 'quantity'], axis=1)
    y = demand_df['quantity']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    model = xg.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    
    metrics = {
        'MAE': mean_absolute_error(y_test, preds),
        'RMSE': np.sqrt(mean_squared_error(y_test, preds)),
        'R2': r2_score(y_test, preds)
    }

    # Feature Importance
    plt.figure(figsize=(10, 8))
    xg.plot_importance(model, max_num_features=15)
    plt.title('XGBoost: Feature Importance (Gain)')
    plt.savefig(f'{audit_dir}/xgboost_feature_importance.png')
    plt.close()

    # Cross Validation
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(model, X, y, cv=cv, scoring='r2')
    metrics['CV_R2_Mean'] = cv_scores.mean()

    return metrics

def audit_regional():
    print("--- Auditing Regional Performance (RF + IF) ---")
    sales_df = pd.read_csv('data/sales.csv')
    sales_df['order_date'] = pd.to_datetime(sales_df['order_date'])
    sales_df['month_year'] = sales_df['order_date'].dt.to_period('M').astype(str)
    region_perf = sales_df.groupby(['month_year', 'region'])['sales_amount'].sum().reset_index()
    region_perf['month'] = pd.to_datetime(region_perf['month_year']).dt.month
    region_perf_encoded = pd.get_dummies(region_perf, columns=['region'])
    
    X = region_perf_encoded.drop(['month_year', 'sales_amount'], axis=1)
    y = region_perf_encoded['sales_amount']
    
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X, y)
    
    region_perf['expected_revenue'] = rf.predict(X)
    region_perf['performance_gap'] = region_perf['sales_amount'] - region_perf['expected_revenue']
    
    iso_forest = IsolationForest(contamination=0.05, random_state=42)
    region_perf['anomaly'] = iso_forest.fit_predict(region_perf[['sales_amount', 'performance_gap']])
    region_perf['anomaly_score'] = iso_forest.decision_function(region_perf[['sales_amount', 'performance_gap']])
    
    # Anomaly counts by region
    anomaly_counts = region_perf[region_perf['anomaly'] == -1].groupby('region').size().reset_index(name='count')
    
    # Plots
    plt.figure(figsize=(12, 6))
    sns.barplot(data=region_perf, x='region', y='sales_amount', hue='anomaly')
    plt.title('Regional Sales Performance with Anomaly Flags')
    plt.savefig(f'{audit_dir}/regional_anomaly_plot.png')
    plt.close()

    return region_perf[region_perf['anomaly'] == -1], anomaly_counts

if __name__ == "__main__":
    p_metrics = audit_prophet()
    x_metrics = audit_xgboost()
    anomalies, anomaly_summary = audit_regional()

    # Write summary to a temp file for the final report
    with open(f'{audit_dir}/audit_summary.txt', 'w') as f:
        f.write("PROPHET METRICS:\n")
        f.write(str(p_metrics) + "\n\n")
        f.write("XGBOOST METRICS:\n")
        f.write(str(x_metrics) + "\n\n")
        f.write("ANOMALY SUMMARY:\n")
        f.write(anomaly_summary.to_string() + "\n\n")
        f.write("DETAILED ANOMALIES:\n")
        f.write(anomalies[['month_year', 'region', 'sales_amount', 'expected_revenue', 'anomaly_score']].to_string())

    print("Audit completed. Outputs in 'forecast_audit_results/'.")
