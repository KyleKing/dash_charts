"""Utilities to build modules (delegated layout & callback methods) for Dash apps."""


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
        pass

    def create_elements(self, ids):
        """Register the callback for creating the main chart.

        Args:
            ids: `self.ids` from base application

        """
        pass

    def return_layout(self, ids):
        """Return Dash application layout.

        Args:
            ids: `self.ids` from base application

        Raises:
            NotImplementedError: Dash HTML object. Default is simple HTML text

        """
        raise NotImplementedError('Must be implemented')  # pragma: no cover

    def create_callbacks(self, parent):
        """Register callbacks to handle user interaction.

        Args:
            parent: parent instance (ex: `self`)

        """
        pass
