# advent-of-code

Python [Advent of Code](https://adventofcode.com/) solutions.

I am currently working through Advent of Code 2024.

## Development environment

The following software versions were used to develop this package:

* Python 3.10.15
* Conda 24.11.0

## Development quickstart

```bash
conda env create --file environment.yml
conda install conda-build
conda develop .

conda activate advent-of-code
python advent_of_code --help
```

## Usage

After following steps in development quickstart.

Display the solution to day 1:

```bash
python advent_of_code --day 1
```

Substitute the day you want to see the solution for, as necessary.

Use `python advent_of_code --help` for more information.

## pre-commit

This repository is configured to use [pre-commit](https://pre-commit.com/) hooks.

To install -- after checking out the repository and activating the Conda environmnent
-- run:

```bash
pre-commit install
```

The required pre-commit hooks should then run whenever you commit to this repository.

To manually run pre-commit against all files:

```bash
pre-commit run --all-files
```
