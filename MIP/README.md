# Linear Programming (LP)

## Getting Started

### Prerequisites
- [Create a venv](#create-a-virtual-environment-venv) to install the python-packages into locally.
- In the environment you choose to run the Jupyter Notebook, make sure to select the `venv` as the kernel to be run.
- If you'd like to run the notebook in the Jupyter-environment, install Jupyter Notebook
  ```sh
  $ pip install notebook
  ```

## Usage

All the code for running the MIP-solver is present in `lp_solver.ipynb`.

- If you'd like to run the notebook in the Jupyter-environment:
  ```sh
  $ cd src
  $ jupyter notebook --ip 127.0.0.1
  ```

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
