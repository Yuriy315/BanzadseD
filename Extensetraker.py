import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import json
import os
from datetime import datetime


class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.expenses = []
        self.filename = "expenses.json"
        self.load_expenses()
        self.create_widgets()
        self.update_table()

    def create_widgets(self):
        # --- Frame для ввода ---
        frame_input = ttk.LabelFrame(self.root, text="Добавить расход")
        frame_input.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Поля ввода
        ttk.Label(frame_input, text="Сумма:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_amount = ttk.Entry(frame_input, width=15)
        self.entry_amount.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Категория:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.combo_category = ttk.Combobox(frame_input, values=["Еда", "Транспорт", "Развлечения", "Жильё", "Здоровье"],
                                           state="readonly")
        self.combo_category.grid(row=1, column=1, padx=5, pady=5)
        self.combo_category.current(0)

        ttk.Label(frame_input, text="Дата:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.date_entry = DateEntry(frame_input, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        # Кнопка добавления
        ttk.Button(frame_input, text="Добавить расход", command=self.add_expense).grid(row=3, column=0, columnspan=2,
                                                                                       pady=10)

        # --- Frame для фильтрации и подсчёта ---
        frame_tools = ttk.LabelFrame(self.root, text="Инструменты")
        frame_tools.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        ttk.Label(frame_tools, text="Категория:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_category_var = tk.StringVar()
        self.filter_category = ttk.Combobox(frame_tools, textvariable=self.filter_category_var,
                                            values=["Все"] + ["Еда", "Транспорт", "Развлечения", "Жильё", "Здоровье"],
                                            state="readonly")
        self.filter_category.current(0)
        self.filter_category.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame_tools, text="Фильтр по категории", command=self.apply_filter).grid(row=0, column=2, padx=5)

        ttk.Label(frame_tools, text="Период:").grid(row=1, column=0, padx=5, pady=5)

        self.start_date = DateEntry(frame_tools, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.start_date.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_tools, text="по").grid(row=1, column=2, padx=2)

        self.end_date = DateEntry(frame_tools, width=12, background='darkblue', foreground='white', borderwidth=2)
        self.end_date.grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(frame_tools, text="Сумма за период", command=self.calculate_sum).grid(row=1, column=4, padx=5)

        # --- Таблица ---
        self.columns = ("date", "category", "amount")
        self.tree = ttk.Treeview(self.root, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=self.get_header(col))
            if col == "amount":
                self.tree.column(col, width=80, anchor="e")
            else:
                self.tree.column(col, width=180)

        self.tree.grid(row=2, column=0, sticky="nsew", padx=10)

        # Полосы прокрутки
        yscroll = ttk.Scrollbar(self.root, orient="vertical", command=self.tree.yview)
        xscroll = ttk.Scrollbar(self.root, orient="horizontal", command=self.tree.xview)

        self.tree.configure(yscroll=yscroll.set, xscroll=xscroll.set)

        yscroll.grid(row=2, column=1, sticky="ns")
        xscroll.grid(row=3, column=0, sticky="ew")

        # Настройка веса сетки для растягивания
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)


def get_header(self, col):
    return {"date": "Дата", "category": "Категория", "amount": "Сумма"}[col]


def add_expense(self):
    amount_raw = self.entry_amount.get().strip()
    category = self.combo_category.get()
    date_str = self.date_entry.get_date().strftime('%Y-%m-%d')

    if not amount_raw:
        messagebox.showerror("Ошибка", "Поле 'Сумма' не должно быть пустым!")
        return

    try:
        amount = float(amount_raw.replace(',', '.'))
        if amount <= 0:
            raise ValueError("Сумма должна быть больше нуля.")
    except ValueError as e:
        messagebox.showerror("Ошибка", f"Неверный формат суммы: {e}")
        return

    expense = {"date": date_str, "category": category.lower(), "amount": amount}
    self.expenses.append(expense)
    self.save_expenses()
    self.update_table()

    # Очистка поля суммы после добавления
    self.entry_amount.delete(0, tk.END)


def apply_filter(self):
    selected_cat = self.filter_category_var.get().lower()

    if selected_cat == "все":
        filtered_expenses = self.expenses
    else:
        filtered_expenses = [exp for exp in self.expenses if exp["category"] == selected_cat]

    self.display_expenses(filtered_expenses)


def calculate_sum(self):
    start_date = self.start_date.get_date()
    end_date = self.end_date.get_date()

    total = sum(
        exp["amount"] for exp in self.expenses
        if start_date <= datetime.strptime(exp["date"], '%Y-%m-%d') <= end_date
    )

    messagebox.showinfo("Итоговая сумма", f"Сумма расходов с {start_date.date()} по {end_date.date()}: {total:.2f} ₽")


def update_table(self):
    self.display_expenses(self.expenses)


def display_expenses(self, expenses_to_display):
    for i in self.tree.get_children():
        self.tree.delete(i)

    for exp in expenses_to_display:
        # Форматирование суммы с пробелом как разделителем тысяч и 2 знака после запятой
        formatted_amount = f"{exp['amount']:,.2f}".replace(',', ' ').replace('.', ',') + " ₽"
        self.tree.insert("", tk.END,
                         values=(exp["date"], exp["category"].capitalize(), formatted_amount))


def save_expenses(self):
    with open(self.filename, 'w', encoding='utf-8') as f:
        json.dump(self.expenses, f)


def load_expenses(self):
    if os.path.exists(self.filename):
        with open(self.filename, 'r', encoding='utf-8') as f:
            try:
                self.expenses = json.load(f)
            except json.JSONDecodeError:
                self.expenses = []
                print("Файл данных поврежден или пуст.")
    else:
        self.expenses = []


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()