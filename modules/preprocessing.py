# modules/preprocessing.py
import pandas as pd

def summary_statistics(df):
    """Returns summary statistics of the dataframe."""
    return df.describe()

def iqr_outlier_removal(df, columns):
    """Removes outliers using the IQR method."""
    Q1 = df[columns].quantile(0.25)
    Q3 = df[columns].quantile(0.75)
    IQR = Q3 - Q1
    filtered_data = df[~((df[columns] < (Q1 - 1.5 * IQR)) | (df[columns] > (Q3 + 1.5 * IQR))).any(axis=1)]
    return filtered_data

def handle_missing_values(df, strategy='median'):
    """Handles missing values in the dataframe by filling them with the specified strategy."""
    numeric_cols = df.select_dtypes(include=['number']).columns  # Only numeric columns
    if strategy == 'median':
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())  # Only fill numeric columns
    elif strategy == 'mean':
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
    elif strategy == 'mode':
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mode().iloc[0])
    else:
        raise ValueError("Strategy must be one of ['median', 'mean', 'mode']")
    
    return df
