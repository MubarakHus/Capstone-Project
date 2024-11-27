from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

import os

current_dir = os.getcwd()
# Navigate to the parent folder
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))


def gender_programing(selected_activity=None):
    df = pd.read_csv(os.path.join(parent_dir, "data", "male_female_per_eco.csv"))
    program_eco = df[
        df["Economic_Activity"]
        == "أنشطة البرمجة الحاسوبية والخبرة الاستشارية وما يتصل بها من أنشطة"
    ]

    rate_differanc_program = program_eco["Rate_Difference"].values.tolist()[0]

    # stacked bar chart
    fig = go.Figure()

    total_male = program_eco["Number_Of_Male_Saudis"].sum()
    total_female = program_eco["Number_Of_Female_Saudis"].sum()
    # Data for the pie chart
    labels = ["ذكر", "أنثى"]
    values = [total_male, total_female]

    fig.add_trace(
        go.Pie(
            labels=labels,
            values=values,
            name="الجنس",
            textinfo="percent",
            insidetextfont=dict(size=15, color="white"),
            marker=dict(colors=["#1fb89b", "#e04764"]),
        )
    )
    fig.update_layout(
        legend_title="الجنس",
        plot_bgcolor="white",
        paper_bgcolor="white",  # Page background
        margin=dict(t=40, b=40, l=40, r=40),  # Adjust margins
        title="أنشطة البرمجة والاستشارات",
        title_x=0.5,
        title_y=0.05,
        width=350,
        height=350,
    )

    return fig, rate_differanc_program


def lib_managment():
    df = pd.read_csv(os.path.join(parent_dir, "data", "male_female_per_eco.csv"))
    lib_managment = df[
        df["Economic_Activity"]
        == "أنشطة المكاتب الرئيسية، والأنشطة الاستشارية في مجال الإدارة"
    ]

    rate_differanc_lib_management = lib_managment["Rate_Difference"].values.tolist()[0]

    # stacked bar chart
    fig = go.Figure()

    total_male = lib_managment["Number_Of_Male_Saudis"].sum()
    total_female = lib_managment["Number_Of_Female_Saudis"].sum()
    # Data for the pie chart
    labels = ["ذكر", "أنثى"]
    values = [total_male, total_female]

    fig.add_trace(
        go.Pie(
            labels=labels,
            values=values,
            name="الجنس",
            textinfo="percent",
            insidetextfont=dict(size=15, color="white"),
            marker=dict(colors=["#1fb89b", "#e04764"]),
        )
    )
    fig.update_layout(
        legend_title="الجنس",
        plot_bgcolor="white",
        paper_bgcolor="white",  # Page background
        margin=dict(t=40, b=40, l=40, r=40),  # Adjust margins
        title="أنشطة ادارة المكتبات ودعم الاعمال",
        title_x=0.5,
        title_y=0.05,
        width=350,
        height=350,
    )

    return fig, rate_differanc_lib_management


def real_estate():
    df = pd.read_csv(os.path.join(parent_dir, "data", "male_female_per_eco.csv"))
    real_estate = df[df["Economic_Activity"] == "الأنشطة العقارية"]

    rate_differanc_real_estate = real_estate["Rate_Difference"].values.tolist()[0]

    # stacked bar chart
    fig = go.Figure()
    total_male = real_estate["Number_Of_Male_Saudis"].sum()
    total_female = real_estate["Number_Of_Female_Saudis"].sum()
    # Data for the pie chart
    labels = ["ذكر", "أنثى"]
    values = [total_male, total_female]

    fig.add_trace(
        go.Pie(
            labels=labels,
            values=values,
            name="الجنس",
            textinfo="percent",
            insidetextfont=dict(size=15, color="white"),
            marker=dict(colors=["#1fb89b", "#e04764"]),
        )
    )
    fig.update_layout(
        legend_title="الجنس",
        plot_bgcolor="white",
        paper_bgcolor="white",  # Page background
        margin=dict(t=40, b=40, l=40, r=40),  # Adjust margins
        title="أنشطة العقار",
        title_x=0.5,
        title_y=0.05,
        width=350,
        height=350,
    )
    return fig, rate_differanc_real_estate


