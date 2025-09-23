# SDEV220 Restaurant Ordering System

Course project: loads a text "database" of menu items and gives you a basic ordering GUI.

## Run the GUI

```powershell
cd "C:\Users\Harold Ligon\Documents\SDEV220"
python main.py
```

## Quick test CLI mode

```powershell
python main.py --cli
```

## If stuff breaks

- `ModuleNotFoundError: gui.restaurant_app` -> you probably ran it from the wrong folder. `cd` into `SDEV220` first.
- Tkinter missing? Re‑install Python from python.org (standard installer includes Tk). On Windows Store versions it can be flaky.
- Nothing loads? Check the `SDEV_220_Final_Project_Group2/DatabaseFiles` folder still has `default.txt` and `default_addons.txt`.

## What's here

- `main.py` – launcher (GUI by default, CLI with `--cli`).
- `gui/restaurant_app.py` – the Tkinter interface.
- `models/` – inventory + product/addon + order classes.
- `SDEV_220_Final_Project_Group2/DatabaseFiles/` – the text data files.

## Future polish ideas (if we keep going)

- Let the UI add addons (they load, just not shown yet).
- Write stock changes back to file.
- Real categories instead of the placeholder.
