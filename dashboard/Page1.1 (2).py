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
num_saudis = region_employee_summary['Number_Of_Saudis'].sum()
num_nonsaudis = region_employee_summary['Number_Of_Nonsaudis'].sum()

region_employee_summary['total_saudis_percentage'] = region_employee_summary.apply(
    lambda row: (row['Number_Of_Saudis'] / row['total_employees'] * 100) if row['total_employees'] > 0 else 0, axis=1
)
region_employee_summary['total_male_saudis_percentage'] = region_employee_summary.apply(
    lambda row: (row['Number_Of_Male_Saudis'] / row['Number_Of_Saudis'] * 100) if row['Number_Of_Saudis'] > 0 else 0, axis=1
)
region_employee_summary['total_female_saudis_percentage'] = region_employee_summary.apply(
    lambda row: (row['Number_Of_Female_Saudis'] / row['Number_Of_Saudis'] * 100) if row['Number_Of_Saudis'] > 0 else 0, axis=1
)


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
    size="total_saudis_percentage",
    hover_name="region",
    color="total_employees",
    title="إجمالي عدد الموظفين حسب المنطقة في المملكة العربية السعودية",
    projection="natural earth",
    #color_continuous_scale="Viridis"
    #color_discrete_sequence=["green"]  # Set all circles to green
)
#(total_male_saudis / total_saudis * 100):.0f}
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
    marker=dict(color="green"),  # Set all circles to green
    hovertemplate="<b>%{hovertext}</b><br> نسبة الموظفين السعوديين: %%{marker.size:.1f} <extra></extra>"
)


# Dash App Initialization
app = Dash(__name__)
# Update Dash App Layout
app.layout = html.Div(
    style={"fontFamily": "Roboto, sans-serif", "backgroundColor": "#F5F5F5", "padding": "20px", "justify-content": "center"},
    children=[
        
        html.H1(
            "نظرة عامة على توزيع الموظفين - المملكة العربية السعودية",
            style={"textAlign": "center", "color": "#333333"}
        ),
        html.H3(
            ".في هذه الصفحة راح نوجهك الئ معلومات مهمه لتوزيع الموظفين في المملكه العربيه السعوديه "
            "اول شي في الرسمات اللي تحت (رسمة 1 "
            "توضح اعلئ خمس مناطق في المملكه العربيه السعوديه في نسية الموظفين السعوديين"
            ,
            style={"textAlign": "center", "color": "#333333"}
        ),
        html.Div(
            style={
                "display": "flex",
                "justifyContent": "center",
                "gap": "20px",  # Space between blocks
                "margin": "20px 0"
            },
            children=[
                html.Div(
                    f"اجمالي عدد الموظفين السعوديين {num_saudis:,}",
                    style={
                        "textAlign": "center",
                        "backgroundColor": "#FFFFFF",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                        "color": "#333333",
                        "fontSize": "18px",
                        "flex": "1"
                    }
                ),
                html.Div(
                    f"اجمالي عدد الموظفين غير السعوديين {num_nonsaudis:,}",
                    style={
                        "textAlign": "center",
                        "backgroundColor": "#FFFFFF",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                        "color": "#333333",
                        "fontSize": "18px",
                        "flex": "1"
                    }
                )
            ]
        ),
        html.Div(
            dcc.Graph(
                id="scatter-map",
                figure=fig_choropleth
            ),
            style={"width": "65%",  "display": "inline-block"}
        ),    

        html.Div(
            dcc.Graph(
                id="dynamic-pie-chart"
            ),
            style={"width": "35%", "display": "inline-block"}
        )
    ]
)

# Update the Pie Chart Callback to Use Map Clicks
@app.callback(
    Output("dynamic-pie-chart", "figure"),
    Input("scatter-map", "clickData")
)
def update_pie_chart(click_data):
    if click_data:
        # Get the clicked region from clickData
        selected_region = click_data["points"][0]["hovertext"]
    else:
        # Default to entire Saudi Arabia
        selected_region = "المملكة العربية السعودية"

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
    #        title=f"توزيع الموظفين في {selected_region}",

    pie_chart.update_layout(
        margin=dict(t=50, b=50, l=50, r=50),
        font=dict(color="#333333"),
        plot_bgcolor="#F5F5F5",
        paper_bgcolor="#F5F5F5"
    )

    return pie_chart

if __name__ == '__main__':
    app.run(debug=True)

