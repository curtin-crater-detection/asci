# Testing

[`scia.py`](scia.py) contains a pure Python implementation of [`SCIA.m`](scia.m), Anthony's original MATLAB secondary crater removal script.

## How to run

Python dependencies are managed using pipenv. Install pipenv and install dependencies with `pipenv install`. Then run a shell with `pipenv shell`. Then execute the script: `python scia.py`

## Comparison

The Python script has a very similar output to the MATLAB script.

Python outputs:

![Python results graph](docs/images/scia_python.png)

```
number of secondary craters:  134
```

MATLAB graph:

![MATLAB results graph](docs/images/scia_matlab.png)

```
number of secondary craters:  140
```
