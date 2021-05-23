"""Tests for Auto Logging time spent on lichess"""

from datetime import datetime, timedelta, timezone

import pytest

import lichess_timesheet as MUT


@pytest.fixture(name="matt_lichess_id")
def matt_lichess_fixture():
    """Matt's lichess user id"""
    return "midnightconquer"


@pytest.fixture(name="game_dict")
def game_dict_fixture():
    """An example game json returned from server"""
    return {
            "id": "Jx4J1oNw",
            "rated": True,
            "variant": "standard",
            "speed": "blitz",
            "perf": "blitz",
            "createdAt": 1621800789652,
            "lastMoveAt": 1621801225047,
            "status": "mate",
            "players": {
                "white": {
                    "user": {
                        "id": "suso963",
                        "name": "SUSO963"
                        },
                    "rating": 1247,
                    "ratingDiff": -6
                    },
                "black": {
                    "user": {
                        "id": "midnightconquer",
                        "name": "midnightconquer"
                        },
                    "rating": 1191,
                    "ratingDiff": 7
                    },
                },
            "winner": "black",
            "moves": "e4 c5 c4 e6 d3 Nf6 Bg5 h6 Bxf6 Qxf6""" +
                     """Nf3 Nc6 a4 Qxb2 Nbd2 Nd4""" +
                     """Rb1 Nc2+ Ke2 Qc3 Rb3 Nd4+ Nxd4 Qxd4 Ke1""" +
                     """f5 Be2 fxe4 Nxe4 d5 Bh5+""" +
                     """Kd7 Qf3 dxc4 Qf7+ Kc6 Qe8+ Bd7 Qg6 cxb3""" +
                     """Nxc5 Qa1+ Bd1 Kxc5 Qh5+ Kc6""" +
                     """Qf3+ Kc7 Ke2 b2 Qf4+ Bd6 Qc4+ Bc6 Bc2""" +
                     """Qxh1 d4 Qc1 a5 b1=Q Qxe6 Qcxc2+ Ke3 Qe1#""",
            "clock": {
                "initial": 300,
                "increment": 0,
                "totalTime": 300
                }

            }


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
def test_get_latest_game(matt_lichess_id):
    """Tests if latest game can be captured"""
    expected_latest_game = ""
    assert expected_latest_game == MUT.get_latest_game(matt_lichess_id)


def test_make_game(game_dict):
    """Tests whether json can be converted to a game"""

    start_game_ts = datetime(
            year=2021, month=5, day=23,
            hour=20, minute=13, second=9,
            tzinfo=timezone.utc) + timedelta(milliseconds=652)

    last_move_ts = datetime(
            year=2021, month=5, day=23,
            hour=20, minute=20, second=25,
            tzinfo=timezone.utc) + timedelta(milliseconds=47)

    expected_game = game_dict, (start_game_ts, last_move_ts)

    assert expected_game == MUT.make_game(game_dict)


def test_ms_epoch_to_datetime():
    """Tests that epoch in ms can be converted to datetime with ms"""
    epoch_in_ms = 1621800789652
    expected_dt = datetime(
            year=2021, month=5, day=23,
            hour=20, minute=13, second=9,
            tzinfo=timezone.utc) + timedelta(milliseconds=652)
    assert expected_dt == MUT.ms_epoch_to_datetime(epoch_in_ms)
