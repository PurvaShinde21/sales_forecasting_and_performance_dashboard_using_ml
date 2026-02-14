"""
Report Generation Module - Stage 5 of the Sales Forecasting Pipeline
"""
import os

def generate_pdf_report(df, results, charts_path, preview_path, base_dir):
    """Generate a PDF project report using fpdf2."""
    from fpdf import FPDF

    print("Generating PDF report...")

    class SalesReport(FPDF):
        def header(self):
            self.set_font('Helvetica', 'B', 10)
            self.set_text_color(100, 100, 100)
            self.cell(0, 8, 'Sales Forecasting & Performance Dashboard - Project Report', align='C')
            self.ln(5)
            self.set_draw_color(52, 152, 219)
            self.set_line_width(0.5)
            self.line(10, self.get_y(), 200, self.get_y())
            self.ln(5)

        def footer(self):
            self.set_y(-15)
            self.set_font('Helvetica', 'I', 8)
            self.set_text_color(150, 150, 150)
            self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

        def section_title(self, title):
            self.set_font('Helvetica', 'B', 14)
            self.set_text_color(44, 62, 80)
            self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
            self.set_draw_color(52, 152, 219)
            self.set_line_width(0.3)
            self.line(10, self.get_y(), 80, self.get_y())
            self.ln(4)

        def body_text(self, text):
            self.set_font('Helvetica', '', 11)
            self.set_text_color(60, 60, 60)
            self.multi_cell(0, 6, text)
            self.ln(3)

    pdf = SalesReport()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # Title Page
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(44, 62, 80)
    pdf.cell(0, 15, 'Sales Forecasting &', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 15, 'Performance Dashboard', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 16)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 10, 'Using Machine Learning', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font('Helvetica', '', 12)
    pdf.cell(0, 8, 'Dataset: Superstore Sales (Kaggle)', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, 'Tools: Python, Scikit-learn, Pandas, Matplotlib, Excel', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, f'Records: {len(df):,} transactions', align='C', new_x="LMARGIN", new_y="NEXT")

    # Problem Statement
    pdf.add_page()
    pdf.section_title('1. Problem Statement')
    pdf.body_text(
        'The objective of this project is to analyze retail sales data from the Superstore dataset '
        'and build machine learning models to predict future sales. This involves data cleaning, '
        'exploratory data analysis (EDA), feature engineering, model training, evaluation, and '
        'creating an interactive Excel dashboard for business stakeholders.'
    )

    # Dataset Description
    pdf.section_title('2. Dataset Description')
    pdf.body_text(
        f'Source: Kaggle - Superstore Sales Dataset\n'
        f'Total Records: {len(df):,}\n'
        f'Features: {df.shape[1]} columns including Order Date, Ship Mode, Segment, '
        f'Category, Sub-Category, Sales, Quantity, Discount, Profit, Region\n'
        f'Date Range: {df["Order Date"].min().strftime("%Y-%m-%d")} to {df["Order Date"].max().strftime("%Y-%m-%d")}\n'
        f'Total Sales: ${df["Sales"].sum():,.2f}\n'
        f'Total Profit: ${df["Profit"].sum():,.2f}'
    )

    # Methodology
    pdf.section_title('3. Methodology')
    pdf.body_text(
        'Step 1 - Data Cleaning: Handled missing values, removed duplicates, parsed dates, '
        'and engineered time-based features (Year, Month, Day of Week, Shipping Days).\n\n'
        'Step 2 - Exploratory Data Analysis: Analyzed sales distribution by category, region, '
        'segment, and sub-category. Examined monthly trends and discount-profit relationships.\n\n'
        'Step 3 - Feature Engineering: Encoded categorical variables (Ship Mode, Segment, Region, '
        'Category, Sub-Category) using Label Encoding. Selected 11 features for modeling.\n\n'
        'Step 4 - Model Training: Trained two regression models:\n'
        '  - Linear Regression (baseline)\n'
        '  - Random Forest Regressor (ensemble method)\n\n'
        'Step 5 - Evaluation: Compared models using R-squared Score, MAE, and RMSE.'
    )

    # Results
    pdf.section_title('4. Model Results')
    pdf.set_font('Helvetica', 'B', 11)
    pdf.set_fill_color(44, 62, 80)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(60, 8, 'Model', border=1, fill=True, align='C')
    pdf.cell(35, 8, 'R2 Score', border=1, fill=True, align='C')
    pdf.cell(35, 8, 'MAE', border=1, fill=True, align='C')
    pdf.cell(35, 8, 'RMSE', border=1, fill=True, align='C')
    pdf.ln()
    pdf.set_text_color(60, 60, 60)
    pdf.set_font('Helvetica', '', 11)
    for name, metrics in results.items():
        pdf.cell(60, 8, name, border=1, align='C')
        pdf.cell(35, 8, f'{metrics["R2"]:.4f}', border=1, align='C')
        pdf.cell(35, 8, f'{metrics["MAE"]:.2f}', border=1, align='C')
        pdf.cell(35, 8, f'{metrics["RMSE"]:.2f}', border=1, align='C')
        pdf.ln()
    pdf.ln(5)
    best_name = max(results, key=lambda k: results[k]['R2'])
    best = results[best_name]
    pdf.body_text(f'Best Model: {best_name} with R2 Score of {best["R2"]:.4f}')

    # EDA Charts
    if os.path.exists(charts_path):
        pdf.add_page()
        pdf.section_title('5. Exploratory Data Analysis - Charts')
        pdf.image(charts_path, x=10, w=190)

    # Dashboard Preview
    if os.path.exists(preview_path):
        pdf.add_page()
        pdf.section_title('6. Dashboard Preview')
        pdf.image(preview_path, x=10, w=190)

    # Conclusion
    pdf.add_page()
    pdf.section_title('7. Conclusion')
    pdf.body_text(
        f'The {best_name} model achieved the best performance with an R2 score of {best["R2"]:.4f}, '
        f'MAE of {best["MAE"]:.2f}, and RMSE of {best["RMSE"]:.2f}. '
        f'Key business insights include:\n\n'
        f'- Technology category generates the highest sales revenue\n'
        f'- Consumer segment is the largest customer base\n'
        f'- West region leads in total sales\n'
        f'- Higher discounts tend to reduce profit margins\n'
        f'- Sales show seasonal patterns with peaks in Q4\n\n'
        f'The Excel dashboard provides an interactive view for stakeholders to explore '
        f'sales performance across different dimensions.'
    )

    report_path = os.path.join(base_dir, "report", "project_report.pdf")
    pdf.output(report_path)
    print(f"Saved PDF report: {report_path}")
    return report_path
