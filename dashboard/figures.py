
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# figures.py
import plotly.graph_objects as go
import plotly.express as px



def create_total_bar(total_saudis, total_nonsaudis):
    total_bar = go.Figure(
        data=[
            go.Bar(
                name="الموظفين السعوديين",
                x=["الموظفين السعوديين"],
                y=[total_saudis],
                text=f"{total_saudis:,}",
                marker_color="#008000",
            ),
            go.Bar(
                name="الموظفين غير السعوديين",
                x=["الموظفين غير السعوديين"],
                y=[total_nonsaudis],
                text=f"{total_nonsaudis:,}",
                marker_color="#00509E",
            ),
        ]
    )
    total_bar.update_layout(
        title="اجمالي عدد الموظفين السعوديين وغير السعوديين",
        yaxis_title="عدد الموظفين",
        barmode="group",
        template="plotly_white",
        font={"size": 16},
    )
    return total_bar


def create_map_chart(data):
    map_chart = px.scatter_geo(
        data,
        lat="lat",
        lon="lon",
        size="total_saudis_percentage",
        hover_name="region",
        color="total_saudis_percentage",
        title="نسب السعودة في مناطق المملكة العربية السعودية",
        projection="natural earth",
    )
    map_chart.update_geos(
        scope="asia",
        center={"lat": 23.8859, "lon": 45.0792},
        fitbounds="locations",
    )
    map_chart.update_traces(
        marker=dict(color="green"),
        hovertemplate="<b>%{hovertext}</b><br> نسبة الموظفين السعوديين: %%{marker.size:.1f} <extra></extra>",
        text=data['region'],
        textposition="middle center",
        textfont=dict(size=10, color="black"),
    )
    map_chart.update_layout(
        font=dict(color="#333333"),
        plot_bgcolor="#F5F5F5",
        paper_bgcolor="#F5F5F5",
    )
    return map_chart


def create_top5_bar(top_5_regions):
    top5_bar = px.bar(
        top_5_regions,
        x="region",
        y="total_saudis_percentage",
        text="total_saudis_percentage",
        labels={"region": "المنطقة", "total_saudis_percentage": "نسبة السعوديين"},
        title="أعلى خمس مناطق في نسبة الموظفين السعوديين",
        color="total_saudis_percentage",
        color_continuous_scale=["#5bb450", "#52a447", "#46923c", "#3b8132", "#276221"],
    )
    top5_bar.update_traces(
        texttemplate='%{text:.2f}%',
        textposition='outside',
        hoverinfo="none",
    )
    top5_bar.update_layout(
        font=dict(color="#333333"),
        plot_bgcolor="#F5F5F5",
        paper_bgcolor="#F5F5F5",
        title_x=0.5,
        hovermode=False,
    )
    return top5_bar


def create_shrqya5_bar(top_activities):
    shrqya5 = go.Figure()
    colors = {
        'Number_Of_Saudis': '#008000',
        'Number_Of_Nonsaudis': '#00509E',
    }
    shrqya5.add_trace(
        go.Bar(
            x=top_activities["Economic_Activity"],
            y=top_activities["total_saudis_percentage"],
            name="السعوديين %",
            marker_color=colors["Number_Of_Saudis"],
            text=[f"{v:.1%}" for v in top_activities["total_saudis_percentage"]],
            textposition="outside",
        )
    )
    shrqya5.add_trace(
        go.Bar(
            x=top_activities["Economic_Activity"],
            y=top_activities["total_non_saudis_percentage"],
            name="غير السعوديين %",
            marker_color=colors["Number_Of_Nonsaudis"],
            text=[f"{v:.1%}" for v in top_activities["total_non_saudis_percentage"]],
            textposition="outside",
        )
    )
    return shrqya5


def create_last5_bar(last_5_regions):
    last5_bar = px.bar(
        last_5_regions,
        x="region",
        y="total_saudis_percentage",
        text="total_saudis_percentage",
        labels={"region": "المنطقة", "total_saudis_percentage": "نسبة السعوديين"},
        title="أقل خمس مناطق في نسبة الموظفين السعوديين",
        color="total_saudis_percentage",
        color_continuous_scale=["#5bb450", "#52a447", "#46923c", "#3b8132", "#276221"],
    )
    last5_bar.update_traces(
        texttemplate='%{text:.2f}%',
        textposition='outside',
        hoverinfo="none",
    )
    last5_bar.update_layout(
        font=dict(color="#333333"),
        plot_bgcolor="#F5F5F5",
        paper_bgcolor="#F5F5F5",
        title_x=0.5,
        hovermode=False,
    )
    return last5_bar


def create_line_chart(data, title):
    line_chart = go.Figure()

    line_chart.add_trace(
        go.Scatter(
            x=data['Qseries'],
            y=data['Saudis_change_perc'],
            mode='lines+markers+text',
            name='Number of Saudis',
            text=[f"{v:.1f}%" if not pd.isnull(v) else "" for v in data['Saudis_change_perc']],
            textposition='top center',
            line=dict(color='#008000'),
        )
    )

    line_chart.add_trace(
        go.Scatter(
            x=data['Qseries'],
            y=data['NonSaudis_change_perc'],
            mode='lines+markers+text',
            name='Number of Non-Saudis',
            text=[f"{v:.1f}%" if not pd.isnull(v) else "" for v in data['NonSaudis_change_perc']],
            textposition='top center',
            line=dict(color='#00509E'),
        )
    )

    line_chart.update_layout(
        title=title,
        xaxis_title='السنة',
        yaxis_title='نسبة التغير',
        font=dict(color="#333333"),
        plot_bgcolor="#F5F5F5",
        paper_bgcolor="#F5F5F5",
        title_x=0.5,
    )
    return line_chart

def create_last5_acti_bar(last_activities):
 # اقل قطاعات في السعودة في المملكة
    last5 = go.Figure()
    colors={
        'Number_Of_Saudis': '#008000',       # Emerald green
        'Number_Of_Nonsaudis': '#00509E'    # Soft navy blue
    }
    last5.add_trace(go.Bar(x=last_activities["Economic_Activity"],
                        y=last_activities["total_saudis_percentage"],
                        name="السعوديين %",
                        marker_color=colors["Number_Of_Saudis"],
                        text=[f"{v:.1%}" for v in last_activities.head(5)["total_saudis_percentage"]],  # Format as percentage
                        textposition="outside"))
    
    last5.add_trace(go.Bar(x=last_activities["Economic_Activity"],
                        y=last_activities["total_non_saudis_percentage"],
                        name="غير السعوديين %",
                        marker_color=colors["Number_Of_Nonsaudis"],
                        text=[f"{v:.1%}" for v in last_activities.head(5)["total_non_saudis_percentage"]], 
                        textposition="outside"))
    return last5

def create_pie(df, region):
    # Pie chart
    aggregated_data = df[['Number_Of_Saudis', 'Number_Of_Nonsaudis']].sum()
    pie_data = pd.DataFrame({'Category': ['السعوديين', 'الغير سعوديين'], 'Count': aggregated_data})
      # Create pie chart
    pie_fig = px.pie(
        pie_data,
        names='Category',
        values='Count',
        title=f"توزيع الموظفين السعوديين في {region}",
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
    return pie_fig