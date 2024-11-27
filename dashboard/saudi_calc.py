from figures import create_total_bar  # Import other necessary figure creation functions
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container
from pages.gender import *
import os
import plotly.express as px
import plotly.graph_objects as go
from figures import *


# Set up file paths
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
data_folder_path = os.path.join(parent_dir, "data")

# Load data
region_employee_summary = pd.read_csv(
    os.path.join(data_folder_path, "region_employee_summary.csv")
)
df_activity_region = pd.read_csv(
    os.path.join(data_folder_path, "df_activity_region.csv")
)
activity_education = pd.read_csv(
    os.path.join(data_folder_path, "activity_education.csv")
)
activity_programming = pd.read_csv(
    os.path.join(data_folder_path, "activity_programming.csv")
)

# Calculate totals
lastQ = df_activity_region[df_activity_region["Qseries"] == "2024-7"]
lastQ_eco = (
    lastQ.groupby("Economic_Activity")[
        [
            "Number_Of_Establishments",
            "Number_Of_Saudis",
            "Number_Of_Male_Saudis",
            "Number_Of_Female_Saudis",
            "Number_Of_Nonsaudis",
            "Number_Of_Male_Nonaudis",
            "Number_Of_Female_Nonaudis",
            "total_employees",
        ]
    ]
    .sum()
    .reset_index()
)
lastQ_region = (
    lastQ.groupby("region")[
        [
            "Number_Of_Establishments",
            "Number_Of_Saudis",
            "Number_Of_Male_Saudis",
            "Number_Of_Female_Saudis",
            "Number_Of_Nonsaudis",
            "Number_Of_Male_Nonaudis",
            "Number_Of_Female_Nonaudis",
            "total_employees",
        ]
    ]
    .sum()
    .reset_index()
)


total_saudis = lastQ["Number_Of_Saudis"].sum()
total_nonsaudis = lastQ["Number_Of_Nonsaudis"].sum()

region_employee_summary["total_saudis_percentage"] = region_employee_summary.apply(
    lambda row: (
        (row["Number_Of_Saudis"] / row["total_employees"] * 100)
        if row["total_employees"] > 0
        else 0
    ),
    axis=1,
)
region_employee_summary.sort_values(by="total_saudis_percentage", inplace=True)
region_employee_summary["order"] = 0
# region_employee_summary["order"] = region_employee_summary["order"].apply(lambda x: x+i for i in range(1, 16))

# Calculate the top 5 regions with the highest percentage of Saudis employed
top_5_regions = region_employee_summary.nlargest(5, "total_saudis_percentage")
last_5_regions = region_employee_summary.nsmallest(5, "total_saudis_percentage")


def get_percent(df):
    # Calculate Saudi and non-Saudi percentages for df_2024
    df["total_saudis_percentage"] = df["Number_Of_Saudis"] / df["total_employees"]
    df["total_non_saudis_percentage"] = 1 - df["total_saudis_percentage"]


get_percent(df_activity_region)
get_percent(lastQ)
get_percent(lastQ_eco)
get_percent(lastQ_region)

lastQ_region = lastQ_region.sort_values(by="total_saudis_percentage", ascending=False)
lastQ_region["order"] = range(1, len(lastQ_region) + 1)

top1_region = lastQ[lastQ["region"] == "المنطقة الشرقية"]
last_region = lastQ[lastQ["region"] == "منطقة نجران"]

top_activities = top1_region.nlargest(5, "total_saudis_percentage")
top_activities_last = last_region.nlargest(5, "total_saudis_percentage")
last_activities = lastQ_eco.nsmallest(5, "total_saudis_percentage")

# Add latitude and longitude to the data
region_coordinates = {
    "منطقة الرياض": {"lat": 24.7136, "lon": 46.6753},
    "منطقة مكة المكرمة": {"lat": 21.3891, "lon": 39.8579},
    "المنطقة الشرقية": {"lat": 26.4207, "lon": 50.0888},
    "منطقة المدينة المنورة": {"lat": 24.5247, "lon": 39.5692},
    "منطقة القصيم": {"lat": 26.3260, "lon": 43.9750},
    "منطقة عسير": {"lat": 18.2164, "lon": 42.5053},
    "منطقة تبوك": {"lat": 28.3838, "lon": 36.5650},
    "منطقة حائل": {"lat": 27.5219, "lon": 41.7057},
    "منطقة الحدود الشمالية": {"lat": 30.9843, "lon": 41.1183},
    "منطقة جازان": {"lat": 16.8892, "lon": 42.5700},
    "منطقة نجران": {"lat": 17.5650, "lon": 44.2236},
    "منطقة الباحة": {"lat": 20.0129, "lon": 41.4677},
    "منطقة الجوف": {"lat": 30.3158, "lon": 38.3691},
}

region_employee_summary["lat"] = region_employee_summary["region"].apply(
    lambda x: region_coordinates[x]["lat"]
)
region_employee_summary["lon"] = region_employee_summary["region"].apply(
    lambda x: region_coordinates[x]["lon"]
)
# معدل نمو التعليم في المملكة
activity_education["sorted_q"] = activity_education["Qseries"].apply(
    lambda x: tuple(map(int, str(x).split("-")))
)
line_data_edu = activity_education.sort_values(by="sorted_q").drop(columns=["sorted_q"])
# line_data = line_data.sort_values(by="Qseries")  # Ensure years are in order
first_saudis_edu = line_data_edu.loc[
    line_data_edu["Qseries"] == line_data_edu["Qseries"].min(), "Number_Of_Saudis"
].iloc[0]
first_nonsaudis_edu = line_data_edu.loc[
    line_data_edu["Qseries"] == line_data_edu["Qseries"].min(), "Number_Of_Nonsaudis"
].iloc[0]
# Calculate percentage change for Saudis and Non-Saudis
line_data_edu["Saudis_change_perc"] = (
    (line_data_edu["Number_Of_Saudis"] - first_saudis_edu) / first_saudis_edu
) * 100
line_data_edu["NonSaudis_change_perc"] = (
    (line_data_edu["Number_Of_Nonsaudis"] - first_nonsaudis_edu) / first_nonsaudis_edu
) * 100


# معدل نمو قطاع البرمجة في المملكة
activity_programming["sorted_q"] = activity_programming["Qseries"].apply(
    lambda x: tuple(map(int, str(x).split("-")))
)
line_data_prog = activity_programming.sort_values(by="sorted_q").drop(
    columns=["sorted_q"]
)
# line_data = line_data.sort_values(by="Qseries")  # Ensure years are in order
# Identify the first quarter's values
first_saudis = line_data_prog.loc[
    line_data_prog["Qseries"] == line_data_prog["Qseries"].min(), "Number_Of_Saudis"
].iloc[0]
first_nonsaudis = line_data_prog.loc[
    line_data_prog["Qseries"] == line_data_prog["Qseries"].min(), "Number_Of_Nonsaudis"
].iloc[0]

# Calculate percentage change relative to the first quarter
line_data_prog["Saudis_change_perc"] = (
    (line_data_prog["Number_Of_Saudis"] - first_saudis) / first_saudis
) * 100
line_data_prog["NonSaudis_change_perc"] = (
    (line_data_prog["Number_Of_Nonsaudis"] - first_nonsaudis) / first_nonsaudis
) * 100
