from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
import json
import sys

# NOTE: Specifically for sorting my uni's classroom hostnames!
name_key = lambda n: int(n.split("-")[-1])

env = Environment(
    loader = FileSystemLoader("templates"),
    autoescape = select_autoescape()
)
tpl = env.get_template("out.j2.html")

data = []
for filename in sys.argv[1:]:
    with open(filename) as f:
        group = json.load(f)
        data.append(group)

now = oldest = int(datetime.now().timestamp())
for group in data:
    for ts in group["values"].values():
        oldest = min(oldest, ts)

chart_range = now - oldest

groups = []
for group in data:
    cells = []
    times = group["values"]
    sorted_names = sorted(group["values"], key=name_key)
    for name in sorted_names:
        ts = datetime.fromtimestamp(times[name]).strftime("%d-%m-%Y %H:%M:%S")
        # 'min-max normalisation' ; https://www.geeksforgeeks.org/data-analysis/normalization-and-scaling/
        percent = ((times[name] - oldest) / chart_range) * 100
        # TODO: make this configurable
        transformed_name = name[-6:]
        cells.append((transformed_name, percent, ts))
    groups.append({
        "name": group["name"],
        "cells": cells
    })

with open("out/index.html", "w") as f:
    f.write(tpl.render(groups=groups))
