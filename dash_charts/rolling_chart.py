"""Rolling Mean and Filled Standard Deviation Chart."""

import bottleneck
import numpy as np
import plotly.graph_objects as go

from .utils_fig import CustomChart, check_raw_data


class RollingChart(CustomChart):
    """Rolling Mean and Filled Standard Deviation Chart for monitoring trends."""

    count_std = 2
    """Count of STD deviations to display. Default 2."""

    count_rolling = 5
    """Count of items to use for rolling calculations. Default 5."""

    label_data = 'Data'
    """Label for the scatter data. Default is 'Data'."""

    annotations = []
    """ FIXME: DOCUMENT. """

    def create_traces(self, df_raw, *, annotations=None):
        """Return traces for plotly chart.

        Args:
            df_raw: pandas dataframe with columns `x: float`, `y: float` and `label: str`
            annotations: list of tuples with values `(x, y, label)`. Default is None

        Returns:
            list: Dash chart traces

        """
        # # TODO: Implement annotations
        # if annotations is not None:
        #     y_range = [-100, 200]  # PLANNED: Use calculation
        #     self.create_annotations(annotations, y_range)

        # Verify data format
        check_raw_data(df_raw, ['x', 'y', 'label'])

        # Create and return the traces
        chart_data = [
            go.Scatter(
                mode='markers',
                name=self.label_data,
                opacity=0.5,
                text=df_raw['label'],
                x=df_raw['x'],
                y=df_raw['y'],
            ),
        ]
        # Only add the rolling calculations if there are a sufficient number of points
        if len(df_raw['x']) >= self.count_rolling:
            rolling_mean = bottleneck.move_mean(df_raw['y'], self.count_rolling)
            rolling_std = bottleneck.move_std(df_raw['y'], self.count_rolling)
            chart_data.extend([
                go.Scatter(
                    fill='toself',
                    hoverinfo='skip',
                    name=f'{self.count_std}x STD Range',
                    opacity=0.5,
                    x=(df_raw['x'].tolist() + df_raw['x'].tolist()[::-1]),
                    y=(np.add(rolling_mean, np.multiply(2, rolling_std)).tolist()
                       + np.subtract(rolling_mean, np.multiply(2, rolling_std)).tolist()[::-1]),
                ),
                go.Scatter(
                    hoverinfo='skip',
                    mode='lines',
                    name='Rolling Mean',
                    opacity=0.9,
                    x=df_raw['x'],
                    y=rolling_mean,
                ),
            ])
        return chart_data

    def create_annotations(self, annotations, y_range):
        """Create the annotations. May be overridden when inherited to customize annotation styling and positioning.

        annotations -- list of tuples with values (x,y,label,color). Color may be None
        y_range -- PLANNED: Document

        """
        self.annotations = [
            go.layout.Annotation(
                arrowcolor='black' if color is None else color,
                arrowhead=7,
                arrowsize=0.3,
                arrowwidth=1.5,
                ax=x, ay=y + np.amax([(y_range[1] - y) * 0.3, 10]),
                bgcolor='black' if color is None else color,
                bordercolor='black' if color is None else color,
                borderpad=2,
                borderwidth=1,
                font={'color': '#ffffff'},
                # hoverlabel={bgcolor, bordercolor, font},
                hovertext=label,
                opacity=0.8,
                showarrow=True,
                text=str(idx + 1),
                x=x, y=y,
                xref='x', yref='y', axref='x', ayref='y',
            )
            for idx, (x, y, label, color) in enumerate(annotations)
        ]

    def create_layout(self):
        """Extend the standard layout.

        Returns:
            dict: layout for Dash figure

        """
        layout = super().create_layout()
        layout['annotations'] = self.annotations
        return layout
