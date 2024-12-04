"""CLI entrypoint."""

from advent_of_code import _cli, _version, day1, day2


def main():
    """Primary entrypoint for the advent_of_code package."""

    parser = _cli.arg_parser()
    args = _cli.parse_args(parser)

    if args.version:
        print(_version.version_info())
        return

    day1.main()
    day2.main()


if __name__ == "__main__":
    SystemExit(main())
