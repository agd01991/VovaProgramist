import pandas as pd
from datetime import datetime
import re

file_path = 'C:/Users/agd01/Documents/VovaProgramist/Raspisanie-FIT-ochnaya-f.o-23_24-vesenniy-sem.-APREL.xlsx'

sheet_names = ['1 курс', '1 курс ', '2 курс', '2 курс ', '3 курс', '3 курс ']

schedule = {}

def add_to_schedule(data: pd.DataFrame, schedule: dict, sheet: str, date: str, time: str, index: int, i: int, col: int):
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

def make_dict_from_xlsx(file_path, sheet_names):
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
                            add_to_schedule(data, schedule, sheet, date, time, index, i, 3)
                        if pd.notnull(data.iloc[index + i][4]):
                            add_to_schedule(data, schedule, sheet, date, time, index, i, 4)

make_dict_from_xlsx(file_path, sheet_names)
# print(schedule['1 курс']['2024-04-01']['11:40-13:10'][0])
# print(schedule)

new_schedule = {}

# Перебор данных в исходном словаре
for course, dates in schedule.items():
    for date, times in dates.items():
        for time, classes in times.items():
            for a_class in classes:
                teacher = a_class['teacher_name']
                subject = a_class['subject']
                classroom = a_class['classroom']

                if teacher not in new_schedule:
                    new_schedule[teacher] = {}     
                if date not in new_schedule[teacher]:
                    new_schedule[teacher][date] = {}            
                if time not in new_schedule[teacher][date]:
                    new_schedule[teacher][date][time] = {}
                new_schedule[teacher][date][time][subject] = subject + ', ' + classroom + ', ' + course

# Вывод нового словаря
# print(new_schedule['Геворкян Э.А.']['2024-04-01'])
# print(new_schedule.keys())
# print('гевор' in str(new_schedule.keys()).lower())
key_found = None
for key in new_schedule.keys():
    if 'гев' in key.lower():  # Преобразуем каждый ключ к нижнему регистру и проверяем вхождение
        key_found = key
        break

# print(key_found) 

# print(new_schedule[key_found])
# получил препода,
# prepod -> date -> time -> subject -> class

today_date = '2024-04-15'

schedule_day = []

schedule_week = {}

# print(new_schedule[key_found]['2024-04-15'])

if key_found:
    schedule_today = new_schedule.get(key_found, {}).get(today_date, None)
    if schedule_today:
        unique_subjects = set()
        # print(f"Расписание для {key_found} на {today_date}:")
        for time, subjects in schedule_today.items():
            for subject, classroom in subjects.items():
                unique_subjects.add(subject)
                print(unique_subjects)
                # print(f"  {time} : {classroom if classroom else 'не указана аудитория'}")
                x = f"  {time} : {classroom if classroom else 'не указана аудитория'}"
                schedule_day.append(x)
        print(f"unique_subjects = {len(unique_subjects)}")
    else:
        print(f"На {today_date} нет расписания для {key_found}")
else:
    print("Учитель с таким именем не найден")
        
print(f"Расписание для {key_found} на {today_date}:")
print(schedule_day)