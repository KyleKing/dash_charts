"""Test the file examples/ex_modules_upload.py."""

import pytest

from .configuration import no_log_errors
from .examples import ex_modules_upload


@pytest.mark.CHROME
def test_smoke_test_ex_modules_upload(dash_duo):
    dash_duo.start_server(ex_modules_upload.app.app)

    import time
    time.sleep(1)

    assert no_log_errors(dash_duo)
