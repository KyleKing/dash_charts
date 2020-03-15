"""Scatter Data with Fitted Line."""

import numpy as np
import plotly.graph_objects as go
from icecream import ic
from scipy import optimize

from .utils_fig import CustomChart, check_raw_data

# TODO: Possible use random method from old line_chart example?
# count = 10
# self.df_demo = [
#     pd.DataFrame(data={
#         'x': [idx for idx in range(count)],
#         'y': sorted([random.expovariate(0.2) for _i in range(count)], reverse=True),
#         'labels': ['Index: {}'.format(idx) for idx in range(count)],
#     }),
# ]


class FittedChart(CustomChart):
    """Scatter and Fitted Line Chart."""

    label_data = 'Data'
    """Label for the scatter data. Default is 'Data'."""

    fit_eqs = []
    """List of fit equations."""

    min_scatter_for_fit = 0
    """List of fit equations."""

    suppress_fit_errors = False
    """If True, bury errors from scipy fit and will print message to console. Default is True."""

    annotations = []
    """FIXME: DOCUMENT"""

    def create_traces(self, df_raw, *, annotations=None):
        """Return traces for plotly chart.

        Args:
            df_raw: pandas dataframe with columns `name: str`, `x: float`, `y: float` and `label: str`
            annotations: list of tuples with values `(x, y, label)`. Default is None

        Returns:
            list: Dash chart traces

        """
        # # TODO: Implement annotations
        # if annotations is not None:
        #     y_range = [-100, 200]  # PLANNED: Use calculation
        #     self.create_annotations(annotations, y_range)

        # Verify data format
        check_raw_data(df_raw, ['name', 'x', 'y', 'label'])

        # Separate raw tidy dataframe into separate scatter plots
        scatter_data = []
        fit_data = []
        for name in set(df_raw['name']):
            df_name = df_raw[df_raw['name'] == name]
            scatter_data.append(go.Scatter(
                customdata=[name],
                mode='markers' if len(self.fit_eqs) else 'lines+markers',
                name=name,
                opacity=0.5,
                text=df_name['label'],
                x=df_name['x'],
                y=df_name['y'],
            ))

            if len(df_name['x']) > self.min_scatter_for_fit:
                for fit_name, fit_equation in self.fit_eqs:
                    fit_data += self.fit_data(name, df_name, fit_name, fit_equation)

        return scatter_data + fit_data

    def fit_data(self, name, df_name, fit_name, fit_equation):
        # FIXME: Document
        fitted_data = []
        try:
            popt, pcov = optimize.curve_fit(fit_equation, xdata=df_name['x'], ydata=df_name['y'], method='lm')
            min_x, max_x = np.min(df_name['x']), np.max(df_name['x'])
            range_x = max_x - min_x
            points_x = sorted([
                min_x - 0.05 * range_x,
                *np.divide(range(int(min_x * 10), int(max_x * 10)), 10),
                max_x + 0.05 * range_x,
            ])
            fitted_data = [go.Scatter(
                hoverinfo='skip',
                mode='lines+markers',
                name=f'{name}-{fit_name}',
                opacity=0.9,
                x=points_x,
                y=fit_equation(points_x, *popt),
            )]
        except (RuntimeError, ValueError) as err:  # pragma: no cover
            if self.suppress_fit_errors:
                ic(err, name)
            else:
                raise

        return fitted_data

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
        # FIXME: Add legend
        return layout
