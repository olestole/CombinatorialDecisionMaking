# Constraint Programming (CP)

## Getting Started

### Prerequisites

- minizinc
  - Install the MinizincIDE and make sure to export it to PATH with
  ```sh
  $ export PATH=/Applications/MiniZincIDE.app/Contents/Resources:$PATH
  ```

### Installation

- [Create a venv](#create-a-virtual-environment-venv) to install the python-packages into locally.

## Usage

Run the `minizinc_solver.py`-script from your terminal

```sh
$ cd src
$ ./minizinc_solver.py
```

**Options**

- Specify the model to be used by specifying option `-m <model_path>`
  - All the CP-models can be found under `CP/models`.
- Specify if you'd like to use Chuffed or GeCode with option `-s <chuffed|gecode>`
- Specify the range of instances you'd like to solve with option `-r <range>`, e.g. `-r 2-9`

The solver will output all the run-results to `/out`.

# Misc

## Create a Virtual Environment (venv)

```bash
# /VLSIdesign

$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

# If you want to install new packages
$ pip install <name-of-new-pip-package>

# When you're done
$ deactivate
```
