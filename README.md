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
