import os
import shutil
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path  # python 2 backport


import click

from .scripts.prh.get_prh_data import PRHData
from .scripts.prh.make_csv_of_prh_data import make_csv_of_prh_data


@click.group()
def prh_tools():
    "Tools for PRH api"
    pass


@prh_tools.command(
    u'fetch-data',
    help='Crawls through PRH api and saves responses as parsed json.'
)
@click.argument(u'BASE_DIR', nargs=1, required=True)
@click.help_option(u'-h', u'--help')
@click.option(u'-y', u'--year', default=1978, type=click.INT)
@click.option(u'-s', u'--start-from-beginning', is_flag=True)
@click.option(u'-pid', u'--package_id', required=True)
@click.pass_context
def fetch(ctx, base_dir, year, start_from_beginning, package_id):


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


@prh_tools.command(
    u'clear',
    help="Clears fetched data"
)
@click.argument(u'BASE_DIR', nargs=1, required=True)
@click.help_option(u'-h', u'--help')
@click.pass_context
def clear(ctx, base_dir):
    try:
        shutil.rmtree(os.path.join(base_dir, 'data', 'json', 'prh_data'))
    except OSError:
        print("Directory does not exist")
