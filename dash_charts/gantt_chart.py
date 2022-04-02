"""Gantt Chart.

Note: does not support resources nor task dependencies; however those could be added by extending this base class.

# Removed Code

```py
# Just snippets of Python code that may be useful in the future
dates = sorted(set(filter(None, df_raw['start'].to_list() + df_raw['end'].to_list())))
self.axis_range = {'x': [dates[0], dates[-1]]}
```

"""

import plotly.graph_objects as go
from palettable.tableau import TableauMedium_10

from .utils_data import format_unix, get_unix
from .utils_fig import CustomChart


class GanttChart(CustomChart):  # noqa: H601
    """Gantt Chart: task and milestone timeline."""

    date_format = '%Y-%m-%d'
    """Date format for bar chart."""

    pallette = TableauMedium_10.hex_colors
    """Default color pallette for project colors."""

    hover_label_settings = {'bgcolor': 'white', 'font_size': 12, 'namelength': 0}
    """Plotly hover label settings."""

    rh = 1
    """Height of each rectangular task."""

    def create_traces(self, df_raw):
        """Return traces for plotly chart.

        Args:
            df_raw: pandas dataframe with columns: `(category, label, start, end, progress)`

        Returns:
            list: Dash chart traces

        """
        # If start is None, assign end to start so that the sort is correct
        start_index = df_raw.columns.get_loc('start')
        end_index = df_raw.columns.get_loc('end')
        for index in [idx for idx, is_na in enumerate(df_raw['start'].isna()) if is_na]:
            df_raw.iloc[index, start_index] = df_raw.iloc[index, end_index]
        df_raw['progress'] = df_raw['progress'].fillna(0)  # Fill possibly missing progress values for milestones
        df_raw = (
            df_raw
            .sort_values(by=['category', 'start'], ascending=False)
            .sort_values(by=['end'], ascending=False)
            .reset_index(drop=True)
        )
        # Create color lookup using categories in sorted order
        categories = set(df_raw['category'])
        self.color_lookup = {cat: self.pallette[idx] for idx, cat in enumerate(categories)}
        # Track which categories have been plotted
        plotted_categories = []
        # Create the Gantt traces
        traces = []
        for task in df_raw.itertuples():
            y_pos = task.Index
            is_first = task.category not in plotted_categories
            plotted_categories.append(task.category)
            traces.append(self._create_task_shape(task, y_pos, is_first))
            if task.progress > 0:
                traces.append(self._create_progress_shape(task, y_pos))
            traces.append(self._create_annotation(task, y_pos))
        return traces

    def _create_hover_text(self, task):
        """Return hover text for given trace.

        Args:
            task: row tuple from df_raw with: `(category, label, start, end, progress)`

        Returns:
            string: HTML-formatted hover text

        """
        dates = [format_unix(get_unix(str_ts, self.date_format), '%a, %d%b%Y') for str_ts in [task.start, task.end]]
        if task.start != task.end:
            date_range = f'<br><b>Start</b>: {dates[0]}<br><b>End</b>: {dates[1]}'
        else:
            date_range = f'<br><b>Milestone</b>: {dates[1]}'
        return f'<b>{task.category}</b><br>{task.label} ({int(task.progress * 100)}%)<br>{date_range}'

    def _create_task_shape(self, task, y_pos, is_first):
        """Create colored task scatter rectangle.

        Args:
            task: row tuple from df_raw with: `(category, label, start, end, progress)`
            y_pos: top y-coordinate of task
            is_first: if True, this is the first time a task of this category will be plotted

        Returns:
            trace: single Dash chart Scatter trace

        """
        color = self.color_lookup[task.category]
        scatter_kwargs = {
            'fill': 'toself',
            'fillcolor': color,
            'hoverlabel': self.hover_label_settings,
            'legendgroup': color,
            'line': {'width': 1},
            'marker': {'color': color},
            'mode': 'lines',
            'showlegend': is_first,
            'text': self._create_hover_text(task),
            'x': [task.start, task.end, task.end, task.start, task.start],
            'y': [y_pos, y_pos, y_pos - self.rh, y_pos - self.rh, y_pos],
        }
        if is_first:
            scatter_kwargs['name'] = task.category
        return go.Scatter(**scatter_kwargs)

    def _create_progress_shape(self, task, y_pos):
        """Create semi-transparent white overlay `self.shapes` to indicate task progress.

        Args:
            task: row tuple from df_raw with: `(category, label, start, end, progress)`
            y_pos: top y-coordinate of task

        Returns:
            trace: single Dash chart Scatter trace

        """
        unix_start = get_unix(task.start, self.date_format)
        unix_progress = (get_unix(task.end, self.date_format) - unix_start) * task.progress + unix_start
        end = format_unix(unix_progress, self.date_format)
        return go.Scatter(
            fill='toself',
            fillcolor='white',
            hoverinfo='skip',
            legendgroup=self.color_lookup[task.category],
            line={'width': 1},
            marker={'color': 'white'},
            mode='lines',
            opacity=0.5,
            showlegend=False,
            x=[task.start, end, end, task.start, task.start],
            y=[y_pos, y_pos, y_pos - self.rh, y_pos - self.rh, y_pos],
        )

    def _create_annotation(self, task, y_pos):
        """Add task label to chart as text overlay.

        Args:
            task: row tuple from df_raw with: `(category, label, start, end, progress)`
            y_pos: top y-coordinate of task

        Returns:
            trace: single Dash chart Scatter trace

        """
        # For milestones with narrow fill, hover can be tricky, so intended to make the whole length of the text
        #   hoverable, but only the x/y point appears to be hoverable although it makes a larger hover zone at least
        return go.Scatter(
            hoverlabel=self.hover_label_settings,
            hovertemplate=f'{self._create_hover_text(task)}<extra></extra>',
            hovertext=self._create_hover_text(task),
            legendgroup=self.color_lookup[task.category],
            mode='text',
            showlegend=False,
            text=task.label,
            textposition='middle left',
            x=[task.end],
            y=[y_pos - self.rh / 2],
        )

    def create_layout(self):
        """Extend the standard layout.

        Returns:
            dict: layout for Dash figure

        """
        layout = super().create_layout()
        # Suppress Y axis ticks/grid
        layout['yaxis']['showgrid'] = False
        layout['yaxis']['showticklabels'] = False
        layout['yaxis']['zeroline'] = False
        return layout
