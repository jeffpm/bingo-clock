import pytest

import app

@pytest.mark.parametrize("max,minutes,expected",
[
    (25, 25, [25]),
    (25, 15, [15]),
    (25, 1, [1]),
    (25, 26, [25, 1]),
    (25, 60, [25, 24, 11]),
    (25, 59, [25, 24, 10]),
    (25, 48, [25, 23]),
    (25, 50, [25, 24, 1])
])
def test_break_down_minutes(max, minutes, expected):
    assert app.break_down_minutes(max, minutes) == expected