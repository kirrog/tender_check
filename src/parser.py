import argparse
from pprint import pprint

import requests

parser = argparse.ArgumentParser(description='Parse KC')
parser.add_argument('-url','--url', help='URL for KC', required=True)
args = parser.parse_args()

resp = requests.get(f'https://zakupki.mos.ru/newapi/api/Auction/Get?auctionId={args.url.rsplit("/", 1)[-1]}')
resp_json = resp.json()

for item in resp_json['items']:
    item_resp = requests.get(f'https://zakupki.mos.ru/newapi/api/Auction/GetAuctionItemAdditionalInfo?itemId={item["id"]}')
    item['specification'] = item_resp.json()


for file in resp_json['files']:
    url = f'https://zakupki.mos.ru/newapi/api/FileStorage/Download?id={file["id"]}'
    file['data'] = b''

    r = requests.get(url)
    for chunk in r.iter_content(chunk_size=512 * 1024):
        if chunk:
            file['data'] += chunk

pprint(resp_json)
