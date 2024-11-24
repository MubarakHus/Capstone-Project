from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os

# Set up file paths
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
data_folder_path = os.path.join(parent_dir, "data")

# Load data
region_employee_summary = pd.read_csv(os.path.join(data_folder_path, "region_employee_summary.csv"))

# Filter for Saudi Arabian regions
saudi_regions = [
    "منطقة الرياض", "منطقة مكة المكرمة", "المنطقة الشرقية", "منطقة المدينة المنورة",
    "منطقة القصيم", "منطقة عسير", "منطقة تبوك", "منطقة حائل", "منطقة الحدود الشمالية",
    "منطقة جازان", "منطقة نجران", "منطقة الباحة", "منطقة الجوف"
]
region_employee_summary = region_employee_summary[
    region_employee_summary['region'].isin(saudi_regions)
]

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
    "منطقة الجوف": {"lat": 30.3158, "lon": 38.3691}
}

region_employee_summary['lat'] = region_employee_summary['region'].apply(lambda x: region_coordinates[x]['lat'])
region_employee_summary['lon'] = region_employee_summary['region'].apply(lambda x: region_coordinates[x]['lon'])

# Visualization: Focused Map on Saudi Arabia
fig_choropleth = px.scatter_geo(
    region_employee_summary,
    lat="lat",
    lon="lon",
    size="total_employees",
    hover_name="region",
    color="total_employees",
    title="إجمالي عدد الموظفين حسب المنطقة في المملكة العربية السعودية",
    projection="natural earth",
    color_continuous_scale="Viridis"
)

fig_choropleth.update_geos(
    scope="asia",  # Limit view to Asia (includes Saudi Arabia)
    center={"lat": 23.8859, "lon": 45.0792},  # Center map on Saudi Arabia
    fitbounds="locations"
)

fig_choropleth.update_layout(
    font=dict(color="#333333"),
    plot_bgcolor="#F5F5F5",
    paper_bgcolor="#F5F5F5"
)

fig_choropleth.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>إجمالي الموظفين: %{marker.size}<extra></extra>"
)

# Dash App Initialization
app = Dash(__name__)

# Layout for the app
app.layout = html.Div(
    style={"fontFamily": "Roboto, sans-serif", "backgroundColor": "#F5F5F5", "padding": "20px"},
    children=[
        html.H1(
            "نظرة عامة على توزيع الموظفين - المملكة العربية السعودية",
            style={"textAlign": "center", "color": "#333333"}
        ),
        html.Div(
            [
                html.Label("اختر المنطقة:", style={"fontSize": "18px", "color": "#333333"}),
                dcc.RadioItems(
                    id="region-radio",
                    options=[
                        {"label": "المملكة العربية السعودية", "value": "المملكة العربية السعودية"}
                    ] + [{"label": region, "value": region} for region in saudi_regions],
                    value="Saudi Arabia",
                    style={"marginBottom": "20px", "fontSize": "16px"}
                ),
            ],
            style={"marginBottom": "30px"}
        ),
        html.Div(
            [
                html.Div(
                    dcc.Graph(figure=fig_choropleth),
                    style={"width": "48%", "display": "inline-block"}
                ),
                html.Div(
                    dcc.Graph(id="dynamic-pie-chart"),
                    style={"width": "48%", "display": "inline-block"}
                )
            ],
            style={"display": "flex", "justifyContent": "space-between"}
        )
    ]
)

# Callback to update the pie chart
@app.callback(
    Output("dynamic-pie-chart", "figure"),
    Input("region-radio", "value")
)
def update_pie_chart(selected_region):
    if selected_region == "المملكة العربية السعودية":
        # Entire Saudi Arabia
        total_saudis = region_employee_summary['Number_Of_Saudis'].sum()
        total_nonsaudis = region_employee_summary['Number_Of_Nonsaudis'].sum()
        total_male_saudis = region_employee_summary['Number_Of_Male_Saudis'].sum()
        total_female_saudis = region_employee_summary['Number_Of_Female_Saudis'].sum()
        total_male_nonsaudis = region_employee_summary['Number_Of_Male_Nonaudis'].sum()
        total_female_nonsaudis = region_employee_summary['Number_Of_Female_Nonaudis'].sum()
    else:
        # Specific region
        region_data = region_employee_summary[region_employee_summary['region'] == selected_region]
        total_saudis = region_data['Number_Of_Saudis'].sum()
        total_nonsaudis = region_data['Number_Of_Nonsaudis'].sum()
        total_male_saudis = region_data['Number_Of_Male_Saudis'].sum()
        total_female_saudis = region_data['Number_Of_Female_Saudis'].sum()
        total_male_nonsaudis = region_data['Number_Of_Male_Nonaudis'].sum()
        total_female_nonsaudis = region_data['Number_Of_Female_Nonaudis'].sum()

    # Ensure division by zero does not occur
    male_saudis_percentage = "0%" if total_saudis == 0 else f"%{(total_male_saudis / total_saudis * 100):.0f}"
    female_saudis_percentage = "0%" if total_saudis == 0 else f"%{(total_female_saudis / total_saudis * 100):.0f}"
    male_nonsaudis_percentage = "0%" if total_nonsaudis == 0 else f"%{(total_male_nonsaudis / total_nonsaudis * 100):.0f}"
    female_nonsaudis_percentage = "0%" if total_nonsaudis == 0 else f"%{(total_female_nonsaudis / total_nonsaudis * 100):.0f}"

    # Use customdata for hover details
    customdata = [
        [
            f"\nاجمالي السعوديين: {total_saudis:,}",
            f"\nالرجال: {male_saudis_percentage}",
            f"\nالنساء: {female_saudis_percentage}"
        ],
        [
            f"\nاجمالي غير السعوديين: {total_nonsaudis:,}",
            f"\nالرجال: {male_nonsaudis_percentage}",
            f"\nالنساء: {female_nonsaudis_percentage}"
        ]
    ]

    # Create the Pie Chart
    pie_chart = go.Figure(
        data=[
            go.Pie(
                labels=["السعوديين", "غير السعوديين"],
                values=[total_saudis, total_nonsaudis],
                hoverinfo="none",
                textinfo="label+percent",
                hole=0.3,
                marker=dict(colors=["#008000", "#00509E"]),
                customdata=customdata
            )
        ]
    )

    # Customize hovertemplate to show details
    pie_chart.update_traces(
        hovertemplate=(
            "<br><b>%{customdata[0]}</b><br>"
            
        )
    )

    pie_chart.update_layout(
        title=f"توزيع الموظفين في {selected_region}",
        margin=dict(t=50, b=50, l=50, r=50),
        font=dict(color="#333333"),
        plot_bgcolor="#F5F5F5",
        paper_bgcolor="#F5F5F5"
    )

    return pie_chart


if __name__ == '__main__':
    app.run(debug=True)