def oil_and_gas():
    df = pd.read_csv(os.path.join(parent_dir, "data", "male_female_per_eco.csv"))
    oil_and_gas = df[df["Economic_Activity"] == "استخراج النفط الخام والغاز الطبيعي"]

    rate_differanc_oil_and_gas = oil_and_gas["Rate_Difference"].values.tolist()[0]
    # stacked bar chart
    fig = go.Figure()
    total_male = oil_and_gas["Number_Of_Male_Saudis"].sum()
    total_female = oil_and_gas["Number_Of_Female_Saudis"].sum()
    # Data for the pie chart
    labels = ["ذكر", "أنثى"]
    values = [total_male, total_female]

    fig.add_trace(
        go.Pie(
            labels=labels,
            values=values,
            name="الجنس",
            textinfo="percent",
            insidetextfont=dict(size=15, color="white"),
            marker=dict(colors=["#1fb89b", "#e04764"]),
        )
    )
    fig.update_layout(
        legend_title="الجنس",
        plot_bgcolor="white",
        paper_bgcolor="white",  # Page background
        margin=dict(t=40, b=40, l=40, r=40),  # Adjust margins
        title="أنشطة استخراج النفط الخام والغاز",
        title_x=0.5,
        title_y=0.05,
        width=350,
        height=350,
    )
    return fig, rate_differanc_oil_and_gas


def gender_trends():
    df = pd.read_csv(
        os.path.join(parent_dir, "data", "male_female_per_year_quarter.csv")
    )
    # stacked bar chart
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=df["year"],
            y=df["Number_Of_Male_Saudis"],
            name="ذكر",
            marker_color="#FFC107",
            width=0.2,
        )
    )

    fig.add_trace(
        go.Bar(
            x=df["year"],
            y=df["Number_Of_Female_Saudis"],
            name="أنثى",
            marker_color="#FF7F50",
            width=0.2,
        )
    )

    fig.update_layout(
        xaxis_title="السنة",
        yaxis_title="عدد الموظفين",
        barmode="group",
        legend_title="الجنس",
        plot_bgcolor="white",  # Chart background
        paper_bgcolor="white",  # Page background
    )
    return fig


def gender_map_real_estate():
    data = pd.read_csv(
        os.path.join(parent_dir, "data", "male_female_per_region_eco.csv")
    )
    data = data[data["Economic_Activity"] == "الأنشطة العقارية"]
    data = data.sort_values(by="Rate_Difference", ascending=False)
    fig = go.Figure()
    color_palette = ["#59a46f", "#59a46f", "#59a46f"]
    fig.add_trace(
        go.Bar(
            x=data["region"],
            y=data["Rate_Difference"],
            text=data["Rate_Difference"],
            textposition="outside",
            width=0.2,
            marker_color=color_palette[: len(data)],
        )
    )
    fig.update_layout(
        xaxis_title="المنطقة",
        yaxis_title="معدل الفرق",
        title_x=0.5,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=14),
        yaxis_showgrid=False,
        yaxis={"visible": False, "showticklabels": False},
    )

    return fig


def gender_map_oil_and_gas():
    data = pd.read_csv(
        os.path.join(parent_dir, "data", "male_female_per_region_eco.csv")
    )
    data = data[data["Economic_Activity"] == "استخراج النفط الخام والغاز الطبيعي"]
    fig = go.Figure()
    color_palette = ["#59a46f", "#59a46f", "#59a46f"]
    fig.add_trace(
        go.Bar(
            x=data["region"],
            y=data["Rate_Difference"],
            text=data["Rate_Difference"],
            textposition="outside",
            width=0.1,
            marker_color=color_palette[: len(data)],
        )
    )
    fig.update_layout(
        xaxis_title="المنطقة",
        yaxis_title="معدل الفرق",
        title_x=0.5,
        plot_bgcolor="white",
        paper_bgcolor="white",
        font=dict(size=14),
        yaxis_showgrid=False,
        yaxis={"visible": False, "showticklabels": False},
    )

    return fig
