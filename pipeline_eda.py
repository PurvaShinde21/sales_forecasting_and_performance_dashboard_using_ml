"""
EDA Analysis Module - Stage 2 of the Sales Forecasting Pipeline
"""
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import os

def run_eda(df, base_dir):
    """Run exploratory data analysis and save charts."""
    print("=" * 60)
    print("STAGE 2: EXPLORATORY DATA ANALYSIS")
    print("=" * 60)

    sns.set_theme(style="whitegrid", palette="deep")
    fig, axes = plt.subplots(3, 2, figsize=(18, 20))
    fig.suptitle('Sales Performance - Exploratory Data Analysis', fontsize=20, fontweight='bold', y=0.98)

    # 1. Sales by Category
    cat_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=True)
    colors_cat = ['#3498db', '#e74c3c', '#2ecc71']
    axes[0, 0].barh(cat_sales.index, cat_sales.values, color=colors_cat, edgecolor='white', height=0.5)
    axes[0, 0].set_title('Total Sales by Category', fontsize=14, fontweight='bold')
    axes[0, 0].set_xlabel('Sales ($)')
    for i, v in enumerate(cat_sales.values):
        axes[0, 0].text(v + 5000, i, f'${v:,.0f}', va='center', fontsize=10)

    # 2. Sales by Region
    reg_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
    colors_reg = ['#1abc9c', '#3498db', '#9b59b6', '#e67e22']
    axes[0, 1].bar(reg_sales.index, reg_sales.values, color=colors_reg, edgecolor='white', width=0.5)
    axes[0, 1].set_title('Total Sales by Region', fontsize=14, fontweight='bold')
    axes[0, 1].set_ylabel('Sales ($)')
    for i, v in enumerate(reg_sales.values):
        axes[0, 1].text(i, v + 5000, f'${v:,.0f}', ha='center', fontsize=10)

    # 3. Monthly Sales Trend
    monthly = df.groupby([df['Order Date'].dt.to_period('M')])['Sales'].sum().reset_index()
    monthly['Order Date'] = monthly['Order Date'].dt.to_timestamp()
    axes[1, 0].plot(monthly['Order Date'], monthly['Sales'], color='#e74c3c', linewidth=2, marker='o', markersize=3)
    axes[1, 0].fill_between(monthly['Order Date'], monthly['Sales'], alpha=0.15, color='#e74c3c')
    axes[1, 0].set_title('Monthly Sales Trend', fontsize=14, fontweight='bold')
    axes[1, 0].set_xlabel('Date')
    axes[1, 0].set_ylabel('Sales ($)')
    axes[1, 0].tick_params(axis='x', rotation=45)

    # 4. Sales by Segment
    seg_sales = df.groupby('Segment')['Sales'].sum()
    colors_seg = ['#f39c12', '#e74c3c', '#3498db']
    axes[1, 1].pie(seg_sales.values, labels=seg_sales.index, autopct='%1.1f%%',
                   colors=colors_seg, startangle=90, textprops={'fontsize': 11})
    axes[1, 1].set_title('Sales Distribution by Segment', fontsize=14, fontweight='bold')

    # 5. Top 10 Sub-Categories by Sales
    sub_sales = df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=True).tail(10)
    axes[2, 0].barh(sub_sales.index, sub_sales.values, color=sns.color_palette('viridis', 10), edgecolor='white')
    axes[2, 0].set_title('Top 10 Sub-Categories by Sales', fontsize=14, fontweight='bold')
    axes[2, 0].set_xlabel('Sales ($)')

    # 6. Discount vs Profit scatter
    sample = df.sample(min(1000, len(df)), random_state=42)
    scatter = axes[2, 1].scatter(sample['Discount'], sample['Profit'],
                                  c=sample['Sales'], cmap='RdYlGn', alpha=0.6, s=30, edgecolors='gray', linewidth=0.3)
    axes[2, 1].set_title('Discount vs Profit (colored by Sales)', fontsize=14, fontweight='bold')
    axes[2, 1].set_xlabel('Discount')
    axes[2, 1].set_ylabel('Profit ($)')
    axes[2, 1].axhline(y=0, color='red', linestyle='--', alpha=0.5)
    plt.colorbar(scatter, ax=axes[2, 1], label='Sales ($)')

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    chart_path = os.path.join(base_dir, "outputs", "charts.png")
    fig.savefig(chart_path, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"Saved EDA charts to: {chart_path}")

    # Print summary stats
    print(f"\nTotal Sales: ${df['Sales'].sum():,.2f}")
    print(f"Total Profit: ${df['Profit'].sum():,.2f}")
    print(f"Average Discount: {df['Discount'].mean():.2%}")
    print(f"Total Orders: {df['Order ID'].nunique()}")
    print(f"Top Category: {cat_sales.index[-1]} (${cat_sales.values[-1]:,.2f})")
    print(f"Top Region: {reg_sales.index[0]} (${reg_sales.values[0]:,.2f})")
    print()

    return chart_path
