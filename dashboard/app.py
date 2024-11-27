from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container
from pages.page1 import *
from pages.gender import *
from figures import *
from pages.overview import *
import saudi_calc as sc


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
        style={"backgroundColor": "#244434", "height": "50px", "width": "1500px"},
    ),
)
# ----------------------------end of Navbar ---------------------------


# ---------------------------- Tabs ---------------------------
tab1_content = dbc.Container(
    children=[
        html.H1("رؤية نمو", className="mt-2"),
        html.P(
            " هو مشروع يركز على تحليل العمق الاقتصادي والاجتماعي للمملكة، هدفنا كان نفهم وين السعودة قاعدة تزدهر، وكيف نقدر نوصل لتوازن أكبر بين الجنسين في مختلف القطاعات. تعرف أن نسبة السعودة تتفاوت بشكل كبير بين المناطق والقطاعات؟ خلال هذا المشروع ، كشفنا نقاط القوة في بعض المناطق والقطاعات ، بالإضافة إلى تحديد المناطق اللي تحتاج لتحسين وتطوير في مجال التوظيف.",
            style={"textAlign": "Right", "color": "#333333", "font-size": "20px"},
        ),
        # Second Row (Three smaller cards below the first card)
        dbc.Row(
            [
                # First smaller card
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            children=[
                                html.Div(
                                    children=[
                                        html.H5(
                                            "89 قطاع",
                                            style={
                                                "textAlign": "center",
                                                "color": "#006666",
                                            },
                                        ),
                                        html.P(
                                            "عدد القطاعات المختلفة في البيانات",
                                            style={
                                                "textAlign": "center",
                                                "color": "#555555",
                                            },
                                        ),  # Change text color
                                    ]
                                )
                            ]
                        ),
                        color="info",
                        outline=True,
                    ),
                    width=4,
                ),
                # Second smaller card
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            html.Div(
                                children=[  # Wrap multiple child elements inside a list
                                    html.H5(
                                        "عدد الصفوف",
                                        style={
                                            "textAlign": "center",
                                            "color": "#006666",
                                        },
                                    ),
                                    html.P(
                                        "40000",
                                        style={
                                            "textAlign": "center",
                                            "color": "#555555",
                                        },
                                    ),
                                ]
                            )
                        ),
                        color="success",
                        outline=True,
                    ),
                    width=4,
                ),
                # Third smaller card
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            html.Div(
                                children=[
                                    html.H5(
                                        "مصدر البيانات",
                                        style={
                                            "textAlign": "center",
                                            "color": "#006666",
                                        },
                                    ),
                                    html.P(
                                        "الهيئة العامة للمنشآت الصغيرة والمتوسطة",
                                        style={
                                            "textAlign": "center",
                                            "color": "#555555",
                                        },
                                    ),
                                ]
                            )
                        ),
                        color="warning",  # Yellow background for the card
                        outline=True,
                    ),
                    width=4,
                ),
            ],
            style={"marginTop": "20px"},
        ),
        # Second Card(Char)
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            html.Div(
                                children=[  # Wrap multiple child elements inside a list
                                    dcc.Graph(
                                        id="growth-chart",
                                        figure={
                                            "data": [
                                                go.Scatter(
                                                    x=df_combined[
                                                        "Year_Quarter"
                                                    ],  # X-axis: Year and Quarter
                                                    y=df_combined[
                                                        "Growth"
                                                    ],  # Y-axis: Growth rate
                                                    mode="lines+markers",  # Line chart with markers
                                                    name="Total_Saudis_Nonsaudis",
                                                    line={
                                                        "color": "rgb(99, 184, 255)",
                                                        "width": 2,
                                                    },  # Light blue line color
                                                    marker={
                                                        "symbol": "circle",  # Circle shape for markers
                                                        "size": 8,  # Marker size
                                                        "line": {
                                                            "width": 2,
                                                            "color": "rgb(99, 184, 255)",
                                                        },
                                                        "color": "white",
                                                    },
                                                )
                                            ],
                                            "layout": go.Layout(
                                                title="معدل نمو التوظيف",
                                                xaxis={},  # X-axis label
                                                yaxis={},  # Y-axis label
                                                showlegend=False,  # Hide legend
                                                plot_bgcolor="white",  # White background for the chart
                                                margin={
                                                    "l": 40,
                                                    "r": 10,
                                                    "t": 50,
                                                    "b": 40,
                                                },  # Adjust margins
                                                font={
                                                    "family": "Arial",
                                                    "size": 20,
                                                    "color": "black",
                                                },  # Set font style and size
                                            ),
                                        },
                                        style={
                                            "width": "100%",
                                            "height": "300px",
                                        },  # Adjust chart size
                                    ),
                                ]
                            )
                        )
                    ),
                    width=12,
                    style={"marginTop": "40px", "marginBottom": "40px"},
                )
            ]
        ),
    ],
)

