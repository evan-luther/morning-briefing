#!/usr/bin/env python3
from datetime import datetime
from zoneinfo import ZoneInfo

day = datetime.now(ZoneInfo("America/New_York")).date().isoformat()
print(f"https://evan-luther.github.io/morning-briefing/?date={day}")
