from dash.dependencies import Input, Output
from components import news_feed,draw_cases_graph
import pandas as pd

#read datasets from john hopkins 
confirmed_global = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv")
recovered_global = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv")
deceased_global = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv")

confirmed_global['Country/Region'].replace(to_replace='US',value='United States of America',inplace=True)
recovered_global['Country/Region'].replace(to_replace='US',value='United States of America',inplace=True)
deceased_global['Country/Region'].replace(to_replace='US',value='United States of America',inplace=True)

cols = confirmed_global.columns
confirmed_dates = confirmed_global.loc[:,cols[4]:cols[-1]]
recovered_dates = recovered_global.loc[:,cols[4]:cols[-1]]
deceased_dates = deceased_global.loc[:,cols[4]:cols[-1]]
dates = confirmed_dates.columns

def get_countries():
    countries_list = list(confirmed_global['Country/Region'].unique())
    return countries_list

def onLoad_country_options():
    '''load country options in the dropdown'''

    country_options = (
        [{'label': country, 'value': country}
         for country in get_countries()]
    )
    return country_options

def daily_increase(data):
    daily = []
    for i in range(len(data)):
        if i == 0:
            daily.append(data[i])
        else:
            daily.append(data[i]-data[i-1])   
    return daily

def confirmedcases_countries(countryName):
    if countryName is not None:
        temp = list(confirmed_dates[confirmed_global['Country/Region']==countryName].iloc[0, :])
        final = daily_increase(temp)
        return final

def recoveredcases_countries(countryName):
    if countryName is not None:
        temp = list(recovered_dates[recovered_global['Country/Region']==countryName].iloc[0, :])
        final = daily_increase(temp)
        return final

def deceasedcases_countries(countryName):
    if countryName is not None:
        temp = list(deceased_dates[deceased_global['Country/Region']==countryName].iloc[0, :])
        final = daily_increase(temp)
        return final


def get_countrycases(countryName):
    confirm_increase = confirmedcases_countries(countryName)
    recover_increase = recoveredcases_countries(countryName)
    deceased_increase = deceasedcases_countries(countryName)

    return confirm_increase,recover_increase,deceased_increase



def register_callbacks(app):

    @app.callback([
            Output(component_id='confirmed',component_property='children'),
            Output(component_id='recovered',component_property='children'),
            Output(component_id='deceased',component_property='children'),
            Output(component_id='mortality',component_property='children'),
            Output(component_id='recovery',component_property='children')

            ],
        [
            Input(component_id='country-selector',component_property='value')
        ]
    )

    def get_list(country_name):
        con_temp = confirmed_global[confirmed_global['Country/Region']==country_name]
        con_value = int(con_temp[con_temp.columns[-1]].sum())
        rec_temp = recovered_global[recovered_global['Country/Region']==country_name]
        rec_value = int(rec_temp[rec_temp.columns[-1]].sum())
        dec_temp = deceased_global[deceased_global['Country/Region']==country_name]
        dec_value = int(dec_temp[dec_temp.columns[-1]].sum())

        mortality_rate = round((dec_value / con_value) * 100,2)
        mortality_rate = str(mortality_rate) + " %"
        recovery_rate = round((rec_value / con_value) * 100,2)
        recovery_rate = str(recovery_rate) + " %"
        return con_value,rec_value,dec_value,mortality_rate,recovery_rate


    @app.callback(
        Output(component_id='cases-graph', component_property='figure'),
        [
            Input(component_id='country-selector',component_property='value')
        ]
    )

    def load_cases_graph(countryName):
        confirm_increase,recover_increase,deceased_increase = get_countrycases(countryName)

        if confirm_increase is not None:
            figure = []
            figure = draw_cases_graph(confirm_increase,recover_increase,deceased_increase,dates)
            return figure


    @app.callback(
            Output("feed-content", "children"),
            [
                Input(component_id="left-tabs-styled-with-inline",component_property="value"),
                Input(component_id='country-selector',component_property='value')
            ],
        )

    def feed_tab_content(tab_value, country):
        """Callback for newsfeed
        """
        print(country)
        if tab_value == "twitter-tab":
            return twitter_feed(country)

        return news_feed(country)
        
