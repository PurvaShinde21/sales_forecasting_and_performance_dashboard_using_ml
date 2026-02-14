"""
ML Modeling Module - Stage 3 of the Sales Forecasting Pipeline
"""
import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.preprocessing import LabelEncoder

def run_ml_model(df, base_dir):
    """Train ML models for sales prediction."""
    print("=" * 60)
    print("STAGE 3: ML SALES PREDICTION MODEL")
    print("=" * 60)

    # Feature engineering
    le_dict = {}
    cat_cols = ['Ship Mode', 'Segment', 'Region', 'Category', 'Sub-Category']
    df_ml = df.copy()
    for col in cat_cols:
        le = LabelEncoder()
        df_ml[col + '_Enc'] = le.fit_transform(df_ml[col].astype(str))
        le_dict[col] = le

    features = ['Quantity', 'Discount', 'Ship Mode_Enc', 'Segment_Enc',
                'Region_Enc', 'Category_Enc', 'Sub-Category_Enc',
                'Order Year', 'Order Month', 'Order DayOfWeek', 'Shipping Days']
    target = 'Sales'

    X = df_ml[features].values
    y = df_ml[target].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Training set: {X_train.shape[0]} samples")
    print(f"Test set:     {X_test.shape[0]} samples")
    print(f"Features:     {features}")
    print()

    results = {}

    # Linear Regression
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    y_pred_lr = lr.predict(X_test)
    r2_lr = r2_score(y_test, y_pred_lr)
    mae_lr = mean_absolute_error(y_test, y_pred_lr)
    rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))
    results['Linear Regression'] = {'R2': r2_lr, 'MAE': mae_lr, 'RMSE': rmse_lr, 'model': lr}
    print(f"Linear Regression:  R²={r2_lr:.4f}  MAE={mae_lr:.2f}  RMSE={rmse_lr:.2f}")

    # Random Forest
    rf = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1, max_depth=15)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    r2_rf = r2_score(y_test, y_pred_rf)
    mae_rf = mean_absolute_error(y_test, y_pred_rf)
    rmse_rf = np.sqrt(mean_squared_error(y_test, y_pred_rf))
    results['Random Forest'] = {'R2': r2_rf, 'MAE': mae_rf, 'RMSE': rmse_rf, 'model': rf}
    print(f"Random Forest:      R²={r2_rf:.4f}  MAE={mae_rf:.2f}  RMSE={rmse_rf:.2f}")

    # Determine best model
    best_name = max(results, key=lambda k: results[k]['R2'])
    best = results[best_name]
    print(f"\nBest Model: {best_name} (R² = {best['R2']:.4f})")

    # Save model
    model_path = os.path.join(base_dir, "models", "sales_prediction_model.pkl")
    joblib.dump(best['model'], model_path)
    print(f"Saved model to: {model_path}")

    # Save results
    results_path = os.path.join(base_dir, "outputs", "results.txt")
    with open(results_path, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("SALES PREDICTION MODEL - EVALUATION RESULTS\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Dataset: Superstore Sales ({len(df)} records)\n")
        f.write(f"Train/Test Split: 80/20\n")
        f.write(f"Features Used: {', '.join(features)}\n")
        f.write(f"Target: {target}\n\n")
        f.write("-" * 60 + "\n")
        f.write(f"{'Model':<25} {'R² Score':<12} {'MAE':<12} {'RMSE':<12}\n")
        f.write("-" * 60 + "\n")
        for name, m in results.items():
            f.write(f"{name:<25} {m['R2']:<12.4f} {m['MAE']:<12.2f} {m['RMSE']:<12.2f}\n")
        f.write("-" * 60 + "\n")
        f.write(f"\nBest Model: {best_name}\n")
        f.write(f"  R² Score: {best['R2']:.4f}\n")
        f.write(f"  MAE:      {best['MAE']:.2f}\n")
        f.write(f"  RMSE:     {best['RMSE']:.2f}\n")

        # Feature importance for RF
        if best_name == 'Random Forest':
            f.write(f"\nFeature Importance (Random Forest):\n")
            importances = sorted(zip(features, rf.feature_importances_), key=lambda x: x[1], reverse=True)
            for feat, imp in importances:
                f.write(f"  {feat:<25} {imp:.4f}\n")

    print(f"Saved results to: {results_path}")
    print()
    return results, features
