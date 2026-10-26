import json
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime, timedelta, timezone
from datetime import timezone as tz
import sys

data = json.load(sys.stdin)
# FIXME: this is temporary for single-classroom data
keys = sorted(data.keys(), key=lambda k: int(k.split("-")[::-1][0]))

now = datetime.now(tz=tz.utc)

size = round(len(keys) / 4)


def label(name: str, time: float) -> str:
    number = name.split("-")[::-1][0]
    dt = datetime.fromtimestamp(time)
    return dt.strftime(f"{number}\n%d/%m\n%H:%M:%S")

times = [data[k] for k in keys]
labels = [label(k, data[k]) for k in keys]
time_rows = []
label_rows = []
print(labels)
print(times)
i = 0
while i < len(keys):
    labelchunk = labels[i:i+size]
    timechunk = times[i:i+size]
    if len(timechunk) < size:
        print(timechunk)
        timechunk.extend([0] * (size - len(timechunk)))
        print(timechunk)
    time_rows.append(timechunk)
    label_rows.append(labelchunk)
    i += size

final = np.array(time_rows)
maxtime = now.timestamp()
mintime = np.min(final)

fig, ax = plt.subplots()
im = ax.imshow(final, norm="log", vmax=maxtime)
ax.set_title(now.strftime(f"{sys.argv[1]} @ %d/%m/%Y %H:%M:%S"))
fig.colorbar(
    im,
    ax=ax,
    format=lambda x, _: str(datetime.fromtimestamp(x)),
    ticks=[maxtime, mintime]
)

for i in range(len(label_rows)):
    for j in range(len(label_rows[i])):
        ax.text(j, i, label_rows[i][j], horizontalalignment='center')

plt.show()