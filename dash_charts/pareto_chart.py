"""Pareto Chart."""

import pandas as pd
import plotly.graph_objects as go

from .utils_data import append_df, validate
from .utils_fig import CustomChart, check_raw_data


def tidy_pareto_data(df_raw, cap_categories):
    """Return compressed Pareto dataframe of only the unique values.

    Args:
        df_raw: pandas dataframe with at minimum the two columns `category: str` and `value: float`
        cap_categories: Maximum number of categories (bars)

    Returns:
        dataframe: pandas dataframe with columns `(value, label, counts, cum_per)`

    """
    df_p = None
    for cat in df_raw['category'].unique():
        df_row = pd.DataFrame(
            data={
                'label': [cat],
                'value': [df_raw.loc[df_raw['category'] == cat]['value'].sum()],
                'counts': df_raw['category'].value_counts()[cat],
            },
        )
        df_p = append_df(df_p, df_row)
    # Sort and calculate percentage
    df_p = (
        df_p[df_p['value'] != 0]
        .sort_values(by=['value'], ascending=False)
        .head(cap_categories)
    )
    df_p['cum_per'] = df_p['value'].divide(df_p['value'].sum()).cumsum()
    return df_p


class ParetoChart(CustomChart):
    """Pareto Chart: both bar and line graph chart for strategic decision making."""

    cap_categories: int = 20
    """Maximum number of categories (bars). Default is 20."""

    show_count: bool = True
    """If True, will show numeric count on each bar. Default is True."""

    yaxis_2_label: str = 'Cumulative Percentage'
    """Label for yaxis 2 that shows the cumulative percentage."""

    _pareto_colors: dict = {'bar': '#4682b4', 'line': '#b44646'}
    _pareto_colors_schema = {
        'bar': {'required': True, 'type': 'string'},
        'line': {'required': True, 'type': 'string'},
    }

    @property
    def pareto_colors(self):
        """Colors for bar and line traces in Pareto chart.

        Returns:
            dict: dictionary with keys `(bar, line)`

        """
        return self._pareto_colors

    @pareto_colors.setter
    def pareto_colors(self, pareto_colors):
        errors = validate(pareto_colors, self._pareto_colors_schema)
        if errors:
            raise RuntimeError(f'Validation of self.pareto_colors failed: {errors}')
        # Assign new pareto_colors
        self._pareto_colors = pareto_colors

    def create_traces(self, df_raw):
        """Return traces for plotly chart.

        Args:
            df_raw: pandas dataframe with at minimum the two columns `category: str` and `value: float`

        Returns:
            list: Dash chart traces

        Raises:
            RuntimeError: if the `df_raw` is missing any necessary columns

        """
        # Check that the raw data frame is properly formatted
        check_raw_data(df_raw, min_keys=['category', 'value'])
        if not pd.api.types.is_string_dtype(df_raw['category']):  # pragma: no cover
            raise RuntimeError(f"category column must be string, but found {df_raw['category'].dtype}")

        # Create and return the traces and optionally add the count to the bar chart
        df_p = tidy_pareto_data(df_raw, self.cap_categories)
        count_kwargs = {'text': df_p['counts'], 'textposition': 'auto'} if self.show_count else {}
        return [
            go.Bar(
                hoverinfo='y', yaxis='y1', name='raw_value',
                marker={'color': self.pareto_colors['bar']},
                x=df_p['label'], y=df_p['value'], **count_kwargs,
            ),
        ] + [
            go.Scatter(
                hoverinfo='y', yaxis='y2', name='cumulative_percentage',
                marker={'color': self.pareto_colors['line']}, mode='lines',
                x=df_p['label'], y=df_p['cum_per'],
            ),
        ]

    def create_layout(self):
        """Extend the standard layout.

        Returns:
            dict: layout for Dash figure

        """
        layout = super().create_layout()
        layout['legend'] = {}
        layout['showlegend'] = False

        layout['margin'] = {'l': 75, 'b': 100, 't': 50, 'r': 125}

        # Update YAxis configuration
        layout['yaxis']['mirror'] = 'ticks'
        layout['yaxis']['showline'] = True
        layout['yaxis']['tickformat'] = '.0f'

        # See multiple axis: https://plot.ly/python/multiple-axes/
        layout['yaxis2'] = {
            'dtick': 0.1,
            'overlaying': 'y',
            'range': [0, 1.01],
            'showgrid': False,
            'side': 'right',
            'tickformat': '.0%',
            'tickmode': 'linear',
            'title': self.yaxis_2_label,
        }

        return layout
