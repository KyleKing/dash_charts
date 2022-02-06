"""Test the file examples/ex_style_bootstrap.py."""

import time

import pytest

from .configuration import no_log_errors
from .examples import ex_style_bootstrap


@pytest.mark.INTERACTIVE()
def test_smoke_test_ex_style_bootstrap(dash_duo):
    """Test ex_style_bootstrap."""
    dash_duo.start_server(ex_style_bootstrap.app.app)

    time.sleep(1)  # act

    assert no_log_errors(dash_duo, ['WARNING'])
