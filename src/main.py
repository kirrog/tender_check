import json

from fuzzywuzzy import fuzz

from src.parser import parse_data_from_url


def search_task(value_: str, text_: str):
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
    return result


def check_case(resp_json):
    project_dogovor_list = [x["text"] for x in resp_json['files'] if
                            x["type"] == "pdf"
                            or "проект контракта" in x["name"].lower()
                            or "проект договора" in x["name"].lower()
                            ]
    project_dogovor_text = project_dogovor_list[0] if len(project_dogovor_list) > 0 else None
    technical_task_list = [x["text"] for x in resp_json['files'] if x["type"] == "docs"
                           or "тз" in x["name"].lower()
                           or "техническое задание" in x["name"].lower()
                           or "тех зад" in x["name"].lower()
                           ]
    technical_task_text = technical_task_list[0] if len(technical_task_list) > 0 else None

    task_list = []

    task_list.append(("name", resp_json["name"]))
    task_list.append(("isContractGuaranteeRequired", resp_json["isContractGuaranteeRequired"]))
    task_list.append(("contractGuaranteeAmount", resp_json["contractGuaranteeAmount"]))

    for i in range(len(resp_json["licenseFiles"])):
        task_list.append((f"licenseFiles_{i}", resp_json["licenseFiles"][i]))

    task_list.append(("startCost", resp_json["startCost"]))
    task_list.append(("lastBetCost", resp_json["lastBetCost"]))

    task_list.append(("startDate", resp_json["startDate"]))
    task_list.append(("endDate", resp_json["endDate"]))

    for i in range(len(resp_json["deliveries"])):
        task_list.append((f"deliveries_{i}_periodDateFrom", resp_json["deliveries"][i]["periodDateFrom"]))
        task_list.append((f"deliveries_{i}_periodDateTo", resp_json["deliveries"][i]["periodDateTo"]))

    for i in range(len(resp_json["items"])):
        task_list.append((f"items_{i}_currentValue", resp_json["items"][i]["currentValue"]))
        task_list.append((f"items_{i}_costPerUnit", resp_json["items"][i]["costPerUnit"]))
        task_list.append((f"items_{i}_okeiName", resp_json["items"][i]["okeiName"]))
        task_list.append((f"items_{i}_okpdName", resp_json["items"][i]["okpdName"]))
        task_list.append((f"items_{i}_productionDirectoryName", resp_json["items"][i]["productionDirectoryName"]))
        task_list.append((f"items_{i}_name", resp_json["items"][i]["name"]))

    answers = {"project": dict(), "technical": dict()}
    for name, value_ in task_list:
        if project_dogovor_text:
            answers["project"][name] = search_task(value_, project_dogovor_text)
        if technical_task_text:
            answers["technical"][name] = search_task(value_, technical_task_text)
    return answers


if __name__ == "__main__":
    case_id = "9864533"
    url = f"https://zakupki.mos.ru/auction/{case_id}"
    resp_json = parse_data_from_url(url)

    answers = check_case(resp_json)

    with open(f"../data/{case_id}.json", "w", encoding="utf-8") as f:
        json.dump(answers, f, ensure_ascii=False)
