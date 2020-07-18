"""Test the file examples/ex_modules_upload.py."""

import pytest

from .examples import ex_modules_upload


@pytest.mark.CHROME
def test_smoke_test_ex_modules_upload(dash_duo):
    dash_duo.start_server(ex_modules_upload.app.app)

    import time
    time.sleep(1)

    assert not dash_duo.get_logs()
