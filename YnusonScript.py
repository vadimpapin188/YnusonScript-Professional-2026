import tkinter as tk
import re
import random
from tkinter import filedialog, Menu

def save_project():
    code = code_entry.get("1.0", tk.END).strip()
    file_path = filedialog.asksaveasfilename(defaultextension=".y-progect", filetypes=[["YnusonScript Project", "*.y-progect"]])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(code)

def load_project():
    file_path = filedialog.askopenfilename(filetypes=[["YnusonScript Project", "*.y-progect"]])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            code_entry.delete("1.0", tk.END)
            code_entry.insert("1.0", file.read())

def auto_correct():
    code = code_entry.get("1.0", tk.END).strip()
    corrected_code = code.replace("no-elemnt", "no-element")
    corrected_code = re.sub(r"\bx\.(\d+)", r"x.\1", corrected_code)
    corrected_code = re.sub(r"\by\.(\d+)", r"y.\1", corrected_code)
    code_entry.delete("1.0", tk.END)
    code_entry.insert("1.0", corrected_code)

def run_code():
    global preview_frame, variables, brush_color, is_game
    for widget in preview_frame.winfo_children():
        widget.destroy()
    
    code = code_entry.get("1.0", tk.END).strip()
    lines = code.split("\n")
    elements = {}
    ai_responses = {}
    variables = {}
    brush_color = "black"
    is_game = False
    
    for line in lines:
        line = line.strip()
        if line.startswith("pr-game"):
            is_game = True
            preview_frame.config(bg="black")
        
        elif line.startswith("txt.y"):
            match = re.search(r"--text = \[(.*?)\] - x\.(\d+) y\.(\d+)", line)
            if match:
                text, x, y = match.groups()
                label = tk.Label(preview_frame, text=text, fg="white" if is_game else "black")
                label.place(x=int(x), y=int(y))
                elements[text] = label

        elif line.startswith("button.y"):
            match = re.search(r"--text = \[(.*?)\] --dd.y = \[(.*?)\] - x\.(\d+) y\.(\d+)", line)
            if match:
                text, action_code, x, y = match.groups()
                
                def action(code=action_code, btn_text=text):
                    if code.startswith("salfetka.y --"):
                        target = code.split("--")[-1].strip()
                        if target in elements:
                            elements[target].destroy()
                            del elements[target]
                    elif code in variables:
                        print(variables[code])
                    else:
                        exec(code)
                
                button = tk.Button(preview_frame, text=text, command=action, fg="white" if is_game else "black", bg="gray")
                button.place(x=int(x), y=int(y))
                elements[text] = button
        
        elif line.startswith("dd.p.y"):
            match = re.search(r"dd.p.y = \[(.*?)\] - \[(\d+)\]", line)
            if match:
                action_code, repeat_count = match.groups()
                for _ in range(int(repeat_count)):
                    exec(action_code)
        
        elif line.startswith("no-elemnt"):
            label = tk.Label(preview_frame, text="", bg=preview_frame.cget("bg"))
            label.place(x=0, y=0)
        
        elif line.startswith(".y"):
            error_message = random.choice(["Ошибка!", "Неизвестный код!", "Фатальная ошибка!", "Программа крашнулась!"])
            label = tk.Label(preview_frame, text=error_message, fg="red", font=("Arial", 12, "bold"))
            label.place(x=random.randint(50, 300), y=random.randint(50, 400))
    
    preview_frame.update()

root = tk.Tk()
root.title("YnusonScript Professional 2025")
root.geometry("800x500")

menu_frame = tk.Frame(root, bg="#282c34", width=800, height=100)
menu_frame.pack(side=tk.TOP, fill=tk.X)

logo_label = tk.Label(menu_frame, text="YnusonScript Professional 2025", font=("Arial", 18, "bold"), fg="white", bg="#282c34")
logo_label.pack(pady=10)

btn_frame = tk.Frame(menu_frame, bg="#282c34")
btn_frame.pack()

new_project_btn = tk.Button(btn_frame, text="Создать проект", command=lambda: code_entry.delete("1.0", tk.END), font=("Arial", 12), bg="#61afef", fg="white")
new_project_btn.pack(side=tk.LEFT, padx=10)

open_project_btn = tk.Button(btn_frame, text="Открыть проект", command=load_project, font=("Arial", 12), bg="#98c379", fg="white")
open_project_btn.pack(side=tk.LEFT, padx=10)

preview_frame = tk.Frame(root, width=400, height=400, bg="white")
preview_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

code_entry = tk.Text(root, width=50)
code_entry.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

run_button = tk.Button(root, text="Запустить", command=run_code)
run_button.pack(side=tk.BOTTOM, expand=True)

save_button = tk.Button(root, text="Сохранить проект", command=save_project)
save_button.pack(side=tk.BOTTOM, expand=True)

load_button = tk.Button(root, text="Загрузить проект", command=load_project)
load_button.pack(side=tk.BOTTOM, expand=True)

menubar = Menu(root)
edit_menu = Menu(menubar, tearoff=0)
edit_menu.add_command(label="Автоисправка", command=auto_correct)
menubar.add_cascade(label="Правка", menu=edit_menu)
root.config(menu=menubar)

root.mainloop()
