import altair as alt
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def make_donut(input_response, input_text, input_color):
    if input_color == 'blue':
        chart_color = ['#29b5e8', '#155F7A']
    if input_color == 'green':
        chart_color = ['#27AE60', '#12783D']
    if input_color == 'orange':
        chart_color = ['#F39C12', '#875A12']
    if input_color == 'red':
        chart_color = ['#E74C3C', '#781F16']

    source = pd.DataFrame({
        'Topic': ['', input_text],
        '% процентов': [100-input_response, input_response]
    })
    source_bg = pd.DataFrame({
        'Topic': ['', input_text],
        '% процентов': [100, 0]
    })

    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta='% процентов',
        color= alt.Color('Topic:N',
                        scale=alt.Scale(
                            #domain=['A', 'B'],
                            domain=[input_text, ''],
                            # range=['#29b5e8', '#155F7A']),  # 31333F
                            range=chart_color),
                        legend=None),
    ).properties(width=150, height=150)

    text = plot.mark_text(align='center', color='#29b5e8', font='Arial', fontSize=28, fontWeight=700, fontStyle='italic').encode(text=alt.value(f'{round(input_response)} %'))
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta='% процентов',
        color= alt.Color('Topic:N',
                        scale=alt.Scale(
                            # domain=['A', 'B'],
                            domain=[input_text, ''],
                            range=chart_color),  # 31333F
                        legend=None),
    ).properties(width=150, height=150)
    return plot_bg + plot + text


def make_pie(labels, values, *, colors=None, pull=None, hole=0, alternative_color_scheme=False):
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=hole,
        textinfo='percent+label',
        textposition='inside',
        insidetextorientation='radial',
        marker_colors=colors or (px.colors.qualitative.Plotly if not alternative_color_scheme else px.colors.qualitative.Vivid),
        pull=pull,
        textfont={'size': 35},
    )])
    fig.update_layout(margin=dict(t=0))    
    return fig

def make_hist(labels, values, colors=None, alternative_color_scheme=False):
    total = sum(values)
    percentages = [(v / total) * 100 for v in values] if total != 0 else [0]*len(values)
    fig = px.bar(
        x=labels,
        y=values,
        color=labels if colors is None else None,
        color_discrete_sequence=colors or (
            px.colors.qualitative.Plotly if not alternative_color_scheme else px.colors.qualitative.Vivid
        ),
        text=[f'{p:.1f}%' for p in percentages],
        labels={'x': '', 'y': ''},
    )
    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis={'categoryorder': 'total descending'},
        uniformtext_minsize=8,
        uniformtext_mode='hide',
        margin=dict(t=30, b=0),
        yaxis_range=[0, max(values) + max(max(values)*0.1, 10)],
    )
    
    fig.update_traces(
        textposition='outside',
        textfont_size=12,
        marker_line_color='rgb(8,48,107)',
        marker_line_width=1.5,
        hovertemplate='<b>%{x}</b><br>Количество: %{y}<br>Доля: %{text}<extra></extra>',
    )
    
    return fig
def choose_color(p1, p2, val, *, reverse=False) -> str:
    colors = ['red', 'orange', 'green']
    if(val < p1):
        idx = 0
    elif(val < p2):
        idx = 1
    else:
        idx = 2

    return colors[idx] if not reverse else colors[-idx-1]

def make_dataframe(df: pd.DataFrame):
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    align='left',
                    font_size=25,
                    height=40),
        cells=dict(values=df.transpose().values.tolist(),
                align='left',
                font_size=25,
                height=50,
                line_width=1,))
    ])
    fig.update_layout(
        autosize=True,
        margin=dict(l=0, r=0, b=0, t=0)
    )
    return fig

def make_time_plot(df, x, metric_name, color=None):
    fig = px.line(df, x=x, y='date', color=color)
    fig.update_layout(dict(
        xaxis_title='Время',
        yaxis_title=metric_name,
    ))
    return fig