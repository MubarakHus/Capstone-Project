

from figures import create_total_bar  # Import other necessary figure creation functions
from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container
from pages.page1 import *
from pages.gender import *
import os
import plotly.express as px
import plotly.graph_objects as go
from figures import (
    create_total_bar,
    create_map_chart,
    create_top5_bar,
    create_shrqya5_bar,
    #create_njran5_bar,
    create_last5_bar,
    create_line_chart,
    create_last5_acti_bar,
    create_pie
)



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
lastQ_eco = lastQ.groupby("Economic_Activity")[['Number_Of_Establishments', 'Number_Of_Saudis', 'Number_Of_Male_Saudis', 'Number_Of_Female_Saudis', 'Number_Of_Nonsaudis', 'Number_Of_Male_Nonaudis', 'Number_Of_Female_Nonaudis', 'total_employees']].sum().reset_index()
lastQ_region = lastQ.groupby("region")[['Number_Of_Establishments', 'Number_Of_Saudis', 'Number_Of_Male_Saudis', 'Number_Of_Female_Saudis', 'Number_Of_Nonsaudis', 'Number_Of_Male_Nonaudis', 'Number_Of_Female_Nonaudis', 'total_employees']].sum().reset_index()


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
get_percent(lastQ_eco)
get_percent(lastQ_region)

lastQ_region = lastQ_region.sort_values(by="total_saudis_percentage", ascending=False)
lastQ_region['order'] = range(1, len(lastQ_region) + 1)

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
    "منطقة الجوف": {"lat": 30.3158, "lon": 38.3691}
}

region_employee_summary['lat'] = region_employee_summary['region'].apply(lambda x: region_coordinates[x]['lat'])
region_employee_summary['lon'] = region_employee_summary['region'].apply(lambda x: region_coordinates[x]['lon'])
# معدل نمو التعليم في المملكة
activity_education["sorted_q"] = activity_education["Qseries"].apply(lambda x: tuple(map(int, str(x).split('-'))))
line_data_edu = activity_education.sort_values(by="sorted_q").drop(columns=["sorted_q"])
#line_data = line_data.sort_values(by="Qseries")  # Ensure years are in order
first_saudis_edu = line_data_edu.loc[line_data_edu['Qseries'] == line_data_edu['Qseries'].min(), 'Number_Of_Saudis'].iloc[0]
first_nonsaudis_edu = line_data_edu.loc[line_data_edu['Qseries'] == line_data_edu['Qseries'].min(), 'Number_Of_Nonsaudis'].iloc[0]
# Calculate percentage change for Saudis and Non-Saudis
line_data_edu['Saudis_change_perc'] = ((line_data_edu['Number_Of_Saudis'] - first_saudis_edu) / first_saudis_edu) * 100
line_data_edu['NonSaudis_change_perc'] = ((line_data_edu['Number_Of_Nonsaudis'] - first_nonsaudis_edu) / first_nonsaudis_edu) * 100


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

app = Dash(
    __name__,
    title="تحليل اتجاه التوظيف في المملكة العربية السعودية",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    meta_tags=[
        {
            "name": "viewport",
            "content": "width=device-width, initial-scale=1",
            "charSet": "“UTF-8”",
        }
    ],
)

# ---------------------------- Navbar ---------------------------
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="./assets/رؤية نمو.png", height="30px")),
                        dbc.Col(
                            dbc.NavbarBrand(
                                "رؤية نمو", className="me-2", style={"color": "white"}
                            )
                        ),
                    ],
                    align="center",
                    className="g-0 me-auto",
                ),
                href="https://plotly.com",
                style={"textDecoration": "none"},
            ),
        ],
        style={
            "backgroundColor": "#244434",
        },
    ),
)
# ----------------------------end of Navbar ---------------------------


