# Installation Guide

This guide helps you set up the Genetic Program for Equation Discovery on Windows and Linux.

## Windows Setup

1. **Install Python 3.10+**
   - Download from [python.org](https://www.python.org/downloads/)
   - Ensure `python` and `pip` are in your PATH

2. **Install dependencies**
   ```
   pip install matplotlib numpy Pillow PyYAML customtkinter CTkToolTip
	```
3. **Clone the project**
	```
	git clone https://github.com/MageMusti/Genetic-Program-For-Equation.git
	cd Genetic-Program-For-Equation
    ```
4. **Run the GUI**
	```
	python main.py --gui
	```
5. **Run CLI**
	```
	python main.py data.csv
	```
## Ubuntu/Linux Setup
1. **Install Python 3.10+**
	```
	sudo apt update
	sudo apt install python3 python3-pip
	```
2. **Install dependencies**
	```
	pip3 install matplotlib numpy Pillow PyYAML
	```
3. **Clone the project**
	```
	git clone https://github.com/MageMusti/Genetic-Program-For-Equation.git
	cd Genetic-Program-For-Equation
    ```
4. **Run the GUI (Tkinter-based)**
	```
	python3 main.py --gui
	```
	Note: CustomTkinter is not supported on restricted Ubuntu systems. The GUI will default to standard Tkinter.
5. **Run CLI**
	```
	python main.py data.csv
	```