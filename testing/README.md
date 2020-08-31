# Testing

[`asci.py`](asci.py) contains a pure Python implementation of [`asci.m`](asci.m), Anthony's original MATLAB secondary crater removal script.

## How to run

Python dependencies are managed using pipenv. Install pipenv and install dependencies with `pipenv install`. Then run a shell with `pipenv shell`. Then execute the script: `python asci.py`

## Comparison

The Python script has a very similar output to the MATLAB script.

Python outputs:

![Python results graph](docs/images/asci_python.png)

```
number of secondary craters:  134
```

MATLAB graph:

![MATLAB results graph](docs/images/asci_matlab.png)

```
number of secondary craters:  140
```
