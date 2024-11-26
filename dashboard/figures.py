import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def create_bar_chart_top_regions(top_5_regions, custom_green_scale):
    """Create bar chart for top 5 regions."""
    fig = px.bar(
        top_5_regions,
        x="region",
        y="total_saudis_percentage",
        text="total_saudis_percentage",
        labels={"region": "Region", "total_saudis_percentage": "Saudization Percentage"},
        title="Top 5 Regions by Saudization Percentage",
        color="total_saudis_percentage",
        color_continuous_scale=custom_green_scale,
    )
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside', hoverinfo="none")
    fig.update_layout(
        font=dict(color="#333333"),
        plot_bgcolor="#F5F5F5",
        paper_bgcolor="#F5F5F5",
        title_x=0.5,
        hovermode=False
    )
    return fig


def create_bar_chart_bottom_regions(last_5_regions, custom_green_scale):
    """Create bar chart for bottom 5 regions."""
    fig = px.bar(
        last_5_regions,
        x="region",
        y="total_saudis_percentage",
        text="total_saudis_percentage",
        labels={"region": "Region", "total_saudis_percentage": "Saudization Percentage"},
        title="Bottom 5 Regions by Saudization Percentage",
        color="total_saudis_percentage",
        color_continuous_scale=custom_green_scale,
    )
    fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside', hoverinfo="none")
    fig.update_layout(
        font=dict(color="#333333"),
        plot_bgcolor="#F5F5F5",
        paper_bgcolor="#F5F5F5",
        title_x=0.5,
        hovermode=False
    )
    return fig


def create_bar_chart_economic_activities(activity_data, colors):
    """Create bar chart for economic activities."""
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=activity_data["Economic_Activity"],
        y=activity_data["total_saudis_percentage"],
        name="Saudis %",
        marker_color=colors["Number_Of_Saudis"],
        text=[f"{v:.1%}" for v in activity_data["total_saudis_percentage"]],
        textposition="outside"
    ))
    fig.add_trace(go.Bar(
        x=activity_data["Economic_Activity"],
        y=activity_data["total_non_saudis_percentage"],
        name="Non-Saudis %",
        marker_color=colors["Number_Of_Nonsaudis"],
        text=[f"{v:.1%}" for v in activity_data["total_non_saudis_percentage"]],
        textposition="outside"
    ))
    return fig


def create_line_chart(line_data):
    """Create line chart for trends over time."""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=line_data['Qseries'],
        y=line_data['Saudis_change_perc'],
        mode='lines+markers+text',
        name='Saudis',
        text=[f"{v:.1f}%" if not pd.isnull(v) else "" for v in line_data['Saudis_change_perc']],
        textposition='top center',
        line=dict(color='#008000')
    ))
    fig.add_trace(go.Scatter(
        x=line_data['Qseries'],
        y=line_data['NonSaudis_change_perc'],
        mode='lines+markers+text',
        name='Non-Saudis',
        text=[f"{v:.1f}%" if not pd.isnull(v) else "" for v in line_data['NonSaudis_change_perc']],
        textposition='top center',
        line=dict(color='#00509E')
    ))
    fig.update_layout(
        title="Trend Over Time",
        xaxis_title='Year',
        yaxis_title='Percentage Change',
        font=dict(color="#333333"),
        plot_bgcolor="#F5F5F5",
        paper_bgcolor="#F5F5F5",
        title_x=0.5
    )
    return fig


def create_geo_scatter(region_employee_summary):
    """Create scatter geo chart for Saudi Arabia."""
    fig = px.scatter_geo(
        region_employee_summary,
        lat="lat",
        lon="lon",
        size="total_saudis_percentage",
        hover_name="region",
        color="total_saudis_percentage",
        title="Distribution of Employees by Region in Saudi Arabia",
        projection="natural earth"
    )
    fig.update_geos(
        scope="asia",
        center={"lat": 23.8859, "lon": 45.0792},
        fitbounds="locations"
    )
    fig.update_layout(
        font=dict(color="#333333"),
        plot_bgcolor="#F5F5F5",
        paper_bgcolor="#F5F5F5"
    )
    return fig
