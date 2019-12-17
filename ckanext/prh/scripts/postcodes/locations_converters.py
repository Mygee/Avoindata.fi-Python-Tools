import pathlib

from util.geo_util import csv_to_json
from scripts.postcodes import opt_to_csv


# A function to convert multiple OPT files to CSV
def convert_opt_to_csv():
    path = pathlib.Path("./data/opt/postcodes/")
    for fname in path.glob('*.OPT'):
        print('Now processing {}'.format({fname}))
        opt_to_csv.convert(fname)


# A function that creates an JSON version of data
def convert_csv_to_json():
    path = pathlib.Path('./csv/')
    for fname in path.glob('*.csv'):
        print('Now processing {}'.format({fname}))
        csv_to_json.godi_data(fname)


# #  Testing accuracy of geo conversion
# def test_etrs_to_wgs84_conversion_accuracy():
#     northern = 7047819
#     eastern = 382272
#     address = 'Kangasvierentie 53 Lestijarvi'

#     test_geo_conversion.test(northern, eastern, address)
