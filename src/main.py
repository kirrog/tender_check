import json
from datetime import datetime

from fuzzywuzzy import fuzz
from natasha import MorphVocab
from natasha import (
    NamesExtractor,
    AddrExtractor,
    DatesExtractor,
    MoneyExtractor
)

from src.parser import parse_data_from_url

morph_vocab = MorphVocab()
# namesExtractor = NamesExtractor(morph_vocab)
# addrExtractor = AddrExtractor(morph_vocab)
datesExtractor = DatesExtractor(morph_vocab)
moneyExtractor = MoneyExtractor(morph_vocab)


def search_task(value_, text_: str, text_extracted, dates_facts, money_facts, task_type):
    result = dict()
    if type(value_) in [int, float]:
        value_ = str(value_)
    result["value_"] = value_
    if type(value_) == str:
        result["type"] = "str"
        result["exists"] = value_.lower() in text_.lower()
        result["leven_partial_ratio"] = fuzz.partial_ratio(value_.lower(), text_.lower())
    else:
        result["type"] = str(type(value_))
        result["exists"] = None
        result["leven_partial_ratio"] = None

    if task_type == "date_search" and value_ is not None:
        d = datetime.strptime(value_[:10], '%d.%m.%Y')
        day_ = d.day
        month_ = d.month
        year_ = d.year
        result["extractor_match"] = False
        for start, stop, year, month, day in dates_facts:
            if str(day) == str(day_) and str(month) == str(month_) and str(year) == str(year_):
                result["extractor_match"] = True

    if task_type == "money" and value_ is not None:
        money = float(value_)
        result["extractor_match"] = False
        for start, stop, amount, currency in money_facts:
            if currency == "RUB" and float(amount) == money:
                result["extractor_match"] = True

    return result


# def process_by_addr_extractor(text):
#     text_list = []
#     facts = []
#     last_pos = 0
#     for match in addrExtractor(text):
#         text_list.append(text[last_pos:match.start])
#         text_list.append("<addr>")
#         last_pos = match.stop
#         facts.append((match.start, match.stop, match.fact.type, match.fact.value))
#     text_list.append(text[last_pos:])
#     return " ".join(" ".join(text_list).split()), facts


def process_by_dates_extractor(text):
    text_list = []
    facts = []
    last_pos = 0
    for match in datesExtractor(text):
        text_list.append(text[last_pos:match.start])
        text_list.append("<date>")
        last_pos = match.stop
        facts.append((match.start, match.stop, match.fact.year, match.fact.month, match.fact.day))
    text_list.append(text[last_pos:])
    return " ".join(" ".join(text_list).split()), facts


def process_by_money_extractor(text):
    text_list = []
    facts = []
    last_pos = 0
    for match in moneyExtractor(text):
        text_list.append(text[last_pos:match.start])
        text_list.append("<money>")
        last_pos = match.stop
        facts.append((match.start, match.stop, match.fact.amount, match.fact.currency))
    text_list.append(text[last_pos:])
    return " ".join(" ".join(text_list).split()), facts


def extract_project_and_technical_texts(resp_json):
    project_dogovor_list = [x["text"] for x in resp_json['files'] if
                            x["type"] == "pdf"
                            or "проект контракта" in x["name"].lower()
                            or "проект договора" in x["name"].lower()
                            ]
    project_dogovor_text_raw = project_dogovor_list[0] if len(project_dogovor_list) > 0 else None
    if project_dogovor_text_raw:
        project_dogovor_text = project_dogovor_text_raw
        # project_dogovor_text, project_dogovor_addr_facts = process_by_addr_extractor(project_dogovor_text)
        project_dogovor_addr_facts = None
        project_dogovor_text, project_dogovor_dates_facts = process_by_dates_extractor(project_dogovor_text)
        project_dogovor_text, project_dogovor_money_facts = process_by_money_extractor(project_dogovor_text)
    else:
        (project_dogovor_text, project_dogovor_addr_facts,
         project_dogovor_dates_facts, project_dogovor_money_facts) = None, None, None, None
    technical_task_list = [x["text"] for x in resp_json['files'] if x["type"] == "docs"
                           or "тз" in x["name"].lower()
                           or "техническое задание" in x["name"].lower()
                           or "тех зад" in x["name"].lower()
                           ]
    technical_task_text_raw = technical_task_list[0] if len(technical_task_list) > 0 else None
    if technical_task_text_raw:
        technical_task_text = technical_task_text_raw
        # technical_task_text, technical_task_addr_facts = process_by_addr_extractor(technical_task_text)
        technical_task_addr_facts = None
        technical_task_text, technical_task_dates_facts = process_by_dates_extractor(technical_task_text)
        technical_task_text, technical_task_money_facts = process_by_money_extractor(technical_task_text)
    else:
        (technical_task_text, technical_task_addr_facts,
         technical_task_dates_facts, technical_task_money_facts) = None, None, None, None
    return ((project_dogovor_text_raw, project_dogovor_text, project_dogovor_addr_facts,
             project_dogovor_dates_facts, project_dogovor_money_facts),
            (technical_task_text_raw, technical_task_text, technical_task_addr_facts,
             technical_task_dates_facts, technical_task_money_facts))


