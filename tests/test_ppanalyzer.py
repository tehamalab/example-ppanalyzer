#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ppanalyzer` package."""

from click.testing import CliRunner
from ppanalyzer import cli, get_app


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    help_result = runner.invoke(cli.main, ['--help'])
    assert help_result.exit_code == 0
    assert 'ppanalyzer' in help_result.output


async def test_home(aiohttp_client):
    """Test / GET.

    Home page."""

    client = await aiohttp_client(get_app())
    resp = await client.get('/')
    assert resp.status == 200


async def test_analyze(aiohttp_client):
    """Test /analyze GET.

    Analyze endpoint."""

    client = await aiohttp_client(get_app())
    resp = await client.get('/analyze')
    assert resp.status == 200
