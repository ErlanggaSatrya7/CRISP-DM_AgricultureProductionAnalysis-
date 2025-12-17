import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'modules'))

import streamlit as st
import pandas as pd
import numpy as np

from modules.data_loader import load_data
from modules.preprocessing import summary_statistics, iqr_outlier_removal, handle_missing_values
from modules.visualization import histogram, boxplot
from modules.export_utils import download_csv, export_data_pdf, export_fig_to_pdf

# ------------------------
# PAGE CONFIG
# ------------------------
st.set_page_config(page_title="Agricultural Production Analysis", layout="wide")
st.title("📊 Agricultural Production Analysis ")

# ------------------------
# LOAD DATA
# ------------------------
df = load_data()

# ------------------------
# DATA OVERVIEW
# ------------------------
st.subheader("1️⃣ Data Overview")
st.write("Here's a preview of the raw data:")
st.dataframe(df.head())

# ------------------------
# Data Cleaning
# ------------------------
st.subheader("2️⃣ Data Cleaning")
st.write("Handling missing values by filling them with the median of each column.")

# Display missing values before cleaning
missing_cols = df.columns[df.isnull().any()]
st.write("Columns with missing values:", missing_cols)

# Handle Missing Values (median strategy)
df_cleaned = handle_missing_values(df, strategy='median')

# Show missing values after cleaning
missing_cols_after = df_cleaned.columns[df_cleaned.isnull().any()]
st.write("Columns with missing values after handling:", missing_cols_after)

# ------------------------
# Remove Duplicates
# ------------------------
st.write("Removing duplicate rows from the data.")
df_cleaned = df_cleaned.drop_duplicates()
st.write(f"Number of rows after removing duplicates: {df_cleaned.shape[0]}")

# ------------------------
# Outlier Handling (IQR)
# ------------------------
st.subheader("3️⃣ Handling Outlier (IQR)")
st.write("Removing outliers using the IQR (Interquartile Range) method.")

selected_cols = st.multiselect("Select columns for IQR outlier removal:", df.select_dtypes(include="number").columns.tolist(), default=df.select_dtypes(include="number").columns.tolist())

st.write("Before IQR outlier removal:")
st.pyplot(histogram(df_cleaned, selected_cols[0], f"Histogram of {selected_cols[0]} Before Outlier Removal"))
st.pyplot(boxplot(df_cleaned, selected_cols[0], f"Boxplot of {selected_cols[0]} Before Outlier Removal"))

df_cleaned = iqr_outlier_removal(df_cleaned, selected_cols)

st.write(f"Number of rows after IQR removal: {df_cleaned.shape[0]}")

st.write("After IQR outlier removal:")
st.pyplot(histogram(df_cleaned, selected_cols[0], f"Histogram of {selected_cols[0]} After Outlier Removal"))
st.pyplot(boxplot(df_cleaned, selected_cols[0], f"Boxplot of {selected_cols[0]} After Outlier Removal"))

# ------------------------
# Data Transformation
# ------------------------
st.subheader("4️⃣ Data Transformation")

st.write("Creating a log-transformed feature for 'Production' to reduce skewness.")
df_cleaned['Log_Production'] = np.log(df_cleaned['Production'] + 1)  

st.write(f"Here's a preview of the data with the log-transformed 'Production' column:")
st.dataframe(df_cleaned[['Production', 'Log_Production']].head())

# ------------------------
# Feature Scaling
# ------------------------
st.subheader("5️⃣ Feature Scaling")

scaling_choice = st.selectbox("Select Scaling Method", ['None', 'Standardization', 'Min-Max'])
if scaling_choice == 'Standardization':
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    df_cleaned[df_cleaned.select_dtypes(include=["float64", "int64"]).columns] = scaler.fit_transform(df_cleaned.select_dtypes(include=["float64", "int64"]))
elif scaling_choice == 'Min-Max':
    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()
    df_cleaned[df_cleaned.select_dtypes(include=["float64", "int64"]).columns] = scaler.fit_transform(df_cleaned.select_dtypes(include=["float64", "int64"]))

# ------------------------
# Exploratory Data Analysis (EDA)
# ------------------------
st.subheader("6️⃣ EDA: Summary Statistics")
st.write("Here's a summary of the data after cleaning and transformations:")
st.dataframe(summary_statistics(df_cleaned))

# ------------------------
# Visualization (After Transformation)
# ------------------------
st.subheader("7️⃣ Visualizing the Cleaned and Transformed Data")
column_to_plot = st.selectbox("Select a column for histogram:", df_cleaned.select_dtypes(include="number").columns.tolist())
st.pyplot(histogram(df_cleaned, column_to_plot, f"Histogram of {column_to_plot} (After Transformation)"))

# ------------------------
# Export / Download
# ------------------------
st.subheader("📥 Download / Export")

download_csv(df_cleaned)

stats_clean = summary_statistics(df_cleaned)
export_data_pdf(df_cleaned, stats_clean, filename="report_agriculture.pdf")

fig_example = histogram(df_cleaned, column_to_plot, f"Histogram of {column_to_plot}")
export_fig_to_pdf(fig_example, filename=f"{column_to_plot}_histogram.pdf")
