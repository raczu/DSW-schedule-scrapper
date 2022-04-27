import sys
import scrapitplease.scrapper as scrapper
import scrapitplease.calendar as calendar
from typing import Dict, List, Optional


def main() -> None:
    try:
        schedule: Optional[List[Dict[str, str]]] = scrapper.scrap(sys.argv[1])
        if calendar.save_to_json(schedule):
            print('[+] Successfully created DSW.json file.')

        if calendar.save_to_ics(schedule):
            print('[+] Successfully created DSW.ics file.')

    except IndexError:
        print('[!] You did not specify a url.')
        sys.exit(1)


if __name__ == '__main__':
    main()
