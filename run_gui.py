import tkinter as tk
import subprocess

def run_search(algo):
    subprocess.run([
        "python", "pacman.py",
        "-l", "smallMaze",
        "-p", "SearchAgent",
        "-a", f"fn={algo}"
    ])

root = tk.Tk()
root.title("Pacman Search Comparison")
root.geometry("300x250")
root.resizable(False, False)

label = tk.Label(root, text="Chọn thuật toán tìm kiếm:", font=("Arial", 14))
label.pack(pady=10)

tk.Button(root, text="Depth-First Search (DFS)", command=lambda: run_search("depthFirstSearch"), width=30).pack(pady=5)
tk.Button(root, text="Breadth-First Search (BFS)", command=lambda: run_search("breadthFirstSearch"), width=30).pack(pady=5)
tk.Button(root, text="Uniform Cost Search (UCS)", command=lambda: run_search("uniformCostSearch"), width=30).pack(pady=5)
tk.Button(root, text="A* Search", command=lambda: run_search("aStarSearch"), width=30).pack(pady=5)

root.mainloop()
