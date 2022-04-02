"""R daattali/TimeVis-like charts for displaying chronological data.

See daattali/TimeVis: https://github.com/daattali/timevis

# NOTE: Consider automated (non-overlapping) text/event placement

- MATLAB Adjust Text: https://github.com/Phlya/adjustText
- D3 Labeler: https://github.com/tinker10/D3-Labeler
- Plotly has implementation for contour? https://github.com/plotly/plotly.js/issues/4674#issuecomment-603571483

"""

import numpy as np
import plotly.graph_objects as go

from .utils_data import DASHED_TIME_FORMAT_YEAR, GDP_TIME_FORMAT, format_unix, get_unix
from .utils_fig import CustomChart


class TimeVisChart(CustomChart):  # noqa: H601
    """Time Vis Chart: resource use timeline."""

    date_format = DASHED_TIME_FORMAT_YEAR
    """Date format for bar chart. Default is `DASHED_TIME_FORMAT_YEAR`."""

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

    _shapes = []
    """List of shapes for plotly layout."""

    def create_traces(self, df_raw):   # noqa: CCR001
        """Return traces for plotly chart.

        Args:
            df_raw: pandas dataframe with columns: `(category, label, start, end)`

        Returns:
            list: Dash chart traces

        """
        # Get all unique category names and create lookup for y positions
        self.categories = sorted(cat for cat in set(df_raw['category'].tolist()) if cat)
        y_pos_lookup = {cat: self.y_space * idx for idx, cat in enumerate(self.categories)}
        # Create the Time Vis traces
        traces = []
        self._shapes = []
        self._annotations = []
        for vis in df_raw.itertuples():
            if vis.category in y_pos_lookup:
                y_pos = y_pos_lookup[vis.category]
                if vis.end:
                    traces.append(self._create_time_vis_shape(vis, y_pos))
                    if vis.label:
                        traces.append(self._create_annotation(vis, y_pos))
                else:
                    traces.append(self._create_event(vis, y_pos))
            else:
                y_pos = 0
                traces.append(self._create_non_cat_shape(vis, y_pos))
        return traces

    def _create_hover_text(self, vis):
        """Return hover text for given trace.

        Args:
            vis: row tuple from df_raw with: `(category, label, start, end)`

        Returns:
            string: HTML-formatted hover text

        """
        new_format = f'%a, {GDP_TIME_FORMAT}'
        start_date = format_unix(get_unix(vis.start, self.date_format), new_format)
        if vis.end:
            end_date = format_unix(get_unix(vis.end, self.date_format), new_format)
            date_range = f'<b>Start</b>: {start_date}<br><b>End</b>: {end_date}'
        else:
            date_range = f'<b>Event</b>: {start_date}'
        return f'<b>{vis.category}</b><br>{vis.label}<br>{date_range}'

    def _create_non_cat_shape(self, vis, y_pos):
        """Create non-category time visualization (vertical across all categories).

        Note: background shape is set below a transparent trace so that hover works

        Args:
            vis: row tuple from df_raw with: `(category, label, start, end)`
            y_pos: top y-coordinate of vis

        Returns:
            trace: single Dash chart Scatter trace

        """
        bot_y = self.y_space * len(self.categories)
        self._shapes.append(
            go.layout.Shape(
                fillcolor=self.fillcolor,
                layer='below',
                line={'width': 0},
                opacity=0.4,
                type='rect',
                x0=vis.start,
                x1=vis.end,
                xref='x',
                y0=bot_y,
                y1=y_pos,
                yref='y',
            ),
        )
        return go.Scatter(
            fill='toself',
            opacity=0,
            hoverlabel=self.hover_label_settings,
            line={'width': 0},
            mode='lines',
            text=self._create_hover_text(vis),
            x=[vis.start, vis.end, vis.end, vis.start, vis.start],
            y=[y_pos, y_pos, bot_y, bot_y, y_pos],
        )

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
            hovertemplate=f'{self._create_hover_text(vis)}<extra></extra>',
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
            self._annotations.append({
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
        self._shapes.append(
            go.layout.Shape(
                layer='below',
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
            ),
        )
        return go.Scatter(
            hoverlabel=self.hover_label_settings,
            hovertemplate=f'{self._create_hover_text(vis)}<extra></extra>',
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
        # Add shapes and append new annotations
        layout['shapes'] = self._shapes
        layout['annotations'] += self._annotations
        return layout
