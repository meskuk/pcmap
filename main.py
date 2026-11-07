from jinja2 import Environment, FileSystemLoader, select_autoescape
from datetime import datetime
import json
import sys

env = Environment(
    loader = FileSystemLoader("templates"),
    autoescape = select_autoescape()
)
tpl = env.get_template("out.j2.html")

# TODO: load multiple files lol
data = []
with open(sys.argv[1]) as f:
    data += json.load(f)

now = int(datetime.now().timestamp())
then = now
for group in data:
    for v in group["values"].values():
        v = min(then, v)

chart_range = now - then

groups = []
for group in data:
    cells = []
    vals = group["values"]
    for v in vals:
        ts = datetime.fromtimestamp(vals[v]).strftime("%d-%m-%Y\n%H:%M:%S")
        # 'min-max normalisation' ; https://www.geeksforgeeks.org/data-analysis/normalization-and-scaling/
        sat = ((vals[v] - then) / chart_range) * 100
        cells.append((v, sat, ts))
    groups.append({
        "name": group["name"],
        "cells": cells
    })

with open("out.html", "w") as f:
    f.write(tpl.render(groups=groups))
