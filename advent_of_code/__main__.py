"""CLI entrypoint."""

from advent_of_code import _cli, _version, day1, day2, day3


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
        day1.main()
        return
    if args.day == 2:
        day2.main()
        return
    if args.day == 3:
        day3.main()
        return

    raise IndexError("No solution for specified day yet")


if __name__ == "__main__":
    SystemExit(main())
