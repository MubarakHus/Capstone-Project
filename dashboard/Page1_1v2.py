from dash import Dash, html, dcc, Input, Output
import plotly.graph_objects as go
import pandas as pd
import os
import plotly.express as px

# Set up file paths
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
data_folder_path = os.path.join(parent_dir, "data")

# Load data
region_employee_summary = pd.read_csv(os.path.join(data_folder_path, "region_employee_summary.csv"))
df_activity_region = pd.read_csv(os.path.join(data_folder_path, "df_activity_region.csv"))
activity_education = pd.read_csv(os.path.join(data_folder_path, "activity_education.csv"))
activity_programming = pd.read_csv(os.path.join(data_folder_path, "activity_programming.csv"))

# Calculate totals
lastQ= df_activity_region[df_activity_region["Qseries"] == "2024-7"]
total_saudis = lastQ["Number_Of_Saudis"].sum()
total_nonsaudis = lastQ["Number_Of_Nonsaudis"].sum()

region_employee_summary['total_saudis_percentage'] = region_employee_summary.apply(
    lambda row: (row['Number_Of_Saudis'] / row['total_employees'] * 100) if row['total_employees'] > 0 else 0, axis=1)
region_employee_summary.sort_values(by="total_saudis_percentage", inplace=True)
region_employee_summary["order"] = 0
#region_employee_summary["order"] = region_employee_summary["order"].apply(lambda x: x+i for i in range(1, 16))

# Calculate the top 5 regions with the highest percentage of Saudis employed
top_5_regions = region_employee_summary.nlargest(5, 'total_saudis_percentage')
last_5_regions = region_employee_summary.nsmallest(5, 'total_saudis_percentage')


def get_percent(df):
    # Calculate Saudi and non-Saudi percentages for df_2024
    df["total_saudis_percentage"] = (df["Number_Of_Saudis"] /df["total_employees"])
    df["total_non_saudis_percentage"] = 1 - df["total_saudis_percentage"]

get_percent(df_activity_region)
get_percent(lastQ)

top1_region = lastQ[lastQ["region"] == "المنطقة الشرقية"]
last_region = lastQ[lastQ["region"] == "منطقة نجران"]
all_regions = lastQ.groupby(['region', 'Economic_Activity'])[['Number_Of_Establishments', 'Number_Of_Saudis', 'Number_Of_Male_Saudis', 'Number_Of_Female_Saudis', 'Number_Of_Nonsaudis', 'Number_Of_Male_Nonaudis', 'Number_Of_Female_Nonaudis', 'total_employees']].sum()
get_percent(all_regions)

top_activities = top1_region.nlargest(5, "total_saudis_percentage")
top_activities_last = last_region.nlargest(5, "total_saudis_percentage")
last_activities = all_regions.nsmallest(5, "total_saudis_percentage")

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

#========================================================منطقة التشارتات========================================================================
# تشارت اجمالي الموظفين
total_bar = go.Figure(
    data=[
        go.Bar(
            name="الموظفين السعوديين",
            x=["الموظفين السعوديين"],
            y=[total_saudis],
            text=f"{total_saudis:,}",
            marker_color="#008000",
        ),
        go.Bar(
            name="الموظفين غير السعوديين",
            x=["الموظفين غير السعوديين"],
            y=[total_nonsaudis],
            text=f"{total_nonsaudis:,}",
            marker_color="#00509E",
        ),
    ]
)
total_bar.update_layout(
    title="اجمالي عدد الموظفين السعوديين وغير السعوديين",
    yaxis_title="عدد الموظفين",
    barmode="group",
    template="plotly_white",
    font={"size": 16},
)
# تشارت الخريطة
"""Create scatter geo chart for Saudi Arabia."""
map_chart = px.scatter_geo(
    region_employee_summary,
    lat="lat",
    lon="lon",
    size="total_saudis_percentage",
    hover_name="region",
    color="total_saudis_percentage",
    title="نسب السعودة في مناطق المملكة العربية السعودية",
    projection="natural earth",
)
map_chart.update_geos(
    scope="asia",
    center={"lat": 23.8859, "lon": 45.0792},
    fitbounds="locations"
)
map_chart.update_traces(
    marker=dict(color="green"),  # Set all circles to green
    hovertemplate="<b>%{hovertext}</b><br> نسبة الموظفين السعوديين: %%{marker.size:.1f} <extra></extra>",
    text=region_employee_summary['region'],  # Display region names on the map
    textposition="middle center",  # Position the text in the middle of each circle
    textfont=dict(size=10, color="black")  # Adjust text size and color
)
map_chart.update_layout(
    font=dict(color="#333333"),
    plot_bgcolor="#F5F5F5",
    paper_bgcolor="#F5F5F5"
)
# أعلى 5 مناطق في السعودة

