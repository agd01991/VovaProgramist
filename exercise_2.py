import tkinter as tk
from tkinter import scrolledtext, messagebox

# Инициализация данных клиентов
clients = {}

def load_clients():
    global clients
    try:
        with open("resourse_2.txt", "r") as file:
            for line in file:
                name, balance = line.strip().split()
                clients[name] = float(balance)
    except FileNotFoundError:
        print("File not found. Starting with an empty client list.")

def save_clients():
    with open("resourse_2.txt", "w") as file:
        for name, balance in clients.items():
            file.write(f"{name} {balance}\n")

def save_history(action, name, amount=0, target_name=None):
    with open("history_2.txt", "a") as file:
        if target_name:
            file.write(f"{action} {amount} from {name} to {target_name}\n")
        else:
            file.write(f"{action} {amount} for {name}\n")

def update_client_list():
    client_list_var.set(list(clients.keys()))

def create_client():
    name = client_name_entry.get()
    if name in clients:
        messagebox.showerror("Error", "Client already exists.")
    else:
        clients[name] = 0.0
        update_client_list()
        save_clients()
        save_history("Created client", name)
        messagebox.showinfo("Success", f"Client {name} created.")

def deposit():
    name = client_listbox.get(tk.ACTIVE)
    amount = float(amount_entry.get())
    if name:
        clients[name] += amount
        save_clients()
        save_history("Deposited", name, amount)
        messagebox.showinfo("Success", f"{amount} deposited to {name}.")
    else:
        messagebox.showerror("Error", "Please select a client.")

def withdraw():
    name = client_listbox.get(tk.ACTIVE)
    amount = float(amount_entry.get())
    if name:
        if clients[name] >= amount:
            clients[name] -= amount
            save_clients()
            save_history("Withdrawn", name, amount)
            messagebox.showinfo("Success", f"{amount} withdrawn from {name}.")
        else:
            messagebox.showerror("Error", "Insufficient funds.")
    else:
        messagebox.showerror("Error", "Please select a client.")

def check_balance():
    name = client_listbox.get(tk.ACTIVE)
    if name:
        balance = clients[name]
        messagebox.showinfo("Balance", f"{name} has {balance:.2f}.")
    else:
        messagebox.showerror("Error", "Please select a client.")

def transfer():
    name_from = client_listbox.get(tk.ACTIVE)
    name_to = transfer_client_listbox.get(tk.ACTIVE)
    amount = float(amount_entry.get())
    if name_from and name_to:
        if clients[name_from] >= amount:
            clients[name_from] -= amount
            clients[name_to] += amount
            save_clients()
            save_history("Transferred", name_from, amount, name_to)
            messagebox.showinfo("Success", f"{amount} transferred from {name_from} to {name_to}.")
        else:
            messagebox.showerror("Error", "Insufficient funds.")
    else:
        messagebox.showerror("Error", "Please select both clients.")

def apply_interest():
    rate = float(rate_entry.get())
    for client in clients:
        clients[client] += clients[client] * rate / 100
    save_clients()
    save_history("Applied interest", "all clients", rate)
    messagebox.showinfo("Success", f"Interest of {rate}% applied to all clients.")

def clear_fields():
    client_name_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    rate_entry.delete(0, tk.END)

# Создание основного окна
root = tk.Tk()
root.title("Bank Account Management System")

# Поле для ввода имени клиента
tk.Label(root, text="Client Name").grid(row=0, column=0, padx=10, pady=5)
client_name_entry = tk.Entry(root)
client_name_entry.grid(row=0, column=1, padx=10, pady=5)

# Кнопка для создания клиента
create_button = tk.Button(root, text="Create Client", command=create_client)
create_button.grid(row=0, column=2, padx=10, pady=5)

# Список клиентов
tk.Label(root, text="Clients").grid(row=1, column=0, padx=10, pady=5)
client_list_var = tk.StringVar(value=list(clients.keys()))
client_listbox = tk.Listbox(root, listvariable=client_list_var, height=6)
client_listbox.grid(row=1, column=1, padx=10, pady=5, columnspan=2)

# Поле для ввода суммы
tk.Label(root, text="Amount").grid(row=2, column=0, padx=10, pady=5)
amount_entry = tk.Entry(root)
amount_entry.grid(row=2, column=1, padx=10, pady=5)

# Кнопки для операций
deposit_button = tk.Button(root, text="Deposit", command=deposit)
deposit_button.grid(row=3, column=0, padx=10, pady=5)

withdraw_button = tk.Button(root, text="Withdraw", command=withdraw)
withdraw_button.grid(row=3, column=1, padx=10, pady=5)

balance_button = tk.Button(root, text="Check Balance", command=check_balance)
balance_button.grid(row=3, column=2, padx=10, pady=5)

# Поле для выбора клиента-получателя
tk.Label(root, text="Transfer To").grid(row=4, column=0, padx=10, pady=5)
transfer_client_listbox = tk.Listbox(root, listvariable=client_list_var, height=6)
transfer_client_listbox.grid(row=4, column=1, padx=10, pady=5, columnspan=2)

# Кнопка для перевода
transfer_button = tk.Button(root, text="Transfer", command=transfer)
transfer_button.grid(row=5, column=0, padx=10, pady=5)

# Поле для ввода процента
tk.Label(root, text="Interest Rate (%)").grid(row=6, column=0, padx=10, pady=5)
rate_entry = tk.Entry(root)
rate_entry.grid(row=6, column=1, padx=10, pady=5)

# Кнопка для начисления процентов
interest_button = tk.Button(root, text="Apply Interest", command=apply_interest)
interest_button.grid(row=6, column=2, padx=10, pady=5)

# Кнопка для очистки полей
clear_button = tk.Button(root, text="Clear", command=clear_fields)
clear_button.grid(row=7, column=0, padx=10, pady=5, columnspan=3, sticky="ew")

# Загрузка данных клиентов
load_clients()
update_client_list()

# Запуск главного цикла приложения
root.mainloop()
