import tkinter as tk
from tkinter import ttk
import subprocess
import pygame
import sys

class PacmanLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pacman Search Problems Launcher")
        self.geometry("400x250")


        ttk.Label(self, text="Choose Problem:").pack(pady=5)
        self.problem_var = tk.StringVar(value="Corners")
        problem_combo = ttk.Combobox(self, textvariable=self.problem_var, state="readonly")
        problem_combo['values'] = ("Corners", "FoodSearch","ClosestDot")
        problem_combo.pack()

        self.algo_combo_frame = ttk.Frame(self)
        self.algo_combo_frame.pack(pady=5)

        ttk.Label(self.algo_combo_frame, text="Choose Algorithm:").pack()
        self.algo_var = tk.StringVar(value="DFS")
        self.algo_combo = ttk.Combobox(self.algo_combo_frame, textvariable=self.algo_var, state="readonly")
        self.algo_combo['values'] = ("DFS", "BFS", "UCS", "A*")
        self.algo_combo.pack()
        problem_combo.bind("<<ComboboxSelected>>", self.on_problem_change)
        run_btn = ttk.Button(self, text="Run Pacman", command=self.run_pacman)
        self.run_btn = ttk.Button(self, text="Run Pacman", command=self.run_pacman)
        self.run_btn.pack(pady=20)

        self.output = tk.Text(self, height=6, width=50)
        self.output.pack()

        run_btn.pack(pady=20)

        self.output = tk.Text(self, height=6, width=50)
        self.output.pack()
    
        

    def on_problem_change(self, event=None):
        problem = self.problem_var.get()
        if problem == "ClosestDot":
            self.algo_combo_frame.pack_forget()
        else:
            self.algo_combo_frame.pack(pady=5, before=self.run_btn)

            
    def run_pacman(self):
        problem = self.problem_var.get()
        algo = self.algo_var.get()

        if problem == "Corners":
            level = "mediumCorners"
            agent = "SearchAgent"
            agent_args = "prob=CornersProblem"
            heuristic = "cornersHeuristic"
        elif problem == "FoodSearch":
            level = "mediumDottedMaze"
            agent = "SearchAgent"
            agent_args = "prob=FoodSearchProblem"
            heuristic = "foodHeuristic"
        elif problem == "ClosestDot":
            level = "mediumMaze"
            agent = "ClosestDotSearchAgent"
            agent_args = ""
            heuristic = ""  
        
        if problem != "ClosestDot":
            if algo == "DFS":
                agent_args += ",fn=depthFirstSearch"
            elif algo == "BFS":
                agent_args += ",fn=breadthFirstSearch"
            elif algo == "UCS":
                agent_args += ",fn=uniformCostSearch"
            else:  # A*
                if heuristic:
                    agent_args += f",fn=aStarSearch,heuristic={heuristic}"
                else:
                    agent_args += ",fn=uniformCostSearch"

        cmd = [sys.executable, "pacman.py", "-l", level, "-p", agent]
        if agent_args:
            cmd += ["-a", agent_args]

        self.output.insert(tk.END, f"Running: {' '.join(cmd)}\n")
        self.output.see(tk.END)

        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = proc.communicate()

        self.output.insert(tk.END, stdout)
        if stderr:
            self.output.insert(tk.END, "\nErrors:\n" + stderr)
        self.output.see(tk.END)


if __name__ == "__main__":
    app = PacmanLauncher()
    app.mainloop()