top5_bar = px.bar(
    top_5_regions,
    x="region",
    y="total_saudis_percentage",
    text="total_saudis_percentage",
    labels={"region": "المنطقة", "total_saudis_percentage": "نسبة السعوديين"},
    title="أعلى خمس مناطق في نسبة الموظفين السعوديين",
    #color="region"
    color="total_saudis_percentage",  # Map the color to the percentage
    color_continuous_scale=[
        "#5bb450", "#52a447", "#46923c","#3b8132", "#276221"
]
    #px.colors.sequential.Greens  # Use the correct 'Greens' color scale
)
top5_bar.update_traces(
    texttemplate='%{text:.2f}%',
    textposition='outside',
    #marker=dict(color="#008000"),
    hoverinfo="none"  # Disable hover functionality
)
top5_bar.update_layout(
    font=dict(color="#333333"),
    plot_bgcolor="#F5F5F5",
    paper_bgcolor="#F5F5F5",
    title_x=0.5,
    hovermode=False  # Disable hover mode completely
)

# أعلى 5 قطاعات في الشرقية
shrqya5 = go.Figure()
colors={
        'Number_Of_Saudis': '#008000',       # Emerald green
        'Number_Of_Nonsaudis': '#00509E'    # Soft navy blue
    }
shrqya5.add_trace(go.Bar(x=top_activities["Economic_Activity"],
                        y=top_activities["total_saudis_percentage"],
                        name="السعوديين %",
                        marker_color=colors["Number_Of_Saudis"],
                        text=[f"{v:.1%}" for v in top_activities.head(5)["total_saudis_percentage"]],  # Format as percentage
                        textposition="outside"))

shrqya5.add_trace(go.Bar(x=top_activities["Economic_Activity"],
                        y=top_activities["total_non_saudis_percentage"],
                        name="غير السعوديين %",
                        marker_color=colors["Number_Of_Nonsaudis"],
                        text=[f"{v:.1%}" for v in top_activities.head(5)["total_non_saudis_percentage"]], 
                        textposition="outside"))

# أقل 5 مناطق سعودة
last5_bar = px.bar(
    last_5_regions,
    x="region",
    y="total_saudis_percentage",
    text="total_saudis_percentage",
    labels={"region": "المنطقة", "total_saudis_percentage": "نسبة السعوديين"},
    title="أقل خمس مناطق في نسبة الموظفين السعوديين",
    #color="region"
    color="total_saudis_percentage",  # Map the color to the percentage
    color_continuous_scale=[
        "#5bb450", "#52a447", "#46923c","#3b8132", "#276221"
]
    #px.colors.sequential.Greens  # Use the correct 'Greens' color scale
)
last5_bar.update_traces(
    texttemplate='%{text:.2f}%',
    textposition='outside',
    #marker=dict(color="#008000"),
    hoverinfo="none"  # Disable hover functionality
)
last5_bar.update_layout(
    font=dict(color="#333333"),
    plot_bgcolor="#F5F5F5",
    paper_bgcolor="#F5F5F5",
    title_x=0.5,
    hovermode=False  # Disable hover mode completely
)
# أكثر مناطق سعودة في نجران
njran5 = go.Figure()
colors={
        'Number_Of_Saudis': '#008000',       # Emerald green
        'Number_Of_Nonsaudis': '#00509E'    # Soft navy blue
    }
njran5.add_trace(go.Bar(x=top_activities_last["Economic_Activity"],
                        y=top_activities_last["total_saudis_percentage"],
                        name="السعوديين %",
                        marker_color=colors["Number_Of_Saudis"],
                        text=[f"{v:.1%}" for v in top_activities_last.head(5)["total_saudis_percentage"]],  # Format as percentage
                        textposition="outside"))

