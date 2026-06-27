import pandas as pd
import sys

def validate_sales(filepath):
    print(f"Validating {filepath}...")
    try:
        df = pd.read_csv(filepath)
        
        errors = []
        
        # Rule 1: Revenue >= 0
        if 'revenue' in df.columns and (df['revenue'] < 0).any():
            errors.append("Validation Error: Found negative revenue values.")
            
        # Rule 2: Quantity > 0
        if 'quantity' in df.columns and (df['quantity'] <= 0).any():
            errors.append("Validation Error: Found quantity <= 0.")
            
        # Rule 3: Date is valid
        if 'date' in df.columns:
            try:
                pd.to_datetime(df['date'])
            except Exception as e:
                errors.append(f"Validation Error: Invalid dates found ({e}).")
                
        if errors:
            for error in errors:
                print(error)
            sys.exit(1)
        else:
            print("Validation successful: All business rules passed.")
            sys.exit(0)
            
    except Exception as e:
        print(f"Failed to read file: {e}")
        sys.exit(1)

if __name__ == '__main__':
    validate_sales('data/sales.csv')
