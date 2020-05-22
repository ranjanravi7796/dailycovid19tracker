import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from callbacks.register_callbacks import onLoad_country_options


#tab styles----

font_size = ".9vw"
color_active = "#F4F4F4"
color_inactive = "#AEAEAE"
color_bg = "#010914"

tabs_styles = {
    "flex-direction": "column",
}
tab_style = {
    "padding": "1vh",
    "color": color_inactive,
    "fontSize": font_size,
    "backgroundColor": color_bg,
}

tab_selected_style = {
    "fontSize": font_size,
    "color": color_active,
    "padding": "1vh",
    "backgroundColor": color_bg,
}

#------------

feed_tabs = dbc.Card(
    [
        html.Div(
            dcc.Tabs(
                id="left-tabs-styled-with-inline",
                value="news-tab",
                children=[
                    dcc.Tab(
                        label="Headlines based on the selected country",
                        value="news-tab",
                        className="left-news-tab",
                        style=tab_style,
                        selected_style=tab_selected_style,
                    )
                ],
                style=tabs_styles,
                colors={
                    "border": None,
                    "primary": None,
                    "background": None,
                },
            ),
            className="left-tabs",
        ),
        dbc.CardBody(
            html.P(
                id="feed-content",
                className="left-col-feed-cards-text",
                ),
            ),
    ]
)



build_layout = html.Div([

html.Div(
    [
        dbc.Row(dbc.Col(html.Div([
        html.H1('Covid-19 Tracker')
    ],className='rightcorner'))),
        dbc.Row(
            [
                dbc.Col(html.Div([
                html.Div('Choose a Country'),
                html.Div(dcc.Dropdown(id='country-selector',
                                      options=onLoad_country_options(),value='India',clearable=False,
                    searchable=True
                         ))
            ]),className='countries-dropdown-container',width=4)],className='centered'),
           dbc.Row(
            [ 
                dbc.Col(html.Div([html.H6(id="confirmed",className="card-title"), html.P("No. of Confirmed")],id='confirmed_css',className='mini_container')),
                dbc.Col(html.Div([html.H6(id="recovered",className="card-title"), html.P("No. of Recovered")],id='recovered_css',className='mini_container')),
                dbc.Col(html.Div([html.H6(id="deceased",className="card-title"), html.P("No. of Deceased")],id='deceased_css',className='mini_container')),
                dbc.Col(html.Div([html.H6(id="mortality",className="card-title"), html.P("Mortality Rate")],id='mortality_css',className='mini_container')),
                dbc.Col(html.Div([html.H6(id="recovery",className="card-title"), html.P("Recovery Rate")],id='recovery_css',className='mini_container'))
            ]
        ),
        dbc.Row([
            dbc.Col(
                html.Div([
            # graph
            dcc.Graph(id='cases-graph')
            # style={},
        ]),width=12)
        ],no_gutters=True),
        dbc.Row([
dbc.Col(feed_tabs,
                className="left-col-twitter-feed-content",
                width=12)
        ])
    ]
)
])