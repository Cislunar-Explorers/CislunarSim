# CislunarSim

Simulation Software for the Cislunar Explorers Mission
[Read the Docs](https://cislunarsim.readthedocs.io/en/latest/)

## Getting Started

Create a virtual Python environment and install all the necessary dependencies. Make sure you run this from the root of the repository!

```bash
python -m venv venv
source venv/bin/activate
pip install -e .
```

You can exit this environment by running `deactivate`. To re-enter an existing environment, all you need is `source venv/bin/activate`.

## Running the Sim

Usage:

```zsh
python src/main.py {file path} [-v]
```

Options:
`file path` (Required): The path of the config file to simulate
`verbose` (Optional): For logging extra information to the terminal

Examples:
```zsh
python src/main.py configs/freefall.json 
python src/main.py configs/test_angles.json -v
```

## Plotting Sim Runs

Usage:

```zsh
python src/utils/plot.py {file path}
```

Options:
`file path` (Required): The path of the csv file to plot

Example:
```zsh
python src/utils/plot.py runs/cislunarsim-1650068219.9772968.csv
```

## IMPORTANT: Python Version MUST be >=3.8

Run `python --version` to find your Python version. If it's lower than 3.8, you must upgrade your Python version.

## Upgrading Python Version:

Run in terminal (Mac users only):

If you don't have Homebrew, run the following:

```zsh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then, upgrade your Python version

```zsh
brew update && brew upgrade python
```

and run the following command to set Python3 as the default interpreter

```zsh
cp /usr/local/bin/python3 /usr/local/bin/python
```
