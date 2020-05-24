import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objs as go
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

"""
this function draws the plot and returns the figure object 
"""
def draw_cases_graph(confirm_increase,recover_increase,deceased_increase,dates):
    dict_temp = {'confirm_increase': confirm_increase, 'recover_increase': recover_increase, 'deceased_increase': deceased_increase}  
    cases_df = pd.DataFrame(dict_temp,index=dates)
    cases_df['dates'] = cases_df.index

    fig = go.Figure(data=go.Scatter(x=dates, y=confirm_increase))

    fig.update_layout(title='Covid-19 Cases Daily Tracker',template='plotly_dark',hovermode="x")

    fig.update_traces(name='Confirmed', showlegend = True)
    fig.add_scatter(x=dates, y=recover_increase,mode='lines',name='Recovered',line_color='lightgreen')
    fig.add_scatter(x=dates, y=deceased_increase,mode='lines',name='Deceased',line_color='red')
    fig.update_yaxes(title_text='No.of.Cases',title_font=dict(size=18, family='Courier'))
    fig.update_xaxes(
        tickangle=300,
        title_text='Date Range',
        title_font=dict(size=18, family='Courier'),
        rangeslider_visible=True
    )
    fig.update_traces(mode="lines", hovertemplate=None)

    return fig