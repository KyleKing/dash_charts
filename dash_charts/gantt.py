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

from .utils_fig import CustomChart


def get_unix(str_ts, date_format):

    return datetime.strptime(str_ts, date_format).timestamp()


class GanttChart(CustomChart):  # noqa: H601
    """Gantt Chart: event and resource timeline."""

    date_format = '%Y-%m-%d'
    """Date format for bar chart."""

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
        # Sort dataframe and create color lookup
        df_raw = (df_raw
                  .sort_values(by=['category', 'start'], ascending=False)
                  .sort_values(by=['end'], ascending=False)
                  .reset_index(drop=True))
        categories = set(df_raw['category'])
        colors = ('#D5D5D3', '#CEAB07')
        self.color_lookup = {cat: colors[idx] for idx, cat in enumerate(categories)}
        groups = []
        # Add all tasks as horizontal bars with progress overlay and text label
        for task in df_raw.itertuples():
            color = self.color_lookup[task.category]
            start = task.start if task.start else task.end
            # FIXME: make this two lines and format as XXMMMYYYY in GDP format
            date_range = (f'{task.start} to ' if task.start else '') + task.end
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
                x=[start, task.end, task.end, start, start],
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

        """
        start = task.start if task.start else task.end
        unix_start = get_unix(start, self.date_format)
        unix_progress = (get_unix(task.end, self.date_format) - unix_start) * task.progress + unix_start
        end = datetime.fromtimestamp(unix_progress).strftime(self.date_format)
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
            x=[start, end, end, start, start],
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
