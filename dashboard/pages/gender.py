from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

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


def gender_percentage():
    data = pd.read_csv(os.path.join(parent_dir, "data", "saudis_total_2022_2024.csv"))
    # Calculate total employees and percentages
    data["Total Employees"] = data["Total Male Saudis"] + data["Total Female Saudis"]
    data["Male Percentage"] = (
        data["Total Male Saudis"] / data["Total Employees"]
    ) * 100
    data["Female Percentage"] = (
        data["Total Female Saudis"] / data["Total Employees"]
    ) * 100

    # Create the bar chart using Plotly Graph Objects
    fig = go.Figure()

    # Add data for males with percentages
    fig.add_trace(
        go.Bar(
            x=data["Year"],
            y=data["Male Percentage"],
            name="ذكور",
            marker_color="#FFC107",  # Soft navy blue
            text=data["Male Percentage"].apply(
                lambda x: f"{x:.1f}%"
            ),  # Display percentage
            textposition="outside",  # Show text outside bars
            width=0.2,
        )
    )

    # Add data for females with percentages
    fig.add_trace(
        go.Bar(
            x=data["Year"],
            y=data["Female Percentage"],
            name="إناث",
            marker_color="#FF7F50",  # Peachy coral
            text=data["Female Percentage"].apply(
                lambda x: f"{x:.1f}%"
            ),  # Display percentage
            textposition="outside",  # Show text outside bars
            width=0.2,
        )
    )

    # Update chart layout
    fig.update_layout(
        yaxis_showgrid=False,
        yaxis={"visible": False, "showticklabels": False},
        xaxis=dict(title="السنة", title_font=dict(color="#555555")),
        legend=dict(title="الجنس", font=dict(color="#555555")),
        plot_bgcolor="white",  # Chart background
        paper_bgcolor="white",  # Page background
        font=dict(color="#555555", size=13),
        barmode="group",  # Grouped bar mode
    )
    return fig


def gender_map_real_estate():
    data = pd.read_csv(
        os.path.join(parent_dir, "data", "male_female_per_region_eco.csv")
    )
    data = data[data["Economic_Activity"] == "الأنشطة العقارية"]
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
    data["lat"] = data["region"].apply(lambda x: region_coordinates[x]["lat"])
    data["lon"] = data["region"].apply(lambda x: region_coordinates[x]["lon"])
    fig = px.scatter_geo(
        data,
        lat="lat",
        lon="lon",
        size="Rate_Difference",
        hover_name="region",
        color="Rate_Difference",
        projection="natural earth",
        text=data["region"],
    )
    fig.update_geos(
        scope="asia", center={"lat": 23.8859, "lon": 45.0792}, fitbounds="locations"
    )
    fig.update_layout(
        font=dict(color="#333333"),
        coloraxis_colorbar=dict(
            title="% معدل الفرق بين الجنسين",  # Title for the color bar
            ticks="outside",  # Set ticks to be outside the bar
            tickwidth=2,  # Width of the ticks
            ticklen=10,  # Length of the ticks
            bgcolor="white",  # Chart background
        ),
    )
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br> معدل الفرق بين الجنسين %%{marker.size:.1f} <extra></extra>",
    )

    return fig


def gender_map_oil_and_gas():
    data = pd.read_csv(
        os.path.join(parent_dir, "data", "male_female_per_region_eco.csv")
    )
    data = data[data["Economic_Activity"] == "استخراج النفط الخام والغاز الطبيعي"]
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
    data["lat"] = data["region"].apply(lambda x: region_coordinates[x]["lat"])
    data["lon"] = data["region"].apply(lambda x: region_coordinates[x]["lon"])
    fig = px.scatter_geo(
        data,
        lat="lat",
        lon="lon",
        size="Rate_Difference",
        hover_name="region",
        color="Rate_Difference",
        projection="natural earth",
        text=data["region"],
    )
    fig.update_geos(
        scope="asia", center={"lat": 23.8859, "lon": 45.0792}, fitbounds="locations"
    )
    fig.update_layout(
        font=dict(color="#333333"),
        coloraxis_colorbar=dict(
            title="% معدل الفرق بين الجنسين",  # Title for the color bar
            ticks="outside",  # Set ticks to be outside the bar
            tickwidth=2,  # Width of the ticks
            ticklen=10,  # Length of the ticks
            bgcolor="white",  # Chart background
        ),
    )
    fig.update_traces(
        hovertemplate="<b>%{hovertext}</b><br> معدل الفرق بين الجنسين %%{marker.size:.1f} <extra></extra>",
    )

    return fig


