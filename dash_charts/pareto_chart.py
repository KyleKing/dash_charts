"""Pareto Chart."""

import pandas as pd
import plotly.graph_objects as go

from .utils_fig import CustomChart


class ParetoChart(CustomChart):
    """Pareto Chart: both bar and line graph chart for strategic decision making."""

    pareto_colors = {'bar': '#4682b4', 'line': '#b44646'}
    """Default colors for pareto bar and line respectively."""

    cap_categories = 20
    """Maximum number of categories (bars). Default is 20."""

    def create_traces(self, raw_df, *, show_count=True):
        """Return traces for plotly chart.

        Args:
            raw_df: pandas dataframe with at minimum the two columns `value: float` and `categories: str`
            show_count: boolean and if True, will show numeric count on each bar. Default is True

        Returns:
            list: Dash chart traces

        Raises:
            RuntimeError: if the `raw_df` is missing any necessary columns

        """
        # Verify data format
        min_keys = ['value', 'categories']
        all_keys = raw_df.keys()
        if len([_k for _k in min_keys if _k in all_keys]) != len(min_keys):
            raise RuntimeError(f'`raw_df` must have keys {min_keys}. Found: {all_keys}')

        # Created compressed Pareto dataframe of only the unique values
        df_p = None
        for cat in raw_df['categories'].unique():
            df_row = pd.DataFrame(data={
                'value': [raw_df.loc[raw_df['categories'] == cat]['value'].sum()],
                'label': [cat],
                'counts': raw_df['categories'].value_counts()[cat],
            })
            df_p = df_row if df_p is None else df_p.append(df_row)
        # Sort and calculate percentage
        df_p = df_p.sort_values(by=['value'], ascending=False).head(self.cap_categories)
        df_p = df_p[df_p['value'] != 0]
        df_p['cumPer'] = df_p['value'].divide(df_p['value'].sum()).cumsum()

        # Create and return the traces and optionally add the count to the bar chart
        count_kwargs = {'text': df_p['counts'], 'textposition': 'auto'} if show_count else {}
        return [
            go.Bar(hoverinfo='y', yaxis='y1', name='Raw Value',
                   marker={'color': self.pareto_colors['bar']},
                   x=df_p['label'], y=df_p['value'], **count_kwargs),
        ] + [
            go.Scatter(hoverinfo='y', yaxis='y2', name='Cumulative Percentage',
                       marker={'color': self.pareto_colors['line']}, mode='lines',
                       x=df_p['label'], y=df_p['cumPer']),
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
