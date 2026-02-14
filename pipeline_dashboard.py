"""
Dashboard & Report Module - Stage 4 of the Sales Forecasting Pipeline
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import os

def create_dashboard_preview(df, base_dir):
    """Create a matplotlib-based dashboard preview image."""
    print("=" * 60)
    print("STAGE 4: DASHBOARD & REPORT GENERATION")
    print("=" * 60)

    sns.set_theme(style="whitegrid")
    fig = plt.figure(figsize=(20, 14), facecolor='#1a1a2e')
    gs = gridspec.GridSpec(3, 4, figure=fig, hspace=0.4, wspace=0.35)

    title_color = '#ffffff'
    text_color = '#e0e0e0'
    accent_colors = ['#00d2ff', '#7b2ff7', '#ff6b6b', '#ffd93d', '#6bcb77']

    fig.suptitle('SALES PERFORMANCE DASHBOARD', fontsize=24, fontweight='bold',
                 color=title_color, y=0.98)

    # KPI Cards (top row)
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    total_orders = df['Order ID'].nunique()
    avg_discount = df['Discount'].mean()

    kpis = [
        ('Total Sales', f'${total_sales:,.0f}', accent_colors[0]),
        ('Total Profit', f'${total_profit:,.0f}', accent_colors[1]),
        ('Total Orders', f'{total_orders:,}', accent_colors[2]),
        ('Avg Discount', f'{avg_discount:.1%}', accent_colors[3]),
    ]
    for i, (label, value, color) in enumerate(kpis):
        ax = fig.add_subplot(gs[0, i])
        ax.set_facecolor('#16213e')
        ax.text(0.5, 0.65, value, transform=ax.transAxes, fontsize=22,
                fontweight='bold', color=color, ha='center', va='center')
        ax.text(0.5, 0.25, label, transform=ax.transAxes, fontsize=12,
                color=text_color, ha='center', va='center')
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color('#2d3561')

    # Monthly Sales Trend
    ax1 = fig.add_subplot(gs[1, :2])
    ax1.set_facecolor('#16213e')
    monthly = df.groupby(df['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
    monthly['Order Date'] = monthly['Order Date'].dt.to_timestamp()
    ax1.plot(monthly['Order Date'], monthly['Sales'], color=accent_colors[0], linewidth=2, marker='o', markersize=3)
    ax1.fill_between(monthly['Order Date'], monthly['Sales'], alpha=0.2, color=accent_colors[0])
    ax1.set_title('Monthly Sales Trend', color=title_color, fontsize=13, fontweight='bold')
    ax1.tick_params(colors=text_color, rotation=45)
    ax1.set_ylabel('Sales ($)', color=text_color)

    # Sales by Category (donut)
    ax2 = fig.add_subplot(gs[1, 2:])
    ax2.set_facecolor('#1a1a2e')
    cat_sales = df.groupby('Category')['Sales'].sum()
    wedges, texts, autotexts = ax2.pie(cat_sales.values, labels=cat_sales.index,
        autopct='%1.1f%%', colors=accent_colors[:3], startangle=90,
        textprops={'color': text_color, 'fontsize': 10}, pctdistance=0.8,
        wedgeprops=dict(width=0.5, edgecolor='#1a1a2e'))
    for t in autotexts:
        t.set_color('white')
        t.set_fontsize(9)
    ax2.set_title('Sales by Category', color=title_color, fontsize=13, fontweight='bold')

    # Sales by Region
    ax3 = fig.add_subplot(gs[2, :2])
    ax3.set_facecolor('#16213e')
    reg_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=True)
    ax3.barh(reg_sales.index, reg_sales.values, color=accent_colors[:4], height=0.5, edgecolor='#1a1a2e')
    ax3.set_title('Sales by Region', color=title_color, fontsize=13, fontweight='bold')
    ax3.tick_params(colors=text_color)
    ax3.set_xlabel('Sales ($)', color=text_color)

    # Profit by Sub-Category (top 8)
    ax4 = fig.add_subplot(gs[2, 2:])
    ax4.set_facecolor('#16213e')
    sub_profit = df.groupby('Sub-Category')['Profit'].sum().sort_values(ascending=True).tail(8)
    colors_bar = ['#ff6b6b' if v < 0 else '#6bcb77' for v in sub_profit.values]
    ax4.barh(sub_profit.index, sub_profit.values, color=colors_bar, height=0.5, edgecolor='#1a1a2e')
    ax4.set_title('Top 8 Sub-Categories by Profit', color=title_color, fontsize=13, fontweight='bold')
    ax4.tick_params(colors=text_color)
    ax4.set_xlabel('Profit ($)', color=text_color)

    preview_path = os.path.join(base_dir, "dashboard", "dashboard_preview.png")
    fig.savefig(preview_path, dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Saved dashboard preview: {preview_path}")
    return preview_path


def create_excel_dashboard(df, base_dir):
    """Create Excel dashboard with charts using xlsxwriter."""
    import xlsxwriter

    xlsx_path = os.path.join(base_dir, "dashboard", "sales_dashboard.xlsx")
    wb = xlsxwriter.Workbook(xlsx_path)

    # Formats
    title_fmt = wb.add_format({'bold': True, 'font_size': 16, 'font_color': '#1a1a2e',
                               'bottom': 2, 'bottom_color': '#3498db'})
    header_fmt = wb.add_format({'bold': True, 'bg_color': '#2c3e50', 'font_color': 'white',
                                'border': 1, 'text_wrap': True, 'align': 'center'})
    money_fmt = wb.add_format({'num_format': '$#,##0.00', 'border': 1, 'align': 'right'})
    num_fmt = wb.add_format({'num_format': '#,##0', 'border': 1, 'align': 'right'})
    pct_fmt = wb.add_format({'num_format': '0.0%', 'border': 1, 'align': 'right'})
    cell_fmt = wb.add_format({'border': 1, 'align': 'left'})
    kpi_val_fmt = wb.add_format({'bold': True, 'font_size': 18, 'font_color': '#2c3e50',
                                  'align': 'center', 'valign': 'vcenter'})
    kpi_lbl_fmt = wb.add_format({'font_size': 10, 'font_color': '#7f8c8d',
                                  'align': 'center', 'valign': 'vcenter'})

    # ───── Sheet 1: Summary Dashboard ─────
    ws = wb.add_worksheet('Dashboard Summary')
    ws.hide_gridlines(2)
    ws.set_tab_color('#3498db')
    ws.set_column('A:A', 3)
    ws.set_column('B:G', 18)

    ws.merge_range('B2:G2', 'Sales Performance Dashboard', title_fmt)

    # KPIs
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    total_orders = df['Order ID'].nunique()
    avg_discount = df['Discount'].mean()

    kpis = [('B', 'Total Sales', f'${total_sales:,.0f}'),
            ('C', 'Total Profit', f'${total_profit:,.0f}'),
            ('D', 'Orders', f'{total_orders:,}'),
            ('E', 'Avg Discount', f'{avg_discount:.1%}'),
            ('F', 'Profit Margin', f'{total_profit/total_sales:.1%}'),
            ('G', 'Avg Order', f'${total_sales/total_orders:,.0f}')]
    for col_letter, label, value in kpis:
        ws.write(f'{col_letter}4', value, kpi_val_fmt)
        ws.write(f'{col_letter}5', label, kpi_lbl_fmt)

    # ───── Sheet 2: Sales by Category ─────
    ws2 = wb.add_worksheet('Category Analysis')
    ws2.set_tab_color('#e74c3c')
    ws2.set_column('A:A', 20)
    ws2.set_column('B:D', 15)

    cat_data = df.groupby('Category').agg({'Sales': 'sum', 'Profit': 'sum', 'Quantity': 'sum'}).reset_index()
    cat_data = cat_data.sort_values('Sales', ascending=False)
    ws2.write('A1', 'Category', header_fmt)
    ws2.write('B1', 'Sales', header_fmt)
    ws2.write('C1', 'Profit', header_fmt)
    ws2.write('D1', 'Quantity', header_fmt)
    for i, row in enumerate(cat_data.itertuples(), 1):
        ws2.write(i, 0, row.Category, cell_fmt)
        ws2.write(i, 1, row.Sales, money_fmt)
        ws2.write(i, 2, row.Profit, money_fmt)
        ws2.write(i, 3, row.Quantity, num_fmt)

    chart1 = wb.add_chart({'type': 'column'})
    chart1.add_series({'name': 'Sales', 'categories': ['Category Analysis', 1, 0, len(cat_data), 0],
                       'values': ['Category Analysis', 1, 1, len(cat_data), 1],
                       'fill': {'color': '#3498db'}})
    chart1.add_series({'name': 'Profit', 'categories': ['Category Analysis', 1, 0, len(cat_data), 0],
                       'values': ['Category Analysis', 1, 2, len(cat_data), 2],
                       'fill': {'color': '#2ecc71'}})
    chart1.set_title({'name': 'Sales & Profit by Category'})
    chart1.set_size({'width': 600, 'height': 400})
    ws2.insert_chart('F2', chart1)

    # ───── Sheet 3: Regional Analysis ─────
    ws3 = wb.add_worksheet('Regional Analysis')
    ws3.set_tab_color('#2ecc71')
    ws3.set_column('A:A', 15)
    ws3.set_column('B:D', 15)

    reg_data = df.groupby('Region').agg({'Sales': 'sum', 'Profit': 'sum', 'Quantity': 'sum'}).reset_index()
    reg_data = reg_data.sort_values('Sales', ascending=False)
    ws3.write('A1', 'Region', header_fmt)
    ws3.write('B1', 'Sales', header_fmt)
    ws3.write('C1', 'Profit', header_fmt)
    ws3.write('D1', 'Quantity', header_fmt)
    for i, row in enumerate(reg_data.itertuples(), 1):
        ws3.write(i, 0, row.Region, cell_fmt)
        ws3.write(i, 1, row.Sales, money_fmt)
        ws3.write(i, 2, row.Profit, money_fmt)
        ws3.write(i, 3, row.Quantity, num_fmt)

    chart2 = wb.add_chart({'type': 'pie'})
    chart2.add_series({'name': 'Sales by Region',
                       'categories': ['Regional Analysis', 1, 0, len(reg_data), 0],
                       'values': ['Regional Analysis', 1, 1, len(reg_data), 1],
                       'data_labels': {'percentage': True}})
    chart2.set_title({'name': 'Sales Distribution by Region'})
    chart2.set_size({'width': 500, 'height': 400})
    ws3.insert_chart('F2', chart2)

    # ───── Sheet 4: Monthly Trend ─────
    ws4 = wb.add_worksheet('Monthly Trend')
    ws4.set_tab_color('#f39c12')
    ws4.set_column('A:A', 15)
    ws4.set_column('B:C', 15)

    monthly = df.groupby(df['Order Date'].dt.to_period('M')).agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    monthly['Order Date'] = monthly['Order Date'].astype(str)
    ws4.write('A1', 'Month', header_fmt)
    ws4.write('B1', 'Sales', header_fmt)
    ws4.write('C1', 'Profit', header_fmt)
    for i, row in enumerate(monthly.itertuples(), 1):
        ws4.write(i, 0, str(row._1), cell_fmt)
        ws4.write(i, 1, row.Sales, money_fmt)
        ws4.write(i, 2, row.Profit, money_fmt)

    chart3 = wb.add_chart({'type': 'line'})
    chart3.add_series({'name': 'Sales', 'categories': ['Monthly Trend', 1, 0, len(monthly), 0],
                       'values': ['Monthly Trend', 1, 1, len(monthly), 1],
                       'line': {'color': '#e74c3c', 'width': 2}})
    chart3.add_series({'name': 'Profit', 'categories': ['Monthly Trend', 1, 0, len(monthly), 0],
                       'values': ['Monthly Trend', 1, 2, len(monthly), 2],
                       'line': {'color': '#2ecc71', 'width': 2}})
    chart3.set_title({'name': 'Monthly Sales & Profit Trend'})
    chart3.set_size({'width': 800, 'height': 400})
    ws4.insert_chart('E2', chart3)

    wb.close()
    print(f"Saved Excel dashboard: {xlsx_path}")
    return xlsx_path
