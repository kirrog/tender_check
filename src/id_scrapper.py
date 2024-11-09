import json

import requests
from tqdm import tqdm

from src.main import check_case
from src.parser import parse_data_from_url

if __name__ == "__main__":
    resp = requests.get(
        'https://old.zakupki.mos.ru/api/Cssp/Purchase/Query?queryDto=%20%7B%0A%20%20%20%20%20%20%20%20%22filter%22%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22typeIn%22%3A%5B1%5D%2C%22auctionSpecificFilter%22%3A%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22stateIdIn%22%3A%5B19000002%2C19000005%2C19000003%2C19000004%2C19000008%5D%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22needSpecificFilter%22%3A%7B%7D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22tenderSpecificFilter%22%3A%7B%7D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22ptkrSpecificFilter%22%3A%7B%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%7D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%22order%22%3A%5B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7B%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22field%22%3A%22relevance%22%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%22desc%22%3Atrue%0A%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%20%7D%0A%20%20%20%20%20%20%20%20%20%20%20%20%5D%2C%0A%20%20%20%20%20%20%20%20%20%20%20%20%22withCount%22%3Atrue%2C%22take%22%3A500%2C%22skip%22%3A500%0A%0A%20%20%20%20%7D')
    resp = resp.json()
    for case in tqdm(list(resp['items'])):
        case_id = case['auctionId']

        url = f"https://zakupki.mos.ru/auction/{case_id}"
        resp_json = parse_data_from_url(url)

        with open(f"../data/resp/{case_id}.json", "w", encoding="utf-8") as f:
            json.dump(resp_json, f, ensure_ascii=False)

        answers = check_case(resp_json)

        with open(f"../data/checks/{case_id}.json", "w", encoding="utf-8") as f:
            json.dump(answers, f, ensure_ascii=False)
