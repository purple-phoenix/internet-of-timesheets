"""Module for auto logging time spent on lichess"""

from typing import Tuple
from datetime import datetime, timezone

import lichess.api

LichessID = str
ActivityInterval = Tuple[datetime, datetime]


def get_most_recent_activity_interval(user_id: LichessID) -> ActivityInterval:
    """Retrives most recent interval of activity for given user """
    user_activity = lichess.api.user_activity(user_id)[0]
    interval = user_activity["interval"]
    start_epoch = interval["start"]
    end_epoch = interval["end"]
    start_dt = datetime.fromtimestamp(int(start_epoch)/1000, timezone.utc)
    end_dt = datetime.fromtimestamp(int(end_epoch)/1000, timezone.utc)
    return start_dt, end_dt
