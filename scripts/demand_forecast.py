import pandas as pd
import numpy as np
import xgboost as xg
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import os
import sys

OUTPUT_DIR = 'reports/forecasts'
os.makedirs(OUTPUT_DIR, exist_ok=True)

def run_demand_forecast():
    print("Loading data...")
    try:
        sales_df = pd.read_csv('data/sales.csv')
    except FileNotFoundError:
        print("data/sales.csv not found.")
        sys.exit(1)
        
    date_col = 'order_date' if 'order_date' in sales_df.columns else 'date'
    sales_df[date_col] = pd.to_datetime(sales_df[date_col])
    
    prod_col = 'product_name' if 'product_name' in sales_df.columns else 'product_id'
    
    demand_df = sales_df.groupby([date_col, prod_col, 'region'])['quantity'].sum().reset_index()
    
    # Feature Engineering
    demand_df['month'] = demand_df[date_col].dt.month
    demand_df['day'] = demand_df[date_col].dt.day
    demand_df['dayofweek'] = demand_df[date_col].dt.dayofweek
    
    model_df = pd.get_dummies(demand_df, columns=['region'])
    
    X = model_df.drop([date_col, prod_col, 'quantity'], axis=1)
    y = model_df['quantity']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)
    
    print("Training XGBoost...")
    model = xg.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5)
    model.fit(X_train, y_train)
    
    preds = model.predict(X_test)
    print(f"MAE: {mean_absolute_error(y_test, preds):.2f}")
    
    # Feature Importance
    importances = model.feature_importances_
    feat_imp_df = pd.DataFrame({'Feature': X.columns, 'Importance': importances}).sort_values('Importance', ascending=False)
    
    plt.figure(figsize=(10, 6))
    plt.barh(feat_imp_df['Feature'], feat_imp_df['Importance'])
    plt.gca().invert_yaxis()
    plt.title('XGBoost Feature Importance')
    plt.savefig(f'{OUTPUT_DIR}/demand_feature_importance.png')
    
    feat_imp_df.to_csv(f'{OUTPUT_DIR}/demand_feature_importance.csv', index=False)
    print(f"Demand forecast and feature importance saved to {OUTPUT_DIR}.")

if __name__ == "__main__":
    run_demand_forecast()
