"""Demonstrate realtime updates in Dash.

Based on: https://medium.com/analytics-vidhya/programming-with-databases-in-python-using-sqlite-4cecbef51ab9

Example Python/SQLite: https://www.dataquest.io/blog/python-pandas-databases/ &
    https://sebastianraschka.com/Articles/2014_sqlite_in_python_tutorial.html

PLANNED: https://plot.ly/python/big-data-analytics-with-pandas-and-sqlite/

"""

import multiprocessing
import time
from pathlib import Path

import dash_core_components as dcc
import dash_html_components as html
import numpy as np
import pandas as pd
from dash.exceptions import PreventUpdate
from dash_charts.scatter_line_charts import RollingChart
from dash_charts.utils_app import AppBase
from dash_charts.utils_callbacks import map_outputs
from dash_charts.utils_dash import SQLConnection, parse_dash_cli_args
from dash_charts.utils_fig import min_graph
from tqdm import tqdm


def use_flag_file(callback, *args, **kwargs):
    """Use a flag file to determine if the callback is to be run.

    Args:
        callback: path to SQLite file
        args: arguments to pass to callback
        kwargs: keyword arguments to pass to callback

    """
    # Use a file to indicate if the function is currently writing to the database
    flag_file = Path(__file__).parent / 'flag-tempfile.log'
    if flag_file.is_file():
        initial = int(flag_file.read_text())
        time.sleep(2)
        if flag_file.is_file() and int(flag_file.read_text()) > initial:
            return  # The thread is currently writing to the flag file

    # Otherwise, create the flag file and run the script
    flag_file.write_text('')
    try:
        callback(*args, flag_file=flag_file, **kwargs)
    finally:
        flag_file.unlink()


def simulate_db_population(db_file, points=1000, delay=0.1, flag_file=None):
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
            if flag_file is not None:
                flag_file.write_text(str(idx))
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

    def create_elements(self):
        """Initialize the charts, tables, and other Dash elements."""
        self.chart_main = RollingChart(
            title='Live-Updating Scatter Plot',
            xlabel='Index',
            ylabel='Value',
        )
        self.chart_main.count_rolling = 20

    def generate_data(self):
        """Start the realtime updates of the database. Function could be run from separate process."""
        db_file = self.db_file
        process = multiprocessing.Process(
            target=use_flag_file, args=[simulate_db_population, db_file], kwargs={'points': 1000, 'delay': 0.05},
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

        @self.callback(outputs, inputs, states, pic=True)
        def update_chart(*raw_args):
            with SQLConnection(self.db_file) as conn:
                df_events = pd.read_sql_query('SELECT id, label, value FROM EVENTS', conn)
            moving_window = 5
            count_points = len(df_events['id'])
            if count_points < moving_window:
                raise PreventUpdate

            for new_key, old_key in [('x', 'id'), ('y', 'value')]:
                df_events[new_key] = df_events[old_key]
            self.chart_main.axis_range = {
                'x': [float(np.max([0, count_points - 500])), count_points],
            }
            new_figure = self.chart_main.create_figure(df_raw=df_events)

            return map_outputs(outputs, [(self.id_chart, 'figure', new_figure)])


instance = RealTimeSQLDemo
if __name__ == '__main__':
    app = instance()
    app.create()
    app.run(**parse_dash_cli_args())
else:
    app = instance()
    app.create()
    FLASK_HANDLE = app.get_server()
