import ctypes
import os
import tkinter as tk
from tkinter import messagebox
from db import (
    отримати_поля,
    отримати_препарати,
    отримати_форсунки,
    зберегти_в_історію,
    отримати_історію,
    видалити_з_історії
)
from add_data import відкрити_вікно_додавання

поле_дані = отримати_поля()
препарати_дані = отримати_препарати()
форсунки_дані = отримати_форсунки()
flow_rate = 0

def показати_екранну_клавіатуру(event=None):
    tabtip_path = r"C:\\PROGRA~1\\COMMON~1\\MICROS~1\\ink\\tabtip.exe"
    if os.path.exists(tabtip_path):
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "open", tabtip_path, None, None, 1)
        except Exception as e:
            print(f"Не вдалося запустити клавіатуру: {e}")
    else:
        print("TabTip.exe не знайдено.")


вікно = tk.Tk()
вікно.title("Розрахунок витрати")
вікно.resizable(False, False)
вікно_ширина = 1100
вікно_висота = 1000
екран_ширина = вікно.winfo_screenwidth()
екран_висота = вікно.winfo_screenheight()
позиція_по_x = (екран_ширина - вікно_ширина) // 2
позиція_по_y = 1  
вікно.geometry(f"{вікно_ширина}x{вікно_висота}+{позиція_по_x}+{позиція_по_y}")

LABEL_WIDTH = 12
FIELD_WIDTH = 33
VIKNO = 32

frame_заголовок = tk.Frame(вікно)
frame_заголовок.pack(fill="x", pady=(10, 10), padx=20)
tk.Label(frame_заголовок, text="Розрахунок витрати", font=("Segoe UI", 32, "bold")).pack(side="left")
tk.Label(frame_заголовок, text="by Sachovski", font=("Segoe UI", 20), fg="gray").pack(side="right")

frame_форма = tk.Frame(вікно)
frame_форма.pack(pady=10, padx=20)

var_поле = tk.StringVar(value="Не вказано поле")
var_препарат = tk.StringVar(value="Не вказано препарат")
var_форсунка = tk.StringVar(value="Оберіть форсунку")
var_тиск = tk.StringVar(value="")
var_швидкість = tk.StringVar(value="")

menu_поле = tk.OptionMenu(frame_форма, var_поле, *["Не вказано поле"] + [name for (_, name, _) in поле_дані])
menu = menu_поле.nametowidget(menu_поле.menuname)
menu.config(font=("Arial", 30))
menu_поле.config(font=("Arial", 30), width=30)
menu_поле.grid(row=0, column=1, pady=5)
tk.Label(frame_форма, text="Поле:", width=LABEL_WIDTH, anchor="w", font=("Segoe UI", 30)).grid(row=0, column=0)

entry_площа = tk.Entry(frame_форма, width=VIKNO, font=("Arial", 30))
entry_площа.grid(row=1, column=1, pady=5)
entry_площа.bind("<FocusIn>", показати_екранну_клавіатуру)  
tk.Label(frame_форма, text="Площа, ар:", width=LABEL_WIDTH, anchor="w", font=("Segoe UI", 30)).grid(row=1, column=0)

menu_препарат = tk.OptionMenu(frame_форма, var_препарат, *["Не вказано препарат"] + [name for (_, name, _, _) in препарати_дані])
menu = menu_препарат.nametowidget(menu_препарат.menuname)
menu.config(font=("Arial", 30))
menu_препарат.config(font=("Arial", 30), width=30)
menu_препарат.grid(row=2, column=1, pady=5)
tk.Label(frame_форма, text="Препарат:", width=LABEL_WIDTH, anchor="w", font=("Segoe UI", 30)).grid(row=2, column=0)


entry_норма = tk.Entry(frame_форма, width=VIKNO, font=("Arial", 30))
entry_норма.grid(row=3, column=1, pady=5)
entry_норма.bind("<FocusIn>", показати_екранну_клавіатуру)  
tk.Label(frame_форма, text="Норма, л/га:", width=LABEL_WIDTH, anchor="w", font=("Segoe UI", 30)).grid(row=3, column=0)

menu_форсунка = tk.OptionMenu(frame_форма, var_форсунка, *list({name for (_, name, _, _, _) in форсунки_дані}))
menu = menu_форсунка.nametowidget(menu_форсунка.menuname)
menu.config(font=("Arial", 30))
menu_форсунка.config(font=("Arial", 30), width=30)
menu_форсунка.grid(row=4, column=1, pady=5)
tk.Label(frame_форма, text="Форсунка:", width=LABEL_WIDTH, anchor="w", font=("Segoe UI", 30)).grid(row=4, column=0)

