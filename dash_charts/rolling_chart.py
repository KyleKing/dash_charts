"""Rolling Mean and Filled Standard Deviation Chart."""

import bottleneck
import numpy as np
import plotly.graph_objects as go

from . import helpers


class RollingChart(helpers.CustomChart):
    """Rolling Mean and Filled Standard Deviation Chart.

    Example Use: Timeseries data

    """

    def createTraces(self, df, dataLbl='Data', rollingCount=5, stdCount=2, annotations=None):
        """Return traces for plotly chart.

        df -- Pandas dataframe with columns names: ['x', 'y', 'label']
        dataLbl --
        rollingCount -- count of items to use for rolling calculations. Default 5
        stdCount -- count of STD deviations to display. Default 2
        annotations -- list of tuples with values (x,y,label)

        """
        if annotations is not None:
            yRange = [-100, 200]  # FIXME: Use calculation
            self.createAnnotations(annotations, yRange)

        chartData = [
            go.Scatter(
                mode='markers',
                name=dataLbl,
                opacity=0.5,
                text=df['label'],
                x=df['x'],
                y=df['y'],
            ),
        ]
        # Only add the rolling calculations if there are a sufficient number of points
        if len(df['x']) >= rollingCount:
            rollingMean = bottleneck.move_mean(df['y'], rollingCount)
            rollingSTD = bottleneck.move_std(df['y'], rollingCount)
            chartData.extend([
                go.Scatter(
                    fill='toself',
                    hoverinfo='skip',
                    name='{}x STD Range'.format(stdCount),
                    opacity=0.5,
                    x=list(df['x']) + list(df['x'])[::-1],
                    y=list(np.add(rollingMean, np.multiply(stdCount, rollingSTD))) + list(
                        np.subtract(rollingMean, np.multiply(stdCount, rollingSTD)))[::-1],
                ),
                go.Scatter(
                    hoverinfo='skip',
                    mode='lines',
                    name='Rolling Mean',
                    opacity=0.9,
                    x=df['x'],
                    y=rollingMean,
                ),
            ])
        return chartData

    def createAnnotations(self, annotations, yRange):
        """Create the annotations. May be overriden when inherited to customize annotation styling and positioning.

        annotations -- list of tuples with values (x,y,label,color). Color may be None
        yRange -- FIXME: Document

        """
        self.annotations = [
            go.layout.Annotation(
                arrowcolor='black' if color is None else color,
                arrowhead=7,
                arrowsize=0.3,
                arrowwidth=1.5,
                ax=x, ay=y + np.amax([(yRange[1] - y) * 0.3, 10]),
                bgcolor='black' if color is None else color,
                bordercolor='black' if color is None else color,
                borderpad=2,
                borderwidth=1,
                font=dict(color='#ffffff'),
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

    def createLayout(self):
        """Override the default layout and add additional settings."""
        layout = super().createLayout()
        layout['annotations'] = self.annotations
        return layout
