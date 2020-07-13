"""Gantt Chart.

# TODO:

- Refactor and cleanup documentation
- Fix hover on deployment
- Review below examples
- Fix color generation for multiple projects

# Inspiration

- https://github.com/alampros/Gantt-Chart/blob/master/gantt-chart-d3.js
- http://guypursey.com/blog/201605302300-d3-timescale-visualisation
- https://shybovycha.github.io/2017/04/09/gantt-chart-with-d3.html
- https://github.com/dk8996/Gantt-Chart

# Other Ideas

- Consider how to display task dependencies
- Consider adding dependencies (end date = start date) where vertical line could connect them?
- Consider relative dates
- -Consider assigning resources with some sort of indicator-

# Removed COde

```py
dates = sorted(set(filter(None, df_raw['start'].to_list() + df_raw['end'].to_list())))
self.axis_range = {'x': [dates[0], dates[-1]]}
```

"""

from datetime import datetime

import plotly.graph_objects as go
from icecream import ic
from palettable.tableau import TableauMedium_10

from .utils_fig import CustomChart


def get_unix(str_ts, date_format):
    """Get unix timestamp from a string timestamp in date_format.

    Args:
        str_ts: string timestamp in `date_format`
        date_format: datetime time stamp format

    Returns:
        int: unix timestamp

    """
    return datetime.strptime(str_ts, date_format).timestamp()


def format_unix(unix_ts, date_format):
    """Format unix timestamp as a string timestamp in date_format.

    Args:
        unix_ts: unix timestamp
        date_format: datetime time stamp format

    Returns:
        string: formatted timestamp in `date_format`

    """
    return datetime.fromtimestamp(unix_ts).strftime(date_format)


class GanttChart(CustomChart):  # noqa: H601
    """Gantt Chart: event and resource timeline."""

    date_format = '%Y-%m-%d'
    """Date format for bar chart."""

    pallette = TableauMedium_10.hex_colors
    """Default color pallette for project colors."""

    def create_traces(self, df_raw):
        """Return traces for plotly chart.

        Args:
            df_raw: pandas dataframe with columns: `(category, label, start, end, progress)`

        Returns:
            list: Dash chart traces

        """
        tasks = []
        self.shapes = []
        self.annotations = []
        # If start is None, assign end to start, ort dataframe, and create color lookup
        start_index = df_raw.columns.get_loc('start')
        end_index = df_raw.columns.get_loc('end')
        for index in [idx for idx, is_na in enumerate(df_raw['start'].isna()) if is_na]:
            # TODO: Why can't I assign all at once?
            #   Should be able to: `df_raw.iloc[df_raw['start'].isna(), start_index] = [...]`
            df_raw.iloc[index, start_index] = df_raw.iloc[index, end_index]
        df_raw = (df_raw
                  .sort_values(by=['category', 'start'], ascending=False)
                  .sort_values(by=['end'], ascending=False)
                  .reset_index(drop=True))
        ic(df_raw)
        categories = set(df_raw['category'])
        self.color_lookup = {cat: self.pallette[idx] for idx, cat in enumerate(categories)}
        groups = []
        # Add all tasks as horizontal bars with progress overlay and text label
        for task in df_raw.itertuples():
            color = self.color_lookup[task.category]
            dates = [format_unix(get_unix(str_ts, self.date_format), '%a, %d%b%Y') for str_ts in [task.start, task.end]]
            if task.start != task.end:
                date_range = f'<br><b>Start</b>: {dates[0]}<br><b>End</b>: {dates[1]}'
            else:
                date_range = f'<br><b>Milestone</b>: {dates[1]}'
            y_pos = task.Index
            is_first = task.category not in groups
            groups.append(task.category)
            scatter_kwargs = dict(
                fill='toself',
                fillcolor=color,
                hoverlabel={'bgcolor': 'white', 'font_size': 12, 'namelength': 0},
                legendgroup=color,
                line={'width': 1},
                marker={'color': color},
                mode='lines',
                showlegend=is_first,
                text=f'<b>{task.category}</b><br>{task.label} ({int(task.progress * 100)}%)<br>{date_range}',
                x=[task.start, task.end, task.end, task.start, task.start],
                y=[y_pos, y_pos, y_pos - 1, y_pos - 1, y_pos],
            )
            if is_first:
                scatter_kwargs['name'] = task.category
            tasks.append(go.Scatter(**scatter_kwargs))
            # Add progress overlay and task label
            if task.progress > 0:
                tasks.append(self._add_progress_shape(task, y_pos))
            tasks.append(self._add_annotation(task, y_pos))
        return tasks

    def _add_annotation(self, task, y_pos):
        """Add task progress to `self.annotations` at y_pos.

        Args:
            task: row tuple from df_raw with: `(category, label, start, end, progress)`
            y_pos: top y-coordinate of task

        Returns:
            trace: single Dash chart Scatter trace

        """
        return go.Scatter(
            hoverinfo='skip',
            legendgroup=self.color_lookup[task.category],
            mode='text',
            showlegend=False,
            text=task.label,
            textposition='middle left',
            x=[task.end],
            y=[y_pos - 0.5],
        )

    def _add_progress_shape(self, task, y_pos):
        """Add semi-transparent white overlay `self.shapes` to indicate task progress.

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
            line_width=0,
            line={'width': 1},
            marker={'color': 'white'},
            mode='lines',
            opacity=0.5,
            showlegend=False,
            x=[task.start, end, end, task.start, task.start],
            y=[y_pos, y_pos, y_pos - 1, y_pos - 1, y_pos],
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
        # Add shapes
        layout['shapes'] = self.shapes
        return layout
