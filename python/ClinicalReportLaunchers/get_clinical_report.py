"""Get a clinical report, either with extended information or not.
Example usages:
 python get_clinical_report.py 1801
 python get_clinical_report.py 1801 --e true
"""

import os
import requests
from requests.auth import HTTPBasicAuth
import sys
import simplejson as json
import argparse

# Load environment variables for request authentication parameters
if "FABRIC_API_PASSWORD" not in os.environ:
    sys.exit("FABRIC_API_PASSWORD environment variable missing")

if "FABRIC_API_LOGIN" not in os.environ:
    sys.exit("FABRIC_API_LOGIN environment variable missing")

FABRIC_API_LOGIN = os.environ['FABRIC_API_LOGIN']
FABRIC_API_PASSWORD = os.environ['FABRIC_API_PASSWORD']
FABRIC_API_URL = os.environ.get('FABRIC_API_URL', 'https://api.fabricgenomics.com')
auth = HTTPBasicAuth(FABRIC_API_LOGIN, FABRIC_API_PASSWORD)


def get_clinical_report(cr_id, extended=False):
    """Use the Omicia API to get a clinical report, either with or without
    extended variant and fields information
    """
    # Construct request
    url = "{}/reports/{}/"
    if extended:
        url += "?extended=True"
    url = url.format(FABRIC_API_URL, cr_id)

    sys.stdout.flush()
    result = requests.get(url, auth=auth)
    return result.json()


def main():
    """Main function. Get a clinical report by ID.
    """
    parser = argparse.ArgumentParser(description='Fetch a clinical report')
    parser.add_argument('c', metavar='clinical_report_id', type=int)
    parser.add_argument('--e', metavar='extended', type=bool, default=False)
    args = parser.parse_args()

    cr_id = args.c
    extended = args.e

    json_response = get_clinical_report(cr_id, extended=extended)
    sys.stdout.write(json.dumps(json_response, indent=4))

if __name__ == "__main__":
    main()
