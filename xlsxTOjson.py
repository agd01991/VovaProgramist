import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from xls2xlsx import XLS2XLSX
import os
import configparser
import re

file_path = 'C:/Users/agd01/Documents/VovaProgramist/Raspisanie-FIT-ochnaya-f.o-23_24-vesenniy-sem.-APREL.xlsx'

sheet_names = ['1 курс', '1 курс ', '2 курс', '2 курс ', '3 курс', '3 курс ']

schedule = {}

for sheet in sheet_names:
    try:
        data = pd.read_excel(file_path, sheet_name=sheet, header=None)
    except ValueError:
        print(f"Лист '{sheet}' не найден в файле.")
        continue

    for index, row in data.iterrows():
        if pd.notnull(row[1]) and isinstance(row[1], datetime):
            date = row[1].strftime('%Y-%m-%d')
            for i in range(11):  # вместо 0, 11 чтобы использовать range корректно
                if index + i < len(data) and pd.notnull(data.iloc[index + i][2]):
                    time = data.iloc[index + i][2]
                    if sheet not in schedule:
                        schedule[sheet] = {}
                    if date not in schedule[sheet]:
                        schedule[sheet][date] = {}
                    if time not in schedule[sheet][date]:
                        schedule[sheet][date][time] = []
                    if pd.notnull(data.iloc[index + i][3]):
                        subject = data.iloc[index + i][3]
                        full_info = data.iloc[index + i + 1][3]
                        if type(full_info) == str:
                            match_name = re.search(r"([А-ЯЁ][а-яё]+ [А-ЯЁ]\.[А-ЯЁ]\.)", full_info)
                            teacher_name = match_name.group(1) if match_name else ''
                            match_classroom = re.search(r"(ауд\. \d+)", full_info)
                            classroom = match_classroom.group(1) if match_classroom else ''
                        entery = {}
                        entery['subject'] = subject
                        entery['teacher_name'] = teacher_name
                        entery['classroom'] = classroom
                        entery['full_info'] = full_info
                        schedule[sheet][date][time].append(entery)
                    if pd.notnull(data.iloc[index + i][4]):
                        subject = data.iloc[index + i][4]
                        full_info = data.iloc[index + i + 1][4]
                        if type(full_info) == str:
                            match_name = re.search(r"([А-ЯЁ][а-яё]+ [А-ЯЁ]\.[А-ЯЁ]\.)", full_info)
                            teacher_name = match_name.group(1) if match_name else ''
                            match_classroom = re.search(r"(ауд\. \d+)", full_info)
                            classroom = match_classroom.group(1) if match_classroom else ''
                        entery = {}
                        entery['subject'] = subject
                        entery['teacher_name'] = teacher_name
                        entery['classroom'] = classroom
                        entery['full_info'] = full_info
                        schedule[sheet][date][time].append(entery)
    
# print(schedule['1 курс']['2024-04-01']['11:40-13:10'][0])
print(schedule)