tab2_content = dbc.Container(
    children=[
        # Title and Introduction
        html.H1("تحليل السعودة", className="mt-2"),
        html.P(
            [
                "لو سافرنا بالزمن ورجعنا 10 سنين، بنلاحظ الفرق في التطور الكبير الي وصلت له المملكة العربية السعودية في السنوات الاخيرة خصوصا في مجال السعودة وتمكين أبناء الوطن.",
                html.Br(),
                "هل كنت تدري أن السعودية احتلت المركز الأول في أعلى معدل نمو بين مجموعة العشرين عام 2022؟ كيف أثر هذا النمو على توظيف السعوديين؟",
                html.Br(),
                "في هذي الرحلة بنعرف وين وصلنا في سعودة القطاعات في المملكة العربية السعودية",
            ],
            style={"font-size": "20px"},
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    # Total Employees Bar Chart
                    dcc.Graph(
                        id="total-bar-chart",
                        figure=create_total_bar(sc.total_saudis, sc.total_nonsaudis),
                    ),
                    # Regions Overview
                    html.H3(
                        "وين تتوقع أعلى منطقة في نسبة السعودة؟",
                        style={"marginTop": "20px"},
                    ),
                    dcc.Dropdown(
                        id="region-dropdown",
                        options=[
                            {"label": region, "value": region}
                            for region in sc.lastQ_region["region"].unique()
                        ],
                        style={"width": "90%", "margin": "5px"},
                    ),
                    html.Div(
                        dbc.Row(
                            [
                                # Pie chart in the first column
                                dbc.Col(
                                    dcc.Graph(
                                        id="pie-chart", style={"height": "400px"}
                                    ),
                                    width=8,  # Adjust width as needed
                                ),
                                # Order display in the second column
                                dbc.Col(
                                    html.Div(
                                        id="order-display",
                                        style={
                                            "textAlign": "center",
                                            "fontSize": "20px",
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
                        id="content-container",  # Add ID to control visibility
                        style={"display": "none"},  # Initially hidden
                    ),
                    # Top 5 Regions Bar Chart
                    html.P(
                        "في الشكل الي تحت نوضح لك أعلى 5 مناطق في نسب السعودة.",
                        style={"marginTop": "20px"},
                    ),
                    dcc.Graph(
                        id="top5-bar-chart",
                        figure=create_top5_bar(sc.top_5_regions),
                    ),
                    # Analysis of Eastern Region
                    html.H3(
                        [
                            "نلاحظ أن الشرقية هي أعلى منطقة في نسب السعودة، ",
                        ]
                    ),
                    html.Br(),
                    "لمعرفة السبب, لازم نعرف وش القطاعات المتوفرة في سوق العمل، وحسب ",
                    html.Strong("الدليل الوطني للأنشطة الاقتصادية ISIC4"),
                    " تملك المملكة ",
                    html.Span("89", style={"color": "#000000", "fontWeight": "bold"}),
                    " قطاع في مستوى النشاط الاقتصادي الثاني.",
                    html.Br(),
                    "وش هي أعلى 5 قطاعات في نسب السعودة في الشرقية؟",
                    dcc.Graph(
                        id="shrqya5-bar-chart",
                        figure=create_shrqya5_bar(sc.top_activities),
                    ),
                    html.P(
                        [
                            " المنطقة الشرقية تتصدر في نسب السعودة بفضل دورها الصناعي، ووجود شركات كبرى مثل ",
                            html.Strong("أرامكو وسابك"),
                            " وشركات البتروكيماويات اللي توفر وظائف كثيرة وتدرب السعوديين باستمرار. غير كذا، المنطقة فيها تنوع كبير في فرص العمل، من النفط إلى التجارة والخدمات، وهذا يزيد الإقبال عليها.",
                            " وتنوع فرص العمل بين النفط والتجارة والخدمات. دعم الحكومة عبر برامج مثل ",
                            html.Strong("هدف "),
                            "في المقابل, خلونا نشوف أقل المناطق في السعودة عشان ناخذ تصور مختلف",
                        ]
                    ),
                    dcc.Graph(
                        id="last5-bar-chart",
                        figure=create_last5_bar(sc.last_5_regions),
                    ),
                    # Analysis of Najran
                    html.H3(
                        [
                            "نجران تملك أقل نسبة سعودة",
                        ]
                    ),
                    html.P(
                        " وجانا فضول نعرف المشكلة في منطقة نجران؟ لذلك بحثنا عن أكثر النشاطات فيها سعودة في المنطقة.",
                    ),
                    dcc.Graph(
                        id="last5-bar-chart",
                        figure=create_shrqya5_bar(sc.top_activities_last),
                    ),
                    html.H5(
                        "من أصل 89 نشاط، هناك 4 نشاطات فقط فيها نسبة سعوديين أكثر من غير سعوديين!"
                    ),
                    html.P(
                        "يرجع ذلك إلى التركيز على القطاعات التقليدية مثل الزراعة والتعدين التي تعتمد على العمالة الوافدة بتكلفة أقل. ومع ذلك، الحكومة تعمل على تحسين الوضع من خلال مبادرات تشجع على تنمية القطاعات السياحية والزراعية، مما يُتوقع أن يزيد من نسبة التوطين في السنوات القادمة."
                    ),
                ]
            ),
            className="mt-2",
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.H1("نشاط التعليم"),
                    "التعليم هو حجر الأساس لاقتصاد كل دولة، ومنه تنطلق الكوادر الي تسهم في بناء المستقبل",
                    html.Br(),
                    "ومن بدايات التعليم كان فيه جهود كبيرة في سعودة الوظائف التعليمية, ومع إطلاق رؤية المملكة 2030، زادت وتيرة هذه الجهود وصارت نتايجها ملحوظة.",
                    # Education Growth Line Chart
                    html.H5("معدل نمو السعودة في التعليم"),
                    dcc.Graph(
                        id="edu-line-chart",
                        figure=create_line_chart(
                            sc.line_data_edu,
                            "معدل نمو السعودة في التعليم على مستوى المملكة",
                        ),
                    ),
                    html.P(
                        [
                            html.H1("نشاط التقنية"),
                            "مع التحول الرقمي ودعم رؤية المملكة 2030، صار نشاط التقنية بشكل عام من أكثر النشاطات الواعدة في المستقبل عشان كذا حبينا نعرف اكثر عن اتجاه نمو سوق العمل في هذا القطاع.",
                        ]
                    ),
                    # Programming Growth Line Chart
                    html.H5("معدل نمو السعودة في التقنية"),
                    dcc.Graph(
                        id="prog-line-chart",
                        figure=create_line_chart(
                            sc.line_data_prog,
                            "معدل نمو السعودة في قطاع التقنية على مستوى المملكة",
                        ),
                    ),
                    # Final Remarks
                    html.P(
                        [
                            " بعد ما تعرفنا عن القطاعات الواعدة جاء ببالنا تساؤل هل فيه عزوف للشعب السعودي عن بعض القطاعات؟"
                        ],
                    ),
                    dcc.Graph(
                        id="last5-bar-chart",
                        figure=create_last5_acti_bar(sc.last_activities),
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
                            "flex": "1",
                        },
                    ),
                ]
            ),
            className="mt-2",
        ),
    ]
)


