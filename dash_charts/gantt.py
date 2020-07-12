"""Gantt Chart.

- N/A: https://plotly.com/python/gantt/
- N/A: https://plotly.com/python/horizontal-bar-charts/#basic-horizontal-bar-chart

- Shapes: https://plotly.com/python/shapes/
- DT Axis: https://stackoverflow.com/a/51231209/3219667
- Hmm: https://stackoverflow.com/questions/58493254/how-to-add-more-than-one-shape-with-loop-in-plotly

Examples

- https://github.com/alampros/Gantt-Chart/blob/master/gantt-chart-d3.js
- http://guypursey.com/blog/201605302300-d3-timescale-visualisation
- https://shybovycha.github.io/2017/04/09/gantt-chart-with-d3.html
- https://github.com/dk8996/Gantt-Chart

# TODO: Gantt Tasks

- Fix hover text to shape
- Show full hover text information on hover (avoid cropping)
- Sort, then draw shapes accordingly. Determine the x/y range
- Show label on YAxis? (Hide numeric values)
- Add bolded headers with horizontal bar for all subtasks
- Add milestones with scatter point

# Other Ideas

- Consider adding dependencies (end date = start date) where vertical line could connect them?
- Consider relative dates
- Consider assigning resources with some sort of indicator
- If items are filtered from the view, compress the YAxis (see axis-breaks in px.scatter?)
- Potentially show slider chart underneath for adjustable time view (probably just use the default zoom)

"""

from datetime import datetime
import plotly.graph_objects as go
from icecream import ic

from .dash_helpers import validate
from .utils_fig import CustomChart, check_raw_data


def get_unix(str_ts, date_format):
    return datetime.strptime(str_ts, date_format).timestamp()


class GanttChart(CustomChart):  # noqa: H601
    """Gantt Chart: event and resource timeline."""

    # # See `wesanderson::wes_palette` for R, such as Darjeeling1

    def create_traces(self, df_raw):
        """Return traces for plotly chart.

        Args:
            df_raw: pandas dataframe with columns: `(category, label, start, end, progress)`

        Returns:
            list: Dash chart traces

        Raises:
            RuntimeError: if the `df_raw` is missing any necessary columns

        """
        events = []
        self.shapes = []
        self.annotations = []
        # FIXME: Replace start==None, with end value! Will fix sort and simplify some logic below
        df_raw = (df_raw
                  .sort_values(by=['category', 'start'], ascending=False)
                  .sort_values(by=['end'], ascending=False)
                  .reset_index(drop=True))
        dates = sorted(set(filter(None, df_raw['start'].to_list() + df_raw['end'].to_list())))
        self.axis_range = {'x': [dates[0], dates[-1]]}
        for event in df_raw.itertuples():
            start = event.start if event.start else event.end
            date_range = (f'{event.start}-' if event.start else '') + event.end
            y_pos = event.Index
            events.append(go.Scatter(
                # fillcolor=self.colors[event.category],
                # legendgroup=self.colors[event.category],
                # marker={'color': self.colors[event.category]},
                mode='lines',
                text=f'<b>{event.category}</b><br>{event.label} ({int(event.progress * 100)}%)<br>{date_range}',
                x=[start, event.end, event.end, start, start],
                y=[y_pos, y_pos, y_pos - 1, y_pos - 1, y_pos],
                showlegend=False,  # FIXME: On first use of the legend group, give name set this to True
            ))
            # Add progress overlay and task label
            if event.progress > 0:
                self._add_progress_shape(event, y_pos)
            self._add_annotation(event, y_pos)
        return events

    def _add_annotation(self, event, y_pos):
        self.annotations.append({
            'showarrow': False,
            'text': event.label,
            'align': 'right',
            'x': event.end,
            'xanchor': 'left',
            'y': y_pos - 0.5,
            'yanchor': 'middle',
        })

    def _add_progress_shape(self, event, y_pos):
        """Add white overlay to indicate task progress."""
        start = event.start if event.start else event.end
        unix_start = get_unix(start, self.date_format)
        unix_progress = (get_unix(event.end, self.date_format) - unix_start) * event.progress + unix_start
        self.shapes.append(go.layout.Shape(
            fillcolor='white',
            layer='above',
            line_width=0,
            opacity=0.5,
            type='rect',
            x0=start,
            x1=datetime.fromtimestamp(unix_progress).strftime(self.date_format),
            xref='x',
            y0=y_pos,
            y1=y_pos - 1,
            yref='y',
        ))

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
