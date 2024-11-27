from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import os

current_dir = os.getcwd()
# Navigate to the parent folder
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
# Load the dataset
df_combined = pd.read_csv(
    os.path.join(parent_dir, "data/total_saudis_nonsaudis_by_quarter.csv")
)

# Remove extra spaces from column names
df_combined.columns = df_combined.columns.str.strip()

# Create a new column combining year and quarter
df_combined["Year_Quarter"] = (
    df_combined["Year"].astype(str) + " Q" + df_combined["Quarter"].astype(str)
)


# Function to calculate growth rate
def calculate_growth(df, column_name):
    growth = [0]  # Start with 0 growth for the first row
    for i in range(1, len(df)):
        growth.append(
            (df[column_name].iloc[i] - df[column_name].iloc[i - 1])
            / df[column_name].iloc[i - 1]
            * 100
        )
    return growth


df_combined["Growth"] = calculate_growth(df_combined, "Total_Saudis_Nonsaudis")
