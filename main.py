from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
import json
import sys

# NOTE: Specifically for sorting my uni's classroom hostnames!
def name_key(n): return int(n.split("-")[-1])

env = Environment(
    loader = FileSystemLoader("templates"),
    autoescape = select_autoescape()
)
list_tpl = env.get_template("list.j2.html")
chart_tpl = env.get_template("out.j2.html")

all_data = []
for filename in sys.argv[1:]:
    with open(filename) as f:
        d = json.load(f)
        collected_at = datetime.fromtimestamp(d["collected_at"])
        d["href"] = collected_at.strftime("%Y%m%d_%H%M%S.html")
        d["link_title"] = collected_at.strftime("%Y-%m-%d %H:%M:%S")
        all_data.append(d)

prev_page = None
next_page = None
for i in range(len(all_data)):
    data = all_data[i]
    rooms = data["rooms"]
    latest = oldest = data["collected_at"]
    for room in rooms:
        for ts in room["times"].values():
            oldest = min(oldest, ts)

    chart_range = latest - oldest

    processed = []
    for room in rooms:
        cells = []
        times = room["times"]
        sorted_names = sorted(room["times"], key=name_key)
        for name in sorted_names:
            ts = datetime.fromtimestamp(times[name]).strftime("%d-%m-%Y %H:%M:%S")
            # 'min-max normalisation' ; https://www.geeksforgeeks.org/data-analysis/normalization-and-scaling/
            percent = ((times[name] - oldest) / chart_range) * 100
            # NOTE: also intended
            # TODO: create a more centralised 
            transformed_name = name[-6:]
            cells.append((transformed_name, percent, ts))
        processed.append({
            "name": room["name"],
            "cells": cells
        })

    if i > 0:
        prev_page = all_data[i-1]["href"]
    if i+1 < len(all_data):
        next_page = all_data[i+1]["href"]
    else:
        next_page = None

    with open("out/"+data["href"], "w") as f:
        f.write(chart_tpl.render(groups=processed, prev_page=prev_page, next_page=next_page))
    if i == 0:
        with open("out/index.html", "w") as f:
            f.write(chart_tpl.render(groups=processed, prev_page=prev_page, next_page=next_page))

with open("out/list.html", "w") as f:
    pages = [
        (p["href"], p["link_title"])
        for p in all_data
    ]
    f.write(list_tpl.render(pages=pages))

