import sys
from argparse import ArgumentParser

from scripts.prh.get_prh_data import get_prh_data

usage = "usage: something here"

parser = ArgumentParser(prog='PROG')
parser.add_argument('BASE_DIR',  help="Directory where files are stored.")
parser.add_argument('-i', '--import', dest='source', help="import data from source (default: PRH)", default="prh")
parser.add_argument('-y', '--year', dest="year", help="starting year")

args = parser.parse_args()
if len(vars(args)) == 0:
    parser.print_help()
    sys.exit(1)

print(args)
if args.source:
    if args.source == "prh":
        get_prh_data(base_directory=args.BASE_DIR, year=args.year)
