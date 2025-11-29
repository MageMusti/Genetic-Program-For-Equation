# GUI Overview

The GUI offers a full-featured interface for configuring, running, and visualizing genetic programming experiments.

## Platform Support

- **Windows**: CustomTkinter (dark/light theme)
- **Linux**: Tkinter (simplified layout)

## Layout Overview

- **Input Section**: Browse or enter path to `.csv` or `.reload` file
- **Hyperparameters**: Set depth, generation size, mutation/crossover rates
- **Function Set**: Select operations to include (e.g., Power, Log)
- **Output Section**: Set paths for PDF report and reload file
- **Start Button**: Begins evolution and report generation

## Theme Toggle (Windows only)

Click the "Toggle Theme" button to switch between dark and light modes.

## Report Generation

After evolution completes:
- PDF report is saved to specified path
- Includes equations, error graphs, prediction plots, and LaTeX tables

## Reload Support

- Save session state to `.reload` file
- Resume later via GUI or CLI