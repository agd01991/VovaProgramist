import tkinter as tk
from tkinter import Canvas

class HanoiGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ханойские башни")
        
        # Создаем холст для рисования
        self.canvas = Canvas(root, width=800, height=600)
        self.canvas.pack()
        
        self.spindles = [8, 7, 6, 5, 4, 3, 2, 1]
        self.disks = {i: [] for i in self.spindles}
        self.init_disks()
        self.draw_spindles()
        self.draw_disks()

    def init_disks(self):
        # Инициализируем диски на шпинделях
        for spindle in self.spindles:
            for n in range(spindle):
                diameter = spindle * 10 + (n + 1)
                self.disks[spindle].append(diameter)

    def draw_spindles(self):
        # Рисуем шпиндели
        for i in range(8):
            x = 50 + i * 90
            self.canvas.create_line(x, 500, x, 100, width=5)
    
    def draw_disks(self):
        # Рисуем диски
        for i, spindle in enumerate(self.spindles):
            x = 50 + i * 90
            y = 500
            for diameter in self.disks[spindle]:
                self.canvas.create_rectangle(x - diameter / 2, y - 20, x + diameter / 2, y, fill="blue")
                y -= 25

    def move_disk(self, from_spindle, to_spindle):
        if not self.disks[from_spindle] or (self.disks[to_spindle] and self.disks[to_spindle][-1] < self.disks[from_spindle][-1]):
            return False  # Невозможно переместить диск
        disk = self.disks[from_spindle].pop()
        self.disks[to_spindle].append(disk)
        self.canvas.delete("all")
        self.draw_spindles()
        self.draw_disks()
        return True

if __name__ == "__main__":
    root = tk.Tk()
    app = HanoiGUI(root)
    root.mainloop()
