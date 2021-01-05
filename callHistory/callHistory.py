#!/usr/bin/env python

# Script for obtaining call history with someone
# Must be provided the message_*.json file
# File can be downloaded from fb and selecting:
# Small-ish Date Range, Format:Json, Media Quality:Low, Tick only Messages box

import json
from datetime import datetime, timedelta

pathToJson = "./message_1.json"
fileout = "callLog.csv"
include_missed_calls = True

def find_evening(ts):
    # calls between midnight and 5am should be listed as
    # part of the evening before
    return ts if ts.hour > 4 else ts - timedelta(days=1)

def parse_call_json(m):
    timefmt = "%I:%M %p"
    datefmt = "%Y-%m-%d"

    end = datetime.fromtimestamp(float(m["timestamp_ms"]) / 1000.)
    duration = timedelta(seconds=m["call_duration"])
    start = end - duration
    evening = find_evening(start)

    row = "{}\t,{},{},{},{}".format(
        m["sender_name"],
        evening.strftime(datefmt),
        start.strftime(timefmt),
        end.strftime(timefmt),
        duration)
    print(row)
    return row

def main():
    with open(pathToJson, "r") as f:
        data = json.load(f)

    msgs = data["messages"]

    csv_text = "Caller, Evening of, Time Called, Time End, Duration (h:mm)"
    for m in msgs:
        if m["type"] == "Call":
            if not include_missed_calls and m["call_duration"] == 0:
                continue
            csv_text += '\n' + parse_call_json(m)

    with open(fileout, "w") as f:
        f.write(csv_text)

if __name__ == '__main__':
    main()
