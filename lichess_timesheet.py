"""Module for auto logging time spent on lichess"""

from typing import Tuple, Optional
from datetime import datetime, timezone

from time import sleep

import lichess.api

LichessID = str
ActivityInterval = Tuple[datetime, datetime]
Game = str


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


def update_chess_timesheet(maybe_last_latest_game: Optional[Game]):
    """Look for new game,if tracking wait and check again,if not start tracking
    If no new game within timeout stop tracking at end of last game"""
    latest_game = get_latest_game()
    if is_tracking_lichess():
        sleep(POLL_RATE)
        update_chess_timesheet(latest_game)
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


def new_game_passed_timeout(latest_game: Game, last_latest_game: Game) -> TransitionState:
    """Determines if the latest_game is beyond
    the threshold of a new tracking event"""


def is_tracking_lichess() -> bool:
    """Determines if Toggl is currently tracking Lichess"""


def start_tracking(game: Game) -> None:
    """Starts tracking Lichess on Toggl"""


def stop_tracking() -> None:
    """Stop tracking Lichess on Toggl"""


def get_latest_game() -> Game:
    """Gets the latest game"""
    return ""
