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
        "Topic": ['', input_text],
        "% процентов": [100-input_response, input_response]
    })
    source_bg = pd.DataFrame({
        "Topic": ['', input_text],
        "% процентов": [100, 0]
    })

    plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
        theta="% процентов",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            #domain=['A', 'B'],
                            domain=[input_text, ''],
                            # range=['#29b5e8', '#155F7A']),  # 31333F
                            range=chart_color),
                        legend=None),
    ).properties(width=150, height=150)

    text = plot.mark_text(align='center', color="#29b5e8", font="Arial", fontSize=28, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{round(input_response)} %'))
    plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
        theta="% процентов",
        color= alt.Color("Topic:N",
                        scale=alt.Scale(
                            # domain=['A', 'B'],
                            domain=[input_text, ''],
                            range=chart_color),  # 31333F
                        legend=None),
    ).properties(width=150, height=150)
    return plot_bg + plot + text


def make_pie(labels, values, colors=None, pull=None, hole=0):
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=hole,
        textinfo='percent+label',
        textposition='inside',
        insidetextorientation='radial',
        marker_colors=colors or px.colors.qualitative.Plotly,
        pull=pull,
        textfont={'size': 35},
    )])
    fig.update_layout(margin=dict(t=0))
    
    
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