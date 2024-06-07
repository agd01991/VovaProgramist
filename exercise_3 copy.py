import tkinter as tk
from math import sqrt, pow, degrees, radians, pi, tanh, log

class AdvancedCalculator:
    def __init__(self, master):
        self.master = master
        self.master.title("Advanced Calculator")
        self.master.geometry("800x800")
        self.display_value = tk.StringVar()
        self.memory = 0
        self.create_ui()
        
    def create_ui(self):
        # Создание дисплея калькулятора
        display = tk.Entry(self.master, textvariable=self.display_value, font=("Arial", 24), bd=10, insertwidth=2, width=14, borderwidth=4)
        display.grid(row=0, column=0, columnspan=4)

        # Определение кнопок и их размещение
        button_specs = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3),
            ('C', 5, 0), ('M+', 5, 1), ('M-', 5, 2), ('MR', 5, 3),
            ('sqrt', 6, 0), ('pow', 6, 1), ('deg_to_dms', 6, 2), ('dms_to_deg', 6, 3),
            ('pi', 7, 0), ('tanh', 7, 1), ('ln', 7, 2)
        ]

        # Создание кнопок и их привязка к командам
        for (text, row, col) in button_specs:
            action = lambda x=text: self.append_value(x)
            if text == '=':
                action = self.evaluate
            elif text == 'C':
                action = self.clear_display
            elif text == 'M+':
                action = self.memory_addition
            elif text == 'M-':
                action = self.memory_subtraction
            elif text == 'MR':
                action = self.memory_recall
            elif text == 'sqrt':
                action = self.calculate_square_root
            elif text == 'pow':
                action = self.calculate_power
            elif text == 'deg_to_dms':
                action = self.convert_deg_to_dms
            elif text == 'dms_to_deg':
                action = self.convert_dms_to_deg
            elif text == 'pi':
                action = self.insert_pi
            elif text == 'tanh':
                action = self.calculate_tanh
            elif text == 'ln':
                action = self.calculate_ln

            tk.Button(self.master, text=text, padx=20, pady=20, font=("Arial", 18), command=action).grid(row=row, column=col)

        # Отдельное размещение кнопок для улучшения читаемости кода
        additional_buttons = [
            ('sqrt', self.calculate_square_root, 6, 0),
            ('pow', self.calculate_power, 6, 1),
            ('deg_to_dms', self.convert_deg_to_dms, 6, 2),
            ('dms_to_deg', self.convert_dms_to_deg, 6, 3),
            ('pi', self.insert_pi, 7, 0),
            ('tanh', self.calculate_tanh, 7, 1),
            ('ln', self.calculate_ln, 7, 2)
        ]

        for (text, cmd, row, col) in additional_buttons:
            tk.Button(self.master, text=text, padx=20, pady=20, font=("Arial", 18), command=cmd).grid(row=row, column=col)


    def append_value(self, value):
        current = self.display_value.get()
        self.display_value.set(current + value)

    def evaluate(self):
        try:
            result = eval(self.display_value.get())
            self.display_value.set(result)
        except ZeroDivisionError:
            self.display_value.set("Error: Div by 0")
        except Exception:
            self.display_value.set("Error")

    def clear_display(self):
        self.display_value.set("")

    def memory_addition(self):
        self.memory += float(self.display_value.get())

    def memory_subtraction(self):
        self.memory -= float(self.display_value.get())

    def memory_recall(self):
        self.display_value.set(self.memory)

    def calculate_square_root(self):
        try:
            self.display_value.set(sqrt(float(self.display_value.get())))
        except ValueError:
            self.display_value.set("Error")

    def calculate_power(self):
        try:
            base, exp = map(float, self.display_value.get().split(','))
            self.display_value.set(pow(base, exp))
        except ValueError:
            self.display_value.set("Error")

    def convert_deg_to_dms(self):
        try:
            deg_value = float(self.display_value.get())
            d = int(deg_value)
            m = int((deg_value - d) * 60)
            s = (deg_value - d - m/60) * 3600
            self.display_value.set(f"{d}° {m}' {s:.2f}\"")
        except ValueError:
            self.display_value.set("Error")

    def convert_dms_to_deg(self):
        try:
            dms_value = self.display_value.get().split()
            d = float(dms_value[0][:-1])
            m = float(dms_value[1][:-1])
            s = float(dms_value[2][:-1])
            degrees_value = d + m/60 + s/3600
            self.display_value.set(degrees_value)
        except ValueError:
            self.display_value.set("Error")

    def insert_pi(self):
        self.display_value.set(pi)

    def calculate_tanh(self):
        try:
            self.display_value.set(tanh(float(self.display_value.get())))
        except ValueError:
            self.display_value.set("Error")

    def calculate_ln(self):
        try:
            self.display_value.set(log(float(self.display_value.get())))
        except ValueError:
            self.display_value.set("Error")

if __name__ == "__main__":
    root = tk.Tk()
    calc = AdvancedCalculator(root)
    root.mainloop()
