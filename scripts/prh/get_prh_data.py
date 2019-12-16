from json import JSONDecodeError
from requests import HTTPError

from util.prh_util import consts

import requests
import json
import datetime

import os.path
import os

industries = consts.ALL_INDUSTRIES

selected_years = [yr for yr in range(2018, 2019)]

failed_requests = []
missing_details_uris = []


class PRHData:

    directory = None
    processed_year = None

    def get_prh_data(self, base_directory="", year=2018, continue_from_previous=True):

        while self.processed_year is not datetime.datetime.now().year:
            try:
                with open(os.path.join(base_directory, 'data', 'json', 'prh_data', 'processed_year.txt'), 'r') as year_file:
                    self.processed_year = int(year_file.read())
            except FileNotFoundError:
                print("No previously processed year")

            if continue_from_previous and self.processed_year:
                year = self.processed_year + 1

            self.directory = os.path.join(
                base_directory,
                'data',
                'json',
                'prh_data',
                str(year))

            os.makedirs(self.directory, exist_ok=True)

            processed = 0
            print('Now processing year: {}'.format(year))
            processed += self.write_company_data(year)
            print('Handled {} companies'.format(processed))

            with open(os.path.join(base_directory, 'data', 'json', 'prh_data', year, "failed_requests"),
                      'w') as outfile:
                json.dump(failed_requests, outfile)
            with open(os.path.join(base_directory, 'data', 'json', 'prh_data', year, "missing_details_uris"),
                      'w') as outfile:
                json.dump(missing_details_uris, outfile)

            with open(os.path.join(base_directory, 'data', 'json', 'prh_data', 'processed_year.txt'), 'w') as year_file:
                year_file.write(year)
                year_file.close()

    def write_company_data(self, year):
        total_company_amount = 0
        for businessline_id in industries:

            print("Business line id: {}".format(businessline_id))

            company_dict = {}
            file_name = 'year_{}_industry _{}.json'.format(year, businessline_id)

            full_path = self.directory + file_name
            print("Full path: {}".format(full_path))
            #  Check if the businessline for the year has already been processed
            if os.path.isfile(full_path):
                print('Businessline already processed')
                continue

            periods = [
                ("{}-01-01".format(year), "{}-01-31".format(year)),
                ("{}-02-01".format(year), "{}-02-29".format(year)),
                ("{}-03-01".format(year), "{}-03-31".format(year)),

                ("{}-04-01".format(year), "{}-04-30".format(year)),
                ("{}-05-01".format(year), "{}-05-31".format(year)),
                ("{}-06-01".format(year), "{}-06-30".format(year)),

                ("{}-07-01".format(year), "{}-07-31".format(year)),
                ("{}-08-01".format(year), "{}-08-31".format(year)),
                ("{}-07-01".format(year), "{}-09-30".format(year)),

                ("{}-10-01".format(year), "{}-10-31".format(year)),
                ("{}-11-01".format(year), "{}-11-30".format(year)),
                ("{}-12-01".format(year), "{}-12-31".format(year))
            ]

            for period in periods:
                date_start = period[0]
                date_end = period[1]

                response_data = self.get_business_line_data(
                    businessline_id, date_start, date_end)
                if response_data == 'over 1000 results':
                    break

                if not response_data:
                    continue

                total_company_amount += len(response_data)

                for row in response_data:
                    try:
                        if row["detailsUri"]:
                            resp = requests.get(row["detailsUri"])
                            resp.raise_for_status()
                            details_response = json.loads(resp.content)

                            if len(details_response["results"]) > 0:
                                details = details_response["results"][0]
                                company_dict[row['name']] = details
                        else:
                            company_dict[row['name']] = row
                            missing_details_uris.append(row['businessId'])
                    except JSONDecodeError as e:
                        print("Error: {}".format(e.msg))
                    except HTTPError as e:
                        failed_requests.append(row["detailsUri"])
                        print("Error: {}".format(e.errno))

            if company_dict:
                with open(self.directory + '/{}'.format(file_name),
                          'w') as outfile:
                    json.dump(company_dict, outfile)

        return total_company_amount


    def get_business_line_data(self, id, date_start, date_end):

        if id < 10:
            id = '0{}'.format(id)

        url = "http://avoindata.prh.fi:80/bis/v1?totalResults=false&maxResults=1000&resultsFrom=0&businessLineCode={}&companyRegistrationFrom={}&companyRegistrationTo={}".format(
            id, date_start, date_end)

        try:
            print("trying url {}".format(url))
            json_response = requests.get(url).content
        except HTTPError as e:
            print("Error: {}".format(e.errno))
            return None

        response_data = json.loads(json_response)["results"]
        print('Period {}/{}'.format(date_start, date_end))
        print("Amount of results: " + str(len(response_data)))
        print()

        if len(response_data) > 999:
            print("This business line has over 1000 companies in this timeperiod")
            print(id)
            return response_data

        return response_data
