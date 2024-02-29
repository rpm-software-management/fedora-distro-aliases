import argparse
import sys

from fedora_distro_aliases import get_distro_aliases

GETTERS = {
    "namever": lambda x: x.namever,
    "branch": lambda x: x.branch,
    "version": lambda x: x.version,
}


def run(output_type: str, aliases: list[str]):
    getter = GETTERS[output_type]
    distro_aliases = get_distro_aliases()

    resolved_aliases: set[str] = set()
    for alias in aliases:
        resolved_aliases.update(getter(x) for x in distro_aliases[alias])

    print(" ".join(resolved_aliases))


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="""Resolve the requested aliases.

        Resolve each of the ALIASES and print them out.

        This script prints out only unique aliases i.e., it is not
        possible to obtain the same alias twice in the output.
        """
    )

    # Handle the output type
    parser.add_argument(
        "-o", "--output-type",
        choices=["namever", "branch", "version"],
        default="namever",
        help="""Choose the output format of the script.

        Available options are namever (e.g., ‹fedora-40›), branch (e.g., ‹f40›),
        or version (e.g., ‹40›).
        """
    )

    # Handle the aliases themselves
    parser.add_argument(
        "aliases",
        nargs="+"
    )
    
    return parser


def main(argv=sys.argv[1:]):
    argv = sys.argv[1:]

    parser = setup_parser()
    args = parser.parse_args(argv)

    run(args.output_type, args.aliases)


if __name__ == '__main__':
    main()
