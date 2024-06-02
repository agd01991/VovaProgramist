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

base_url = "https://www.muiv.ru"
url = base_url + "/studentu/fakultet-it/raspisaniya/"

def download_file(download_url, file_name):
    response = requests.get(download_url)
    if response.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {file_name}")
        return True
    else:
        print(f"Failed to download {file_name}")
        return False
    
def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)

def save_config(teacher_name, file_path, last_update):
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'TeacherName': teacher_name, 'FilePath': file_path, 'LastUpdate': last_update}
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def load_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    teacher_name = config['DEFAULT'].get('TeacherName', '')
    file_path = config['DEFAULT'].get('FilePath', '')
    last_update = config['DEFAULT'].get('LastUpdate', '')
    return teacher_name, file_path, last_update

def check_update_needed(last_update):
    if last_update:
        last_update_time = datetime.strptime(last_update, '%Y-%m-%d %H:%M:%S')
        if datetime.now() - last_update_time < timedelta(hours=4):
            return False
    return True

def update_files():
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        bachelor_block = soup.find('div', class_='mb-5')
        h2 = bachelor_block.find('h2')
        if h2 and h2.text.strip() == "Бакалавриат":
            download_items = bachelor_block.find_all('div', class_='download__item')
            for item in download_items:
                link = item.find('a', class_='download__src')
                if link and 'href' in link.attrs and (link['href'].endswith('.xlsx') or link['href'].endswith('.xls')):
                    file_url = base_url + link['href']
                    file_name = file_url.split('/')[-1]
                    if download_file(file_url, file_name):
                        if file_name.endswith('.xls'):
                            new_file_name = file_name[:-3] + 'xlsx'
                            x2x = XLS2XLSX(file_name)
                            x2x.to_xlsx(new_file_name)
                            os.remove(file_name)
                        save_config(default_teacher_name, default_file_path, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        print("Failed to retrieve the page")

def process_new_algorithm(file_path, teacher_name):
    # Новый алгоритм обработки данных
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
    
    return schedule

def add_to_schedule(data, schedule, sheet, date, time, index, i, col):
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
    entry = {
        'subject': subject,
        'teacher_name': teacher_name,
        'classroom': classroom,
        'full_info': full_info
    }
    if date not in schedule[sheet]:
        schedule[sheet][date] = {}
    if time not in schedule[sheet][date]:
        schedule[sheet][date][time] = []
    schedule[sheet][date][time].append(entry)

def process_and_show_schedule():
    teacher_name = teacher_name_entry.get()
    file_path = file_path_entry.get()
    if not file_path:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите файл Excel")
        return
    if not teacher_name:
        messagebox.showerror("Ошибка", "Пожалуйста, введите имя преподавателя")
        return

    schedule = process_new_algorithm(file_path, teacher_name)
    
    output_text.delete('1.0', tk.END)    

    if schedule:
        for sheet, dates in schedule.items():
            output_text.insert(tk.END, f"Расписание для {sheet}:\n")
            for date, times in dates.items():
                output_text.insert(tk.END, f"На {date}:\n")
                for time, classes in times.items():
                    for class_info in classes:
                        output_text.insert(tk.END, f"{time}: {class_info['subject']} в аудитории {class_info['classroom']}, Преподаватель: {class_info['teacher_name']}\n")
                output_text.insert(tk.END, "\n")
    else:
        output_text.insert(tk.END, "На сегодня пар нет\n")

default_teacher_name, default_file_path, last_update = load_config()

if check_update_needed(last_update):
    update_files()
    config = configparser.ConfigParser()
    config.read('config.ini')
    last_update = config['DEFAULT'].get('LastUpdate', '')

root = tk.Tk()
root.title("Расписание преподавателей")

label = tk.Label(root, text="Введите фамилию преподавателя, формат Иванов И.И.:")
label.pack()

teacher_name_entry = tk.Entry(root)
teacher_name_entry.insert(0, default_teacher_name)
teacher_name_entry.pack()

file_path_button = tk.Button(root, text="Выберите файл Excel", command=open_file_dialog)
file_path_button.pack()

file_path_entry = tk.Entry(root)
file_path_entry.insert(0, default_file_path)
file_path_entry.pack()

process_button = tk.Button(root, text="Показать расписание на сегодня", command=process_and_show_schedule)
process_button.pack()

output_text = tk.Text(root, height=10, width=50)
output_text.pack()

root.mainloop()
