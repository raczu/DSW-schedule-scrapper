import sys
import ttScrapper.scrapper as scrapper
import ttScrapper.calendar as calendar
from typing import Dict, List, Any


def main():
    try:
        timetable: List[Dict[str, Any]] = scrapper.scrap(sys.argv[1])
        if timetable is not None:
            if calendar.save_to_json(timetable):
                pass

            if calendar.save_to_ics(timetable):
                pass
    except IndexError:
        print('[!] You did not specify a url.')
        sys.exit(1)


if __name__ == '__main__':
    main()
