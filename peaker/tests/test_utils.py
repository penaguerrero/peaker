import numpy as np
from peaker.utils import convert_units, TIMEZONES


def test_timezones():
    # Test some of the local time zones
    timezones = ["EST", "GMT", "MT", "PT"]
    for tz in timezones:
        assert tz in TIMEZONES


def test_convert_utils():
    bytes_arr = np.array([1e9, 1e10])
    converted, units = convert_units(bytes_arr, desired_units=None)

    assert converted.size == 2
    assert units == "GB"
