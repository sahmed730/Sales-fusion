import pandas as pd
import os

def main():
    sales_path = 'data/sales.csv'
    data_path = 'data/data.CSV'
    output_path = 'reports/metric_reconciliation.md'
    
    os.makedirs('reports', exist_ok=True)
    
    try:
        sales_df = pd.read_csv(sales_path)
        data_df = pd.read_csv(data_path)
        
        # Assuming both have a 'revenue' or 'Sales' column
        # Finding the closest matching column for revenue
        sales_rev_col = next((col for col in sales_df.columns if 'rev' in col.lower() or 'sale' in col.lower()), None)
        data_rev_col = next((col for col in data_df.columns if 'rev' in col.lower() or 'sale' in col.lower()), None)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('# 📈 Metric Reconciliation Report\n\n')
            f.write('Comparing `sales.csv` and `data.CSV`.\n\n')
            
            if sales_rev_col and data_rev_col:
                sales_total = sales_df[sales_rev_col].sum()
                data_total = data_df[data_rev_col].sum()
                diff = sales_total - data_total
                
                f.write(f'- **sales.csv total (`{sales_rev_col}`)**: {sales_total:,.2f}\n')
                f.write(f'- **data.CSV total (`{data_rev_col}`)**: {data_total:,.2f}\n')
                f.write(f'- **Absolute Difference**: {abs(diff):,.2f}\n')
                f.write(f'- **Status**: {"✅ Match" if abs(diff) < 1.0 else "❌ Discrepancy Found"}\n')
            else:
                f.write('Could not find revenue columns to compare.\n')
                
    except Exception as e:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f'# 📈 Metric Reconciliation Report\n\nError: {e}\n')

if __name__ == '__main__':
    main()
