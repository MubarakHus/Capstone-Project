from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html
from dash_bootstrap_components._components.Container import Container
from pages.page1 import *


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

tab3_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 3!", className="card-text"),
        ]
    ),
    className="mt-2",
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

if __name__ == "__main__":
    app.run(debug=True)
