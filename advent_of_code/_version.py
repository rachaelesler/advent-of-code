"""CLI Versioning."""

from typing import Optional

from pkg_resources import DistributionNotFound, get_distribution

__version__: Optional[str]
try:
    __version__ = get_distribution(__package__).version
except DistributionNotFound:
    __version__ = None


def version_info() -> str:
    """Return package version information."""
    # pylint: disable=import-outside-toplevel
    import os
    import platform
    import sys

    info = {
        "advent-of-code version": __version__,
        "install path": os.path.dirname(os.path.abspath(__file__)),
        "python version": sys.version,
        "platform": platform.platform(),
    }
    return "\n".join(
        "{:>30} {}".format(k + ":", str(v).replace("\n", " "))
        for k, v in info.items()
    )


__all__ = ["__version__", "version_info"]
