"""Command-line entrypoints for this package."""

from __future__ import annotations

import argparse


def arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="advent-of-code",
        description="Solutions for Advent of Code 2024",
    )

    parser.add_argument(
        "--version",
        dest="version",
        action="store_true",
        help="Display tool version",
    )

    return parser


def parse_args(parser: argparse.ArgumentParser) -> argparse.Namespace:
    return parser.parse_args()
