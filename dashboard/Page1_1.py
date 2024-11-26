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
# Load data for all years
df_2022 = pd.read_csv(os.path.join(data_folder_path, "activity_group22.csv"))
df_2023 = pd.read_csv(os.path.join(data_folder_path, "activity_group23.csv"))
df_2024 = pd.read_csv(os.path.join(data_folder_path, "activity_group24.csv"))
region_activity = pd.read_csv(os.path.join(data_folder_path, "activity_region_group24.csv"))
df = pd.concat([df_2022, df_2023, df_2024], ignore_index=True)
najran_df = pd.read_csv(os.path.join(data_folder_path, "najran_df.csv"))

num_saudis = region_employee_summary['Number_Of_Saudis'].sum()
num_nonsaudis = region_employee_summary['Number_Of_Nonsaudis'].sum()

def get_percent(df):
    # Calculate Saudi and non-Saudi percentages for df_2024
    df["total_saudis_percentage"] = (df["Number_Of_Saudis"] /df["total_employees"])
    df["total_non_saudis_percentage"] = 1 - df["total_saudis_percentage"]

get_percent(region_employee_summary)
get_percent(df)
get_percent(region_activity)

'''
region_employee_summary['total_saudis_percentage'] = region_employee_summary.apply(
    lambda row: (row['Number_Of_Saudis'] / row['total_employees'] * 100) if row['total_employees'] > 0 else 0, axis=1
)
'''
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
custom_green_scale = [
        "#5bb450", "#52a447", "#46923c","#3b8132", "#276221"
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

# Calculate the top 5 regions with the highest percentage of Saudis employed
top_5_regions = region_employee_summary.nlargest(5, 'total_saudis_percentage')
last_5_regions = region_employee_summary.nsmallest(5, 'total_saudis_percentage')

top1_region = region_activity[region_activity["region"] == "المنطقة الشرقية"]
last_region = region_activity[region_activity["region"] == "منطقة نجران"]

# Create the bar chart figure
fig_bar_chart = px.bar(
    top_5_regions,
    x="region",
    y="total_saudis_percentage",
    text="total_saudis_percentage",
    labels={"region": "المنطقة", "total_saudis_percentage": "نسبة السعوديين"},
    title="أعلى خمس مناطق في نسبة الموظفين السعوديين",
    #color="region"
    color="total_saudis_percentage",  # Map the color to the percentage
    color_continuous_scale=custom_green_scale
    #px.colors.sequential.Greens  # Use the correct 'Greens' color scale
)
fig_bar_chart.update_traces(
    texttemplate='%{text:.2f}%',
    textposition='outside',
    #marker=dict(color="#008000"),
    hoverinfo="none"  # Disable hover functionality
)
fig_bar_chart.update_layout(
    font=dict(color="#333333"),
    plot_bgcolor="#F5F5F5",
    paper_bgcolor="#F5F5F5",
    title_x=0.5,
    hovermode=False  # Disable hover mode completely
)
# Bar chart
top_activities = top1_region.nlargest(5, "total_saudis_percentage")

# Bar chart
top_activities_last = last_region.nlargest(5, "total_saudis_percentage")
bar_fig = go.Figure()
colors={
        'Number_Of_Saudis': '#008000',       # Emerald green
        'Number_Of_Nonsaudis': '#00509E'    # Soft navy blue
    }
bar_fig.add_trace(go.Bar(x=top_activities["Economic_Activity"],
                        y=top_activities["total_saudis_percentage"],
                        name="السعوديين %",
                        marker_color=colors["Number_Of_Saudis"],
                        text=[f"{v:.1%}" for v in top_activities.head(5)["total_saudis_percentage"]],  # Format as percentage
                        textposition="outside"))

bar_fig.add_trace(go.Bar(x=top_activities["Economic_Activity"],
                        y=top_activities["total_non_saudis_percentage"],
                        name="غير السعوديين %",
                        marker_color=colors["Number_Of_Nonsaudis"],
                        text=[f"{v:.1%}" for v in top_activities.head(5)["total_non_saudis_percentage"]], 
                        textposition="outside"))

bar_fig_last = go.Figure()
colors={
        'Number_Of_Saudis': '#008000',       # Emerald green
        'Number_Of_Nonsaudis': '#00509E'    # Soft navy blue
    }
bar_fig_last.add_trace(go.Bar(x=top_activities_last["Economic_Activity"],
                        y=top_activities_last["total_saudis_percentage"],
                        name="السعوديين %",
                        marker_color=colors["Number_Of_Saudis"],
                        text=[f"{v:.1%}" for v in top_activities_last.head(5)["total_saudis_percentage"]],  # Format as percentage
                        textposition="outside"))

bar_fig_last.add_trace(go.Bar(x=top_activities_last["Economic_Activity"],
                        y=top_activities_last["total_non_saudis_percentage"],
                        name="غير السعوديين %",
                        marker_color=colors["Number_Of_Nonsaudis"],
                        text=[f"{v:.1%}" for v in top_activities_last.head(5)["total_non_saudis_percentage"]], 
                        textposition="outside"))
bar_fig_last.update_layout(
        title="أعلى خمس قطاعات في نسبة السعودة في نجران",
        yaxis_title='نسبة السعوديين',
        font=dict(color="#333333"),
        plot_bgcolor="#F5F5F5",
        paper_bgcolor="#F5F5F5",
        title_x=0.5
    )

bar_fig2 = px.bar(
    last_5_regions,
    x="region",
    y="total_saudis_percentage",
    text="total_saudis_percentage",
    labels={"region": "المنطقة", "total_saudis_percentage": "نسبة السعوديين"},
    title="أقل خمس مناطق في نسبة الموظفين السعوديين",
    #color="region"
    color="total_saudis_percentage",  # Map the color to the percentage
    color_continuous_scale=custom_green_scale
    #px.colors.sequential.Greens  # Use the correct 'Greens' color scale
)
bar_fig2.update_traces(
    texttemplate='%{text:.2f}%',
    textposition='outside',
    #marker=dict(color="#008000"),
    hoverinfo="none"  # Disable hover functionality
)
bar_fig2.update_layout(
    font=dict(color="#333333"),
    plot_bgcolor="#F5F5F5",
    paper_bgcolor="#F5F5F5",
    title_x=0.5,
    hovermode=False  # Disable hover mode completely
)

line_data = najran_df[najran_df['Economic_Activity'] == "التعليم"]
        # Sort the DataFrame using a custom key
line_data["sorted_q"] = najran_df["Qseries"].apply(lambda x: tuple(map(int, str(x).split('-'))))
line_data = line_data.sort_values(by="sorted_q").drop(columns=["sorted_q"])
#line_data = line_data.sort_values(by="Qseries")  # Ensure years are in order

# Calculate percentage change for Saudis and Non-Saudis
line_data['Saudis_change_perc'] = line_data['Number_Of_Saudis'].pct_change() * 100
line_data['NonSaudis_change_perc'] = line_data['Number_Of_Nonsaudis'].pct_change() * 100

line_fig = go.Figure()

# Add lines for Saudis and Non-Saudis
line_fig.add_trace(go.Scatter(
    x=line_data['Qseries'],
    y=line_data['Saudis_change_perc'],
    mode='lines+markers+text',
    name='Number of Saudis',
    text=[f"{v:.1f}%" if not pd.isnull(v) else "" for v in line_data['Saudis_change_perc']],
    textposition='top center',
    line=dict(color='#008000')
))

line_fig.add_trace(go.Scatter(
    x=line_data['Qseries'],
    y=line_data['NonSaudis_change_perc'],
    mode='lines+markers+text',
    name='Number of Non-Saudis',
    text=[f"{v:.1f}%" if not pd.isnull(v) else "" for v in line_data['NonSaudis_change_perc']],
    textposition='top center',
    line=dict(color='#00509E')
))

line_fig.update_layout(
    title=f"اتجاه السعودة للتعليم في منطقة نجران",
    xaxis_title='السنة',
    yaxis_title='نسبة التغير',
    font=dict(color="#333333"),
    plot_bgcolor="#F5F5F5",
    paper_bgcolor="#F5F5F5",
    title_x=0.5
)
# Visualization: Focused Map on Saudi Arabia
fig_choropleth = px.scatter_geo(
    region_employee_summary,
    lat="lat",
    lon="lon",
    size="total_saudis_percentage",
    hover_name="region",
    color="total_saudis_percentage",
    title="إجمالي عدد الموظفين حسب المنطقة في المملكة العربية السعودية",
    projection="natural earth"
)
fig_choropleth.update_geos(
    scope="asia",
    center={"lat": 23.8859, "lon": 45.0792},
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
    style={"fontFamily": "Roboto, sans-serif", "backgroundColor": "#F5F5F5", "padding": "20px", "justify-content": "center","direction": "rtl"},
    children=[
        html.H1(
            "نظرة عامة على توزيع الموظفين - المملكة العربية السعودية",
            style={"textAlign": "center", "color": "#333333"}
        ),
         html.Div(
            style={
                "display": "flex",
                "justifyContent": "center",
                "gap": "20px",
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
        html.P((
            [".في هذه الصفحة راح نوجهك الئ معلومات مهمه لتوزيع الموظفين في المملكه العربيه السعودية",
             html.Br(),
                ".في البداية جانا فضول نعرف إيش أعلى مناطق في السعودية فيهاأكبر نسبة سعودة" ,
                ]
                
            ),
            style={
                "textAlign": "justify",
                "color": "#333333",
                "margin": "20px 0",
                "lineHeight": "1.8",
                "fontSize": "18px",
                "backgroundColor": "#FFFFFF",
                "padding": "15px",
                "borderRadius": "8px",
                "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"
            }
        ),
        
        # Add bar chart below the description
        html.Div(
            dcc.Graph(
                id="top-5-bar-chart",
                figure=fig_bar_chart
            ),
            style={"margin": "20px 0"}
        ),
        html.P(
            (
                "الرسمة أعلاه توضح لنا أعلئ خمس مناطق في المملكة بناءً على نسبة الموظفين السعوديين "
                "مقارنةً بعدد الموظفين الإجمالي في كل منطقة. مثلاً، نلاحظ أن منطقة الشرقية تتصدر القائمة "
                " ومع ذلك نشوف ان النسبة لاتتجاوز 28%."
                "هذا يعطينا فكرة ان فيه مجال لزيادة عدد الموظفين السعوديين في مناطق المملكة. "
                "واتخاذ القرارات بناءً عليها لدعم المناطق ذات النسب الأقل وتحقيق توازن في سوق العمل."
            ),
            style={
                "textAlign": "justify",
                "color": "#333333",
                "margin": "20px 0",
                "lineHeight": "1.8",
                "fontSize": "18px",
                "backgroundColor": "#FFFFFF",
                "padding": "15px",
                "borderRadius": "8px",
                "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"
            }
        ),
        html.P(
            (
                ["لاحظنا ان الشرقية هي أعلى منطقة في نسبة السعودة, وتبادر الى بالنا سؤال ثاني",
                 html.Br(),
                 "وش أعلى القطاعات سعودة في المنطقة الشرقية؟"]
            ),
            style={
                "textAlign": "justify",
                "color": "#333333",
                "margin": "20px 0",
                "lineHeight": "1.8",
                "fontSize": "18px",
                "backgroundColor": "#FFFFFF",
                "padding": "15px",
                "borderRadius": "8px",
                "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"
            }
        ),
        html.Div(
            dcc.Graph(
                id="top-bar-chart",
                figure=bar_fig
            ),
            style={"margin": "20px 0"}
        ),
        html.P(
            (
                ["بعد ما عرفنا اعلى نشاطات السعودة في الشرقية",
                 html.Br(),
                 "خلونا نشوف أقل المناطق في نسب السعودة"]
            ),
            style={
                "textAlign": "justify",
                "color": "#333333",
                "margin": "20px 0",
                "lineHeight": "1.8",
                "fontSize": "18px",
                "backgroundColor": "#FFFFFF",
                "padding": "15px",
                "borderRadius": "8px",
                "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"
            }
        ),
        html.Div(
            dcc.Graph(
                id="last-5-bar-chart",
                figure=bar_fig2
            ),
            style={"margin": "20px 0"}
        ),
        html.P(
            (
                ["لاحظنا ان نجران هي أقل منطقة في نسب السعودة, وهذا يطرح سؤال في بالنا",
                 html.Br(),
                 "وش هي أعلى قطاعات تملك نسب سعودة في نجران؟"]
            ),
            style={
                "textAlign": "justify",
                "color": "#333333",
                "margin": "20px 0",
                "lineHeight": "1.8",
                "fontSize": "18px",
                "backgroundColor": "#FFFFFF",
                "padding": "15px",
                "borderRadius": "8px",
                "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"
            }
        ),
        html.Div(
            dcc.Graph(
                id="last-bar-chart",
                figure=bar_fig_last
            ),
            style={"margin": "20px 0"}
        ),
        html.P(
            (
                ["نلاحظ ان النشاطات الي فيها عدد السعوديين اكثر من الاجانب قليل جدا في نجران",
                 html.Br(),
                 "جانا فضول نعرف أكثر هل الوضع الراهن في تحسن أم في انخفاض؟",
                 html.Br(),
                 "سوينا مقارنة على مدار ثلاث سنوات في بعض النشاطات عشان ناخذ لمحة عن الوضع"]
            ),
            style={
                "textAlign": "justify",
                "color": "#333333",
                "margin": "20px 0",
                "lineHeight": "1.8",
                "fontSize": "18px",
                "backgroundColor": "#FFFFFF",
                "padding": "15px",
                "borderRadius": "8px",
                "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"
            }
        ),
        html.Div(
            dcc.Graph(
                id="line-chart",
                figure=line_fig
            ),
            style={"margin": "20px 0"}
        ),
        html.P(
            (
                ["نلاحظ انه في الربع الأخير في سنة 2024 فيه قفزة ملحوظة في عدد الموظفين السعوديين, مقارنة في الارباع السابقة خلال السنوات الماضية.",
                 html.Br(),
                 "على الرغم من ان نسبة الموظفين السعوديين في تعليم نجران اقل من نسبة غير السعوديين, الا ان هذه القفزة تشير الا انه هناك جهود حثيثة لزيادة السعودة في جميع مناطق المملكة"
                 ]
            ),
            style={
                "textAlign": "justify",
                "color": "#333333",
                "margin": "20px 0",
                "lineHeight": "1.8",
                "fontSize": "18px",
                "backgroundColor": "#FFFFFF",
                "padding": "15px",
                "borderRadius": "8px",
                "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"
            }
        ),
        html.P(
            (
                "طيب خلونا نقول عندك فضول وتبي تشوف مناطق ثانيه غير الخمس الاولى اللي في الرسمة السابقه مع تفاصيل اكقر،"
                "تقدر تحت من الخريطة تضغط على المنطقة وراح تتحدث رسمة 2 بجنب الخريطة بناء اختيارك للمنطقة."
                "راح تظهرلك تفاصيل اكثر منها نسبة الموظفين السعوديين وغير السعوديين,"
                "وتقدر بعد اذا حطيت السهم على احد الاقسام في الرسمة، يظهرلك معلومات عن عدد الموظفين ونسبة الموظفين حسب الجنس"
            ),
            style={
                "textAlign": "justify",
                "color": "#333333",
                "margin": "20px 0",
                "lineHeight": "1.8",
                "fontSize": "18px",
                "backgroundColor": "#FFFFFF",
                "padding": "15px",
                "borderRadius": "8px",
                "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)"
            }
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

# Callback to update the pie chart based on map click
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
    pie_chart.update_traces(
        hovertemplate=(
            "<br><b>%{customdata[0]}</b><br>"
            
        )
    )
    pie_chart.update_layout(
        font=dict(color="#333333"),
        plot_bgcolor="#F5F5F5",
        paper_bgcolor="#F5F5F5"
    )
    return pie_chart

if __name__ == '__main__':
    app.run(debug=True)
