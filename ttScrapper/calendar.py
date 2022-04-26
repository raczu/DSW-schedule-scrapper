import icalendar
import json
import os
from typing import Dict, List, Any

DEFAULT_PATH: str = os.getcwd()


def save_to_ics(timetable: List[Dict[str, Any]]) -> bool:
    """
    Returns true if the timetable has been
    successfully saved to .ics file type
    """
    pass


def save_to_json(timetable: List[Dict[str, Any]]) -> bool:
    """
    Returns true if the timetable has been
    successfully saved to .json file type
    """
    pass
