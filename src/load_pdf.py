from pathlib import Path

import PyPDF2


def read_pdf2text(pdf_file_path: Path) -> str:
    reader = PyPDF2.PdfReader(str(pdf_file_path))
    pdf_texts = []
    for i in range(len(reader.pages)):
        page_text = reader.pages[i].extract_text()
        pdf_texts.append(page_text)
    return " ".join(" ".join(pdf_texts).split())


if __name__ == "__main__":
    file_path = Path('/home/kirrog/projects/hackatons/tender_check/cases/9869988/Проект контракта.pdf')
    text = read_pdf2text(file_path)
    print(text)
