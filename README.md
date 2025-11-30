# Genetic Program for Equation Discovery

A cross-platform symbolic regression engine using genetic programming to evolve mathematical expressions that fit input-output data. Designed for research workflows and GUI-based experimentation.

## Features

- Symbolic regression via genetic programming
- CLI and GUI interfaces (Tkinter for Linux, CustomTkinter for Windows)
- Configurable hyperparameters via YAML
- Function set selection (e.g., power, trig, log)
- Reloadable sessions and PDF report generation
- Splash screen and theme toggle support
- Exportable equations in Python, C, and LaTeX formats

## Quick Start

```
# Run GUI (auto-selects platform)
python main.py --gui

# Run CLI
python main.py data.csv --MAXGEN:100 --MAXDEPTH:5 --FSET:ELPT

```
## Requirements
- Python 3.10+
- matplotlib, numpy, Pillow, PyYAML
- customtkinter, CTkToolTip (Windows only)\
See INSTALL.md for setup instructions.

## Project Structure
```
core/               # Genetic engine, nodes, programs, evolution
interface/          # GUI and CLI interfaces
Reload.py           # Session persistence
CreateTex.py        # PDF report generation
main.py             # Entry point
```
## Documentation
- INSTALL.md: Setup instructions
- CONFIG.md: YAML config format
- GUI.md: GUI layout and usage

## Author
Created by [MageMusti](https://www.github.com/MageMusti)
