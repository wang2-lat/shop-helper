import pandas as pd
from pathlib import Path

def import_customers(csv_file: Path, db_file: Path) -> int:
    """Import customers from CSV and append to database"""
    new_data = pd.read_csv(csv_file)
    
    if db_file.exists():
        existing = pd.read_csv(db_file)
        combined = pd.concat([existing, new_data], ignore_index=True)
        combined.drop_duplicates(subset=["email"], keep="last", inplace=True)
    else:
        combined = new_data
    
    combined.to_csv(db_file, index=False)
    return len(new_data)

def export_customers(db_file: Path, output_file: Path) -> int:
    """Export customers to CSV file"""
    if not db_file.exists():
        return 0
    
    data = pd.read_csv(db_file)
    data.to_csv(output_file, index=False)
    return len(data)

def search_customers(db_file: Path, query: str) -> pd.DataFrame:
    """Search customers by name or email"""
    if not db_file.exists():
        return pd.DataFrame()
    
    data = pd.read_csv(db_file)
    query_lower = query.lower()
    
    mask = data.apply(lambda row: query_lower in str(row).lower(), axis=1)
    return data[mask]
