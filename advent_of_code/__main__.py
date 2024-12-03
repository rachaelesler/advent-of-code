"""CLI entrypoint."""

from advent_of_code import _cli, _version, day_one


def main():
    """Primary entrypoint for the advent_of_code package."""

    parser = _cli.arg_parser()
    args = _cli.parse_args(parser)

    if args.version:
        print(_version.version_info())
        return

    day_one.main()


if __name__ == "__main__":
    SystemExit(main())
