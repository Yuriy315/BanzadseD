import tkinter as tk
from tkinter import ttk, messagebox
import json
import os


class BookTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker")
        self.books = []
        self.filename = "books.json"
        self.load_books()
        self.create_widgets()
        self.update_table()

    def create_widgets(self):
        # --- Frame для ввода ---
        frame_input = ttk.LabelFrame(self.root, text="Добавить книгу")
        frame_input.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Поля ввода
        ttk.Label(frame_input, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_title = ttk.Entry(frame_input, width=30)
        self.entry_title.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Автор:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_author = ttk.Entry(frame_input, width=30)
        self.entry_author.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Жанр:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_genre = ttk.Entry(frame_input, width=30)
        self.entry_genre.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Страниц:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_pages = ttk.Entry(frame_input, width=10)
        self.entry_pages.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Кнопка добавления
        ttk.Button(frame_input, text="Добавить книгу", command=self.add_book).grid(row=4, column=0, columnspan=2,
                                                                                   pady=10)

        # --- Frame для фильтрации ---
        frame_filter = ttk.LabelFrame(self.root, text="Фильтр")
        frame_filter.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        ttk.Label(frame_filter, text="Жанр:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_genre_var = tk.StringVar()
        self.filter_genre = ttk.Entry(frame_filter, textvariable=self.filter_genre_var)
        self.filter_genre.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_filter, text="Мин. страниц:").grid(row=1, column=0, padx=5, pady=5)
        self.filter_pages_var = tk.StringVar()
        self.filter_pages = ttk.Entry(frame_filter, textvariable=self.filter_pages_var)
        self.filter_pages.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame_filter, text="Применить фильтр", command=self.apply_filter).grid(row=2, columnspan=2)

        # --- Таблица ---
        self.columns = ("title", "author", "genre", "pages")
        self.tree = ttk.Treeview(self.root, columns=self.columns, show="headings")

        for col in self.columns:
            self.tree.heading(col, text=self.get_header(col))
            self.tree.column(col, width=150)

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
    return {"title": "Название", "author": "Автор", "genre": "Жанр", "pages": "Страниц"}[col]


def add_book(self):
    title = self.entry_title.get().strip()
    author = self.entry_author.get().strip()
    genre = self.entry_genre.get().strip()
    pages_raw = self.entry_pages.get().strip()

    if not title or not author or not genre or not pages_raw:
        messagebox.showerror("Ошибка", "Все поля должны быть заполнены!")
        return

    if not pages_raw.isdigit():
        messagebox.showerror("Ошибка", "Количество страниц должно быть числом!")
        return

    pages = int(pages_raw)
    if pages <= 0:
        messagebox.showerror("Ошибка", "Количество страниц должно быть больше 0!")
        return

    book = {"title": title, "author": author, "genre": genre.lower(), "pages": pages}
    self.books.append(book)
    self.save_books()
    self.update_table()

    # Очистка полей после добавления
    self.entry_title.delete(0, tk.END)
    self.entry_author.delete(0, tk.END)
    self.entry_genre.delete(0, tk.END)
    self.entry_pages.delete(0, tk.END)


def apply_filter(self):
    genre_filter = self.filter_genre_var.get().strip().lower()

    try:
        min_pages = int(self.filter_pages_var.get())
        if min_pages < 0:
            min_pages = 0
            self.filter_pages_var.set("0")
            messagebox.showwarning("Предупреждение", "Мин. страниц не может быть отрицательным. Установлено 0.")
    except ValueError:
        min_pages = 0

    filtered_books = []

    for book in self.books:
        match_genre = (genre_filter == "") or (book["genre"] == genre_filter)
        match_pages = book["pages"] >= min_pages

        if match_genre and match_pages:
            filtered_books.append(book)

    self.display_books(filtered_books)


def update_table(self):
    self.display_books(self.books)


def display_books(self, books_to_display):
    for i in self.tree.get_children():
        self.tree.delete(i)

    for book in books_to_display:
        self.tree.insert("", tk.END,
                         values=(book["title"], book["author"], book["genre"], book["pages"]))


def save_books(self):
    with open(self.filename, 'w', encoding='utf-8') as f:
        json.dump(self.books, f, ensure_ascii=False)


def load_books(self):
    if os.path.exists(self.filename):
        with open(self.filename, 'r', encoding='utf-8') as f:
            try:
                self.books = json.load(f)
            except json.JSONDecodeError:
                self.books = []
                print("Файл данных поврежден или пуст.")
    else:
        self.books = []


if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()