import dash
import dash_bootstrap_components as dbc
from callbacks import register_callbacks
from layout.app_layout import build_layout



BS = "https://stackpath.bootstrapcdn.com/bootswatch/4.4.1/slate/bootstrap.min.css"
#initialize dash app
app = dash.Dash(__name__,external_stylesheets=[BS])

server = app.server

app.title = 'Covid-19 Tracker'

app.layout = build_layout

#initialize the callbacks
register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True)