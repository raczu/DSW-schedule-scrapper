from icalendar import Calendar, Event
from datetime import datetime
import json
import os
from typing import Dict, List, Optional

DEFAULT_PATH: str = os.getcwd()


def save_to_ics(schedule: Optional[List[Dict[str, str]]]) -> bool:
    """
    Returns true if the schedule has been
    successfully saved to .ics file type
    """

    if schedule is not None:
        c: Calendar = Calendar()
        c.add('X-WR-CALNAME', 'Zajęcia DSW')
        c.add('X-WR-TIMEZONE', 'Europe/Warsaw')
        element: Dict[str, str]

        for element in schedule:
            e: Event = Event()

            dt_from: datetime = datetime.combine(
                datetime.strptime(element['classes_date'], '%Y-%m-%d').date(),
                datetime.strptime(element['hour_from'], '%H:%M').time()
            )
            dt_to: datetime = datetime.combine(
                datetime.strptime(element['classes_date'], '%Y-%m-%d').date(),
                datetime.strptime(element['hour_to'], '%H:%M').time()
            )

            e.add('dtstart', dt_from)
            e.add('dtend', dt_to)
            e.add('summary', element['subject'])
            e.add('description', element['teacher'])
            e.add('location', element['classroom'])

            c.add_component(e)

        with open(f'{DEFAULT_PATH}/DSW.ics', 'wb') as f:
            f.write(c.to_ical())
        return True

    return False


def save_to_json(schedule: Optional[List[Dict[str, str]]]) -> bool:
    """
    Returns true if the schedule has been
    successfully saved to .json file type
    """

    if schedule is not None:
        with open(f'{DEFAULT_PATH}/DSW.json', 'w', encoding='utf-8') as f:
            json.dump(schedule, f, ensure_ascii=False, indent=4)
        return True

    return False
