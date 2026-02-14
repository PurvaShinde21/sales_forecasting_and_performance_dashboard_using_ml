"""
Notebook Generator - Creates .ipynb files from the pipeline logic
"""
import json
import os

def make_cell(cell_type, source):
    """Create a notebook cell."""
    cell = {
        "cell_type": cell_type,
        "metadata": {},
        "source": [line + "\n" for line in source.split("\n")]
    }
    if cell_type == "code":
        cell["execution_count"] = None
        cell["outputs"] = []
    return cell

def make_notebook(cells):
    """Create a notebook structure."""
    return {
        "nbformat": 4,
        "nbformat_minor": 5,
        "metadata": {
            "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
            "language_info": {"name": "python", "version": "3.11.0"}
        },
        "cells": cells
    }

def generate_notebooks(base_dir):
    """Generate all 3 Jupyter notebooks."""
    nb_dir = os.path.join(base_dir, "notebooks")

    # ── Notebook 1: Data Cleaning ──
    cells1 = [
        make_cell("markdown", "# 01 - Data Cleaning\n## Superstore Sales Dataset"),
        make_cell("code", "import pandas as pd\nimport numpy as np"),
        make_cell("code", "df = pd.read_csv('../dataset/superstore.csv', encoding='latin-1')\nprint(f'Shape: {df.shape}')\ndf.head()"),
        make_cell("code", "df.info()"),
        make_cell("code", "df.isnull().sum()"),
        make_cell("code", "df.describe()"),
        make_cell("markdown", "## Data Cleaning Steps"),
        make_cell("code", "# Remove duplicates\nbefore = len(df)\ndf.drop_duplicates(inplace=True)\nprint(f'Duplicates removed: {before - len(df)}')"),
        make_cell("code", "# Parse dates\ndf['Order Date'] = pd.to_datetime(df['Order Date'], format='mixed')\ndf['Ship Date'] = pd.to_datetime(df['Ship Date'], format='mixed')"),
        make_cell("code", "# Feature engineering\ndf['Order Year'] = df['Order Date'].dt.year\ndf['Order Month'] = df['Order Date'].dt.month\ndf['Order DayOfWeek'] = df['Order Date'].dt.dayofweek\ndf['Shipping Days'] = (df['Ship Date'] - df['Order Date']).dt.days"),
        make_cell("code", "print(f'Cleaned dataset: {df.shape}')\ndf.head()"),
        make_cell("code", "df.to_csv('../dataset/superstore_cleaned.csv', index=False)\nprint('Saved cleaned dataset.')"),
    ]
    with open(os.path.join(nb_dir, "01_data_cleaning.ipynb"), "w") as f:
        json.dump(make_notebook(cells1), f, indent=1)

    # ── Notebook 2: EDA ──
    cells2 = [
        make_cell("markdown", "# 02 - Exploratory Data Analysis\n## Superstore Sales Dataset"),
        make_cell("code", "import pandas as pd\nimport numpy as np\nimport matplotlib.pyplot as plt\nimport seaborn as sns\nsns.set_theme(style='whitegrid')"),
        make_cell("code", "df = pd.read_csv('../dataset/superstore_cleaned.csv')\ndf['Order Date'] = pd.to_datetime(df['Order Date'])\nprint(f'Shape: {df.shape}')"),
        make_cell("markdown", "## Sales by Category"),
        make_cell("code", "cat_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)\ncat_sales.plot(kind='bar', color=['#3498db','#e74c3c','#2ecc71'], figsize=(8,5))\nplt.title('Sales by Category')\nplt.ylabel('Sales ($)')\nplt.tight_layout()\nplt.show()"),
        make_cell("markdown", "## Monthly Sales Trend"),
        make_cell("code", "monthly = df.groupby(df['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()\nmonthly['Order Date'] = monthly['Order Date'].dt.to_timestamp()\nplt.figure(figsize=(12,5))\nplt.plot(monthly['Order Date'], monthly['Sales'], color='#e74c3c', linewidth=2)\nplt.fill_between(monthly['Order Date'], monthly['Sales'], alpha=0.15, color='#e74c3c')\nplt.title('Monthly Sales Trend')\nplt.ylabel('Sales ($)')\nplt.xticks(rotation=45)\nplt.tight_layout()\nplt.show()"),
        make_cell("markdown", "## Sales by Region"),
        make_cell("code", "reg_sales = df.groupby('Region')['Sales'].sum()\nplt.figure(figsize=(8,5))\nreg_sales.plot(kind='pie', autopct='%1.1f%%', colors=['#1abc9c','#3498db','#9b59b6','#e67e22'])\nplt.title('Sales by Region')\nplt.ylabel('')\nplt.tight_layout()\nplt.show()"),
        make_cell("markdown", "## Discount vs Profit"),
        make_cell("code", "plt.figure(figsize=(8,5))\nplt.scatter(df['Discount'], df['Profit'], alpha=0.3, c=df['Sales'], cmap='RdYlGn', s=20)\nplt.colorbar(label='Sales')\nplt.xlabel('Discount')\nplt.ylabel('Profit')\nplt.title('Discount vs Profit')\nplt.axhline(y=0, color='red', linestyle='--', alpha=0.5)\nplt.tight_layout()\nplt.show()"),
        make_cell("markdown", "## Top 10 Sub-Categories by Sales"),
        make_cell("code", "sub_sales = df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=True).tail(10)\nplt.figure(figsize=(10,6))\nsub_sales.plot(kind='barh', color=sns.color_palette('viridis', 10))\nplt.title('Top 10 Sub-Categories by Sales')\nplt.xlabel('Sales ($)')\nplt.tight_layout()\nplt.show()"),
    ]
    with open(os.path.join(nb_dir, "02_eda_analysis.ipynb"), "w") as f:
        json.dump(make_notebook(cells2), f, indent=1)

    # ── Notebook 3: ML Model ──
    cells3 = [
        make_cell("markdown", "# 03 - Sales Prediction Model\n## Linear Regression & Random Forest"),
        make_cell("code", "import pandas as pd\nimport numpy as np\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.linear_model import LinearRegression\nfrom sklearn.ensemble import RandomForestRegressor\nfrom sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error\nfrom sklearn.preprocessing import LabelEncoder\nimport joblib"),
        make_cell("code", "df = pd.read_csv('../dataset/superstore_cleaned.csv')\nprint(f'Shape: {df.shape}')"),
        make_cell("markdown", "## Feature Engineering"),
        make_cell("code", "cat_cols = ['Ship Mode', 'Segment', 'Region', 'Category', 'Sub-Category']\nfor col in cat_cols:\n    le = LabelEncoder()\n    df[col + '_Enc'] = le.fit_transform(df[col].astype(str))"),
        make_cell("code", "features = ['Quantity', 'Discount', 'Ship Mode_Enc', 'Segment_Enc',\n            'Region_Enc', 'Category_Enc', 'Sub-Category_Enc',\n            'Order Year', 'Order Month', 'Order DayOfWeek', 'Shipping Days']\ntarget = 'Sales'\n\nX = df[features].values\ny = df[target].values\n\nX_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\nprint(f'Train: {X_train.shape}, Test: {X_test.shape}')"),
        make_cell("markdown", "## Linear Regression"),
        make_cell("code", "lr = LinearRegression()\nlr.fit(X_train, y_train)\ny_pred_lr = lr.predict(X_test)\nprint(f'R2: {r2_score(y_test, y_pred_lr):.4f}')\nprint(f'MAE: {mean_absolute_error(y_test, y_pred_lr):.2f}')\nprint(f'RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_lr)):.2f}')"),
        make_cell("markdown", "## Random Forest Regressor"),
        make_cell("code", "rf = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=15)\nrf.fit(X_train, y_train)\ny_pred_rf = rf.predict(X_test)\nprint(f'R2: {r2_score(y_test, y_pred_rf):.4f}')\nprint(f'MAE: {mean_absolute_error(y_test, y_pred_rf):.2f}')\nprint(f'RMSE: {np.sqrt(mean_squared_error(y_test, y_pred_rf)):.2f}')"),
        make_cell("markdown", "## Save Best Model"),
        make_cell("code", "joblib.dump(rf, '../models/sales_prediction_model.pkl')\nprint('Model saved!')"),
    ]
    with open(os.path.join(nb_dir, "03_sales_prediction_model.ipynb"), "w") as f:
        json.dump(make_notebook(cells3), f, indent=1)

    print(f"Generated 3 notebooks in: {nb_dir}")
