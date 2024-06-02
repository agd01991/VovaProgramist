import tkinter as tk
from math import sqrt, pow, degrees, radians, pi, tanh, log

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("400x600")
        self.result = tk.StringVar()
        self.memory = 0
        self.create_widgets()
        
    def create_widgets(self):
        entry = tk.Entry(self.root, textvariable=self.result, font=("Arial", 24), bd=10, insertwidth=2, width=14, borderwidth=4)
        entry.grid(row=0, column=0, columnspan=4)
        
        buttons = [
            '7', '8', '9', '/', 
            '4', '5', '6', '*', 
            '1', '2', '3', '-', 
            '0', '.', '=', '+',
            'C', 'M+', 'M-', 'MR',
            'sqrt', 'pow', 'deg_to_dms', 'dms_to_deg', 'pi', 'tanh', 'ln'
        ]
        
        row = 1
        col = 0
        for button in buttons:
            if col > 3:
                col = 0
                row += 1
            if button not in {'=', 'C', 'M+', 'M-', 'MR', 'sqrt', 'pow', 'deg_to_dms', 'dms_to_deg', 'pi', 'tanh', 'ln'}:
                tk.Button(self.root, text=button, padx=20, pady=20, font=("Arial", 18), command=lambda b=button: self.append_to_expression(b)).grid(row=row, column=col)
            elif button == '=':
                tk.Button(self.root, text=button, padx=20, pady=20, font=("Arial", 18), command=self.calculate).grid(row=row, column=col)
            elif button == 'C':
                tk.Button(self.root, text=button, padx=20, pady=20, font=("Arial", 18), command=self.clear).grid(row=row, column=col)
            elif button == 'M+':
                tk.Button(self.root, text=button, padx=20, pady=20, font=("Arial", 18), command=self.memory_add).grid(row=row, column=col)
            elif button == 'M-':
                tk.Button(self.root, text=button, padx=20, pady=20, font=("Arial", 18), command=self.memory_subtract).grid(row=row, column=col)
            elif button == 'MR':
                tk.Button(self.root, text=button, padx=20, pady=20, font=("Arial", 18), command=self.memory_recall).grid(row=row, column=col)
            elif button == 'sqrt':
                tk.Button(self.root, text=button, padx=20, pady=20, font=("Arial", 18), command=self.square_root).grid(row=row, column=col)
            elif button == 'pow':
                tk.Button(self.root, text=button, padx=20, pady=20, font=("Arial", 18), command=self.power).grid(row=row, column=col)
            elif button == 'deg_to_dms':
                tk.Button(self.root, text=button, padx=20, pady=20, font=("Arial", 18), command=self.deg_to_dms).grid(row=row, column=col)
            elif button == 'dms_to_deg':
                tk.Button(self.root, text=button, padx=20, pady=20, font=("Arial", 18), command=self.dms_to_deg).grid(row=row, column=col)
            elif button == 'pi':
                tk.Button(self.root, text=button, padx=20, pady=20, font=("Arial", 18), command=self.pi_value).grid(row=row, column=col)
            elif button == 'tanh':
                tk.Button(self.root, text=button, padx=20, pady=20, font=("Arial", 18), command=self.hyperbolic_tan).grid(row=row, column=col)
            elif button == 'ln':
                tk.Button(self.root, text=button, padx=20, pady=20, font=("Arial", 18), command=self.natural_log).grid(row=row, column=col)
            col += 1

    def append_to_expression(self, value):
        current_text = self.result.get()
        self.result.set(current_text + value)

    def calculate(self):
        try:
            result = eval(self.result.get())
            self.result.set(result)
        except ZeroDivisionError:
            self.result.set("Error: Division by zero")
        except Exception:
            self.result.set("Error")

    def clear(self):
        self.result.set("")

    def memory_add(self):
        self.memory += float(self.result.get())

    def memory_subtract(self):
        self.memory -= float(self.result.get())

    def memory_recall(self):
        self.result.set(self.memory)

    def square_root(self):
        try:
            self.result.set(sqrt(float(self.result.get())))
        except ValueError:
            self.result.set("Error")

    def power(self):
        try:
            base, exp = map(float, self.result.get().split(','))
            self.result.set(pow(base, exp))
        except ValueError:
            self.result.set("Error")

    def deg_to_dms(self):
        try:
            degrees = float(self.result.get())
            d = int(degrees)
            m = int((degrees - d) * 60)
            s = (degrees - d - m/60) * 3600
            self.result.set(f"{d}° {m}' {s:.2f}\"")
        except ValueError:
            self.result.set("Error")

    def dms_to_deg(self):
        try:
            dms = self.result.get().split()
            d = float(dms[0][:-1])
            m = float(dms[1][:-1])
            s = float(dms[2][:-1])
            deg = d + m/60 + s/3600
            self.result.set(deg)
        except ValueError:
            self.result.set("Error")

    def pi_value(self):
        self.result.set(pi)

    def hyperbolic_tan(self):
        try:
            self.result.set(tanh(float(self.result.get())))
        except ValueError:
            self.result.set("Error")

    def natural_log(self):
        try:
            self.result.set(log(float(self.result.get())))
        except ValueError:
            self.result.set("Error")

if __name__ == "__main__":
    root = tk.Tk()
    calc = Calculator(root)
    root.mainloop()
