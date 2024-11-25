from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import os
import plotly.graph_objects as go

# Define file paths
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)
data_folder_path = os.path.join(parent_dir, "data")

# Load data for all years
df_2022 = pd.read_csv(os.path.join(data_folder_path, "activity_group22.csv"))
df_2023 = pd.read_csv(os.path.join(data_folder_path, "activity_group23.csv"))
df_2024 = pd.read_csv(os.path.join(data_folder_path, "activity_group24.csv"))

# Add 'Year' column to each dataset
df_2022['Year'] = 2022
df_2023['Year'] = 2023
df_2024['Year'] = 2024

# Combine data into a single DataFrame
df = pd.concat([df_2022, df_2023, df_2024], ignore_index=True)
df.fillna(0, inplace=True)  # Fill missing values

# Calculate Saudi and non-Saudi percentages for df_2024
df_2024["Saudi_per"] = df_2024["Number_Of_Saudis"] / (df_2024["Number_Of_Saudis"] + df_2024["Number_Of_Nonsaudis"])
df_2024["nonSaudi_per"] = 1 - df_2024["Saudi_per"]

# Initialize Dash app
app = Dash(__name__)
# Dash layout
app.layout = html.Div(
    style={"fontFamily": "Roboto, sans-serif", "backgroundColor": "#F5F5F5", "padding": "20px"},
    children=[
        html.H1(
            "نظرة عامة على السعوَدة حسب النشاط",
            style={"textAlign": "center", "color": "#333333"}
        ),
        html.H3(
            "اكثر نشاطات فيها سعوَدة",
            style={"textAlign": "center", "color": "#333333"}
        ),
        # Bar chart at the top
        dcc.Graph(
            id="bar-chart",
            style={"height": "600px", "margin-bottom": "20px"}
        ),
        html.H3(
            "أقل نشاطات فيها سعوَدة",
            style={"textAlign": "center", "color": "#333333"}
        ),
        dcc.Graph(
            id="bar-chart2",
            style={"height": "600px", "margin-bottom": "20px"}
        ),
        # Radio buttons to select year
        html.Div(
            [html.H3(
            "تصفح بنفسك",
            style={"textAlign": "center", "color": "#333333"}
        ),
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
    ]
)
# Callback to update charts
@app.callback(
    [Output('pie-chart', 'figure'),
     Output('line-chart', 'figure'),
     Output('bar-chart', 'figure'),
     Output('bar-chart2', 'figure'),
     Output('total-employees-info', 'children')],
    [Input('year-radio', 'value'),
     Input('activity-dropdown', 'value')]
)
def update_charts(selected_year, selected_activity):
    # Filter data for the selected year and activity
    filtered_df = df[(df['Year'] == selected_year) & (df['Economic_Activity'] == selected_activity)]
    if filtered_df.empty:
        return go.Figure(), go.Figure(), go.Figure(), "لا توجد بيانات للعرض"
    
    # Pie chart
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

    # Line chart
    line_data = df[df['Economic_Activity'] == selected_activity]
    line_data = line_data.sort_values(by="Qseries")  # Ensure years are in order

    # Calculate percentage change for Saudis and Non-Saudis
    line_data['Saudis_change_perc'] = line_data['Number_Of_Saudis'].pct_change() * 100
    line_data['NonSaudis_change_perc'] = line_data['Number_Of_Nonsaudis'].pct_change() * 100

    line_fig = go.Figure()

    # Add lines for Saudis and Non-Saudis
    line_fig.add_trace(go.Scatter(
        x=line_data['Qseries'],
        y=line_data['Number_Of_Saudis'],
        mode='lines+markers+text',
        name='Number of Saudis',
        text=[f"{v:.1f}%" if not pd.isnull(v) else "" for v in line_data['Saudis_change_perc']],
        textposition='top center',
        line=dict(color='#008000')
    ))

    line_fig.add_trace(go.Scatter(
        x=line_data['Qseries'],
        y=line_data['Number_Of_Nonsaudis'],
        mode='lines+markers+text',
        name='Number of Non-Saudis',
        text=[f"{v:.1f}%" if not pd.isnull(v) else "" for v in line_data['NonSaudis_change_perc']],
        textposition='top center',
        line=dict(color='#00509E')
    ))

    line_fig.update_layout(
        title=f"Trend of Employment in {selected_activity}",
        xaxis_title='Year',
        yaxis_title='Number of Employees',
        font=dict(color="#333333"),
        plot_bgcolor="#F5F5F5",
        paper_bgcolor="#F5F5F5",
        title_x=0.5
    )

    
    # Bar chart
    top_activities = df_2024.nlargest(25, "Saudi_per")
    last_activities = df_2024.nsmallest(25, "Saudi_per")
    bar_fig = go.Figure()
    colors={
            'Number_Of_Saudis': '#008000',       # Emerald green
            'Number_Of_Nonsaudis': '#00509E'    # Soft navy blue
        }
    bar_fig.add_trace(go.Bar(x=top_activities["Economic_Activity"],
                            y=top_activities["Saudi_per"],
                            name="السعوديين %",
                            marker_color=colors["Number_Of_Saudis"],
                            text=[f"{v:.1%}" for v in top_activities.head(25)["Saudi_per"]],  # Format as percentage
                            textposition="outside"))
    
    bar_fig.add_trace(go.Bar(x=top_activities["Economic_Activity"],
                             y=top_activities["nonSaudi_per"],
                             name="غير السعوديين %",
                             marker_color=colors["Number_Of_Nonsaudis"],
                             text=[f"{v:.1%}" for v in top_activities.head(25)["nonSaudi_per"]], 
                             textposition="outside"))
    bar_fig2 = go.Figure()
    
    bar_fig2.add_trace(go.Bar(x=last_activities["Economic_Activity"],
                            y=last_activities["Saudi_per"],
                            name="السعوديين %",
                            marker_color=colors["Number_Of_Saudis"],
                            text=[f"{v:.1%}" for v in last_activities.head(25)["Saudi_per"]],  # Format as percentage
                            textposition="outside"))
    
    bar_fig2.add_trace(go.Bar(x=last_activities["Economic_Activity"],
                             y=last_activities["nonSaudi_per"],
                             name="غير السعوديين %",
                             marker_color=colors["Number_Of_Nonsaudis"],
                             text=[f"{v:.1%}" for v in last_activities.head(25)["nonSaudi_per"]], 
                             textposition="outside"))
    # Total employees
    filtered_df['total_employees'] = filtered_df['Number_Of_Saudis'] + filtered_df['Number_Of_Nonsaudis']
    total_employees = filtered_df['total_employees'].sum()
    total_employees_text = f"إجمالي الموظفين: {total_employees:,}"
    
    return pie_fig, line_fig, bar_fig, bar_fig2, total_employees_text

if __name__ == '__main__':
    app.run(debug=True)