# ---------------------------- Tabs ---------------------------
tab1_content = [
    dbc.Row(
        children=[
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        children=[
                            html.H5(
                                "إجمالي عدد الموظفين حسب الجنس",
                                className="card-text",
                            ),
                            html.H6(
                                sum_employees() + " موظف", style={"color": "#00509E"}
                            ),
                        ]
                    ),
                    className="mt-2",
                ),
            ),
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        children=[
                            html.H5(
                                "تفصيل عدد الموظفين السعوديين وغير السعوديين",
                                className="card-text",
                            ),
                            dbc.Col(
                                html.H6(
                                    "سعوديين:" + " " + saudi_total(),
                                    style={"color": "#00509E"},
                                ),
                            ),
                            dbc.Col(
                                html.H6(
                                    "غير سعوديين:" + " " + nonsaudi_total(),
                                    style={"color": "#00509E"},
                                ),
                            ),
                        ]
                    ),
                    className="mt-2",
                ),
            ),
            dbc.Card(
                dbc.CardBody(
                    children=[
                        dcc.Graph(figure=employement_trends()),
                    ]
                ),
                className="mt-2",
            ),
        ]
    )
]



# Assuming all required data is preloaded and available as variables
tab2_content = dbc.Card(
    dbc.CardBody(
        [
            # Title and Introduction
            html.H5("تحليل السعودة", className="card-title"),
            html.P(
                [ 
                    "لو سافرنا بالزمن ورجعنا 10 سنين، بنلاحظ الفرق في التطور الكبير الي وصلت له المملكة العربية السعودية في السنوات الاخيرة خصوصا في مجال السعودة وتمكين أبناء الوطن.",
                    html.Br(),
                    "هل كنت تدري أن السعودية احتلت المركز الأول في أعلى معدل نمو بين مجموعة العشرين عام 2022؟ كيف أثر هذا النمو على توظيف السعوديين؟",
                    html.Br(),
                    "في هذي الرحلة بنعرف وين وصلنا في سعودة القطاعات في المملكة العربية السعودية",
                ]
            ),

            # Total Employees Bar Chart
            dcc.Graph(
                id="total-bar-chart",
                figure=create_total_bar(total_saudis, total_nonsaudis),
            ),

            # Regions Overview
            html.P(
                "وين تتوقع أعلى منطقة في نسبة السعودة؟",
                style={"marginTop": "20px"},
            ),
            dcc.Dropdown(
        id="region-dropdown",
        options=[{"label": region, "value": region} for region in lastQ_region["region"].unique()],
        value=lastQ_region["region"].iloc[5],  # Default value
        style={"width": "50%", "margin": "auto"}
    ),
    dbc.Row(
                [
                    # Pie chart in the first column
                    dbc.Col(
                        dcc.Graph(id="pie-chart", style={"height": "400px"}),
                        width=8,  # Adjust width as needed
                    ),
                    # Order display in the second column
                    dbc.Col(
                        html.Div(
                            id="order-display",
                            style={
                                "textAlign": "center",
                                "fontSize": "36px",
                                "fontWeight": "bold",
                                "color": "#000",
                                "padding": "10px",
                                "border": "2px solid #ccc",
                                "borderRadius": "8px",
                                "backgroundColor": "#f9f9f9",
                                "height": "100%",  # Make it align with the pie chart height
                                "display": "flex",
                                "justifyContent": "center",
                                "alignItems": "center",
                            },
                        ),
                        width=4,  # Adjust width as needed
                    ),
                ],
                align="center",  # Center align the row content vertically
            ),

            # Top 5 Regions Bar Chart
            html.P(
                "في الشكل الي تحت نوضح لك أعلى 5 مناطق في نسب السعودة.",
                style={"marginTop": "20px"},
            ),
            dcc.Graph(
                id="top5-bar-chart",
                figure=create_top5_bar(top_5_regions),
            ),

            # Analysis of Eastern Region
            html.P(
                [
                    "نلاحظ أن الشرقية هي أعلى منطقة في نسب السعودة، ",
                    html.Span("وش السبب؟", style={"color": "#000000", "fontWeight": "bold"}),
                    html.Br(),
                    "عشان نعرف الجواب لازم نعرف وش القطاعات المتوفرة في سوق العمل، وحسب ",
                    html.Strong("الدليل الوطني للأنشطة الاقتصادية ISIC4"),
                    " تملك المملكة ",
                    html.Span("89", style={"color": "#000000", "fontWeight": "bold"}),
                    " قطاع في مستوى النشاط الاقتصادي الثاني.",
                    html.Br(),
                    "وش هي أعلى 5 قطاعات في نسب السعودة في الشرقية؟",
                ]
            ),
            dcc.Graph(
                id="shrqya5-bar-chart",
                figure=create_shrqya5_bar(top_activities),
            ),
            html.P(
                [
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
                ]
            ),

            # Least 5 Regions Bar Chart
            html.P(
                [
                    "في المقابل، خلونا نشوف أقل المناطق في السعودة عشان ناخذ تصور مختلف.",
                ],
                style={"marginTop": "20px"},
            ),
            dcc.Graph(
                id="last5-bar-chart",
                figure=create_last5_bar(last_5_regions),
            ),

            # Analysis of Najran
            html.P(
                [
                    "نلاحظ أن ",
                    html.Strong("نجران"),
                    " تملك ",
                    html.Span("أقل", style={"color": "#000000", "fontWeight": "bold"}),
                    " نسبة سعودة. وجانا فضول نعرف المشكلة في منطقة نجران؟",
                    html.Br(),
                    "لذلك بحثنا عن أكثر النشاطات فيها سعودة في المنطقة.",
                ]
            ),
            dcc.Graph(
                id="last5-bar-chart",
                figure=create_shrqya5_bar(top_activities_last),
            ),
            
            html.P(
                [
                    "لاحظنا ان عدد النشاطات الي فيها نسبة سعوديين أكثر من الغير سعوديين هي ",
                    html.Span(" 4 "),
                    "نشاطات فقط من أصل",
                    html.Span(" 89 "),
                    "نشاط",
                    html.Br(),
                    "وفكرنا في عدة اسباب ولقينا ان التركيز الكبير كان على القطاعات التقليدية مثل ",
                    html.Strong("الزراعة والتعدين، "),
                    "وهي مجالات غالبًا تعتمد على العمالة الوافدة لتكلفتها الأقل.",
                    html.Br(),
                    "مع ذلك، الحكومة مستمرة على تحسين الوضع من خلال مبادرات تشجع على تنمية القطاعات السياحية والزراعية، ونتوقع زيادة نسبة التوطين في السنوات المقبلة "
                ]
            ),
            html.P(
                [
                    "بعد ما شفنا أكثر من منظور للسعودة في المملكة, حبينا نشوف أهم القطاعات القريبة منا",
                    html.H1("التعليم"),
                    "التعليم هو حجر الأساس لاقتصاد كل دولة، ومنه تنطلق الكوادر الي تسهم في بناء المستقبل",
                    html.Br(),
                    " نظام التعليم في المملكة من تأسيسها على يد الملك عبدالعزيز آل سعود رحمه الله، وأعطت الحكومة التعليم أولوية قصوى لتحقيق التنمية الشاملة.",
                    html.Br(),
                    "ومن بدايات التعليم كان فيه جهود كبيرة في سعودة الوظائف التعليمية, ومع إطلاق رؤية المملكة 2030، زادت وتيرة هذه الجهود وصارت نتايجها ملحوظة."
                    

                ]
            ),
            # Education Growth Line Chart
            html.H5("معدل نمو السعودة في التعليم"),
            dcc.Graph(
                id="edu-line-chart",
                figure=create_line_chart(line_data_edu, "معدل نمو السعودة في التعليم على مستوى المملكة"),
            ),
            html.P(
                [
                    html.H1("البرمجة"),
                    "مع التحول الرقمي ودعم رؤية المملكة 2030، صار قطاع البرمجة والتقنية بشكل عام من أكثر القطاعات الواعدة في المستقبل عشان كذا حبينا نعرف اكثر عن اتجاه نمو سوق العمل في هذا القطاع.",
                    

                ]
            ),
            
            # Programming Growth Line Chart
            html.H5("معدل نمو السعودة في البرمجة"),
            dcc.Graph(
                id="prog-line-chart",
                figure=create_line_chart(line_data_prog, "معدل نمو السعودة في قطاع البرمجة على مستوى المملكة"),
            ),

            # Final Remarks
            html.P(
                [
                   "بعد ما تعرفنا عن القطاعات الواعدة جاء ببالنا تساؤل .. هل فيه قطاعات غير واعدة للمواطنين؟",
                   "وهل فيه عزوف للشعب السعودي عن بعض القطاعات؟"

                ],
                
            ),
            dcc.Graph(
                id="last5-bar-chart",
                figure=create_last5_acti_bar(last_activities)
            ),
            html.H3(
                [
                    "هذا يطرح تساؤل آخر .. هل تتوقعون بالمستقبل بتزيد السعودة في هذي القطاعات؟",
                ],
                style={
                        "textAlign": "center",
                        "backgroundColor": "#FFFFFF",
                        "padding": "20px",
                        "borderRadius": "8px",
                        "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                        "color": "#333333",
                        "fontSize": "18px",
                        "flex": "1"
                    },
            ),
        ]
    ),
    className="mt-2",
)