def gender_programing(selected_activity=None):
    df = pd.read_csv(os.path.join(parent_dir, "data", "male_female_per_eco.csv"))
    program_eco = df[
        df["Economic_Activity"]
        == "أنشطة البرمجة الحاسوبية والخبرة الاستشارية وما يتصل بها من أنشطة"
    ]

    rate_differanc_program = program_eco["Rate_Difference"].values.tolist()[0]

    # stacked bar chart
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=program_eco["Economic_Activity"],
            y=program_eco["Number_Of_Male_Saudis"],
            name="ذكر",
            marker_color="#FFC107",
            textposition="outside",
            width=0.2,
        )
    )

    fig.add_trace(
        go.Bar(
            x=program_eco["Economic_Activity"],
            y=program_eco["Number_Of_Female_Saudis"],
            name="أنثى",
            marker_color="#FF7F50",
            textposition="outside",
            width=0.2,
        )
    )

    fig.update_layout(
        yaxis_showgrid=False,
        yaxis={"visible": False, "showticklabels": False},
        barmode="group",
        legend_title="الجنس",
        plot_bgcolor="white",  # Chart background
        paper_bgcolor="white",  # Page background
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

    fig.add_trace(
        go.Bar(
            x=lib_managment["Economic_Activity"],
            y=lib_managment["Number_Of_Male_Saudis"],
            name="ذكر",
            marker_color="#FFC107",
            textposition="outside",
            width=0.2,
        )
    )

    fig.add_trace(
        go.Bar(
            x=lib_managment["Economic_Activity"],
            y=lib_managment["Number_Of_Female_Saudis"],
            name="أنثى",
            marker_color="#FF7F50",
            textposition="outside",
            width=0.2,
        )
    )

    fig.update_layout(
        yaxis_showgrid=False,
        yaxis={"visible": False, "showticklabels": False},
        barmode="group",
        legend_title="الجنس",
        plot_bgcolor="white",  # Chart background
        paper_bgcolor="white",  # Page background
    )
    return fig, rate_differanc_lib_management


def real_estate():
    df = pd.read_csv(os.path.join(parent_dir, "data", "male_female_per_eco.csv"))
    real_estate = df[df["Economic_Activity"] == "الأنشطة العقارية"]

    rate_differanc_real_estate = real_estate["Rate_Difference"].values.tolist()[0]

    # stacked bar chart
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=real_estate["Economic_Activity"],
            y=real_estate["Number_Of_Male_Saudis"],
            name="ذكر",
            marker_color="#FFC107",
            textposition="outside",
            width=0.2,
        )
    )

    fig.add_trace(
        go.Bar(
            x=real_estate["Economic_Activity"],
            y=real_estate["Number_Of_Female_Saudis"],
            name="أنثى",
            marker_color="#FF7F50",
            textposition="outside",
            width=0.2,
        )
    )

    fig.update_layout(
        yaxis_showgrid=False,
        yaxis={"visible": False, "showticklabels": False},
        barmode="group",
        legend_title="الجنس",
        plot_bgcolor="white",  # Chart background
        paper_bgcolor="white",  # Page background
    )
    return fig, rate_differanc_real_estate


def oil_and_gas():
    df = pd.read_csv(os.path.join(parent_dir, "data", "male_female_per_eco.csv"))
    oil_and_gas = df[df["Economic_Activity"] == "استخراج النفط الخام والغاز الطبيعي"]

    rate_differanc_oil_and_gas = oil_and_gas["Rate_Difference"].values.tolist()[0]
    # stacked bar chart
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=oil_and_gas["Economic_Activity"],
            y=oil_and_gas["Number_Of_Male_Saudis"],
            name="ذكر",
            marker_color="#FFC107",
            textposition="outside",
            width=0.2,
        )
    )

    fig.add_trace(
        go.Bar(
            x=oil_and_gas["Economic_Activity"],
            y=oil_and_gas["Number_Of_Female_Saudis"],
            name="أنثى",
            marker_color="#FF7F50",
            textposition="outside",
            width=0.2,
        )
    )

    fig.update_layout(
        yaxis_showgrid=False,
        yaxis={"visible": False, "showticklabels": False},
        barmode="group",
        legend_title="الجنس",
        plot_bgcolor="white",  # Chart background
        paper_bgcolor="white",  # Page background
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
