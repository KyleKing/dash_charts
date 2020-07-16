"""R daattali/TimeVis-like charts for displaying chronological data.

See daattali/TimeVis: https://github.com/daattali/timevis

"""

# TODO: Consider automated (non-overlapping) text/event placement...
# https://github.com/Phlya/adjustText
# https://github.com/tinker10/D3-Labeler
# Plotly Contour? https://github.com/plotly/plotly.js/issues/4674#issuecomment-603571483

import numpy as np
import plotly.graph_objects as go
from icecream import ic

from .dash_helpers import format_unix, get_unix
from .utils_fig import CustomChart


class TimeVisChart(CustomChart):  # noqa: H601
    """Time Vis Chart: resource use timeline."""

    date_format = '%Y-%m-%d %H:%M:%S'
    """Date format for bar chart."""

    fillcolor = '#D5DDF6'
    """Default fillcolor for time vis events."""

    hover_label_settings = {'bgcolor': 'white', 'font_size': 12, 'namelength': 0}
    """Plotly hover label settings."""

    rh = 1
    """Height of each rectangular time vis."""

    y_space = -1.5 * rh
    """Vertical spacing between rectangles."""

    def create_traces(self, df_raw):
        """Return traces for plotly chart.

        Args:
            df_raw: pandas dataframe with columns: `(category, label, start, end)`

        Returns:
            list: Dash chart traces

        """
        self.categories = sorted([*set(df_raw['category'].tolist())])
        y_pos_lookup = {cat: self.y_space * idx for idx, cat in enumerate(self.categories)}
        # Create the Time Vis traces
        traces = []
        for vis in df_raw.itertuples():
            y_pos = y_pos_lookup[vis.category]
            traces.append(self._create_time_vis_shape(vis, y_pos))
            if vis.label:
                traces.append(self._create_annotation(vis, y_pos))
        return traces

    def _create_hover_text(self, vis):
        """Return hover text for given trace.

        Args:
            vis: row tuple from df_raw with: `(category, label, start, end)`

        Returns:
            string: HTML-formatted hover text

        """
        dates = [format_unix(get_unix(str_ts, self.date_format), '%a, %d%b%Y %H:%M') for str_ts in [vis.start, vis.end]]
        return f'<b>{vis.category}</b><br>{vis.label}<br><b>Start</b>: {dates[0]}<br><b>End</b>: {dates[1]}'

    def _create_time_vis_shape(self, vis, y_pos):
        """Create filled rectangle for time visualization.

        Args:
            vis: row tuple from df_raw with: `(category, label, start, end)`
            y_pos: top y-coordinate of vis

        Returns:
            trace: single Dash chart Scatter trace

        """
        return go.Scatter(
            fill='toself',
            fillcolor=self.fillcolor,
            hoverlabel=self.hover_label_settings,
            line={'width': 0},
            mode='lines',
            text=self._create_hover_text(vis),
            x=[vis.start, vis.end, vis.end, vis.start, vis.start],
            y=[y_pos, y_pos, y_pos - self.rh, y_pos - self.rh, y_pos],
        )

    def _create_annotation(self, vis, y_pos):
        """Create vis progress to `self.annotations` at y_pos.

        Args:
            vis: row tuple from df_raw with: `(category, label, start, end, progress)`
            y_pos: top y-coordinate of vis

        Returns:
            trace: single Dash chart Scatter trace

        """
        return go.Scatter(
            hoverlabel=self.hover_label_settings,
            hovertemplate=self._create_hover_text(vis) + '<extra></extra>',
            hovertext=self._create_hover_text(vis),
            mode='text',
            text=vis.label,
            textposition='middle right',
            x=[vis.start],
            y=[y_pos - self.rh / 2],
        )

    def create_layout(self):
        """Extend the standard layout.

        Returns:
            dict: layout for Dash figure

        """
        layout = super().create_layout()
        # Set YAxis tick marks for category names (https://plotly.com/python/tick-formatting)
        layout['yaxis']['tickmode'] = 'array'
        layout['yaxis']['tickvals'] = np.subtract(
            np.multiply(
                np.array(range(len(self.categories))),
                self.y_space,
            ),
            self.rh / 2,
        )
        layout['yaxis']['ticktext'] = [*self.categories]
        # layout['yaxis']['showgrid'] = False
        layout['yaxis']['zeroline'] = False
        # Hide legend
        layout['legend'] = {}
        layout['showlegend'] = False
        return layout
