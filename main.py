import tkinter as tk
from tkinter import filedialog, ttk

current_file = None
open_tabs = {}
saved = 0

root = tk.Tk()
root.title("OpenDoc Text")
root.attributes("-zoomed", True)

menu = tk.Menu(root)
root.config(menu=menu)

frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

notebook = ttk.Notebook(frame)
notebook.pack(fill="both", expand=True)

def get_current_text_widget():
    current = notebook.select()
    if not current:
        return None
    frame = notebook.nametowidget(current)
    for widget in frame.winfo_children():
        if isinstance(widget, tk.Text) and widget.cget("state") != "disabled":
            return widget
    return None

def update_line_numbers_widget(text_widget, line_widget):
    line_widget.config(state="normal")
    line_widget.delete("1.0", tk.END)
    row_count = int(text_widget.index("end-1c").split(".")[0])+1
    line_widget.insert("1.0", "\n".join(str(i) for i in range(1, row_count)))
    line_widget.config(state="disabled")

def unsaved():
    global saved
    saved = 0

def new_tab(file_path=None, content=""):
    global open_tabs
    tab_frame = tk.Frame(notebook)

    line_widget = tk.Text(tab_frame, width=5, padx=5, font=("Consolas", 12), state="disabled", bg="#f0f0f0")
    line_widget.pack(side="left", fill="y")

    text_widget = tk.Text(tab_frame, font=("Consolas", 12), undo=True, wrap="none")
    text_widget.insert("1.0", content)
    text_widget.pack(fill="both", expand=True)

    text_widget.bind("<KeyRelease>", lambda e: [update_line_numbers_widget(text_widget, line_widget), unsaved()])

    filename = file_path if file_path else "Untitled"
    open_tabs[filename] = text_widget
    notebook.add(tab_frame, text=filename)
    notebook.select(tab_frame)
    update_line_numbers_widget(text_widget, line_widget)

def close_tab():
    current_tab = notebook.select()
    if not current_tab:
        return

    tab_frame = notebook.nametowidget(current_tab)
    notebook.forget(current_tab) 

    for filename, widget in list(open_tabs.items()):
        if widget in tab_frame.winfo_children():
            del open_tabs[filename] 
            break

def new_file():
    global current_file
    current_file = None
    new_tab()
    root.title("Untitled - OpenDoc Text")

def open_file():
    global current_file
    global saved
    path = filedialog.askopenfilename(filetypes=[
        ("All Files", "*.*"),
        ("Python Files", "*.py"),
        ("Text Files", "*.txt"),
        ("C Files", "*.c"),
        ("C++ Files", "*.cpp"),
        ("C# Files", "*.cs"),
        ("HTML Files", "*.html"),
        ("CSS Files", "*.css"),
        ("XML Files", "*.xml"),
        ("Open Text", "*.otxt")
    ])
    if path:
        current_file = path
        saved = 1
        with open(path, "r") as f:
            content = f.read()
        new_tab(file_path=path, content=content)
        root.title(f"{path} - OpenDoc Text")

def save_file():
    global current_file
    global saved
    widget = get_current_text_widget()
    if not widget:
        return
    if not current_file:
        save_as()
    else:
        with open(current_file, "w") as f:
            f.write(widget.get("1.0", tk.END))
    saved = 1

def save_as():
    global current_file
    widget = get_current_text_widget()
    if not widget:
        return
    path = filedialog.asksaveasfilename(
        filetypes=[
            ("Open Text", "*.otxt"),
            ("Python Files", "*.py"),
            ("Text Files", "*.txt"),
            ("C Files", "*.c"),
            ("C++ Files", "*.cpp"),
            ("C# Files", "*.cs"),
            ("HTML Files", "*.html"),
            ("CSS Files", "*.css"),
            ("XML Files", "*.xml"),
            ("All Files", "*.*")
        ]
    )
    if path:
        with open(path, "w") as f:
            f.write(widget.get("1.0", tk.END))
        current_file = path
        root.title(f"{path} - OpenDoc Text")


filemenu = tk.Menu(menu, tearoff=0)
filemenu.add_command(label="New", command=new_file, accelerator="Ctrl+N")
filemenu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
filemenu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
filemenu.add_command(label="Save As", command=save_as, accelerator="Ctrl+Shift+S")
menu.add_cascade(label="File", menu=filemenu)

editmenu = tk.Menu(menu, tearoff=0)
editmenu.add_command(label="Undo", command=lambda: get_current_text_widget().edit_undo(), accelerator="Ctrl+Z")
editmenu.add_command(label="Redo", command=lambda: get_current_text_widget().edit_redo(), accelerator="Ctrl+Y")
menu.add_cascade(label="Edit", menu=editmenu)

tabmenu = tk.Menu(menu, tearoff=0)
tabmenu.add_command(label="New Tab", command=new_tab, accelerator="Ctrl+Shift+N")
tabmenu.add_command(label="Close Tab", command=close_tab, accelerator="Ctrl+Q")
menu.add_cascade(label="Tab", menu=tabmenu)
root.bind("<Control-n>", lambda e: new_file())
root.bind("<Control-o>", lambda e: open_file())
root.bind("<Control-s>", lambda e: save_file())
root.bind("<Control-S>", lambda e: save_as())
root.bind("<Control-z>", lambda e: get_current_text_widget().edit_undo())
root.bind("<Control-y>", lambda e: get_current_text_widget().edit_redo())
root.bind("<Control-q>", lambda e: close_tab())
root.bind("<Control-Shift-N>", lambda e: new_tab())

new_file()

root.mainloop()
