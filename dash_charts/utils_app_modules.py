"""Utilities to build modules (delegated layout & callback methods) for Dash apps."""

import pandas as pd
from dash import dcc


class ModuleBase:  # noqa: H601
    """Base class for building a modular component for use in a Dash application."""

    all_ids = None
    """List of ids to register for this module."""

    def __init__(self, name):
        """Initialize module.

        Args:
            name: unique string name for this module

        Raises:
            NotImplementedError: if child class has not created a list, `all_ids`

        """
        if self.all_ids is None:
            raise NotImplementedError('Child class must create list of `self.all_ids`')  # pragma: no cover

        # Make ids unique and update all ids so that modules can be reused in the same app
        self.name = name
        self._ids = {_id: f'{self.name}__{_id}' for _id in self.all_ids}
        self.all_ids = self._ids.values()

        self.initialize_mutables()

    def get(self, _id):
        """Return the  the callback for creating the main chart.

        Args:
            _id: id from this module that is found in `self.all_ids`

        Returns:
            str: unique id name from instance of this module

        """
        return self._ids[_id]

    def initialize_mutables(self):
        """Initialize the mutable data members to prevent modifying one attribute and impacting all instances."""
        ...

    def create_elements(self, ids):
        """Register the callback for creating the main chart.

        Args:
            ids: `self._il` from base application

        """
        ...  # pragma: no cover

    def return_layout(self, ids):
        """Return Dash application layout.

        Args:
            ids: `self._il` from base application

        Raises:
            NotImplementedError: Dash HTML object. Default is simple HTML text

        """
        raise NotImplementedError('Must be implemented')  # pragma: no cover

    def create_callbacks(self, parent):
        """Register callbacks to handle user interaction.

        Args:
            parent: parent instance (ex: `self`)

        """
        ...  # pragma: no cover


class DataCache(ModuleBase):  # noqa: H601
    """Module to store data in UI and later loaded as needed."""

    id_cache = 'cache'
    """Session ID."""

    all_ids = [id_cache]
    """List of ids to register for this module."""

    def return_layout(self, ids, storage_type='memory', **store_kwargs):
        """Return Dash application layout.

        `dcc.Store` documentation: https://dash.plotly.com/dash-core-components/store

        Args:
            ids: `self._il` from base application
            storage_type: `dcc.Store` storage type. Default is memory to clear on refresh
            store_kwargs: additional keyword arguments to pass to `dcc.Store`

        Returns:
            dict: Dash HTML object.

        """
        return dcc.Store(id=ids[self.get(self.id_cache)], storage_type=storage_type, **store_kwargs)

    def return_write_df_map(self, df_table):
        """Return list of tuples for `map_outputs` that includes the new data cache JSON.

        Args:
            df_table: dataframe to show in table

        Returns:
            list: list of tuples for `map_outputs`

        """
        return [(self.get(self.id_cache), 'data', df_table.to_json())]

    def read_df(self, args):
        """Return list of tuples for `map_outputs` that includes the new data cache JSON.

        Args:
            args: either `a_in` or `a_state`, whichever has the id_cache-data

        Returns:
            dataframe: returns dataframe read from `dcc.Store`

        """
        return pd.read_json(args[self.get(self.id_cache)]['data'])