fig_programming, rate_diff_prog = gender_programing()
fig_lib_managment, rate_diff_lib = lib_managment()
fig_real_estate, rate_diff_real = real_estate()
fig_oil_and_gas, rate_diff_oil = oil_and_gas()
tab3_content = dbc.Container(
    children=[
        html.H1("التوازن بين الجنسين", className="mt-2"),
        html.P(
            "تعد قضية التوازن بين الجنسين في سوق العمل من اكثر القضايا التي اهتمت بها رؤية المملكة ,2030 يوم بعد يوم ومع اقترابنا للرؤية, ما هي المرحلة التي وصلت إليها هذه القضية الآن؟ "
        ),
        dbc.Card(
            dbc.CardBody(
                children=[
                    # Title
                    html.H5(
                        "النسبة المئوية للموظفين السعوديين حسب الجنس والسنة ",
                        className="card-text",
                    ),
                    # Bar chart
                    dcc.Graph(
                        id="bar-chart",
                    ),
                    html.P(
                        "يتضح من الرسم البياني أن الفجوة بين نسبة الذكور ونسبة الإناث في الوظائف السعودية تتناقص تدريجيًا على مدار السنوات:"
                    ),
                    html.Ol(
                        children=[
                            html.Li("عام 2022:"),
                            html.Ul(
                                [
                                    html.Li("نسبة الذكور: 60.8%."),
                                    html.Li("نسبة الإناث: 39.2%."),
                                    html.Li(
                                        "الفجوة بين النسب: 21.6% (فرق كبير نسبيًا بين الجنسين)."
                                    ),
                                ],
                                style={"margin": "20px"},
                            ),
                            html.Li("عام 2023:"),
                            html.Ul(
                                [
                                    html.Li("نسبة الذكور: 59.2%."),
                                    html.Li("نسبة الإناث: 40.8%."),
                                    html.Li("الفجوة بين النسب تقل إلى 18.4%."),
                                ],
                                style={"margin": "20px"},
                            ),
                            html.Li("عام 2024:"),
                            html.Ul(
                                [
                                    html.Li("نسبة الذكور: 58.8%."),
                                    html.Li("نسبة الإناث: 41.2%."),
                                    html.Li(
                                        "الفجوة تتقلص أكثر إلى 17.6%، وهو دليل على استمرار التوجه نحو التوازن."
                                    ),
                                ],
                                style={"margin": "20px"},
                            ),
                        ]
                    ),
                ]
            ),
            className="mt-2",
        ),
        html.P(
            "استطلعنا بشكل عام تقلص الفجوة بين الجنسين, ولكن على مختلف النشاطات الاقتصادية في سوق العمل, تبرز تساؤلات ملهمة مثل:  'هل هناك نشاطات يهيمن عليها جنس معين على آخر؟ ' او  'ما هي النشاطات المتوازنة في التوظيف للجنسين؟' بهدف معرفة النشاطات الواعدة للتوازن بين الجنسين والنشاطات المتدنية ومعرفة اسباب اختلافها.",
            style={"margin": "20px"},
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            children=[
                                html.H5(
                                    "دراسة توزيع السعوديين حسب الجنس في القطاعات",
                                    className="card-text",
                                ),
                                html.P("لنأخذ بعين الاعتبار عدة نشاطات:"),
                                dbc.ListGroup(
                                    [
                                        dbc.ListGroupItem("أنشطة البرمجة والاستشارات"),
                                        dbc.ListGroupItem(
                                            "أنشطة ادارة المكتبات ودعم الاعمال"
                                        ),
                                        dbc.ListGroupItem("الانشطة العقارية"),
                                        dbc.ListGroupItem(
                                            "أنشطة استخراج النفط الخام والغاز"
                                        ),
                                    ],
                                    flush=True,
                                ),
                                dbc.Row(
                                    children=[
                                        dbc.Col(
                                            dcc.Graph(
                                                figure=fig_programming,
                                                style={
                                                    "height": "400px",
                                                    "width": "500px",
                                                },
                                            ),
                                        ),
                                        dbc.Col(
                                            dcc.Graph(
                                                figure=fig_lib_managment,
                                                style={
                                                    "height": "400px",
                                                    "width": "500px",
                                                },
                                            ),
                                        ),
                                        html.P(
                                            "نلاحظ ان النشاطات التقنية والاستشارية تحقق توازن بين الجنسين وذلك بمعدل فرق منخفض:"
                                        ),
                                        html.Ul(
                                            [
                                                html.Li(
                                                    str(rate_diff_prog)
                                                    + "%"
                                                    + " في أنشطة البرمجة والاستشارات "
                                                ),
                                                html.Li(
                                                    str(rate_diff_lib) + "%"
                                                    " في أنشطة ادارة المكتبات ودعم الاعمال "
                                                ),
                                            ],
                                            style={"margin-right": "20px"},
                                        ),
                                        dbc.Col(
                                            dcc.Graph(
                                                figure=fig_real_estate,
                                                style={
                                                    "height": "400px",
                                                    "width": "500px",
                                                },
                                            ),
                                        ),
                                        dbc.Col(
                                            dcc.Graph(
                                                figure=fig_oil_and_gas,
                                                style={
                                                    "height": "400px",
                                                    "width": "500px",
                                                },
                                            ),
                                        ),
                                        html.P(
                                            "اما بالنسبة لأنشطة العقار والنفط والغاز, نلاحظ وجود فجوة كبيرة بين الجنسين بمعدل فرق:"
                                        ),
                                        html.Ul(
                                            [
                                                html.Li(
                                                    str(rate_diff_real)
                                                    + "%"
                                                    + " في أنشطة العقار "
                                                ),
                                                html.Li(
                                                    str(rate_diff_oil) + "%"
                                                    " في أنشطة استخراج النفط الخام والغاز "
                                                ),
                                            ],
                                            style={"margin-right": "20px"},
                                        ),
                                        html.P(
                                            "ولمعرفة سبب معدل الفرق الكبير, سنتعرف على المناطق التي تعاني من فرق الفجوة الكبيرة في هذه الانشطة:"
                                        ),
                                        html.H5(
                                            "بالنسبة لانشطة العقار:",
                                            className="card-text",
                                        ),
                                        dcc.Graph(figure=gender_map_real_estate()),
                                        html.P(
                                            "ترجع اسباب الفجوة الكبيرة بين الجنسين الى عدة اسباب منها:"
                                        ),
                                        html.Ol(
                                            [
                                                html.Li(
                                                    "تعتبر الرياض المركز الاقتصادي الأبرز في المملكة، حيث تتمركز فيها أغلب المشاريع العقارية الكبرى. وسبب وجود الفجوة في الوضع الحالي بسبب طبيعة المشاريع التي تتميز بحجم استثماري كبير ومتطلبات خاصة من حيث الخبرة في مجالات التمويل والعلاقات التجارية",
                                                    style={"margin": "10px"},
                                                ),
                                                html.Li(
                                                    " في مكة، يتمركز النشاط العقاري حول الأعمال التجارية المرتبطة بموسم الحج والعمرة. بالنسبة للنساء، هناك تحديات اجتماعية قد تؤثر على مشاركتهن في المجال العقاري."
                                                ),
                                                html.P(
                                                    [
                                                        " بشكل عام، جهود تمكين المرأة في المملكة تشهد تطورًا مستمرًا، أبرزها دعم المرأة في العمل داخل المشاريع العقارية الكبرى مثل مشروع روشن، حيث يشكل العنصر النسائي 46% من العاملين في هذا المشروع ",
                                                        html.A(
                                                            "صحيفة سبق الالكترونية",
                                                            href="https://sabq.org/saudia/756esbohyw",
                                                            target="_blank",
                                                        ),
                                                    ],
                                                    style={"margin": "10px"},
                                                ),
                                            ],
                                            style={"margin": "20px"},
                                        ),
                                        html.H5(
                                            "بالنسبة لأنشطة استخراج النفط الخام والغاز:",
                                            className="card-text",
                                        ),
                                        dcc.Graph(figure=gender_map_oil_and_gas()),
                                        html.P(
                                            "اما هنا فيرجع سبب الفجوة بسبب أن الشرقية تُعد المركز الرئيسي للصناعات النفطية في المملكة، حيث توجد أكبر الحقول النفطية مثل  'الظهران ' و 'بقيق '. غالبية الوظائف هنا ميدانية أو في مناطق نائية، مثل الحقول الصحراوية، مما يُصعب على النساء العمل فيها بسبب التحديات الاجتماعية والبيئية. ومع ذلك, تتجه أرامكو السعودية الى تعزيز مشاركة المرأة السعودية في فطاع النفط والغاز."
                                        ),
                                        html.P(
                                            '"نحن نعي تأثير المرأة داخل أرامكو السعودية وعلى قطاع النفط والغاز على حدٍّ سواء، وقد طورنا بيئة ثرية لتمكين المرأة تتضمن مجموعة من برامج القيادة والتوجيه لتطوير المهارات والتقدم المهني السريع...ووفقًا لآخر إحصائية قدّمت النساء العاملات في أرامكو السعودية أكثر من 170 براءة اختراع في السنوات الأخيرة" (أرامكو السعودية)',
                                            style={
                                                "font-style": "italic",
                                                "color": "blue",
                                                "margin": "15px;",
                                            },
                                        ),
                                    ]
                                ),
                            ]
                        ),
                        className="mt-2",
                    )
                ),
            ]
        ),
    ]
)


tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_content, label="نظرة عامة", label_style={"color": "#333333"}),
        dbc.Tab(
            tab2_content,
            label="تحليل السعودة",
            label_style={"color": "#333333"},
        ),
        dbc.Tab(
            tab3_content, label="تحليل حسب الجنس", label_style={"color": "#333333"}
        ),
    ],
)
# ----------------------------end of Tabs ---------------------------

# create webpage layout
app.layout = dbc.Container(
    children=[navbar, tabs],
    style={"direction": "rtl", "font-family": "Tajawal", "background-color": "#F5F5F5"},
    fluid=True,
)

@app.callback(
    Output("order-display", "children"),
    Input("region-dropdown", "value"),
)
def update_order_display(selected_region):
    # Filter the dataframe to find the order for the selected region
    selected_order = lastQ_region.loc[
        lastQ_region["region"] == selected_region, "order"
    ].values[0]
    # Return the order as the displayed content
    return f"ترتيب المنطقة: {selected_order}"

# Callback to update the bar chart
@app.callback(Output("bar-chart", "figure"), Input("bar-chart", "id"))
def update_chart(_):
    fig = gender_percentage()
    return fig

@app.callback(
    Output("pie-chart", "figure"),
    Input("region-dropdown", "value")
)
def update_pie_chart(selected_region):
    # Filter the DataFrame for the selected region
    filtered_df = lastQ_region[lastQ_region["region"] == selected_region]
    # Create the pie chart using the create_pie function
    return create_pie(filtered_df, selected_region)

@app.callback(Output("region-map", "figure"), Input("region-map", "id"))
def update_map(_):
    print("hi")


if __name__ == "__main__":
    app.run(debug=True)