menu_тиск = tk.OptionMenu(frame_форма, var_тиск, "")
menu = menu_тиск.nametowidget(menu_тиск.menuname)
menu.config(font=("Arial", 30))
menu_тиск.config(font=("Arial", 30), width=30)
menu_тиск.grid(row=5, column=1, pady=5)
tk.Label(frame_форма, text="Тиск (бар):", width=LABEL_WIDTH, anchor="w", font=("Segoe UI", 30)).grid(row=5, column=0)

menu_швидкість = tk.OptionMenu(frame_форма, var_швидкість, "")
menu = menu_швидкість.nametowidget(menu_швидкість.menuname)
menu.config(font=("Arial", 30))
menu_швидкість.config(font=("Arial", 30), width=30)
menu_швидкість.grid(row=6, column=1, pady=5)
tk.Label(frame_форма, text="Швидкість:", width=LABEL_WIDTH, anchor="w", font=("Segoe UI", 30)).grid(row=6, column=0)

entry_ширина = tk.Entry(frame_форма, width=VIKNO, font=("Arial", 30))
entry_ширина.insert(0, "50")
entry_ширина.grid(row=7, column=1, pady=5)
entry_ширина.bind("<FocusIn>", показати_екранну_клавіатуру)  
tk.Label(frame_форма, text="Ширина (см):", width=LABEL_WIDTH, anchor="w", font=("Segoe UI", 30)).grid(row=7, column=0)

label_результат = tk.Label(вікно, text="", font=("Segoe UI", 30))
label_результат.pack()


def оновити_параметри_форсунки(*args):
    вибрана = var_форсунка.get()
    тиски = set()
    швидкості = set()
    for (_, name, pressure, speed, _) in форсунки_дані:
        if name == вибрана:
            тиски.add(str(pressure))
            швидкості.add(str(speed))
    menu_тиск['menu'].delete(0, 'end')
    for т in sorted(тиски):
        menu_тиск['menu'].add_command(label=т, command=lambda value=т: var_тиск.set(value))
    var_тиск.set("")
    menu_швидкість['menu'].delete(0, 'end')
    for ш in sorted(швидкості):
        menu_швидкість['menu'].add_command(label=ш, command=lambda value=ш: var_швидкість.set(value))
    var_швидкість.set("")
    label_результат.config(text="")

def оновити_площу(*args):
    вибране_поле = var_поле.get()
    if вибране_поле == "Не вказано поле":
        entry_площа.delete(0, tk.END)
    else:
        for (_, name, area) in поле_дані:
            if name == вибране_поле:
                entry_площа.delete(0, tk.END)
                entry_площа.insert(0, str(area))

def оновити_норму(*args):
    вибраний_препарат = var_препарат.get()
    if вибраний_препарат == "Не вказано препарат":
        entry_норма.delete(0, tk.END)
    else:
        for (_, name, rate_min, _) in препарати_дані:
            if name == вибраний_препарат:
                entry_норма.delete(0, tk.END)
                entry_норма.insert(0, str(rate_min))

def оновити_витрату_води(*args):
    global flow_rate
    назва = var_форсунка.get()
    тиск = var_тиск.get()
    швидкість = var_швидкість.get()
    if not (назва and тиск and швидкість):
        return
    for (_, name, p, s, rate) in форсунки_дані:
        if name == назва and str(p) == тиск and str(s) == швидкість:
            flow_rate = rate
            label_результат.config(text=f"Витрата води: {flow_rate:.2f} л/га")
            return
    label_результат.config(text="Витрату не знайдено для цієї комбінації.")

def розрахувати():
    try:
        площа = float(entry_площа.get())
        норма = float(entry_норма.get())
        витрата_води = float(flow_rate) * (площа / 100)

        вибраний_препарат = var_препарат.get()
        rate_max = None
        if вибраний_препарат != "Не вказано препарат":
            for (_, name, _, r_max) in препарати_дані:
                if name == вибраний_препарат:
                    rate_max = r_max
                    break
        else:
            rate_max = норма

        rate_max = float(rate_max)
        total_pesticide = площа * (норма / 100)
        total_pesticide1 = площа * (rate_max / 100)
        total_water = витрата_води + total_pesticide

        label_результат.config(
            text=f"Витрата води: {витрата_води:.1f} л\n"
                 f"Кількість препарату(min-max): {total_pesticide:.3f} - {total_pesticide1:.3f} л\n"
                 f"Загальна кількість робочого розчину: {total_water:.0f} л"
        )
    except ValueError:
        messagebox.showerror("Помилка", "Перевірте правильність введення чисел у полях.")
    except Exception as e:
        messagebox.showerror("Помилка", f"Невідома помилка: {str(e)}")