fig_programming, rate_diff_prog = gender_programing()
fig_lib_managment, rate_diff_lib = lib_managment()
fig_real_estate, rate_diff_real = real_estate()
fig_oil_and_gas, rate_diff_oil = oil_and_gas()
tab3_content = dbc.Container(
    children=[
        html.H1("التوازن بين الجنسين", className="mt-2"),
        html.P(
            " قضية التوازن بين الجنسين في سوق العمل من اكثر القضايا التي اهتمت بها رؤية المملكة ,2030 يوم بعد يوم ومع اقترابنا للرؤية, وش هي المرحلة التي وصلت لها هذه القضية الآن؟ ",
            style={"font-size": "20px"},
        ),
        dbc.Card(
            dbc.CardBody(
                children=[
                    # Title
                    dbc.Row(
                        children=[
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        children=[
                                            html.H3(
                                                "عام 2022",
                                                style={"textAlign": "center"},
                                                className="mb-4",
                                            ),
                                            html.P(
                                                [
                                                    html.Img(
                                                        src="./assets/arabian_man.png",
                                                        alt="Male Icon",
                                                        style={
                                                            "width": "30px",
                                                            "marginRight": "5px",
                                                        },
                                                    ),
                                                    "نسبة الذكور: 60.8%.",
                                                ]
                                            ),
                                            html.P(
                                                [
                                                    html.Img(
                                                        src="./assets/arabian_woman.png",
                                                        alt="Female Icon",
                                                        style={
                                                            "width": "30px",
                                                            "marginRight": "5px",
                                                        },
                                                    ),
                                                    "نسبة الإناث: 39.2%.",
                                                ]
                                            ),
                                            html.P(
                                                "الفجوة بين النسب: 21.6% (فرق كبير نسبيًا بين الجنسين)."
                                            ),
                                        ],
                                        style={"height": "250px"},
                                    ),
                                ),
                                xs=12,
                                sm=12,
                                md=6,
                                lg=4,
                                xl=4,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        children=[
                                            html.H3(
                                                "عام 2023",
                                                style={"textAlign": "center"},
                                                className="mb-4",
                                            ),
                                            html.P(
                                                [
                                                    html.Img(
                                                        src="./assets/arabian_man.png",
                                                        alt="Male Icon",
                                                        style={
                                                            "width": "30px",
                                                            "marginRight": "5px",
                                                        },
                                                    ),
                                                    "نسبة الذكور: 59.2%.",
                                                ]
                                            ),
                                            html.P(
                                                [
                                                    html.Img(
                                                        src="./assets/arabian_woman.png",
                                                        alt="Female Icon",
                                                        style={
                                                            "width": "30px",
                                                            "marginRight": "5px",
                                                        },
                                                    ),
                                                    "نسبة الإناث: 40.8%.",
                                                ]
                                            ),
                                            html.P("الفجوة بين النسب تقل إلى 18.4%."),
                                        ],
                                        style={"height": "250px"},
                                    )
                                ),
                                xs=12,
                                sm=12,
                                md=6,
                                lg=4,
                                xl=4,
                            ),
                            dbc.Col(
                                dbc.Card(
                                    dbc.CardBody(
                                        children=[
                                            html.H3(
                                                "عام 2024",
                                                style={"textAlign": "center"},
                                                className="mb-4",
                                            ),
                                            html.P(
                                                [
                                                    html.Img(
                                                        src="./assets/arabian_man.png",  # Path to male icon
                                                        alt="Male Icon",
                                                        style={
                                                            "width": "30px",
                                                            "marginRight": "5px",
                                                        },
                                                    ),
                                                    "نسبة الذكور: 58.8%.",
                                                ]
                                            ),
                                            html.P(
                                                [
                                                    html.Img(
                                                        src="./assets/arabian_woman.png",  # Path to female icon
                                                        alt="Female Icon",
                                                        style={
                                                            "width": "30px",
                                                            "marginRight": "5px",
                                                        },
                                                    ),
                                                    "نسبة الإناث: 41.2%.",
                                                ]
                                            ),
                                            html.P(
                                                "الفجوة تتقلص أكثر إلى 17.6%، وهو دليل على استمرار التوجه نحو التوازن."
                                            ),
                                        ],
                                        style={"height": "250px"},
                                    )
                                ),
                                xs=12,
                                sm=12,
                                md=6,
                                lg=4,
                                xl=4,
                            ),
                        ],
                    ),
                ]
            ),
            className="mt-2",
        ),
        html.P(
            " هل يوجد نشاطات يهيمن عليها جنس معين على آخر؟ او ايش هي النشاطات المتوازنة في التوظيف للجنسين؟ بهدف معرفة النشاطات الواعدة للتوازن بين الجنسين والنشاطات المتدنية ومعرفة اسباب اختلافها",
            style={"margin": "20px", "font-size": "20px"},
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
                                html.P("خلونا ناخذ بعين الاعتبار عدة نشاطات:"),
                                dbc.ListGroup(
                                    [
                                        dbc.ListGroupItem("أنشطة التقنية والاستشارات"),
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
                                            "نلاحظ ان النشاطات التقنية والاستشارية تحقق توازن بين الجنسين وذلك بمعدل فرق منخفض"
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
                                            "عشان نعرف سبب معدل الفرق الكبير, بنتعرف على المناطق التي تعاني من فرق الفجوة الكبيرة في هذه الانشطة:"
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
                                                    " سبب وجود الفجوة في الرياض في الوضع الحالي بسبب طبيعة المشاريع التي يتميز فيها حجم استثماري كبير ومتطلبات خاصة من حيث الخبرة في مجالات التمويل والعلاقات التجارية",
                                                    style={"margin": "10px"},
                                                ),
                                                html.Li(
                                                    " في مكة، يتمركز النشاط العقاري حول الأعمال التجارية المرتبطة بموسم الحج والعمرة. بالنسبة للنساء,  التحديات اجتماعية ممكن تؤثر على مشاركتهم في المجال العقاري."
                                                ),
                                                html.P(
                                                    [
                                                        " بشكل عام، جهود تمكين المرأة في المملكة تشهد تطور مستمر، أبرزها دعم المرأة في العمل داخل المشاريع العقارية الكبرى مثل مشروع روشن، حيث يشكل العنصر النسائي 46% من العاملين في هذا المشروع ",
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
                                            "اما هنا فيرجع سبب الفجوة بسبب أن الشرقية تُعد المركز الرئيسي للصناعات النفطية في المملكة، بحيث يوجد فيها أكبر الحقول النفطية مثل  'الظهران ' و 'بقيق '. غالبية الوظائف هنا ميدانية أو في مناطق نائية، مثل الحقول الصحراوية، بحيث جعل فيه صعوبة على النساء العمل فيها بسبب التحديات الاجتماعية والبيئية. ومع ذلك, تتجه أرامكو السعودية الى تعزيز مشاركة المرأة السعودية في فطاع النفط والغاز."
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
    Output(
        "content-container", "style"
    ),  # ID of the container wrapping pie chart and order display
    Input("region-dropdown", "value"),
)
def toggle_visibility(selected_region):
    if selected_region:
        return {"display": "block"}  # Show container
    return {"display": "none"}  # Hide container


@app.callback(
    Output("order-display", "children"),
    Input("region-dropdown", "value"),
)
def update_order_display(selected_region):
    # Filter the dataframe to find the order for the selected region
    if selected_region:
        selected_order = sc.lastQ_region.loc[
            sc.lastQ_region["region"] == selected_region, "order"
        ].values[0]
        # Return the order as the displayed content
        return f"ترتيب المنطقة: {selected_order}"


@app.callback(Output("pie-chart", "figure"), Input("region-dropdown", "value"))
def update_pie_chart(selected_region):
    # Filter the DataFrame for the selected region
    filtered_df = sc.lastQ_region[sc.lastQ_region["region"] == selected_region]
    # Create the pie chart using the create_pie function
    return create_pie(filtered_df, selected_region)


if __name__ == "__main__":
    app.run(debug=True)
