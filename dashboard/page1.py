from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd

import os

current_dir = os.getcwd()

parent_dir = os.path.dirname(current_dir)

data_folder_path = os.path.join(parent_dir, "data")

all_data=pd.read_csv(os.path.join(data_folder_path,"df_q_group.csv"))
app = Dash(__name__) 

fig = px.line(
        all_data,
        x="Q",
        y="total_employees",
        color="year",
        title="عدد الموظفين حسب السنة",
        labels={"Q": "الربع", "total_employees": "عدد الموظفين", "year": "السنة"}
    )
# 
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
   Dash: A web application framework for your data. '''),

    dcc.Graph(
      id='empperyear',
        figure=fig
    )])

if __name__ == '__main__':
  app.run(debug=True)