# Genetic-Program-For-Equation
This is a Python based Genetic Program Implementation, 
That Takes an list of Input Data(Numbers or Set of Numbers) and Corresponding Output Values and tries to Find a Best FIt Equation Using Selection,Crossover and Mutation and Gives Result as a Latex PDF Document.
## Summary
The `GeneticProgramy.py` takes a csv file as argument and Assumes the Values in the last column as Output values and Remaining Columns as set of Input Values.
It Creates a Generation of Programs Where Each program Operates on the Input Data and it's Fitness is Measured based on its Difference Form Actual Output.
The Fitness Score is Used for Selection Algorithm to Create a New Generation Which Gives Better Results
The New Generation Then Goes through Crossovers and Mutation to Introduce Diversity in Generation.
This Process is Repeated With the New Generation Until A perfect Fit is Found or The Number of Generation is Exhausted.
The Values of Hyperparameters, Top 5 Best performing Eqautions and Table of Total Error,Average Error and Minimum Error is Saved as a Latex PDF as Result.


## Installation

### Prerequiste
For this Program The Following are Required:
> Python 3.10+ (Python 3.12 recommend)

> Pyyaml

> Texlive (For pdflatex)

The Envivorments Paths to these Must be Set in your system.
### Setup

Clone This Repository Using

`git clone https://github.com/MageMusti/Genetic-Program-For-Equation`

## Usage

Browse To the Repository Directory on you Terminal
Then run the Program as Follows:

`python GeneticProgram.py /path/to/csvfile`

Some Example csv files are Provided in the CSV Directory.
### Hyper Parameters
The Program has Following Configurable Hyper Parameters.

MAXDEPTH: Sets the Max Depth of Eqaution Tree. Alter to Control Complexity of Result.(Default: 2)
MAXGEN: Number of Maximum Generation to Explore Before Exiting. (Default: 20)
GENSIZE:Number of Programs per Generation.(Default: 10)
XOP: The Probability of a Crossover Occuring.(Default: 0.8)
MAXXO: The Maximum Number of Crossover That Occur Per Generation.(Default: Floor of GENSIZE/5)
MUTP:  The Probability of a Mutation Occuring.(Default: 0.5)
MAXMUT: The Maximum Number of Mutation That Occur Per Generation.(Default: Floor of GENSIZE/10)
REPORT: The Path to Report PDF file Without .pdf Extenstion.(Default: Result.pdf in Project Directory)
VERBOSE: Pause After Each Generation to Show Crossover and Mutation verbose Output with Total and Average Error(Default: False)
