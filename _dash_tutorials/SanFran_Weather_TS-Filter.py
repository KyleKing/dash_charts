"""Line Plot with Dropdown and Time Filter."""

import os

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash_charts.helpers import min_graph

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = (pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2016-weather-data-seattle.csv')
      .dropna())
df["Date"] = pd.to_datetime(df["Date"])
df["year"] = df["Date"].dt.year

if 'DYNO' in os.environ:
    app_name = os.environ['DASH_APP_NAME']
else:
    app_name = 'dash-lineplot'


app.layout = html.Div([html.Div([
    html.H1("Weather Records for Seattle")], style={'textAlign': "center"}),
    html.Div([
        dcc.Dropdown(
            id="selected-value", multi=True, value=["Mean_TemperatureC"],
            options=[
                {"label": "Maximum Temperature", "value": "Max_TemperatureC"},
                {"label": "Mean Temperature", "value": "Mean_TemperatureC"},
                {"label": "Minimum Temperature", "value": "Min_TemperatureC"},
            ],
        ),
    ],
    className="row",
    style={"display": "block", "width": "60%", "margin-left": "auto", "margin-right": "auto"}),
    html.Div([min_graph(id="my-graph")]),
    html.Div([
        dcc.RangeSlider(
            id="year-range", min=1948, max=2015, step=1, value=[1998, 2000],
            marks={
                "1948": str(1948), "1954": str(1954), "1966": str(1966), "1975": str(1975), "1983": str(1983),
                "1994": str(1994), "2000": str(2000), "2005": str(2005), "2010": str(2010), "2012": str(2012),
                "2015": str(2015),
            },
        ),
    ]),
], className="container")


@app.callback(
    Output('my-graph', 'figure'),
    [Input('selected-value', 'value'), Input('year-range', 'value')])
def update_figure(selected, year):
    """Update the plotted figure."""
    text = {"Max_TemperatureC": "Maximum Temperature", "Mean_TemperatureC": "Mean Temperature",
            "Min_TemperatureC": "Minimum Temperature"}
    data = df[(df["year"] >= year[0]) & (df["year"] <= year[1])]
    trace = []
    for type in selected:
        trace.append(go.Scatter(x=data["Date"], y=data[type], name=text[type], mode='lines',
                                marker={'size': 8, "opacity": 0.6, "line": {'width': 0.5}}, ))
    return {
        "data": trace,
        "layout": go.Layout(
            title="Temperature Variations Over Time", colorway=['#fdae61', '#abd9e9', '#2c7bb6'],
            yaxis={"title": "Temperature ( degree celsius )"}, xaxis={"title": "Date"},
        ),
    }


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
