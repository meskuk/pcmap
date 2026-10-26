# pcmap

An experiment to make a coloured "map" of PCs in my university by their `lastlogon` time in Active Directory.

To run the project you'll need:
- The names of two domain controllers on your network (my script doesn't really do more yet)
- A proper filter for computers
- matplotlib for Python

Then you just pipe the PowerShell script output into `main.py`: `./collect.ps1 | python main.py`

![Example output](example.png)