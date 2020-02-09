# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import webbrowser
from threading import Timer
import subprocess
import time

port = 5000 # or simply open on the default `8050` port

def open_browser():
    webbrowser.open_new("http://localhost:{}".format(port))
    #time.sleep(5)
    subprocess.call(["xdotool", "key", "F11"])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == '__main__':
    Timer(3, open_browser).start()

    app.run_server(debug=True, port=port)
