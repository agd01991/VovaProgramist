import pandas as pd
from datetime import datetime
import re

file_path = 'C:/Users/agd01/Documents/VovaProgramist/Raspisanie-FIT-ochnaya-f.o-23_24-vesenniy-sem.-APREL.xlsx'

sheet_names = ['1 курс', '1 курс ', '2 курс', '2 курс ', '3 курс', '3 курс ']

schedule = {}

def add_to_schedule(data: pd.DataFrame, schedule: dict, sheet: str, date: str, time: str, i: int, col: int):
    subject = data.iloc[index + i][col]
    full_info = data.iloc[index + i + 1][col]
    if type(full_info) == str:
        match_name = re.search(r"([А-ЯЁ][а-яё]+ [А-ЯЁ]\.[А-ЯЁ]\.)", full_info)
        teacher_name = match_name.group(1) if match_name else ''
        match_classroom = re.search(r"(ауд\. \d+)", full_info)
        classroom = match_classroom.group(1) if match_classroom else ''
    else:
        teacher_name = ''
        classroom = ''
    entery = {}
    entery['subject'] = subject
    entery['teacher_name'] = teacher_name
    entery['classroom'] = classroom
    entery['full_info'] = full_info
    schedule[sheet][date][time].append(entery)

for sheet in sheet_names:
    try:
        data = pd.read_excel(file_path, sheet_name=sheet, header=None)
    except ValueError:
        print(f"Лист '{sheet}' не найден в файле.")
        continue

    for index, row in data.iterrows():
        if pd.notnull(row[1]) and isinstance(row[1], datetime):
            date = row[1].strftime('%Y-%m-%d')
            for i in range(11):
                if index + i < len(data) and pd.notnull(data.iloc[index + i][2]):
                    time = data.iloc[index + i][2]
                    if sheet not in schedule:
                        schedule[sheet] = {}
                    if date not in schedule[sheet]:
                        schedule[sheet][date] = {}
                    if time not in schedule[sheet][date]:
                        schedule[sheet][date][time] = []
                    if pd.notnull(data.iloc[index + i][3]):
                        add_to_schedule(data, schedule, sheet, date, time, i, 3)
                    if pd.notnull(data.iloc[index + i][4]):
                        add_to_schedule(data, schedule, sheet, date, time, i, 4)

    
# print(schedule['1 курс']['2024-04-01']['11:40-13:10'][0])
print(schedule)