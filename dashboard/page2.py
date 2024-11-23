from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import os

# Define file paths
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
data_folder_path = os.path.join(parent_dir, "data")

# Load data for all years
df_2022 = pd.read_csv(os.path.join(data_folder_path, "activity_group22.csv"))
df_2023 = pd.read_csv(os.path.join(data_folder_path, "activity_group23.csv"))
df_2024 = pd.read_csv(os.path.join(data_folder_path, "activity_group24.csv"))

# Combine data into one DataFrame with a "Year" column
df_2022['Year'] = 2022
df_2023['Year'] = 2023
df_2024['Year'] = 2024
df = pd.concat([df_2022, df_2023, df_2024], ignore_index=True)

# Initialize Dash app
app = Dash(__name__)

# Dash layout
app.layout = html.Div(
    style={"fontFamily": "Roboto, sans-serif", "backgroundColor": "#F5F5F5", "padding": "20px"},
    children=[
        html.H1(
            "نظرة عامة على الموظفين حسب النشاط",
            style={"textAlign": "center", "color": "#333333"}
        ),
        html.Div([
            # Radio buttons to select year
            html.Div(
                [
                    html.Label(
                        "اختر السنة",
                        style={"margin-bottom": "10px", "color": "#333333", "fontSize": "18px"}
                    ),
                    dcc.RadioItems(
                        id='year-radio',
                        options=[
                            {"label": str(year), "value": year} for year in df['Year'].unique()
                        ],
                        value=df['Year'].unique()[0],  # Default year
                        labelStyle={"display": "inline-block", "margin-right": "15px"},
                        style={"margin-bottom": "20px"}
                    ),
                ]
            ),
            # Dropdown to select activity
            html.Div(
                [
                    html.Label(
                        "اختر النشاط",
                        style={"margin-bottom": "10px", "color": "#333333", "fontSize": "18px"}
                    ),
                    dcc.Dropdown(
                        id='activity-dropdown',
                        options=[
                            {"label": activity, "value": activity} for activity in df['Economic_Activity'].unique()
                        ],
                        value=df['Economic_Activity'].unique()[0],  # Default activity
                        placeholder="اختر النشاط",
                        style={"margin-bottom": "20px"}
                    ),
                ]
            ),
            # Pie chart and total employees
            html.Div(
                style={"display": "flex", "alignItems": "center"},
                children=[
                    dcc.Graph(id='pie-chart', style={"flex": "3", "margin-right": "20px"}),
                    html.Div(
                        id='total-employees-info',
                        style={
                            "flex": "1",
                            "textAlign": "center",
                            "backgroundColor": "#FFFFFF",
                            "padding": "10px",
                            "borderRadius": "8px",
                            "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.1)",
                            "color": "#333333",
                            "fontSize": "18px"
                        }
                    ),
                ]
            ),
            # Line chart
            dcc.Graph(id='line-chart')
        ])
    ]
)

# Callback to update pie chart, line chart, and total employees
@app.callback(
    [Output('pie-chart', 'figure'),
     Output('line-chart', 'figure'),
     Output('total-employees-info', 'children')],
    [Input('year-radio', 'value'),
     Input('activity-dropdown', 'value')]
)
def update_charts(selected_year, selected_activity):
    # Filter data for the selected year and activity
    filtered_df = df[(df['Year'] == selected_year) & (df['Economic_Activity'] == selected_activity)]
    
    # Aggregate Saudi and Non-Saudi counts for the pie chart
    aggregated_data = filtered_df[['Number_Of_Saudis', 'Number_Of_Nonsaudis']].sum()
    pie_data = pd.DataFrame({'Category': ['السعوديين', 'الغير سعوديين'], 'Count': aggregated_data})
    
    # Create pie chart
    pie_fig = px.pie(
        pie_data,
        names='Category',
        values='Count',
        title=f"توزيع الموظفين حسب الجنسية في {selected_activity} لعام {selected_year}",
        color='Category',
        color_discrete_map={
            'السعوديين': '#008000',       # Emerald green
            'الغير سعوديين': '#00509E'   # Soft navy blue
        }
    )
    pie_fig.update_layout(
        title={"x": 0.5, "xanchor": "center"},
        font=dict(color="#333333"),
        plot_bgcolor="#F5F5F5",
        paper_bgcolor="#F5F5F5"
    )
    
    # Filter data for the line chart by activity
    line_data = df[df['Economic_Activity'] == selected_activity]
    line_fig = px.line(
        line_data,
        x='Year',
        y=['Number_Of_Saudis', 'Number_Of_Nonsaudis'],
        title=f"اتجاه عدد الموظفين حسب السنة للنشاط {selected_activity}",
        labels={"value": "عدد الموظفين", "Year": "السنة", "variable": "الفئة"},
        color_discrete_map={
            'Number_Of_Saudis': '#008000',       # Emerald green
            'Number_Of_Nonsaudis': '#00509E'    # Soft navy blue
        }
    )
    line_fig.update_layout(
        title={"x": 0.5, "xanchor": "center"},
        font=dict(color="#333333"),
        plot_bgcolor="#F5F5F5",
        paper_bgcolor="#F5F5F5"
    )
    
    # Get total employees for the selected activity and year
    total_employees = filtered_df['total_employees'].sum()
    total_employees_text = f"إجمالي الموظفين: {total_employees:,}"

    return pie_fig, line_fig, total_employees_text

if __name__ == '__main__':
    app.run(debug=True)
