"""Module for auto logging time spent on lichess"""

from typing import Any, Dict, Optional, Tuple
from datetime import datetime, timedelta, timezone

from time import sleep

import lichess.api

LichessID = str
ActivityInterval = Tuple[datetime, datetime]
StartGameTimestamp = datetime
LastMoveTimestamp = datetime
GameTimestamps = Tuple[StartGameTimestamp, LastMoveTimestamp]
Game = Tuple[Dict[str, Any],
             GameTimestamps,
             ]


def get_most_recent_activity_interval(user_id: LichessID) -> ActivityInterval:
    """Retrives most recent interval of activity for given user """
    user_activity = lichess.api.user_activity(user_id)[0]
    interval = user_activity["interval"]
    start_epoch = interval["start"]
    end_epoch = interval["end"]
    start_dt = datetime.fromtimestamp(int(start_epoch)/1000, timezone.utc)
    end_dt = datetime.fromtimestamp(int(end_epoch)/1000, timezone.utc)
    return start_dt, end_dt


POLL_RATE = 5
GAME_TIMEOUT = 5


def update_chess_timesheet(lichess_id: LichessID,
                           maybe_last_latest_game: Optional[Game]):
    """Look for new game,if tracking wait and check again,if not start tracking
    If no new game within timeout stop tracking at end of last game"""
    latest_game = get_latest_game(lichess_id)
    if is_tracking_lichess():
        sleep(POLL_RATE)
        update_chess_timesheet(lichess_id, latest_game)
    should_stop_tracking, should_start_tracking = \
        no_new_game(latest_game, maybe_last_latest_game)
    if should_stop_tracking:
        stop_tracking()
    elif should_start_tracking:
        start_tracking(latest_game)


StopTracker = bool
StartNewTracker = bool

TransitionState = Tuple[StopTracker, StartNewTracker]

STOPTRACKING = True
DONTSTOPTRACKING = False
STARTTRACKING = True
DONTSTARTTRACKING = False


def no_new_game(latest_game: Game,
                maybe_last_latest_game: Optional[Game]) -> TransitionState:
    """Determines if no new game has been
    started since the last latest game"""
    # If there was no previous game, then we have not recursed
    # latest_game is not new if it is the first tracked game
    if maybe_last_latest_game is None:
        return DONTSTOPTRACKING, STARTTRACKING
    last_latest_game: Game = maybe_last_latest_game
    # No new game has been started
    if latest_game == last_latest_game:
        return STOPTRACKING, DONTSTARTTRACKING
    return new_game_passed_timeout(latest_game, last_latest_game)


def new_game_passed_timeout(latest_game: Game,
                            last_latest_game: Game) -> TransitionState:
    """Determines if the latest_game is beyond
    the threshold of a new tracking event"""
    assert latest_game
    assert last_latest_game


def is_tracking_lichess() -> bool:
    """Determines if Toggl is currently tracking Lichess"""


def start_tracking(game: Game) -> None:
    """Starts tracking Lichess on Toggl"""
    assert game


def stop_tracking() -> None:
    """Stop tracking Lichess on Toggl"""


def get_latest_game(lichess_id: LichessID) -> Game:
    """Gets the latest game"""
    games = lichess.api.user_games(lichess_id)
    return make_game(next(games))


def ms_epoch_to_datetime(epoch_in_ms: int,
                         dtz: timezone = timezone.utc) -> datetime:
    """Consumes an epoch in milliseconds and returns its equivalent datetime"""
    msec = epoch_in_ms % 1000
    seconds = epoch_in_ms // 1000
    datetime_in_s = datetime.fromtimestamp(seconds, dtz)
    datetime_in_ms = datetime_in_s + timedelta(milliseconds=msec)
    return datetime_in_ms


def make_game(game_dict: Dict[str, Any]) -> Game:
    """Consumes json output and produces a game"""
    start_game_epoch = game_dict["createdAt"]
    last_move_epoch = game_dict["lastMoveAt"]
    start_game_ts = ms_epoch_to_datetime(start_game_epoch)
    last_move_ts = ms_epoch_to_datetime(last_move_epoch)

    return game_dict, (start_game_ts, last_move_ts)





