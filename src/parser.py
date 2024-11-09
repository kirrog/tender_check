import argparse
from pprint import pprint

import requests

parser = argparse.ArgumentParser(description='Parse KC')
parser.add_argument('-url','--url', help='URL for KC', required=True)
args = parser.parse_args()

resp = requests.get(f'https://zakupki.mos.ru/newapi/api/Auction/Get?auctionId={args.url.rsplit("/", 1)[-1]}')
pprint(resp.json())