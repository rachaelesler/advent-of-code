"""CLI entrypoint."""

from advent_of_code import _cli, _version
from advent_of_code.day01 import day01
from advent_of_code.day02 import day02
from advent_of_code.day03 import day03
from advent_of_code.day04 import day04


def main():
    """Primary entrypoint for the advent_of_code package."""

    parser = _cli.arg_parser()
    args = _cli.parse_args(parser)

    if args.version:
        print(_version.version_info())
        return

    if not args.day:
        raise ValueError("No day specified")

    if args.day == 1:
        day01.main()
        return
    if args.day == 2:
        day02.main()
        return
    if args.day == 3:
        day03.main()
        return
    if args.day == 4:
        day04.main()
        return

    raise IndexError("No solution for specified day yet")


if __name__ == "__main__":
    SystemExit(main())
