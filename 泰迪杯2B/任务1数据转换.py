from PyPDF2 import PdfReader
from pdfminer.high_level import extract_pages, extract_text
from pdfminer.layout import LTTextContainer, LTChar, LTRect, LTFigure
import pdfplumber
import os
import json
path = './data'
output = './output'
files = os.listdir(path)
for file in files:
    if file.endswith('.pdf'):
        txt = ""
        table = []
        with pdfplumber.open(path+"/"+file) as pdf:
            for page in pdf.pages:
                txt+=page.extract_text()
                table.append(page.extract_table())
        with open(f"{output}/{file}.txt", "w", encoding='utf-8') as f:
            f.write(txt)
        json.dump(table,open(f"{output}/{file}.json", "w", encoding='utf-8'),ensure_ascii=False)  
        
        
        # number_of_pages = len(reader.pages)
        # for i in range(number_of_pages):
        #     page = reader.pages[i]
        #     txt += page.extract_text()
        # with open(f"{output}/{file}.txt", "w", encoding='utf-8') as f:
        #     f.write(txt)