def зберегти_дані():
    try:
        поле = var_поле.get()
        площа = float(entry_площа.get())
        препарат = var_препарат.get()
        норма = float(entry_норма.get())
        форсунка = var_форсунка.get()
        тиск = float(var_тиск.get())
        швидкість = float(var_швидкість.get())
        витрата_води = float(flow_rate) * (площа / 100)
        total_pesticide = площа * (норма / 100)
        total_water = витрата_води + total_pesticide
        зберегти_в_історію(
            поле, площа, препарат, норма, форсунка, тиск,
            швидкість, витрата_води, total_pesticide, total_water
        )
        messagebox.showinfo("Збережено", "Дані успішно збережено в історії.")
    except Exception as e:
        messagebox.showerror("Помилка", f"Не вдалося зберегти: {str(e)}")

def відкрити_вікно_історії():
    вікно_історії = tk.Toplevel()
    вікно_історії.title("Історія")
    вікно_історії.geometry("1900x800")
    вікно_історії.grab_set()
    tree = tk.ttk.Treeview(вікно_історії, columns=(
        "id", "field", "area", "pesticide", "rate", "nozzle", "pressure", "speed",
        "flow", "pesticide_total", "water_total", "created_at"
    ), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=130)
    for запис in отримати_історію():
        tree.insert('', 'end', values=запис)
    tree.pack(expand=True, fill="both", pady=10, padx=10)
    def видалити_запис():
        вибране = tree.selection()
        if not вибране:
            messagebox.showwarning("Увага", "Оберіть запис для видалення.")
            return
        if not messagebox.askyesno("Підтвердження", "Ви впевнені, що хочете видалити запис?"):
            return
        for item in вибране:
            record_id = tree.item(item)["values"][0]
            видалити_з_історії(record_id)
            tree.delete(item)
    tk.Button(
        вікно_історії, text="Видалити вибране", command=видалити_запис,
        bg="#dc3545", fg="white", font=("Segoe UI", 30)
    ).pack(pady=5)

def оновити_меню_полів_та_препаратів():
    global поле_дані, препарати_дані

    поле_дані = отримати_поля()
    препарати_дані = отримати_препарати()
    menu_поле['menu'].delete(0, 'end')
    menu_поле['menu'].add_command(label="Не вказано поле", command=lambda: var_поле.set("Не вказано поле"))
    for (_, name, _) in поле_дані:
        menu_поле['menu'].add_command(label=name, command=lambda value=name: var_поле.set(value))

    menu_препарат['menu'].delete(0, 'end')
    menu_препарат['menu'].add_command(label="Не вказано препарат", command=lambda: var_препарат.set("Не вказано препарат"))
    for (_, name, _, _) in препарати_дані:
        menu_препарат['menu'].add_command(label=name, command=lambda value=name: var_препарат.set(value))

var_форсунка.trace_add("write", оновити_параметри_форсунки)
var_тиск.trace_add("write", оновити_витрату_води)
var_швидкість.trace_add("write", оновити_витрату_води)
var_поле.trace_add("write", оновити_площу)
var_препарат.trace_add("write", оновити_норму)

tk.Button(вікно, text="Розрахувати", command=розрахувати,
          bg="#0078D7", fg="white", font=("Segoe UI", 25, "bold"), width=50, height=1).pack(pady=2)

frame_кнопки = tk.Frame(вікно)
frame_кнопки.pack(pady=10)

tk.Button(frame_кнопки, text="Додати дані", 
          command=lambda: відкрити_вікно_додавання(оновити_меню_полів_та_препаратів),
          bg="#28a745", fg="white", font=("Segoe UI", 25), width=18).pack(side="left", padx=5)


tk.Button(frame_кнопки, text="Зберегти", command=зберегти_дані,
          bg="#007BFF", fg="white", font=("Segoe UI", 25), width=18).pack(side="left", padx=5)

tk.Button(frame_кнопки, text="Історія", command=відкрити_вікно_історії,
          bg="#6f42c1", fg="white", font=("Segoe UI", 25), width=18).pack(side="left", padx=5)

вікно.mainloop()