njran5.add_trace(go.Bar(x=top_activities_last["Economic_Activity"],
                        y=top_activities_last["total_non_saudis_percentage"],
                        name="غير السعوديين %",
                        marker_color=colors["Number_Of_Nonsaudis"],
                        text=[f"{v:.1%}" for v in top_activities_last.head(5)["total_non_saudis_percentage"]], 
                        textposition="outside"))

njran5.update_layout(
        title="أعلى خمس قطاعات في نسبة السعودة في نجران",
        yaxis_title='نسبة السعوديين',
        font=dict(color="#333333"),
        plot_bgcolor="#F5F5F5",
        paper_bgcolor="#F5F5F5",
        title_x=0.5
    )

# معدل نمو التعليم في المملكة
activity_education["sorted_q"] = activity_education["Qseries"].apply(lambda x: tuple(map(int, str(x).split('-'))))
line_data_edu = activity_education.sort_values(by="sorted_q").drop(columns=["sorted_q"])
#line_data = line_data.sort_values(by="Qseries")  # Ensure years are in order
first_saudis_edu = line_data_edu.loc[line_data_edu['Qseries'] == line_data_edu['Qseries'].min(), 'Number_Of_Saudis'].iloc[0]
first_nonsaudis_edu = line_data_edu.loc[line_data_edu['Qseries'] == line_data_edu['Qseries'].min(), 'Number_Of_Nonsaudis'].iloc[0]
# Calculate percentage change for Saudis and Non-Saudis
line_data_edu['Saudis_change_perc'] = ((line_data_edu['Number_Of_Saudis'] - first_saudis_edu) / first_saudis_edu) * 100
line_data_edu['NonSaudis_change_perc'] = ((line_data_edu['Number_Of_Nonsaudis'] - first_nonsaudis_edu) / first_nonsaudis_edu) * 100
edu_line = go.Figure()

# Add lines for Saudis and Non-Saudis
edu_line.add_trace(go.Scatter(
    x=line_data_edu['Qseries'],
    y=line_data_edu['Saudis_change_perc'],
    mode='lines+markers+text',
    name='Number of Saudis',
    text=[f"{v:.1f}%" if not pd.isnull(v) else "" for v in line_data_edu['Saudis_change_perc']],
    textposition='top center',
    line=dict(color='#008000')
))

edu_line.add_trace(go.Scatter(
    x=line_data_edu['Qseries'],
    y=line_data_edu['NonSaudis_change_perc'],
    mode='lines+markers+text',
    name='Number of Non-Saudis',
    text=[f"{v:.1f}%" if not pd.isnull(v) else "" for v in line_data_edu['NonSaudis_change_perc']],
    textposition='top center',
    line=dict(color='#00509E')
))

edu_line.update_layout(
    title=f"معدل نمو السعودة في التعليم على مستوى المملكة",
    xaxis_title='السنة',
    yaxis_title='نسبة التغير',
    font=dict(color="#333333"),
    plot_bgcolor="#F5F5F5",
    paper_bgcolor="#F5F5F5",
    title_x=0.5
)
# معدل نمو قطاع البرمجة في المملكة
activity_programming["sorted_q"] = activity_programming["Qseries"].apply(lambda x: tuple(map(int, str(x).split('-'))))
line_data_prog = activity_programming.sort_values(by="sorted_q").drop(columns=["sorted_q"])
#line_data = line_data.sort_values(by="Qseries")  # Ensure years are in order
# Identify the first quarter's values
first_saudis = line_data_prog.loc[line_data_prog['Qseries'] == line_data_prog['Qseries'].min(), 'Number_Of_Saudis'].iloc[0]
first_nonsaudis = line_data_prog.loc[line_data_prog['Qseries'] == line_data_prog['Qseries'].min(), 'Number_Of_Nonsaudis'].iloc[0]

# Calculate percentage change relative to the first quarter
line_data_prog['Saudis_change_perc'] = ((line_data_prog['Number_Of_Saudis'] - first_saudis) / first_saudis) * 100
line_data_prog['NonSaudis_change_perc'] = ((line_data_prog['Number_Of_Nonsaudis'] - first_nonsaudis) / first_nonsaudis) * 100

# Create the plot
prog_line = go.Figure()

