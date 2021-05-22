"""Tests for Auto Logging time spent on lichess"""

import pytest

from datetime import datetime, timezone

import lichess_timesheet as MUT


@pytest.fixture(name="matt_lichess_id")
def matt_lichess_fixture():
    """Matt's lichess user id"""
    return "midnightconquer"


def test_get_most_recent_activity_interval(matt_lichess_id):
    """Tests whether most recent activity interval timestamps can be found"""
    activity_interval: MUT.ActivityInterval =\
        MUT.get_most_recent_activity_interval(matt_lichess_id)
    start_interval = activity_interval[0]
    end_interval = activity_interval[1]
    assert end_interval > start_interval


@pytest.mark.dev_test
def test_is_tracking_lichess():
    """Tests whether script can determine
    if Toggl is currently tracking Lichess"""
    assert not MUT.is_tracking_lichess()


@pytest.mark.dev_test
def test_get_latest_game():
    """Tests if latest game can be captured"""
