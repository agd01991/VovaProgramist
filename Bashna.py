import tkinter as tk
from tkinter import ttk

class HanoiTowers:
    def __init__(self, root):
        self.root = root
        self.root.title("Hanoi Towers")
        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack()
        
        self.spindles = [[], [], [], [], [], [], [], []]
        self.diameters = []
        self.moves = []

        self.init_spindles()
        self.draw_towers()

    def init_spindles(self):
        initial_setup = "70208210"
        for i, count in enumerate(initial_setup):
            count = int(count)
            for j in range(count):
                diameter = (i + 1) * 10 + j
                self.spindles[i].append(diameter)
                self.diameters.append(diameter)
        
        self.diameters.sort()

    def draw_towers(self):
        self.canvas.delete("all")
        width = 80
        height = 20
        base_y = 500

        for i in range(8):
            x = 50 + i * 100
            self.canvas.create_rectangle(x - width/2, base_y, x + width/2, base_y - height * 8, outline="black")
            for j, disk in enumerate(self.spindles[i]):
                self.canvas.create_rectangle(x - disk/2, base_y - height * (j + 1), x + disk/2, base_y - height * j, fill="blue")

    def move_disk(self, from_spindle, to_spindle):
        if self.spindles[from_spindle] and (not self.spindles[to_spindle] or self.spindles[to_spindle][-1] > self.spindles[from_spindle][-1]):
            disk = self.spindles[from_spindle].pop()
            self.spindles[to_spindle].append(disk)
            self.draw_towers()

    def solve(self):
        self.moves = []
        self.hanoi(len(self.diameters), 7, 0, 6)
        self.animate_solution()

    def hanoi(self, n, source, target, auxiliary):
        if n > 0:
            self.hanoi(n-1, source, auxiliary, target)
            self.moves.append((source, target))
            self.hanoi(n-1, auxiliary, target, source)

    def animate_solution(self):
        if self.moves:
            from_spindle, to_spindle = self.moves.pop(0)
            self.move_disk(from_spindle, to_spindle)
            self.root.after(500, self.animate_solution)

    def calculate_minimum_iterations(self):
        return 2**len(self.diameters) - 1

    def visualize_progress(self, progress):
        if not self.moves:
            self.hanoi(len(self.diameters), 7, 0, 6)
        steps = int(progress / 100 * len(self.moves))
        self.reset_spindles()
        for i in range(steps):
            from_spindle, to_spindle = self.moves[i]
            self.move_disk(from_spindle, to_spindle)

    def reset_spindles(self):
        self.spindles = [[] for _ in range(8)]
        initial_setup = "70208210"
        for i, count in enumerate(initial_setup):
            count = int(count)
            for j in range(count):
                diameter = (i + 1) * 10 + j
                self.spindles[i].append(diameter)
        self.draw_towers()

class HanoiGUI:
    def __init__(self, root):
        self.root = root
        self.hanoi = HanoiTowers(root)
        
        control_frame = tk.Frame(root)
        control_frame.pack()

        tk.Button(control_frame, text="Solve", command=self.solve).pack(side="left")
        tk.Button(control_frame, text="Min Iterations", command=self.show_min_iterations).pack(side="left")

        self.iterations_label = tk.Label(control_frame, text="")
        self.iterations_label.pack(side="left")

        self.progress_var = tk.DoubleVar()
        tk.Label(control_frame, text="Progress (%):").pack(side="left")
        tk.Entry(control_frame, textvariable=self.progress_var).pack(side="left")
        tk.Button(control_frame, text="Visualize Progress", command=self.visualize_progress).pack(side="left")

    def solve(self):
        self.hanoi.solve()

    def show_min_iterations(self):
        min_iterations = self.hanoi.calculate_minimum_iterations()
        self.iterations_label.config(text=f"Min Iterations: {min_iterations}")

    def visualize_progress(self):
        progress = self.progress_var.get()
        self.hanoi.visualize_progress(progress)

if __name__ == "__main__":
    root = tk.Tk()
    gui = HanoiGUI(root)
    root.mainloop()
