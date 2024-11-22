from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

import os

current_dir = os.getcwd()

parent_dir = os.path.dirname(current_dir)

data_folder_path = os.path.join(parent_dir, "data")

all_data=pd.read_csv(os.path.join(data_folder_path,"df_q_group.csv"))
app = Dash(__name__) 


# page 1: نظرة عامة على اتجاهات التوظيف

# create the graph
fig = px.line(
        all_data,
        x="Q",
        y="total_employees",
        color="year",
    
        labels={"Q": "الربع", "total_employees": "عدد الموظفين", "year": "السنة"},
        markers=True

    )
# style the graph
fig.update_layout(
    title={
        "text": "عدد الموظفين حسب السنة",
        "x": 0.5, # center the title
        "xanchor": "center",
        "yanchor": "top",
    },
    font=dict(color="#333333"),
    plot_bgcolor="#F5F5F5",
    paper_bgcolor="#F5F5F5",
)
 
# create webpage layout 
app.layout = html.Div(
    style={"fontFamily": "Roboto, sans-serif", "backgroundColor": "#F5F5F5", "padding": "20px"},
    children=[
      # create banner for logo
        html.H1(
            "نظرة عامة على اتجاهات التوظيف",
            style={"textAlign": "center", "color": "#333333"}
        ),
        html.Div(
            [
         
                html.Div(
                    dcc.Graph(figure=fig),
                    style={"width": "48%", "display": "inline-block"}
                ),
            ],
            style={"display": "flex", "justifyContent": "space-between"}
        )
    ]
)

if __name__ == '__main__':
  app.run(debug=True)