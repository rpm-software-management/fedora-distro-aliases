import click

from fedora_distro_aliases import get_distro_aliases

GETTERS = {
    "namever": lambda x: x.namever,
    "branch": lambda x: x.branch,
    "version": lambda x: x.version,
}


@click.command()
@click.option(
    "-o",
    "--output-type",
    type=click.Choice(("namever", "branch", "version"), case_sensitive=False),
    default="namever",
    help="""Choose the output format of the script.

    Available options:\n
    * namever — e.g., ‹fedora-40›\n
    * branch — e.g., ‹f40›\n
    * version — e.g., ‹40›
    """
)
@click.argument("aliases", required=True, nargs=-1)
def cli(aliases: list[str], output_type: str):
    """Resolve the requested aliases.

    Resolve each of the ALIASES and print them out.

    This script prints out only unique aliases i.e., it is not possible to
    obtain the same alias twice in the output.
    """
    getter = GETTERS[output_type]
    distro_aliases = get_distro_aliases()

    resolved_aliases: set[str] = set()
    for alias in aliases:
        resolved_aliases.update(getter(x) for x in distro_aliases[alias])

    print(" ".join(resolved_aliases))