# Add lines for Saudis and Non-Saudis
prog_line.add_trace(go.Scatter(
    x=line_data_prog['Qseries'],
    y=line_data_prog['Saudis_change_perc'],
    mode='lines+markers+text',
    name='Number of Saudis',
    text=[f"{v:.1f}%" if not pd.isnull(v) else "" for v in line_data_prog['Saudis_change_perc']],
    textposition='top center',
    line=dict(color='#008000')
))

prog_line.add_trace(go.Scatter(
    x=line_data_prog['Qseries'],
    y=line_data_prog['NonSaudis_change_perc'],
    mode='lines+markers+text',
    name='Number of Non-Saudis',
    text=[f"{v:.1f}%" if not pd.isnull(v) else "" for v in line_data_prog['NonSaudis_change_perc']],
    textposition='top center',
    line=dict(color='#00509E')
))

prog_line.update_layout(
    title=f"معدل نمو السعودة في قطاع البرمجة على مستوى المملكة",
    xaxis_title='السنة',
    yaxis_title='نسبة التغير',
    font=dict(color="#333333"),
    plot_bgcolor="#F5F5F5",
    paper_bgcolor="#F5F5F5",
    title_x=0.5
)

# اقل قطاعات في السعودة في المملكة
last5 = go.Figure()
colors={
        'Number_Of_Saudis': '#008000',       # Emerald green
        'Number_Of_Nonsaudis': '#00509E'    # Soft navy blue
    }
last5.add_trace(go.Bar(x=last_activities["Economic_Activity"],
                        y=last_activities["total_saudis_percentage"],
                        name="السعوديين %",
                        marker_color=colors["Number_Of_Saudis"],
                        text=[f"{v:.1%}" for v in last_activities.head(5)["total_saudis_percentage"]],  # Format as percentage
                        textposition="outside"))

last5.add_trace(go.Bar(x=last_activities["Economic_Activity"],
                        y=last_activities["total_non_saudis_percentage"],
                        name="غير السعوديين %",
                        marker_color=colors["Number_Of_Nonsaudis"],
                        text=[f"{v:.1%}" for v in last_activities.head(5)["total_non_saudis_percentage"]], 
                        textposition="outside"))


#========================================================منطقة التشارتات========================================================================

# Dash App Initialization
app = Dash(__name__)
myStyle = {
        "textAlign": "justify",
        "color": "#333333",
        "margin": "20px 0",
        "lineHeight": "1.8",
        "fontSize": "18px",
        "backgroundColor": "#FFFFFF",
        "padding": "15px",
        "borderRadius": "8px",
        "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
    }
