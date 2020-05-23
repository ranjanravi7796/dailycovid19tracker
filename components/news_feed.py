import gc
import json
import pycountry
import requests
import pandas as pd
import dash_bootstrap_components as dbc
import dash_html_components as html

#from final.cache import server_cache
#from final.config import config


#@server_cache.memoize(timeout=900)
def news_feed(country="India") -> dbc.ListGroup:
    """Displays newsfeed for a selected country
    :return list_group: A bootstramp ListGroup containing ListGroupItem returns
    news feeds.
    """
    API_KEY = '75b0dd25fe9045d29596ff8f19432b97'

    URL = "https://newsapi.org/v2/top-headlines?"

    countries_code = {}
    for ctry in pycountry.countries:
        countries_code[ctry.name] = ctry.alpha_2
    
    input_code = countries_code.get(country, 'Unknown code')
    if input_code != "Unknown code":
        mydata = {"q":"coronavirus","language":"en","country":input_code,'apiKey':API_KEY}
    else:
        mydata = {"q":"coronavirus","language":"en",'apiKey':API_KEY}

    response = requests.get(URL,params=mydata)

    if response.status_code == 200:
        json_data = response.json()
        if json_data.get('totalResults') > 0:
            tempdf = pd.DataFrame.from_records(json_data)
        else:
            mydata = {"q":"coronavirus","language":"en",'apiKey':API_KEY}
            response = requests.get(URL,params=mydata)
            json_data = response.json()
            tempdf = pd.DataFrame.from_records(json_data)
            
        total = json_data.get('totalResults')
        if total > 15:
            total = 15
        columns = ["title", "url", "source","published"]
        rowslist = []
        for item in range(total):
            title = tempdf['articles'][item].get('title')
            url = tempdf['articles'][item].get('url')
            source = tempdf['articles'][item].get('source').get('name')
            publish = tempdf['articles'][item].get('publishedAt')
            publish = publish.split('T')
            rowslist.append([title,url,source,publish[0]])

        df = pd.DataFrame(data=rowslist,columns=columns)

        max_rows = 15
        list_group = dbc.ListGroup(
            [
                dbc.ListGroupItem(
                    [
                        html.Div(
                            [
                                html.H6(
                                    f"{df.iloc[i]['title']}.",
                                    className="news-txt-headline",
                                ),
                                html.P(
                                    f"{df.iloc[i]['source']}"
                                    f"  {df.iloc[i]['published']}",
                                    className="news-txt-by-dt",
                                ),
                            ],
                            className="news-item-container",
                        )
                    ],
                    className="news-item",
                    href=df.iloc[i]["url"],
                    target="_blank",
                )
                for i in range(min(len(df), max_rows))
            ],
            flush=True,
        )

        del response, json_data, df, tempdf
        gc.collect()

    else:
        list_group = []

    return list_group