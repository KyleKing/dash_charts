"""Charts for plotting scatter or fitted data."""

import numpy as np
import plotly.graph_objects as go
from scipy import optimize

from .utils_fig import CustomChart, check_raw_data


def create_rolling_traces(df_raw, count_rolling, count_std):
    """Calculate traces for rolling average and standard deviation.

    Args:
        df_raw: pandas dataframe with columns `x: float`, `y: float` and `label: str`
        count_rolling: number of points to use for the rolling calculation
        count_std: number of standard deviations to use for the standard deviation

    Returns:
        list: of Scatter traces for rolling mean and std

    """
    rolling_mean = df_raw['y'].rolling(count_rolling).mean().tolist()
    rolling_std = df_raw['y'].rolling(count_std).std().tolist()
    return [
        go.Scatter(
            fill='toself',
            hoverinfo='skip',
            name=f'{count_std}x STD Range',
            opacity=0.5,
            x=(df_raw['x'].tolist() + df_raw['x'].tolist()[::-1]),
            y=(
                np.add(rolling_mean, np.multiply(count_std, rolling_std)).tolist()
                + np.subtract(rolling_mean, np.multiply(count_std, rolling_std)).tolist()[::-1]
            ),
        ),
        go.Scatter(
            hoverinfo='skip',
            mode='lines',
            name='Rolling Mean',
            opacity=0.9,
            x=df_raw['x'],
            y=rolling_mean,
        ),
    ]


def create_fit_traces(df_raw, name, fit_equation, suppress_fit_errors=False):  # noqa: CCR001
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
        fitted_data = [
            go.Scatter(
                mode='lines+markers',
                name=name,
                opacity=0.9,
                text=f'popt:{[round(param, 3) for param in popt]}',
                x=x_values,
                y=fit_equation(x_values, *popt),
            ),
        ]
    except (RuntimeError, ValueError) as err:  # pragma: no cover
        if not suppress_fit_errors:
            raise

    return fitted_data  # noqa: R504


class RollingChart(CustomChart):
    """Rolling Mean and Filled Standard Deviation Chart for monitoring trends."""

    count_std = 5
    """Count of STD deviations to display. Default 5."""

    count_rolling = count_std
    """Count of items to use for rolling calculations. Default `count_std`."""

    label_data = 'Data'
    """Label for the scatter data. Default is 'Data'."""

    def create_traces(self, df_raw):
        """Return traces for plotly chart.

        Args:
            df_raw: pandas dataframe with columns `x: float`, `y: float` and `label: str`

        Returns:
            list: Dash chart traces

        """
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
            chart_data.extend(
                create_rolling_traces(df_raw, self.count_rolling, self.count_std),
            )

        return chart_data


class FittedChart(CustomChart):
    """Scatter Chart with optional Fitted Lines."""

    label_data = 'Data'
    """Label for the scatter data. Default is 'Data'."""

    fit_eqs = []
    """List of fit equations."""

    fallback_mode = 'lines+markers'
    """If not fit_eqs are specified, will fallback to `lines+markers`. Can be set to `markers`."""

    min_scatter_for_fit = 0
    """List of fit equations."""

    suppress_fit_errors = False
    """If True, bury errors from scipy fit and will print message to console. Default is True."""

    def create_traces(self, df_raw):   # noqa: CCR001
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
            scatter_data.append(
                go.Scatter(
                    customdata=[name],
                    mode='markers' if self.fit_eqs else self.fallback_mode,
                    name=name,
                    opacity=0.5,
                    text=df_name['label'],
                    x=df_name['x'],
                    y=df_name['y'],
                ),
            )

            if len(df_name['x']) > self.min_scatter_for_fit:
                for fit_name, fit_equation in self.fit_eqs:
                    fit_traces.extend(
                        create_fit_traces(df_name, f'{name}-{fit_name}', fit_equation, self.suppress_fit_errors),
                    )

        return scatter_data + fit_traces
