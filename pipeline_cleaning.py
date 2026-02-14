"""
Data Cleaning Module - Stage 1 of the Sales Forecasting Pipeline
"""
import pandas as pd
import numpy as np
import os

def run_data_cleaning(base_dir):
    """Clean the Superstore dataset and save cleaned version."""
    print("=" * 60)
    print("STAGE 1: DATA CLEANING")
    print("=" * 60)

    # Load data
    raw_path = os.path.join(base_dir, "dataset", "superstore.csv")
    df = pd.read_csv(raw_path, encoding='latin-1')
    print(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Columns: {list(df.columns)}")

    # Check for missing values
    missing = df.isnull().sum()
    missing_cols = missing[missing > 0]
    if len(missing_cols) > 0:
        print(f"\nMissing values found:\n{missing_cols}")
        # Fill numeric nulls with median, categorical with mode
        for col in missing_cols.index:
            if df[col].dtype in ['float64', 'int64']:
                df[col].fillna(df[col].median(), inplace=True)
            else:
                df[col].fillna(df[col].mode()[0], inplace=True)
        print("Missing values filled.")
    else:
        print("\nNo missing values found.")

    # Remove duplicates
    before = len(df)
    df.drop_duplicates(inplace=True)
    after = len(df)
    print(f"Duplicates removed: {before - after}")

    # Parse dates
    df['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed', dayfirst=False)
    df['Ship Date'] = pd.to_datetime(df['Ship Date'], format='mixed', dayfirst=False)

    # Feature engineering
    df['Order Year'] = df['Order Date'].dt.year
    df['Order Month'] = df['Order Date'].dt.month
    df['Order DayOfWeek'] = df['Order Date'].dt.dayofweek
    df['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days

    print(f"Added features: Order Year, Order Month, Order DayOfWeek, Shipping Days")
    print(f"Date range: {df['Order Date'].min()} to {df['Order Date'].max()}")
    print(f"Final cleaned dataset: {df.shape[0]} rows, {df.shape[1]} columns")

    # Save cleaned data
    clean_path = os.path.join(base_dir, "dataset", "superstore_cleaned.csv")
    df.to_csv(clean_path, index=False)
    print(f"Saved cleaned data to: {clean_path}")
    print()

    return df
