from datetime import datetime
from pathlib import Path
import re

def parking_fee(arrival: datetime, departure: datetime) -> int:
    if departure < arrival:
        return 0
    delta = departure - arrival
    total_minutes = int(delta.total_seconds() / 60)
    if total_minutes <= 30:
        return 0
    days = total_minutes // 1440
    remaining_minutes = total_minutes % 1440
    total_daily_fee = days * 10_000
    if days > 0 and remaining_minutes == 0:
        remaining_fee = 0
    else:
        first_half_minutes = min(remaining_minutes, 180)
        second_half_minutes = max(0, remaining_minutes - 180)
        remaining_fee = min((first_half_minutes * 5) + (second_half_minutes * (500 / 60)), 10_000)
    return int(round(total_daily_fee + remaining_fee))

def main():
    data = Path("input.txt").read_text(encoding="utf-8")
    parsed = (re.split(r"\t+", x.strip()) for x in data.split("\n")[2:] if x.strip())
    fmt = "%Y-%m-%d %H:%M:%S"
    for [_, arrival, departure] in parsed:
        try:
            print(parking_fee(datetime.strptime(arrival, fmt), datetime.strptime(departure, fmt)))
        except ValueError:
            pass


if __name__ == "__main__":
    main()
