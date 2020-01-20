from ckan.lib.cli import (
    load_config,
    paster_click_group,
    click_config_option
)

import click

from scripts.prh.get_prh_data import PRHData
from scripts.prh.make_csv_of_prh_data import make_csv_of_prh_data


prh_group = paster_click_group(
    summary="Tools for PRH api"
)


@prh_group.command(
    u'fetch-data',
    help='Crawls through PRH api and saves responses as parsed json.'
)
@click.argument(u'BASE_DIR', nargs=1, required=True)
@click.help_option(u'-h', u'--help')
@click_config_option
@click.option(u'-y', u'--year', default=1978, type=click.INT)
@click.option(u'-c', u'--continue_from_previous', is_flag=True, default=True)
@click.option(u'-pid', u'--package_id', required=True)
@click.pass_context
def fetch(ctx, base_dir, year, continue_from_previous, package_id, config):
    load_config(config or ctx.obj['config'])
    PRHData().get_prh_data(base_directory=base_dir, year=year,
                           continue_from_previous=continue_from_previous)
    filename = make_csv_of_prh_data(base_directory=base_dir)

    from scripts.prh.upload_to_ckan import upload_to_ckan
    upload_to_ckan(package_id, filename)
