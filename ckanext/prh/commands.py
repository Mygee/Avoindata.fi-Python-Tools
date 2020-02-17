import os
import shutil
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path  # python 2 backport

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
@click.option(u'-s', u'--start-from-beginning', is_flag=True)
@click.option(u'-pid', u'--package_id', required=True)
@click.pass_context
def fetch(ctx, base_dir, year, start_from_beginning, package_id, config):
    load_config(config or ctx.obj['config'])

    if Path(os.path.join(base_dir, 'data', 'json', 'prh_data', 'all_done.txt')).is_file():
        print("Nothing to do")

    else:
        PRHData().get_prh_data(base_directory=base_dir, year=year,
                               start_from_beginning=start_from_beginning)
        filename = make_csv_of_prh_data(base_directory=base_dir)
        from scripts.prh.upload_to_ckan import upload_to_ckan
        upload_to_ckan(package_id, filename)

        with open(os.path.join(base_dir, 'data', 'json', 'prh_data', 'all_done.txt'), 'w') as done_file:
            done_file.write("done")
            done_file.close()

@prh_group.command(
    u'clear',
    help="Clears fetched data"
)
@click.argument(u'BASE_DIR', nargs=1, required=True)
@click.help_option(u'-h', u'--help')
@click_config_option
@click.pass_context
def clear(ctx, base_dir, config):
    load_config(config or ctx.obj['config'])
    try:
        shutil.rmtree(os.path.join(base_dir, 'data', 'json', 'prh_data'))
    except OSError:
        print("Directory does not exist")
