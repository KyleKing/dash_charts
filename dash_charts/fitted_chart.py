"""Scatter Data with Fitted Line."""

import numpy as np
import plotly.graph_objects as go
from icecream import ic
from scipy import optimize

from .utils_fig import CustomChart, check_raw_data


def create_fit_traces(df_raw, name, fit_equation, suppress_fit_errors=False):
    """Create traces for specified equation.

    Args:
        df_raw: pandas dataframe with columns `name: str`, `x: float`, `y: float` and `label: str`
        name: unique name for trace
        fit_equation: equation used
        suppress_fit_errors: If True, bury errors from scipy fit. Default is False.

    Returns:
        list: of Scatter traces for fitted equation

    """
    fitted_data = []
    try:
        popt, pcov = optimize.curve_fit(fit_equation, xdata=df_raw['x'], ydata=df_raw['y'], method='lm')
        # Calculate representative x values for plotting fit
        x_min = np.min(df_raw['x'])
        x_max = np.max(df_raw['x'])
        x_range = x_max - x_min
        x_values = sorted([
            x_min - 0.05 * x_range,
            *np.divide(range(int(x_min * 10), int(x_max * 10)), 10),
            x_max + 0.05 * x_range,
        ])
        fitted_data = [go.Scatter(
            mode='lines+markers',
            name=name,
            opacity=0.9,
            text=f'popt:{[round(param, 3) for param in popt]}',
            x=x_values,
            y=fit_equation(x_values, *popt),
        )]
    except (RuntimeError, ValueError) as err:  # pragma: no cover
        if suppress_fit_errors:
            ic(err, name)
        else:
            raise

    return fitted_data  # noqa: R504


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

    def create_traces(self, df_raw):
        """Return traces for plotly chart.

        Args:
            df_raw: pandas dataframe with columns `name: str`, `x: float`, `y: float` and `label: str`

        Returns:
            list: Dash chart traces

        """
        # Verify data format
        check_raw_data(df_raw, ['name', 'x', 'y', 'label'])

        # Separate raw tidy dataframe into separate scatter plots
        scatter_data = []
        fit_traces = []
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
                    fit_traces.extend(
                        create_fit_traces(df_name, f'{name}-{fit_name}', fit_equation, self.suppress_fit_errors),
                    )

        return scatter_data + fit_traces
