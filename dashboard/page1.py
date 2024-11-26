from dash import Dash, html, dcc
import pandas as pd
import os
from figures import (
    createbarcharttopregions,
    createbarchart_bottom_regions,
    create_bar_chart_economic_activities,
    create_line_chart,
    create_geo_scatter,
)

current_dir = os.getcwd()
data_folder_path = os.path.join(current_dir, "data")

region_employee_summary = pd.read_csv(os.path.join(data_folder_path, "region_employee_summary.csv"))
top_5_regions = region_employee_summary.nlargest(5, 'total_saudis_percentage')
last_5_regions = region_employee_summary.nsmallest(5, 'total_saudis_percentage')

colors = {
    'Number_Of_Saudis': '#008000',
    'Number_Of_Nonsaudis': '#00509E',
}
custom_green_scale = ["#5bb450", "#52a447", "#46923c", "#3b8132", "#276221"]

fig_top_regions = create_bar_chart_top_regions(top_5_regions, custom_green_scale)
fig_bottom_regions = create_bar_chart_bottom_regions(last_5_regions, custom_green_scale)
fig_geo = create_geo_scatter(region_employee_summary)

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(figure=fig_top_regions),
    dcc.Graph(figure=fig_bottom_regions),
    dcc.Graph(figure=fig_geo),
])

if __name__ == '__main__':
    app.run_server(debug=True)