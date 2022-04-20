# CislunarSim

Simulation Software for the Cislunar Explorers Mission

## Getting Started

```bash
python -m venv venv
source venv/bin/activate
pip install -e .
```

## IMPORTANT: Python Version MUST be 3.8 and above

Run

```
python -V
```

in terminal to find your Python version. If it's lower than 3.8, you should upgrade your Python version.

## Upgrading Python Version:

Run in terminal (Mac users only):

If you don't have Homebrew, run the following:

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then, upgrade your Python version

```
brew update && brew upgrade python
```

and run the following command to set Python3 as the default interpreter

```
cp /usr/local/bin/python3 /usr/local/bin/python
```