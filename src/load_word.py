from pathlib import Path

import docx


def read_pdf2text(pdf_file_path: Path) -> str:
    doc = docx.Document(str(pdf_file_path))
    texts = []
    for paragraph in doc.paragraphs:
        texts.append(paragraph.text)
    return " ".join(" ".join(texts).split())


if __name__ == "__main__":
    file_path = Path('/home/kirrog/projects/hackatons/tender_check/cases/9864533/ТЗ № П-ПУиЗР-2024.docx')
    text = read_pdf2text(file_path)
    print(text)
