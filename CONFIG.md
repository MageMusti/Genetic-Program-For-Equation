# Configuration File Format (`.yaml`)

You can define hyperparameters and function sets using a YAML config file.

## Sample Config

```
RESULT: Report
MAXDEPTH: 5
GENSIZE: 100
MAXGEN: 1000
XOP: 0.9
MAXXO: 50
MUTP: 0.2
MAXMUT: 10
NEWP: 0.15
MAXNEW: 10
VERBOSE: true
RELOAD: true
FSET: ELPT
```
## Function Set Codes
| Code | Operation |
|:---|:---|
|E|Exponentiation|
|L|Logarithm and Exponential|
|P|Square and Cube|
|R|Square Root and Cube Root|
|T|sin,cos and tan|

## Usage
```
python main.py --CONFIG:Sample.yaml data.csv
```
## Export Config from GUI
Use the "Export Config" button to save current hyperparameters to a YAML file