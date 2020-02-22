"""Alignment chart."""
import math

import numpy as np
import plotly.graph_objects as go

from .utils_fig import MarginalChart


class AlignChart(MarginalChart):
    """Alignment/Distortion/Positioning Error Chart.

    Example Use: analyze inspection data for trends in misalignment, such as in molded parts

    """

    def __init__(self, title='', xlabel='', ylabel='', layout_overrides=(), meas_lbl='Meas', ideal_lbl='Ideal',
                 pad=0):
        """Initialize chart parameters.

        title -- optional, string title for chart. Defaults to blank
        xlabel/ylabel -- optional, X and Y Axis axis titles. Defaults to blank
        layout_overrides -- Custom parameters in format (ParentKey, SubKey, and Value) to customize 'go.layout'
        meas_lbl/ideal_lbl -- optional, legend names for the respective values
        pad -- optional, internal padding within the chart. Defaults to 0

        """
        super().__init__(title, xlabel, ylabel, layout_overrides)
        # Store the additional kwargs as data members
        self.meas_lbl = meas_lbl
        self.ideal_lbl = ideal_lbl
        self.pad = pad

    def listify_data(self, df, stretch):
        """Convert the dataframe into a list for plotting.

        df -- Pandas dataframe with columns names: ['x', 'y', 'x_delta', 'y_delta', 'label']
        stretch -- optional, float value to change the spacing between ideal and measured coordinates

        """
        meas_labels = []
        data = {
            'x': {self.ideal_lbl: [], self.meas_lbl: []},
            'y': {self.ideal_lbl: [], self.meas_lbl: []},
        }
        for row in df.itertuples():
            meas_labels.append(row.label)
            data['x'][self.ideal_lbl].append(row.x)
            data['y'][self.ideal_lbl].append(row.y)
            data['x'][self.meas_lbl].append(row.x + stretch * row.x_delta)
            data['y'][self.meas_lbl].append(row.y + stretch * row.y_delta)

        # Calculate the chart range
        self.range = {}
        for axis in ['x', 'y']:
            vals = data[axis][self.ideal_lbl] + data[axis][self.meas_lbl]
            self.range[axis] = math.floor(min(vals) - self.pad), math.ceil(max(vals) + self.pad)
        return (meas_labels, data)

    def create_traces(self, df, stretch=1):
        """Return traces for plotly chart.

        df -- Pandas dataframe with columns names: ['x', 'y', 'x_delta', 'y_delta', 'label']
        stretch -- optional, float value to change the spacing between ideal and measured coordinates

        ```python
        # Example dataframe
        df = pd.DataFrame(data={
            'x': [1, 2, 1, 2],
            'y': [1, 2, 2, 1],
            'x_delta': [0.01, 0.02, 0.005, -0.04],
            'y_delta': [0.01, -0.05, 0.005, 0.005],
            'label': ['A', 'B', 'C', 'D'],
        })
        ```

        """
        # PLANNED: Handle multiple data sets/missing points? - use greyscale for ideal?

        meas_labels, data = self.listify_data(df, stretch)
        # Plot the ideal and measured scatter points
        chart_data = [
            go.Scatter(
                legendgroup='Points',
                mode='markers',
                name=lbl,
                opacity=1 if lbl == self.meas_lbl else 0.2,
                text=meas_labels if lbl == self.meas_lbl else lbl,
                x=data['x'][lbl],
                y=data['y'][lbl],
            ) for lbl in [self.ideal_lbl, self.meas_lbl]
        ]
        # Plot a semi-transparent connecting line between related points
        chart_data.extend([
            go.Scatter(
                line={'color': '#D93D40', 'dash': 'solid'},
                mode='lines',
                opacity=0.15,
                showlegend=False,
                x=[data['x'][self.ideal_lbl][idx], data['x'][self.meas_lbl][idx]],
                y=[data['y'][self.ideal_lbl][idx], data['y'][self.meas_lbl][idx]],
            ) for idx in range(len(meas_labels))
        ])
        return chart_data

    def create_marg_top(self, df, stretch=1):
        """Return traces for the top marginal chart.

        df -- Pandas dataframe with columns names: ['x', 'y', 'x_delta', 'y_delta', 'label']
        stretch -- optional, float value to change the spacing between ideal and measured coordinates

        """
        return [
            go.Box(
                marker_color='royalblue',
                name=str(x_val),
                showlegend=False,
                x=df['x'][df['x'] == x_val] + df['x_delta'][df['x'] == x_val] * stretch,
            )
            for x_val in np.sort(df['x'].unique())
        ]

    def create_marg_right(self, df, stretch=1):
        """Return traces for the right marginal chart.

        df -- Pandas dataframe with columns names: ['x', 'y', 'x_delta', 'y_delta', 'label']
        stretch -- optional, float value to change the spacing between ideal and measured coordinates

        """
        df['yNew'] = df['y'] + df['y_delta'] * stretch
        return [
            go.Box(
                marker_color='royalblue',
                name=str(y_val),
                showlegend=False,
                x=[idx] * len(df['y'] == y_val),
                y=df['yNew'][df['y'] == y_val],
            )
            for idx, y_val in enumerate(np.sort(df['y'].unique()))
        ]

    def create_layout(self):
        """Override the default layout and add additional settings."""
        layout = super().create_layout()
        for axis in ['yaxis', 'xaxis']:
            layout[axis]['zeroline'] = False
        layout['yaxis']['scaleanchor'] = 'x'
        layout['yaxis']['scaleratio'] = 1
        layout['legend'] = {}  # Reset legend to default position on top right
        return layout
