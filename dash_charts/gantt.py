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

import plotly.graph_objects as go

from .dash_helpers import validate
from .utils_fig import CustomChart, check_raw_data


class GanttChart(CustomChart):  # noqa: H601
    """Gantt Chart: event and resource timeline."""

    axis_range = {'x': ('2015-01-01', '2015-06-20'), 'y': (-5, 5)}

    def add_annotations(self):
        """Calculate coordinate chart layout. Called by __init__, but can be called later to update the chart."""
        self.annotations.extend([
            {
                'showarrow': False,
                'text': 'Your text here',
                'align': 'right',
                'x': '2015-02-03',
                'xanchor': 'right',
                'y': 1,
                'yanchor': 'bottom',
            },
            {
                'showarrow': False,
                'text': 'Your second text here',
                'align': 'right',
                'x': '2015-05-03',
                'xanchor': 'right',
                'y': 5,
                'yanchor': 'bottom',
            },
        ])

    def create_traces(self, df_raw):
        """Return traces for plotly chart.

        Args:
            df_raw: pandas dataframe with at minimum the two columns `category: str` and `value: float`

        Returns:
            list: Dash chart traces

        Raises:
            RuntimeError: if the `df_raw` is missing any necessary columns

        """
        # # Check that the raw data frame is properly formatted
        # check_raw_data(df_raw, min_keys=['category', 'value'])
        # if not pd.api.types.is_string_dtype(df_raw['category']):  # pragma: no cover
        #     raise RuntimeError(f"category column must be string, but found {df_raw['category'].dtype}")

        # # Create and return the traces and optionally add the count to the bar chart
        # df_p = tidy_pareto_data(df_raw, self.cap_categories)
        # count_kwargs = {'text': df_p['counts'], 'textposition': 'auto'} if self.show_count else {}

        self.add_annotations()

        return [
            go.Scatter(
                x=['2015-02-01'],
                y=[-14],
                mode='lines',
            ),
        ]

    def create_layout(self):
        """Extend the standard layout.

        Returns:
            dict: layout for Dash figure

        """
        layout = super().create_layout()

        layout['shapes'] = [
            go.layout.Shape(
                type='rect',
                xref='x', yref='y',
                # x0=1, x1=3,
                # y0=1, y1=2,
                x0='2015-02-01', x1='2015-06-01',
                y0=-2, y1=2,
                line_width=0,  # line=dict(color='LightSkyBlue'),
                opacity=0.5,
                layer='below',
                fillcolor='LightSkyBlue',
            ),
        ]

        return layout
