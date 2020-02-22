"""Pareto Chart."""

from dataclasses import dataclass, field

import pandas as pd
import plotly.graph_objects as go

from .utils_fig import CustomChart


@dataclass
class ParetoParameters:
    """Dataclass for Pareto Parameters."""

    # _pareto_colors: field(init=False, repr=False)
    _pareto_colors: field(repr=False)

    cap_categories: int = 20
    """Maximum number of categories (bars). Default is 20."""

    show_count: bool = True
    """If True, will show numeric count on each bar. Default is True."""

    pareto_colors: dict = {'bar': '#4682b4', 'line': '#b44646'}

    @property
    def pareto_colors(self):
        """Colors for bar and line traces in Pareto chart.

        Returns:
            dict: dictionary with keys `(bar, line)`

        """
        return self._pareto_colors

    @pareto_colors.setter
    def pareto_colors(self, pareto_colors):
        expected_keys = sorted(self.pareto_colors.keys())
        if sorted(pareto_colors.keys()) != expected_keys:
            raise RuntimeError(f'Expected {pareto_colors} to have keys: {expected_keys}')
        self._pareto_colors = pareto_colors


class ParetoChart(CustomChart, ParetoParameters):
    """Pareto Chart: both bar and line graph chart for strategic decision making."""

    cap_categories: int = 20
    """Maximum number of categories (bars). Default is 20."""

    show_count: bool = True
    """If True, will show numeric count on each bar. Default is True."""

    pareto_colors: dict = {'bar': '#4682b4', 'line': '#b44646'}
    """Colors for bar and line traces in Pareto chart."""

    def tidy_pareto_data(self, raw_df):
        """Return compressed Pareto dataframe of only the unique values.

        Args:
            raw_df: pandas dataframe with at minimum the two columns `category: str` and `value: float`

        Returns:
            dataframe: pandas dataframe with columns `(value, label, counts, cum_per)`

        """
        df_p = None
        for cat in raw_df['category'].unique():
            df_row = pd.DataFrame(data={
                'label': [cat],
                'value': [raw_df.loc[raw_df['category'] == cat]['value'].sum()],
                'counts': raw_df['category'].value_counts()[cat],
            })
            df_p = df_row if df_p is None else df_p.append(df_row)
        # Sort and calculate percentage
        df_p = (df_p[df_p['value'] != 0]
                .sort_values(by=['value'], ascending=False)
                .head(self.cap_categories))
        df_p['cum_per'] = df_p['value'].divide(df_p['value'].sum()).cumsum()
        return df_p

    def create_traces(self, raw_df):
        """Return traces for plotly chart.

        Args:
            raw_df: pandas dataframe with at minimum the two columns `category: str` and `value: float`

        Returns:
            list: Dash chart traces

        Raises:
            RuntimeError: if the `raw_df` is missing any necessary columns

        """
        # Verify data format
        min_keys = ['category', 'value']
        all_keys = raw_df.keys()
        if len([_k for _k in min_keys if _k in all_keys]) != len(min_keys):
            raise RuntimeError(f'`raw_df` must have keys {min_keys}. Found: {all_keys}')
        elif not pd.api.types.is_string_dtype(raw_df['category']):
            raise RuntimeError(f"category column must be string, but found {raw_df['category'].dtype}")

        # Create and return the traces and optionally add the count to the bar chart
        df_p = self.tidy_pareto_data(raw_df)
        count_kwargs = {'text': df_p['counts'], 'textposition': 'auto'} if self.show_count else {}
        return [
            go.Bar(hoverinfo='y', yaxis='y1', name='Raw Value',
                   marker={'color': self.pareto_colors['bar']},
                   x=df_p['label'], y=df_p['value'], **count_kwargs),
        ] + [
            go.Scatter(hoverinfo='y', yaxis='y2', name='Cumulative Percentage',
                       marker={'color': self.pareto_colors['line']}, mode='lines',
                       x=df_p['label'], y=df_p['cum_per']),
        ]

    def create_layout(self):
        """Override the standard layout and add additional settings.

        Returns:
            dict: layout for Dash figure

        """
        layout = super().create_layout()
        layout['legend'] = {}
        layout['showlegend'] = False

        # Update YAxis configuration
        layout['yaxis']['mirror'] = 'ticks'
        layout['yaxis']['showline'] = True
        layout['yaxis']['tickformat'] = '.1f'

        # See multiple axis: https://plot.ly/python/multiple-axes/
        layout['yaxis2'] = {
            'dtick': 0.1,
            'overlaying': 'y',
            'range': [0, 1.01],
            'showgrid': False,
            'side': 'right',
            'tickformat': '.0%',
            'tickmode': 'linear',
            'title': 'Cumulative Percentage',
        }

        return layout
