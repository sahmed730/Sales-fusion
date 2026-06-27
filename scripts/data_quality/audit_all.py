import os
import pandas as pd
from datetime import datetime

data_dir = 'data'
output_file = 'reports/data_quality_audit.md'

os.makedirs('reports', exist_ok=True)

with open(output_file, 'w', encoding='utf-8') as f:
    f.write('# Data Quality Audit Report\n\n')
    f.write(f'**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\n')
    
    for file in os.listdir(data_dir):
        if file.endswith('.csv') or file.endswith('.CSV'):
            f.write(f'## `{file}`\n')
            filepath = os.path.join(data_dir, file)
            try:
                # Read only a sample if it's too large, or we can read all to get accurate nulls
                # But to avoid memory issues for very large files, we'll try to read it all.
                df = pd.read_csv(filepath)
                total_rows = len(df)
                f.write(f'- **Total Rows**: {total_rows:,}\n')
                f.write(f'- **Total Columns**: {len(df.columns)}\n\n')
                
                f.write('### Missing Values\n')
                f.write('| Column | Missing Count | Missing % |\n')
                f.write('|--------|---------------|-----------|\n')
                for col in df.columns:
                    missing = df[col].isnull().sum()
                    if missing > 0:
                        pct = (missing / total_rows) * 100
                        f.write(f'| {col} | {missing:,} | {pct:.2f}% |\n')
                
                # If no missing values
                if df.isnull().sum().sum() == 0:
                    f.write('| *All columns* | 0 | 0.00% |\n')
                    
            except Exception as e:
                f.write(f'*Error processing file: {e}*\n')
            f.write('\n---\n\n')

print(f"Data quality audit completed: {output_file}")
