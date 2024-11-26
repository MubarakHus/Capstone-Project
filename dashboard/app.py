from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container
from pages.page1 import *
from pages.gender import *


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

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
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


# Callback to update the bar chart
@app.callback(Output("bar-chart", "figure"), Input("bar-chart", "id"))
def update_chart(_):
    fig = gender_percentage()
    return fig


@app.callback(Output("region-map", "figure"), Input("region-map", "id"))
def update_map(_):
    print("hi")


if __name__ == "__main__":
    app.run(debug=True)
