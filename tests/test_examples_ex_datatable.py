"""Test the file examples/ex_datatable.py."""

import time

import pytest

from .configuration import no_log_errors
from .examples import ex_datatable


@pytest.mark.INTERACTIVE()
def test_smoke_test_ex_datatable(dash_duo):
    """Test ex_datatable."""
    pytest.skip('Currently failing until "ids" is fixed')  # FIXME: Fix the "ids" error

    dash_duo.start_server(ex_datatable.app.app)

    time.sleep(1)  # act

    assert no_log_errors(dash_duo)
