"""R daattali/TimeVis-like charts for displaying chronological data.

See daattali/TimeVis: https://github.com/daattali/timevis

# NOTE: Consider automated (non-overlapping) text/event placement

- MATLAB Adjust Text: https://github.com/Phlya/adjustText
- D3 Labeler: https://github.com/tinker10/D3-Labeler
- Plotly has implementation for contour? https://github.com/plotly/plotly.js/issues/4674#issuecomment-603571483

"""

import numpy as np
import plotly.graph_objects as go

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

    categories = None
    """List of string category names set in self.create_traces()."""

    shapes = []
    """List of shapes for plotly layout."""

    def create_traces(self, df_raw):
        """Return traces for plotly chart.

        Args:
            df_raw: pandas dataframe with columns: `(category, label, start, end)`

        Returns:
            list: Dash chart traces

        """
        # Get all unique category names and create lookup for y positions
        self.categories = sorted([*set(df_raw['category'].tolist())])
        y_pos_lookup = {cat: self.y_space * idx for idx, cat in enumerate(self.categories)}
        # Sort for the events to be first so that the vertical line is in the background
        df_raw = df_raw.sort_values(by=['end'], ascending=False)
        # Create the Time Vis traces
        traces = []
        self.shapes = []
        self.annotations = []
        for vis in df_raw.itertuples():
            y_pos = y_pos_lookup[vis.category]
            if vis.end:
                traces.append(self._create_time_vis_shape(vis, y_pos))
                if vis.label:
                    traces.append(self._create_annotation(vis, y_pos))
            else:
                traces.append(self._create_event(vis, y_pos))
        return traces

    def _create_hover_text(self, vis):
        """Return hover text for given trace.

        Args:
            vis: row tuple from df_raw with: `(category, label, start, end)`

        Returns:
            string: HTML-formatted hover text

        """
        new_format = '%a, %d%b%Y %H:%M:%S'
        start_date = format_unix(get_unix(vis.start, self.date_format), new_format)
        if vis.end:
            end_date = format_unix(get_unix(vis.end, self.date_format), new_format)
            date_range = f'<b>Start</b>: {start_date}<br><b>End</b>: {end_date}'
        else:
            date_range = f'<b>Event</b>: {start_date}'
        return f'<b>{vis.category}</b><br>{vis.label}<br>{date_range}'

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
        """Add vis label to chart as text overlay.

        Args:
            vis: row tuple from df_raw with: `(category, label, start, end)`
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

    def _create_event(self, vis, y_pos):
        """Create singular event with vertical line, marker, and text.

        If label is longer than 10 characters, then the annotation is shown offset with an arrow.

        Args:
            vis: row tuple from df_raw with: `(category, label, start, end)`
            y_pos: top y-coordinate of vis

        Returns:
            trace: single Dash chart Scatter trace

        """
        if len(vis.label) > 10:
            self.annotations.append({
                'align': 'right',
                'arrowcolor': self.fillcolor,
                'showarrow': True,
                'arrowhead': 2,
                'text': vis.label,
                'x': vis.start,
                'xanchor': 'right',
                'y': y_pos - self.rh / 2,
                'yanchor': 'middle',
            })
        self.shapes.append(go.layout.Shape(
            line={
                'color': self.fillcolor,
                'dash': 'longdashdot',
                'width': 2,
            },
            type='line',
            x0=vis.start,
            x1=vis.start,
            xref='x',
            y0=self.y_space * len(self.categories),
            y1=y_pos - self.rh / 2,
            yref='y',
        ))
        return go.Scatter(
            hoverlabel=self.hover_label_settings,
            hovertemplate=self._create_hover_text(vis) + '<extra></extra>',
            hovertext=self._create_hover_text(vis),
            marker={'color': self.fillcolor},
            mode='markers+text',
            text='' if len(vis.label) > 10 else vis.label,
            textposition='top center',
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
        layout['yaxis']['zeroline'] = False
        # Hide legend
        layout['legend'] = {}
        layout['showlegend'] = False
        # Add shapes
        layout['shapes'] = self.shapes
        return layout
