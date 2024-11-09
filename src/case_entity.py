from pathlib import Path
from typing import Dict

class ProductEntity:
    name:str
    quantity:int
    cost:float
    final_cost:float
    other_data = dict()

class CaseEntity:
    data: Dict
    tech_task: str
    project_contract: str


if __name__ == "__main__":
    from src.load_pdf import read_pdf2text
    from src.load_word import read_word2text

    data = {
        "zakup_name": "ЗАПАСНЫЕ ЧАСТИ ДЛЯ ТРАНСПОРТНЫХ СРЕДСТВ",  # Check if it can be founded in texts
        "usl_isp_contr": "Обязательное электронное исполнение с использованием УПД",
        "obesp_isp_contr": "Не требуется",
        # if not "не требуется" -> check exists in техническом задании и/или в проекте контракта
        "nal_sertif|lic": [],
        # if has list of licenses -> such list should be in техническом задании и/или в проекте контракта
        "graphic_postvki": "", # dates or days period should be in техническом задании и/или в проекте контракта
        "steps_postavki": [], # such list of steps should be in техническом задании и/или в проекте контракта
        "max_price": "10", # if exists -> should be the same in техническом задании и/или в проекте контракта or
        "start_price": "10", # if exists -> should be final value («Цена Контракта») in техническом задании и/или в проекте контракта
        "products": []
    }
    tech_task = read_word2text(
        Path("/home/kirrog/projects/hackatons/tender_check/cases/9864533/ТЗ № П-ПУиЗР-2024.docx")) # if exists -> check if characteristics and quantity exists
    # If in tech task there are more characteristics - return mark about it
    project_contract = read_pdf2text(
        Path("/home/kirrog/projects/hackatons/tender_check/cases/9864533/Проект контракта.pdf"))
