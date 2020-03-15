"""Utilities to build modules (delegated layout & callback methods) for Dash apps."""


class ModuleBase:
    """Base class for building a modular component for use in a Dash application."""

    all_ids = None
    """List of ids to register for this module."""

    def __init__(self):
        """Initialize module.

        Raises:
            NotImplementedError: if child class has not created a list, `all_ids`

        """
        if self.all_ids is None:
            raise NotImplementedError('Child class must create list of `self.all_ids`')  # pragma: no cover

    def create_elements(self, ids):
        """Register the callback for creating the main chart.

        Args:
            ids: requires `self.ids` from base application

        """
        pass

    def return_layout(self, ids):
        """Return Dash application layout.

        Args:
            ids: requires `self.ids` from base application

        Raises:
            NotImplementedError: Dash HTML object. Default is simple HTML text

        """
        raise NotImplementedError('Must be implemented')  # pragma: no cover

    def create_callbacks(self, ids):
        """Register callbacks to handle user interaction.

        Args:
            ids: requires `self.ids` from base application

        """
        pass
