"""Pareto chart.

dash ref: https://dash.plot.ly/
plotly ref: https://plot.ly/python/reference/

"""

from pathlib import Path

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

app = dash.Dash(__name__, assets_folder=str(Path.cwd() / 'pages/assets'))


def createPareto(df, ylabel='Measurement (units)', colors=('#62A4D1', '#C5676B')):
    """Return a 'figure' object for a 2-axis Pareto chart.

    df -- Pandas dataframe with keys (value, percent)
    ylabel -- optional yaxis label, defaults to "Measurement (units)"
    colors -- optional color scheme. 1st value is for the bar color. 2nd is for cum percentage

    """
    # Verify data format
    expecK = ['value', 'label']
    foundK = df.keys()
    assert all([_k in foundK for _k in expecK]), 'df must have keys {}'.format(expecK)

    # Sort and calculate percentage
    df = df.sort_values(by=['value'], ascending=False)
    df['cumPer'] = df['value'].divide(df['value'].sum()).cumsum().fillna(1)

    # Create chart dictionary
    return {
        'data': [
            go.Bar(
                marker={'color': colors[0]},
                name='Raw Value',
                x=df['label'],
                y=df['value'],
            ),
        ] + [
            go.Scatter(
                line={'color': colors[1], 'dash': 'solid'},
                mode='lines',
                name='Cumulative Percentage',
                x=df['label'],
                y=df['cumPer'],
                yaxis='y2',
            ),
        ],
        'layout': go.Layout(
            title=go.layout.Title(text='Demo Pareto Plot'),
            showlegend=False,
            # FYI: can either use dict() or {} syntax
            xaxis={
                'automargin': True,
                'showgrid': True,
            },
            yaxis=dict(
                showgrid=True,
                title=ylabel,
                zeroline=True,
            ),
            # See multiple axis: https://plot.ly/python/multiple-axes/
            yaxis2=dict(
                overlaying='y',
                range=[0, 1],
                side='right',
                tickfont=dict(color=colors[1]),
                tickformat='%',
                title='Cumulative Percentage',
                titlefont=dict(color=colors[1]),
            ),
            hovermode='closest',
        ),
    }


# Example dataframe with some example labels
dfDemo = pd.DataFrame(data={
    'value': [76, 131, None, 41, 42, 92],
    'label': [
        'Every Cloud Has a Silver Lining',  # or What Goes Up Must Come Down',
        'Back To the Drawing Board',  # and Mountain Out of a Molehill',
        'Lickety Split',
        'Mountain Out of a Molehill',
        'Everything But The Kitchen Sink',
        'Happy as a Clam',
    ],
})

app.layout = html.Div(
    className='app-content',
    children=[
        html.H4(children='Project'),
        html.Div([
            dcc.Graph(
                id='pareto-chart',
                figure=createPareto(dfDemo),
            ),
        ]),
    ],
)

if __name__ == '__main__':
    app.run_server(debug=True)
