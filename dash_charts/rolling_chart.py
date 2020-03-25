"""Rolling Mean and Filled Standard Deviation Chart."""

import bottleneck
import numpy as np
import plotly.graph_objects as go

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
    rolling_mean = bottleneck.move_mean(df_raw['y'], count_rolling)
    rolling_std = bottleneck.move_std(df_raw['y'], count_rolling)
    return [
        go.Scatter(
            fill='toself',
            hoverinfo='skip',
            name=f'{count_std}x STD Range',
            opacity=0.5,
            x=(df_raw['x'].tolist() + df_raw['x'].tolist()[::-1]),
            y=(np.add(rolling_mean, np.multiply(count_std, rolling_std)).tolist()
                + np.subtract(rolling_mean, np.multiply(count_std, rolling_std)).tolist()[::-1]),
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


class RollingChart(CustomChart):
    """Rolling Mean and Filled Standard Deviation Chart for monitoring trends."""

    count_std = 2
    """Count of STD deviations to display. Default 2."""

    count_rolling = 5
    """Count of items to use for rolling calculations. Default 5."""

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
