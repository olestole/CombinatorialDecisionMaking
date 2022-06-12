# VLSI Design

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#constraint-programming-cp">Constraint Programming (CP)</a>
    </li>
    <li>
      <a href="#propositional-satisfiability-sat">Propositional Satisfiability (SAT)</a>
    </li>
    <li>
      <a href="#linear-programming-lp">Linear Programming (LP)</a>
    </li>
    <li>
      <a href="#misc">Misc</a>
    </li>
  </ol>
</details>

## About The Project

Projectwork for [Combinatorial Decision Making and Optimization](https://www.unibo.it/en/teaching/course-unit-catalogue/course-unit/2021/446597), University of Bologna 2022. This project aims to solve the problem of VLSI (Very Large Scale Integration) - trend of integrating circuits into silicon chips. Given a fixed-width plate and a list of rectangular circuits, the goal is to place the circuits on the plate in order to minimize the length of the fixed-width plate.

The problem has been solved using three different approaches; [Constraint Programming (CP)](#constraint-programming-cp), [Propositional Satisfiability (SAT)](#propositional-satisfiability-sat), and [Linear Programming (LP)](#linear-programming-lp).

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
$ cd CP
$ ./minizinc_solver.py
```

**Options**

- Specify the model to be used by specifying option `-m <model_path>`
  - All the CP-models can be found under `CP/models`.
- Specify if you'd like to use Chuffed or GeCode with option `-s <chuffed|gecode>`
- Specify the range of instances you'd like to solve with option `-r <range>`, e.g. `-r 2-9`

The solver will output all the run-results to `/cp_solutions`.

# Propositional Satisfiability (SAT)

## Getting Started

### Prerequisites

- [Create a venv](#create-a-virtual-environment-venv) to install the python-packages into locally.
- In the environment you choose to run the Jupyter Notebook, make sure to select the `venv` as the kernel to be run.
- If you'd like to run the notebook in the Jupyter-environment, install Jupyter Notebook
  ```sh
  $ pip install notebook
  ```

## Usage

All the code for running the SAT-solver is present in `sat_solver.ipynb`.

- If you'd like to run the notebook in the Jupyter-environment:
  ```sh
  $ cd SAT
  $ jupyter notebook --ip 127.0.0.1
  ```

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
  $ cd MIP
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
