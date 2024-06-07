import tkinter as tk
from tkinter import scrolledtext, messagebox

# Инициализация данных клиентов
client_data = {}

def load_client_data():
    global client_data
    try:
        with open("resourse_2.txt", "r") as f:
            for line in f:
                name, balance = line.strip().split()
                client_data[name] = float(balance)
    except FileNotFoundError:
        print("Файл не найден. Начинаем с пустого списка клиентов.")

def save_client_data():
    with open("result_2.txt", "w") as f:
        for name, balance in client_data.items():
            f.write(f"{name} {balance}\n")

def refresh_client_list():
    client_list_var.set(list(client_data.keys()))

def add_client():
    name = client_name_entry.get()
    if name in client_data:
        messagebox.showerror("Ошибка", "Клиент уже существует.")
    else:
        client_data[name] = 0.0
        refresh_client_list()
        save_client_data()
        messagebox.showinfo("Успешно", f"Клиент {name} создан.")

def deposit_funds():
    name = client_listbox.get(tk.ACTIVE)
    amount = float(amount_entry.get())
    if name:
        client_data[name] += amount
        save_client_data()
        messagebox.showinfo("Успешно", f"{amount} зачислено на счет {name}.")
    else:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите клиента.")

def withdraw_funds():
    name = client_listbox.get(tk.ACTIVE)
    amount = float(amount_entry.get())
    if name:
        if client_data[name] >= amount:
            client_data[name] -= amount
            save_client_data()
            messagebox.showinfo("Успешно", f"{amount} снято со счета {name}.")
        else:
            messagebox.showerror("Ошибка", "Недостаточно средств.")
    else:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите клиента.")

def check_client_balance():
    name = client_listbox.get(tk.ACTIVE)
    if name:
        balance = client_data[name]
        messagebox.showinfo("Баланс", f"На счету {name} {balance:.2f}.")
    else:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите клиента.")

def transfer_funds():
    name_from = client_listbox.get(tk.ACTIVE)
    name_to = transfer_client_listbox.get(tk.ACTIVE)
    amount = float(amount_entry.get())
    if name_from and name_to:
        if client_data[name_from] >= amount:
            client_data[name_from] -= amount
            client_data[name_to] += amount
            save_client_data()
            messagebox.showinfo("Успешно", f"{amount} переведено от {name_from} к {name_to}.")
        else:
            messagebox.showerror("Ошибка", "Недостаточно средств.")
    else:
        messagebox.showerror("Ошибка", "Пожалуйста, выберите обоих клиентов.")

def apply_interest_rate():
    rate = float(rate_entry.get())
    for client in client_data:
        client_data[client] += client_data[client] * rate / 100
    save_client_data()
    messagebox.showinfo("Успешно", f"Процент {rate}% применен ко всем клиентам.")

def clear_input_fields():
    client_name_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    rate_entry.delete(0, tk.END)

# Создание основного окна
root = tk.Tk()
root.title("Система управления банковскими счетами")

# Поле для ввода имени клиента
tk.Label(root, text="Имя клиента").grid(row=0, column=0, padx=10, pady=5)
client_name_entry = tk.Entry(root)
client_name_entry.grid(row=0, column=1, padx=10, pady=5)

# Кнопка для создания клиента
create_button = tk.Button(root, text="Создать клиента", command=add_client)
create_button.grid(row=0, column=2, padx=10, pady=5)

# Список клиентов
tk.Label(root, text="Клиенты").grid(row=1, column=0, padx=10, pady=5)
client_list_var = tk.StringVar(value=list(client_data.keys()))
client_listbox = tk.Listbox(root, listvariable=client_list_var, height=6)
client_listbox.grid(row=1, column=1, padx=10, pady=5, columnspan=2)

# Поле для ввода суммы
tk.Label(root, text="Сумма").grid(row=2, column=0, padx=10, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=2, column=1, padx=10, pady=5)

# Кнопки для операций
deposit_button = tk.Button(root, text="Зачислить", command=deposit_funds)
deposit_button.grid(row=3, column=0, padx=10, pady=5)

withdraw_button = tk.Button(root, text="Снять", command=withdraw_funds)
withdraw_button.grid(row=3, column=1, padx=10, pady=5)

balance_button = tk.Button(root, text="Проверить баланс", command=check_client_balance)
balance_button.grid(row=3, column=2, padx=10, pady=5)

# Поле для выбора клиента-получателя
tk.Label(root, text="Перевести к").grid(row=4, column=0, padx=10, pady=5)
transfer_client_listbox = tk.Listbox(root, listvariable=client_list_var, height=6)
transfer_client_listbox.grid(row=4, column=1, padx=10, pady=5, columnspan=2)

# Кнопка для перевода
transfer_button = tk.Button(root, text="Перевод", command=transfer_funds)
transfer_button.grid(row=5, column=0, padx=10, pady=5)

# Поле для ввода процента
tk.Label(root, text="Процентная ставка (%)").grid(row=6, column=0, padx=10, pady=5)
rate_entry = tk.Entry(root)
rate_entry.grid(row=6, column=1, padx=10, pady=5)

# Кнопка для начисления процентов
interest_button = tk.Button(root, text="Начислить проценты", command=apply_interest_rate)
interest_button.grid(row=6, column=2, padx=10, pady=5)

# Кнопка для очистки полей
clear_button = tk.Button(root, text="Очистить", command=clear_input_fields)
clear_button.grid(row=7, column=0, padx=10, pady=5, columnspan=3, sticky="ew")

# Загрузка данных клиентов
load_client_data()
refresh_client_list()

# Запуск главного цикла приложения
root.mainloop()
