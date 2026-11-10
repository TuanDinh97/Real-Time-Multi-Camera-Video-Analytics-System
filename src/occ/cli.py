"""Entry point for the `occ` command."""

import argparse
from importlib.metadata import version


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="occ", description="Indoor occupancy system")
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {version('indoor-occupancy')}",
    )
    parser.parse_args(argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())