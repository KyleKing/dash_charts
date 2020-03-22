"""Demonstrate realtime updates in Dash.

Based on: https://medium.com/analytics-vidhya/programming-with-databases-in-python-using-sqlite-4cecbef51ab9

Example Python/SQLite: https://www.dataquest.io/blog/python-pandas-databases/ &
    https://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html

PLANNED: https://plot.ly/python/big-data-analytics-with-pandas-and-sqlite/

"""

import multiprocessing
import time
from pathlib import Path

import bottleneck
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
from dash_charts.dash_helpers import SQLConnection, parse_cli_port
from dash_charts.utils_app import AppBase
from dash_charts.utils_callbacks import map_outputs
from dash_charts.utils_fig import min_graph
from icecream import ic
from tqdm import tqdm

# from dash_charts.rolling_chart import RollingChart


def simulate_db_population(db_file, points=1000, delay=0.1):
    """Populate a SQL database in real time so that the changes can be visualized in a chart.

    Args:
        db_file: path to SQLite file
        points: total number of points to create. Default is 1000
        delay: time to wait between creating each new data point (in seconds). Default is 0.1seconds

    """
    # Clear database if it exists
    if db_file.is_file():
        db_file.unlink()

    with SQLConnection(db_file) as conn:
        # Create EVENTS table
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE EVENTS (
            id   INT   PRIMARY KEY   NOT NULL,
            label   TEXT   NOT NULL,
            value   INT   NOT NULL
        );""")
        conn.commit()

        # Generate random data points
        mu, sigma = (10, 8)  # mean and standard deviation
        samples = np.random.normal(mu, sigma, points)

        # Fill the database with sample data
        for idx in tqdm(range(points)):
            value = (-1 if idx > 500 else 1) * idx / 10.0  # Introduce variability
            cursor.execute('INSERT INTO EVENTS (id, label, value) VALUES'  # noqa: S608
                           f' ({idx}, "idx-{idx}", {samples[idx] + value})')
            conn.commit()
            time.sleep(delay)


class RealTimeSQLDemo(AppBase):
    """Example creating a rolling mean chart."""

    name = 'Example Scatter of Real Time SQL Data'
    """Application name"""

    db_file = Path(__file__).parent / 'realtime-sql-data.sqlite'
    """Path to the SQLite database file."""

    chart_main = None
    """Main chart (Scatter)."""

    id_chart = 'real-time-chart'
    """Unique name for the main chart."""

    id_interval = 'graph-update'
    """ID of the interval element to regularly update the UI."""

    def initialization(self):
        """Initialize ids with `self.register_uniq_ids([...])` and other one-time actions."""
        super().initialization()
        self.register_uniq_ids([self.id_chart, self.id_interval])

        self._generate_data()

    def create_elements(self):
        """Initialize the charts, tables, and other Dash elements."""
        # self.chart_main = RollingChart(
        #     title='Sample Timeseries Chart with Rolling Calculations',
        #     xlabel='Index',
        #     ylabel='Measured Value',
        # )
        pass  # FIXME: Implement

    def _generate_data(self):
        """Start the realtime updates of the database. Function could be run from separate process."""
        ic(self.db_file)
        db_file = self.db_file
        process = multiprocessing.Process(
            target=simulate_db_population, args=[db_file], kwargs={'points': 400, 'delay': 0.1},
        )
        process.start()

    def return_layout(self):
        """Return Dash application layout.

        Returns:
            dict: Dash HTML object

        """
        return html.Div(
            style={
                'maxWidth': '1000px',
                'marginRight': 'auto',
                'marginLeft': 'auto',
            },
            children=[
                html.H4(children=self.name),
                min_graph(id=self.ids[self.id_chart], animate=True),
                dcc.Interval(id=self.ids[self.id_interval], interval=1000, n_intervals=0),
            ],
        )

    def create_callbacks(self):
        """Create Dash callbacks."""
        outputs = [(self.id_chart, 'figure')]
        inputs = [(self.id_interval, 'n_intervals')]
        states = []

        @self.callback(outputs, inputs, states)
        def update_chart(*raw_args):
            with SQLConnection(self.db_file) as conn:
                df_events = pd.read_sql_query('SELECT id, label, value FROM EVENTS', conn)
            moving_window = 5
            count_points = len(df_events['id'])
            if count_points < moving_window:
                raise PreventUpdate

            # Demo fitting wth a polynomial (not that useful)
            fit = np.poly1d(np.polyfit(df_events['id'], df_events['value'], moving_window))
            # Demo using a moving mean/std
            rolling_mean = bottleneck.move_mean(df_events['value'], moving_window)
            rolling_std = bottleneck.move_std(df_events['value'], moving_window)
            new_figure = {
                'data': [
                    go.Scatter(
                        mode='markers',
                        name='scatter',
                        text=df_events['label'],
                        x=df_events['id'],
                        y=df_events['value'],
                        opacity=0.3,
                    ),
                    go.Scatter(
                        name='2x STD',
                        fill='toself',
                        x=df_events['id'].tolist() + df_events['id'].tolist()[::-1],
                        y=(np.add(rolling_mean, np.multiply(2, rolling_std)).tolist()
                           + np.subtract(rolling_mean, np.multiply(2, rolling_std)).tolist()[::-1]),
                        opacity=0.5,
                    ),
                    go.Scatter(
                        mode='lines',
                        name='fit',
                        x=df_events['id'],
                        y=fit(df_events['id']),
                        opacity=0.7,
                    ),
                    go.Scatter(
                        mode='lines',
                        name='move_mean',
                        x=df_events['id'],
                        y=rolling_mean,
                        opacity=0.9,
                    ),
                ],
                'layout': go.Layout(
                    title=go.layout.Title(text='Live-Updating Plot'),
                    xaxis={
                        'automargin': True,
                        'range': [0, count_points],
                        'showgrid': True,
                        'title': 'Index',
                    },
                    yaxis={
                        'automargin': True,
                        'zeroline': True,
                        'autorange': True,
                        'showgrid': True,
                        'title': 'value',
                    },
                    legend={'orientation': 'h'},
                    hovermode='closest',
                ),
            }

            # new_figure = self.chart_main.create_figure(df_raw=df_events, show_count=True)
            return map_outputs(outputs, [(self.id_chart, 'figure', new_figure)])


instance = RealTimeSQLDemo
if __name__ == '__main__':
    port = parse_cli_port()
    app = instance()
    app.create()
    app.run(port=port, debug=False)  # TODO: Pass as CLI arguments
else:
    app = instance()
    app.create()
    FLASK_HANDLE = app.get_server()