def check_case(resp_json):
    project_dogovor_data, technical_task_data = extract_project_and_technical_texts(resp_json)
    (project_dogovor_text_raw, project_dogovor_text, project_dogovor_addr_facts,
     project_dogovor_dates_facts, project_dogovor_money_facts) = project_dogovor_data
    (technical_task_text_raw, technical_task_text, technical_task_addr_facts,
     technical_task_dates_facts, technical_task_money_facts) = technical_task_data

    task_list = []

    task_list.append(("name", resp_json["name"], None))
    task_list.append(("isContractGuaranteeRequired", resp_json["isContractGuaranteeRequired"], None))
    task_list.append(("contractGuaranteeAmount", resp_json["contractGuaranteeAmount"], "money"))

    for i in range(len(resp_json["licenseFiles"])):
        task_list.append((f"licenseFiles_{i}_name", resp_json["licenseFiles"][i]["fileName"], None))

    task_list.append(("startCost", resp_json["startCost"], "money"))
    task_list.append(("lastBetCost", resp_json["lastBetCost"], "money"))

    task_list.append(("startDate", resp_json["startDate"], "date_search"))
    task_list.append(("endDate", resp_json["endDate"], "date_search"))

    for i in range(len(resp_json["deliveries"])):
        task_list.append(
            (f"deliveries_{i}_periodDateFrom", resp_json["deliveries"][i]["periodDateFrom"], "date_search"))
        task_list.append((f"deliveries_{i}_periodDateTo", resp_json["deliveries"][i]["periodDateTo"], "date_search"))

    for i in range(len(resp_json["items"])):
        task_list.append((f"items_{i}_currentValue", resp_json["items"][i]["currentValue"], None))
        task_list.append((f"items_{i}_costPerUnit", resp_json["items"][i]["costPerUnit"], "money"))
        task_list.append((f"items_{i}_okeiName", resp_json["items"][i]["okeiName"], None))
        task_list.append((f"items_{i}_okpdName", resp_json["items"][i]["okpdName"], None))
        task_list.append((f"items_{i}_productionDirectoryName", resp_json["items"][i]["productionDirectoryName"], None))
        task_list.append((f"items_{i}_name", resp_json["items"][i]["name"], None))

    answers = {"project": dict(), "technical": dict()}
    for name, value_, task_type in task_list:
        if project_dogovor_text_raw:
            answers["project"][name] = search_task(value_, project_dogovor_text_raw, project_dogovor_text,
                                                   project_dogovor_dates_facts,
                                                   project_dogovor_money_facts, task_type)
        if technical_task_text_raw:
            answers["technical"][name] = search_task(value_, technical_task_text_raw, technical_task_text,
                                                     technical_task_dates_facts,
                                                     technical_task_money_facts, task_type)
    return answers


if __name__ == "__main__":
    case_id = "9869909"
    url = f"https://zakupki.mos.ru/auction/{case_id}"
    resp_json = parse_data_from_url(url)

    answers = check_case(resp_json)

    with open(f"../data/{case_id}.json", "w", encoding="utf-8") as f:
        json.dump(answers, f, ensure_ascii=False)
