"""
Sales Forecasting & Performance Dashboard - Main Pipeline
=========================================================
Run this script to execute the complete pipeline:
  python run_pipeline.py

Stages:
  1. Data Cleaning
  2. Exploratory Data Analysis
  3. ML Model Training & Evaluation
  4. Dashboard & Preview Generation
  5. PDF Report Generation
  6. Jupyter Notebook Generation
"""
import os
import sys
import time

# Set base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

def main():
    start = time.time()
    print("\n" + "=" * 60)
    print("  SALES FORECASTING & PERFORMANCE DASHBOARD")
    print("  Complete ML Pipeline")
    print("=" * 60 + "\n")

    # Stage 1: Data Cleaning
    from pipeline_cleaning import run_data_cleaning
    df = run_data_cleaning(BASE_DIR)

    # Stage 2: EDA
    from pipeline_eda import run_eda
    charts_path = run_eda(df, BASE_DIR)

    # Stage 3: ML Model
    from pipeline_model import run_ml_model
    results, features = run_ml_model(df, BASE_DIR)

    # Stage 4: Dashboard
    from pipeline_dashboard import create_dashboard_preview, create_excel_dashboard
    preview_path = create_dashboard_preview(df, BASE_DIR)
    create_excel_dashboard(df, BASE_DIR)

    # Stage 5: Report
    from pipeline_report import generate_pdf_report
    generate_pdf_report(df, results, charts_path, preview_path, BASE_DIR)

    # Stage 6: Notebooks
    from pipeline_notebooks import generate_notebooks
    generate_notebooks(BASE_DIR)

    elapsed = time.time() - start
    print("\n" + "=" * 60)
    print("  PIPELINE COMPLETE!")
    print(f"  Time elapsed: {elapsed:.1f} seconds")
    print("=" * 60)
    print("\nGenerated files:")
    for root, dirs, files in os.walk(BASE_DIR):
        # Skip __pycache__
        dirs[:] = [d for d in dirs if d != '__pycache__']
        level = root.replace(BASE_DIR, '').count(os.sep)
        indent = '  ' * level
        folder = os.path.basename(root)
        if level > 0:
            print(f'{indent}{folder}/')
        for file in sorted(files):
            if file.endswith('.pyc'):
                continue
            fpath = os.path.join(root, file)
            size = os.path.getsize(fpath)
            if size > 1024 * 1024:
                size_str = f"{size / (1024*1024):.1f} MB"
            elif size > 1024:
                size_str = f"{size / 1024:.1f} KB"
            else:
                size_str = f"{size} B"
            print(f'{indent}  {file} ({size_str})')

if __name__ == "__main__":
    main()
