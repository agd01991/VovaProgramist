import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
from xls2xlsx import XLS2XLSX
import os
import configparser

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


def find_schedule_by_teacher_name(teacher_name, file_path, sheet_names):
    today = datetime.today().strftime('%Y-%m-%d')
    schedule = {}
    subjects = {}
    for sheet in sheet_names:
        try:
            data = pd.read_excel(file_path, sheet_name=sheet, header=None)
        except ValueError:
            print(f"Лист '{sheet}' не найден в файле.")
            continue

        for index, row in data.iterrows():
            if teacher_name.lower() in str(row[3]).lower():
                tName = data.iloc[index][3]
                fIndex = 1
                while pd.isnull(data.iloc[index - fIndex][3]):
                    fIndex += 1
                subject = data.iloc[index - fIndex][3]
                subject_indx = index - fIndex
                    
                fIndex = 0
                while pd.isnull(data.iloc[index - fIndex][0]):
                    fIndex += 1

                day = data.iloc[index - fIndex][0]
                date = data.iloc[index - fIndex][1]
                time = []
                for time_index in range(subject_indx, index):
                    time_entry = data.iloc[time_index][2]
                    if pd.notnull(time_entry):
                        time.append(time_entry)

                if pd.notnull(date) and date != 'nan':
                    date = date.strftime('%Y-%m-%d')

                if date == today:
                    schedule_entry = f"{day}, {date}: {subject} в {time}, {tName}"
                    if sheet in schedule:
                        schedule[sheet].append(schedule_entry)
                    else:
                        schedule[sheet] = [schedule_entry]
                    if subject not in subjects:
                        subjects[subject] = []                    
    print(schedule)
    print(subjects)
    return schedule, subjects

def open_file_dialog():
    file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    file_path_entry.delete(0, tk.END)
    file_path_entry.insert(0, file_path)

def process_and_show_schedule():
    teacher_name = teacher_name_entry.get()
    file_path = file_path_entry.get()
    if not file_path:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите файл Excel")
        return
    if not teacher_name:
        messagebox.showerror("Ошибка", "Пожалуйста, введите имя преподавателя")
        return

    save_config(teacher_name, file_path, last_update)
    sheet_names = ['1 курс', '1 курс ', '2 курс', '2 курс ', '3 курс', '3 курс ']
    schedule, subjects = find_schedule_by_teacher_name(teacher_name, file_path, sheet_names)
    output_text.delete('1.0', tk.END)

    

    if schedule:
        for course, schedule_list in schedule.items():
            output_text.insert(tk.END, f"Расписание для {course}:\n")
            for schedule_item in schedule_list:
                output_text.insert(tk.END, schedule_item + "\n")
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

process_button = tk.Button(root, text="Показать расписание", command=process_and_show_schedule)
process_button.pack()

output_text = tk.Text(root, height=10, width=50)
output_text.pack()

root.mainloop()
