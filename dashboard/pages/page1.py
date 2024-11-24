from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

import os

current_dir = os.getcwd()
# Navigate to the parent folder
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))


def format_number(num):
    if num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"  # millions
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"  # thousands
    else:
        return str(num)


def sum_employees():
    df = pd.read_csv(os.path.join(parent_dir, "data", "df.csv"))
    tot_emps_eco_act = df.loc[df["Q"] == 4]
    df["total_employees_"] = (
        tot_emps_eco_act["Number_Of_Saudis"] + tot_emps_eco_act["Number_Of_Nonsaudis"]
    )
    sum = tot_emps_eco_act["total_employees_"].sum().round(1)
    sum = format_number(sum)
    return sum


def saudi_total():
    df = pd.read_csv(os.path.join(parent_dir, "data", "df.csv"))
    saudi = format_number(df["Number_Of_Saudis"].sum())
    return saudi


def nonsaudi_total():
    df = pd.read_csv(os.path.join(parent_dir, "data", "df.csv"))
    nonsaudi = format_number(df["Number_Of_Nonsaudis"].sum())
    return nonsaudi


def employement_trends():

    all_data = pd.read_csv(os.path.join(parent_dir, "data", "df_q_group.csv"))

    # page 1: نظرة عامة على اتجاهات التوظيف

    # create the graph
    fig = px.line(
        all_data,
        x="Q",
        y="total_employees",
        color="year",
        labels={"Q": "الربع", "total_employees": "عدد الموظفين", "year": "السنة"},
        markers=True,
    )
    # style the graph
    fig.update_layout(
        title={
            "text": "عدد الموظفين حسب السنة",
            "x": 0.5,  # center the title
            "xanchor": "center",
            "yanchor": "top",
        },
        font=dict(color="#333333"),
        plot_bgcolor="#F5F5F5",
        paper_bgcolor="#F5F5F5",
    )

    return fig