# Update Dash App Layout
app.layout = html.Div(
    style={
        "fontFamily": "Roboto, sans-serif",
        "backgroundColor": "#F5F5F5",
        "padding": "20px",
        "justify-content": "center",
        "direction": "rtl",
    },
    children=[
        html.H1(
            "وين وصلنا في السعودة؟",
            style={"textAlign": "center", "color": "#333333"},
        ),
        html.P(
            [
                "لو سافرنا بالزمن ورجعنا 10 سنين, بنلاحظ الفرق في التطور الكبير الي وصلت له المملكة العربية السعودية في السنوات الاخيرة خصوصا في مجال السعودة وتمكين أبناء الوطن.",
                html.Br(),
                "هل كنت تدري ان السعودية احتلت المركز الأول في أعلى معدل نمو بين مجموعة العشرين عام 2022, كيف أثر هذا النمو على توظيف السعوديين؟",
                html.Br(),
                "في هذي الرحلة بنعرف وين وصلنا في سعودة القطاعات في المملكة العربية السعودية",
            ],
            style=myStyle,
        ),
        html.Div(
            dcc.Graph(
                id="total-bar-chart",
                figure=total_bar,
            ),
            style={"margin": "20px 0"},
        ),
        html.P(
            [
                "وين تتوقع أعلى منطقة في نسبة السعودة؟",
            ],
            style=myStyle,
        ),
        html.Div(
            dcc.Graph(
                id="scatter-map",
                figure=map_chart
            ),
            style={"width": "65%",  "display": "inline-block"}
        ),
        html.Div(
            dcc.Graph(
                id="dynamic-pie-chart"
            ),
            style={"width": "35%", "display": "inline-block"}
        ),
        html.P(
            [
                "في الشكل الي تحت نوضح لك أعلى 5 مناطق في نسب السعودة"
            ],
            style=myStyle,
        ),
         html.Div(
            dcc.Graph(
                id="top-5-bar-chart",
                figure=top5_bar
            ),
            style={"margin": "20px 0"}
        ),
         html.P(
    [
        "نلاحظ ان الشرقية هي أعلى منطقة في نسب السعودة, ",
        html.Span(
            "وش السبب؟", 
            style={
                "fontSize": "20px", 
                "color": "red", 
                "fontWeight": "bold"
            }
        ),
        html.Br(),
        "عشان نعرف الجواب لازم نعرف وش القطاعات المتوفرة في سوق العمل, وحسب ",
        html.Strong("الدليل الوطني للأنشطة الاقتصادية ISIC4"), 
        " تملك المملكة ",
        html.Span(
            "89", 
            style={
                "fontSize": "20px", 
                "color": "red", 
                "fontWeight": "bold"
            }
        ),
        " قطاع في مستوى النشاط الاقتصادي الثاني ",
        html.Br(),
        "وش هي أعلى 5 قطاعات في نسب السعودة في الشرقية؟"
    ],
    style=myStyle,
),
         html.Div(
            dcc.Graph(
                id="shrqya-5-bar-chart",
                figure=shrqya5
            ),
            style={"margin": "20px 0"}
        ),
         html.P([
            "الشرقية تتصدر لأنها قلب الصناعة في المملكة، وكلنا نعرف ",
            html.Strong("أرامكو وسابك"), 
            " وشركات البتروكيماويات اللي توفر وظائف كثيرة وتدرب السعوديين باستمرار. غير كذا، المنطقة فيها تنوع كبير في فرص العمل، من النفط إلى التجارة والخدمات، وهذا يزيد الإقبال عليها.",
            html.Br(),
           "الحكومة كذلك لعبت دور كبير بدعم السعودة، وبرامج مثل ",
            html.Strong("هدف "),
            "ساعدت الشركات في تحقيق نسب عالية بتوظيف المواطنين. وما ننسى التعليم القوي هناك، مع جامعات ومعاهد تجهز الشباب لسوق العمل مباشرة.",
            html.Br(),
            "أيضا، البنية التحتية المتطورة مثل الموانئ والمدن الصناعية جذبت استثمارات، وهذه الاستثمارات جابت معها وظائف. لما نجمع كل هالعوامل، نقدر ناخذ تصور عن سبب تصدر الشرقية في نسب السعودة.",
            html.Br(),
            "في المقابل, خلونا نشوف أقل المناطق في السعودة عشان ناخذ تصور مختلف"
           
         ],style=myStyle),
    html.Div(
            dcc.Graph(
                id="last5-bar",
                figure=last5_bar
            ),
            style={"margin": "20px 0"}
        ),
    html.P([
            "نلاحظ ان ",
            html.Strong("نجران "),
            "تملك",
            html.Span(
            " أقل ", 
            style={
                "fontSize": "20px", 
                "color": "red", 
                "fontWeight": "bold"
            }
        ),
        "نسبة سعودة, وجانا فضول نعرف المشكلة في منطقة نجران؟",
         html.Br(),
         ".لذلك بحثنا عن أكثر نشاطات فيها سعودة في المنطقة"   
         ],style=myStyle),
    html.Div(
            dcc.Graph(
                id="njran5-bar",
                figure=njran5
            ),
            style={"margin": "20px 0"}
        ),
    html.P([
            "لاحظنا ان عدد النشاطات الي فيها نسبة سعوديين أكثر من الغير سعوديين هي ",
            html.Span(
            " 4 ", 
            style={
                "fontSize": "20px", 
                "color": "red", 
                "fontWeight": "bold"
            }
        ),
        "نشاطات فقط من أصل",
        html.Span(
            " 89 ", 
            style={
                "fontSize": "20px", 
                "color": "red", 
                "fontWeight": "bold"
            }
        ),
        "نشاط",
         html.Br(),
         "وفكرنا في عدة اسباب ولقينا ان التركيز الكبير كان على القطاعات التقليدية مثل ",
            html.Strong("الزراعة والتعدين، "),
            "وهي مجالات غالبًا تعتمد على العمالة الوافدة لتكلفتها الأقل.",
         html.Br(),
         "مع ذلك، الحكومة مستمرة على تحسين الوضع من خلال مبادرات تشجع على تنمية القطاعات السياحية والزراعية، ونتوقع زيادة نسبة التوطين في السنوات المقبلة "
         ],style=myStyle),
    html.P([
            "بعد ما شفنا أكثر من منظور للسعودة في المملكة, حبينا نشوف أهم القطاعات القريبة منا"
         ],style=myStyle),
    html.H1("التعليم",style={"textAlign": "center", "color": "#333333"}),
    html.P([
            "التعليم هو حجر الأساس لاقتصاد كل دولة، ومنه تنطلق الكوادر الي تسهم في بناء المستقبل",
            html.Br(),
            " نظام التعليم في المملكة من تأسيسها على يد الملك عبدالعزيز آل سعود رحمه الله، وأعطت الحكومة التعليم أولوية قصوى لتحقيق التنمية الشاملة.",
            html.Br(),
            "ومن بدايات التعليم كان فيه جهود كبيرة في سعودة الوظائف التعليمية, ومع إطلاق رؤية المملكة 2030، زادت وتيرة هذه الجهود وصارت نتايجها ملحوظة."
         ],style=myStyle),
    html.Div(
            dcc.Graph(
                id="edu-line",
                figure=edu_line
            ),
            style={"margin": "20px 0"}
        ),
        html.H1("البرمجة",style={"textAlign": "center", "color": "#333333"}),
        html.P([
            "مع التحول الرقمي ودعم رؤية المملكة 2030، صار قطاع البرمجة والتقنية بشكل عام من أكثر القطاعات الواعدة في المستقبل عشان كذا حبينا نعرف اكثر عن اتجاه نمو سوق العمل في هذا القطاع.",
         ],style=myStyle),
        html.Div(
            dcc.Graph(
                id="prog-line",
                figure=prog_line
            ),
            style={"margin": "20px 0"}
        ),
        html.H2([
            "بعد ما تعرفنا عن القطاعات الواعدة جاء ببالنا تساؤل .. هل فيه قطاعات غير واعدة للمواطنين؟",
            "وهل فيه عزوف للشعب السعودي عن بعض القطاعات؟"
         ],style=myStyle),
        html.Div(
            dcc.Graph(
                id="last5",
                figure=last5
            ),
            style={"margin": "20px 0"}
        ),
    ],
)
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
        order = None  # No order for entire Saudi Arabia
    else:
        # Specific region
        region_data = region_employee_summary[region_employee_summary['region'] == selected_region]
        total_saudis = region_data['Number_Of_Saudis'].sum()
        total_nonsaudis = region_data['Number_Of_Nonsaudis'].sum()
        total_male_saudis = region_data['Number_Of_Male_Saudis'].sum()
        total_female_saudis = region_data['Number_Of_Female_Saudis'].sum()
        total_male_nonsaudis = region_data['Number_Of_Male_Nonaudis'].sum()
        total_female_nonsaudis = region_data['Number_Of_Female_Nonaudis'].sum()
        order = region_data['order'].values[0]  # Get the order value for the specific region

    # Ensure division by zero does not occur
    male_saudis_percentage = "0%" if total_saudis == 0 else f"%{(total_male_saudis / total_saudis * 100):.0f}"
    female_saudis_percentage = "0%" if total_saudis == 0 else f"%{(total_female_saudis / total_saudis * 100):.0f}"
    male_nonsaudis_percentage = "0%" if total_nonsaudis == 0 else f"%{(total_male_nonsaudis / total_nonsaudis * 100):.0f}"
    female_nonsaudis_percentage = "0%" if total_nonsaudis == 0 else f"%{(total_female_nonsaudis / total_nonsaudis * 100):.0f}"
    
    # Custom data for the hover template
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

    # Pie chart data
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

    # Update hover template and title
    pie_chart.update_traces(
        hovertemplate="<br><b>%{customdata[0]}</b><br>",
    )

    # Update layout to include region order if applicable
    region_title = f"نسب السعودة في {selected_region} (الترتيب: {order})" if order is not None else f"نسب السعودة في {selected_region}"
    
    pie_chart.update_layout(
        title=region_title,
        font=dict(color="#333333"),
        plot_bgcolor="#F5F5F5",
        paper_bgcolor="#F5F5F5"
    )

    return pie_chart

if __name__ == "__main__":
    app.run(debug=True)
