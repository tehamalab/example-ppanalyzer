# -*- coding: utf-8 -*-

"""Console script for ppanalyzer."""
import sys
import click
from .ppanalyzer import web


@click.command()
@click.option('--port', '-p', help='port', default=8080, type=int)
def main(port=8080):
    """Runner for ppanalyzer web app."""
    click.echo("Start ppanalyzer web app ...")
    web(port=port)
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
