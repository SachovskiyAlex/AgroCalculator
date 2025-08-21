import tkinter as tk
import os
import ctypes
from tkinter import ttk, messagebox
from db import (
    додати_поле, додати_препарат,
    отримати_поля, отримати_препарати,
    видалити_поле, видалити_препарат
)

def показати_екранну_клавіатуру(event=None):
    tabtip_path = r"C:\\PROGRA~1\\COMMON~1\\MICROS~1\\ink\\tabtip.exe"
    if os.path.exists(tabtip_path):
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "open", tabtip_path, None, None, 1)
        except Exception as e:
            print(f"Не вдалося запустити клавіатуру: {e}")
    else:
        print("TabTip.exe не знайдено.")


def відкрити_вікно_додавання(callback=None):
    вікно = tk.Toplevel()
    вікно.title("Керування даними")
    вікно.resizable(False, False)

    # Розміри вікна
    ширина = 1100
    висота = 950
    екран_ширина = вікно.winfo_screenwidth()
    позиція_x = (екран_ширина - ширина) // 2
    позиція_y = 10  
    вікно.geometry(f"{ширина}x{висота}+{позиція_x}+{позиція_y}")
    def on_close():
        if callback:
            callback()
        вікно.destroy()

    вікно.protocol("WM_DELETE_WINDOW", on_close)
    вікно.grab_set()
    вікно.focus_force()
    style = ttk.Style()
    style.configure("TNotebook.Tab", font=("Arial", 20))

    notebook = ttk.Notebook(вікно)
    notebook.pack(padx=10, pady=10, fill="both", expand=True)

    frame_поле = ttk.Frame(notebook)
    notebook.add(frame_поле, text="Поле")

    tk.Label(frame_поле, text="Назва поля:", font=("Arial", 30)).pack(pady=5)
    entry_назва_поля = tk.Entry(frame_поле, width=30, font=("Arial", 30))
    entry_назва_поля.pack()
    entry_назва_поля.bind("<FocusIn>", показати_екранну_клавіатуру)


    tk.Label(frame_поле, text="Площа (ар):", font=("Arial", 30)).pack(pady=5)
    entry_площа_га = tk.Entry(frame_поле, width=30, font=("Arial", 30))
    entry_площа_га.pack()
    entry_площа_га.bind("<FocusIn>", показати_екранну_клавіатуру)

    def додати_поле_дія():
        try:
            назва = entry_назва_поля.get().strip()
            площа = float(entry_площа_га.get().strip())
            додати_поле(назва, площа)
            messagebox.showinfo("Успішно", "Поле додано!")
            entry_назва_поля.delete(0, tk.END)
            entry_площа_га.delete(0, tk.END)
            оновити_список_полів()
        except Exception as e:
            messagebox.showerror("Помилка", f"Невірно введені дані: {e}")

    tk.Button(frame_поле, text="Додати поле", font=("Arial", 30), command=додати_поле_дія).pack(pady=10)

    ttk.Separator(frame_поле, orient="horizontal").pack(fill="x", pady=5)

    var_поле_видалити = tk.StringVar(value="Оберіть поле")
    combo_поле_видалити = tk.OptionMenu(frame_поле, var_поле_видалити, "")
    menu = combo_поле_видалити.nametowidget(combo_поле_видалити.menuname)
    menu.config(font=("Arial", 30))
    combo_поле_видалити.config(font=("Arial", 30), width=30)
    combo_поле_видалити.pack(pady=5)

    def оновити_список_полів():
        меню = combo_поле_видалити.nametowidget(combo_поле_видалити.menuname)
        меню.delete(0, 'end')
        for назва in [назва for (_, назва, _) in отримати_поля()]:
            меню.add_command(label=назва, command=lambda value=назва: var_поле_видалити.set(value))

    def видалити_поле_дія():
        вибране = var_поле_видалити.get()
        if вибране:
            видалити_поле(вибране)
            messagebox.showinfo("Успішно", "Поле видалено!")
            оновити_список_полів()

    tk.Button(frame_поле, text="Видалити поле", font=("Arial", 30), command=видалити_поле_дія, fg="red").pack(pady=5)
    оновити_список_полів()

    frame_препарат = ttk.Frame(notebook)
    notebook.add(frame_препарат, text="Препарат")

    tk.Label(frame_препарат, text="Назва препарату:", font=("Arial", 30)).pack(pady=5)
    entry_назва_препарату = tk.Entry(frame_препарат, width=30, font=("Arial", 30))
    entry_назва_препарату.pack()
    entry_назва_препарату.bind("<FocusIn>", показати_екранну_клавіатуру)
    

    tk.Label(frame_препарат, text="Норма мін (л/га):", font=("Arial", 30)).pack(pady=5)
    entry_норма_min = tk.Entry(frame_препарат, width=30, font=("Arial", 30))
    entry_норма_min.pack()
    entry_норма_min.bind("<FocusIn>", показати_екранну_клавіатуру)

    tk.Label(frame_препарат, text="Норма макс (л/га):", font=("Arial", 30)).pack(pady=5)
    entry_норма_max = tk.Entry(frame_препарат, width=30, font=("Arial", 30))
    entry_норма_max.pack()
    entry_норма_max.bind("<FocusIn>", показати_екранну_клавіатуру)

    def додати_препарат_дія():
        try:
            назва = entry_назва_препарату.get().strip()
            норма_min = float(entry_норма_min.get().strip())
            норма_max = float(entry_норма_max.get().strip())
            додати_препарат(назва, норма_min, норма_max)
            messagebox.showinfo("Успішно", "Препарат додано!")
            entry_назва_препарату.delete(0, tk.END)
            entry_норма_min.delete(0, tk.END)
            entry_норма_max.delete(0, tk.END)
            оновити_список_препаратів()
        except Exception as e:
            messagebox.showerror("Помилка", f"Невірно введені дані: {e}")

    tk.Button(frame_препарат, text="Додати препарат", font=("Arial", 30), command=додати_препарат_дія).pack(pady=10)

    ttk.Separator(frame_препарат, orient="horizontal").pack(fill="x", pady=5)

    var_препарат_видалити = tk.StringVar(value="Оберіть препарат")
    combo_препарат_видалити = tk.OptionMenu(frame_препарат, var_препарат_видалити, "")
    menu = combo_препарат_видалити.nametowidget(combo_препарат_видалити.menuname)
    menu.config(font=("Arial", 30))
    combo_препарат_видалити.config(font=("Arial", 30), width=30)
    combo_препарат_видалити.pack(pady=5)

    def оновити_список_препаратів():
        меню = combo_препарат_видалити.nametowidget(combo_препарат_видалити.menuname)
        меню.delete(0, 'end')
        for назва in [назва for (_, назва, _, _) in отримати_препарати()]:
            меню.add_command(label=назва, command=lambda value=назва: var_препарат_видалити.set(value))

    def видалити_препарат_дія():
        вибране = var_препарат_видалити.get()
        if вибране:
            видалити_препарат(вибране)
            messagebox.showinfo("Успішно", "Препарат видалено!")
            оновити_список_препаратів()

    tk.Button(frame_препарат, text="Видалити препарат", font=("Arial", 30), command=видалити_препарат_дія, fg="red").pack(pady=5)
    оновити_список_препаратів()


