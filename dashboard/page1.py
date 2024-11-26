import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output
from figures import create_figures  # Import function to generate figures
from styles import layout_style  # Import custom styles
import os
import pandas as pd

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set up file paths
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
data_folder_path = os.path.join(parent_dir, "data")

# Load data
region_employee_summary = pd.read_csv(os.path.join(data_folder_path, "region_employee_summary.csv"))
activity_group = pd.read_csv(os.path.join(data_folder_path, "activity_group24.csv"))
najran_df = pd.read_csv(os.path.join(data_folder_path, "najran_df.csv"))
activity_summary = pd.read_csv(os.path.join(data_folder_path, "activity_summary.csv"))

# Generate figures
figures = create_figures(region_employee_summary, activity_group, najran_df)

# Define app layout
app.layout = html.Div(
    style=layout_style,  # Apply styles
    children=[
        dbc.Container(
            [
                dbc.Row(dbc.Col(html.H1("Saudi Employment Analysis", className="text-center mb-4"))),
                dbc.Row(
                    [
                        dbc.Col(dcc.Graph(figure=figures["fig_top_regions"]), width=6),
                        dbc.Col(dcc.Graph(figure=figures["fig_bottom_regions"]), width=6),
                    ]
                ),
                dbc.Row(
                    dbc.Col(
                        html.Div(
                            [
                                html.Label("Select a Region:"),
                                dcc.Dropdown(
                                    id='region-dropdown',
                                    options=[
                                        {'label': region, 'value': region}
                                        for region in region_employee_summary['region'].unique()
                                    ],
                                    value=region_employee_summary['region'].iloc[0]
                                ),
                                dcc.Graph(id='activity-chart'),
                            ]
                        ),
                        width=12,
                    )
                ),
                dbc.Row(dbc.Col(dcc.Graph(figure=figures["fig_najran_trends"]), width=12)),
            ],
            fluid=True,
        )
    ]
)

# Callback to update economic activities by region
@app.callback(
    Output('activity-chart', 'figure'),
    [Input('region-dropdown', 'value')]
)
def update_activity_chart(selected_region):
    filtered_data = activity_group[activity_group['region'] == selected_region]
    fig = px.bar(
        filtered_data,
        x='Economic_Activity',
        y='total_saudis_percentage',
        title=f'Economic Activities in {selected_region}',
        labels={'Economic_Activity': 'Activity', 'total_saudis_percentage': 'Saudization %'},
        color='total_saudis_percentage',
        color_continuous_scale='Blues'
    )
    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
