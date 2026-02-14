# 📊 Sales Forecasting & Performance Dashboard using Machine Learning

## Problem Statement
Analyze retail sales data from the **Superstore Sales Dataset** and predict future sales using Machine Learning models. The project includes data cleaning, exploratory data analysis, ML-based sales prediction, an interactive Excel dashboard, and a comprehensive project report.

## Dataset
- **Source:** [Kaggle – Superstore Sales Dataset](https://www.kaggle.com/datasets/vivek468/superstore-dataset-final)
- **Records:** ~9,994 transactions
- **Features:** Order Date, Ship Mode, Segment, Category, Sub-Category, Sales, Quantity, Discount, Profit, Region, and more.

## Project Structure
```
sales-forecasting-ml-dashboard/
│
├── README.md
├── requirements.txt
├── .gitignore
├── run_pipeline.py
│
├── dataset/
│   ├── superstore.csv
│   └── superstore_cleaned.csv
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_eda_analysis.ipynb
│   └── 03_sales_prediction_model.ipynb
│
├── dashboard/
│   ├── sales_dashboard.xlsx
│   └── dashboard_preview.png
│
├── models/
│   └── sales_prediction_model.pkl
│
├── outputs/
│   ├── charts.png
│   └── results.txt
│
└── report/
    └── project_report.pdf
```

## Tools & Technologies
| Tool | Purpose |
|------|---------|
| Python 3.11 | Core programming language |
| Pandas, NumPy | Data manipulation & analysis |
| Matplotlib, Seaborn | Data visualization |
| Scikit-learn | Machine Learning models |
| XlsxWriter / OpenPyXL | Excel dashboard creation |
| FPDF2 | PDF report generation |
| Microsoft Excel | Dashboard viewing |

## ML Models Used
- **Linear Regression** — Baseline model
- **Random Forest Regressor** — Ensemble model for improved accuracy

## Evaluation Metrics
| Metric | Description |
|--------|-------------|
| **R² Score** | Proportion of variance explained by the model |
| **MAE** | Mean Absolute Error |
| **RMSE** | Root Mean Squared Error |

## How to Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the complete pipeline
```bash
python run_pipeline.py
```

This will:
- Clean the data and save `dataset/superstore_cleaned.csv`
- Generate EDA charts at `outputs/charts.png`
- Train ML models, save best model at `models/sales_prediction_model.pkl`
- Save evaluation metrics to `outputs/results.txt`
- Create the Excel dashboard at `dashboard/sales_dashboard.xlsx`
- Generate dashboard preview at `dashboard/dashboard_preview.png`
- Generate the project report at `report/project_report.pdf`
- Generate Jupyter notebooks in `notebooks/`

## Results
- **Random Forest** achieved a strong **R² score** for sales prediction, outperforming Linear Regression.
- Key insights: Technology category drives highest sales, Consumer segment is the largest customer base, and the West region leads in revenue.
```markdown

```
## Dashboard Preview
<img width="2475" height="1929" alt="image" src="https://github.com/user-attachments/assets/b4d134e2-3052-477f-a797-7c73775d374d" />

```
```
## License
This project is for educational purposes.

