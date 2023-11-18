import tkinter as tk
from tkinter import messagebox
from accounts import *

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LegionBank - авторизация")
        self.root.geometry("400x400")

        # Переменные для хранения введенных данных
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Создание виджетов для окна входа
        tk.Label(root, text="Логин:").pack(pady=10)
        tk.Entry(root, textvariable=self.username_var).pack(pady=5)
        tk.Label(root, text="Пароль:").pack(pady=10)
        tk.Entry(root, textvariable=self.password_var, show="*").pack(pady=5)

        # Кнопка для входа
        tk.Button(root, text="Войти", command=self.login).pack(pady=10)

        # Кнопка для открытия окна регистрации
        tk.Button(root, text="Регистрация", command=self.open_registration_window).pack(pady=5)

    def login(self):
        # Получение введенных данных
        username = self.username_var.get()
        password = self.password_var.get()

        result = LoadAccount(username, password)
        # Здесь можно добавить логику для проверки введенных данных
        # Например, проверить их с базой данных пользователей
        if result != "Successfull":
            messagebox.showerror("Ошибка входа", result)
        else:
            account = Account(username, password)
            messagebox.showinfo("Успешный вход", "Добро пожаловать, {}".format(username))

        
        # Пример простой проверки
        # if username == "user" and password == "password":
        #     messagebox.showinfo("Успешный вход", "Добро пожаловать, {}".format(username))
        # else:
        #     messagebox.showerror("Ошибка входа", "Неверный логин или пароль")

    def open_registration_window(self):
        # Создание нового окна для регистрации
        registration_window = tk.Toplevel(self.root)
        registration_window.title("LegionBank - регистрация")
        registration_window.geometry("400x400")

        # Здесь можно добавить виджеты для ввода данных при регистрации
        # Например, поля для ввода логина, пароля, подтверждения пароля и т.д.

        tk.Label(registration_window, text="Логин:").pack(pady=10)
        tk.Entry(registration_window).pack(pady=5)

        tk.Label(registration_window, text="Пароль:").pack(pady=10)
        tk.Entry(registration_window, show="*").pack(pady=5)

        tk.Label(registration_window, text="Подтвердите пароль:").pack(pady=10)
        tk.Entry(registration_window, show="*").pack(pady=5)

        # Кнопка для завершения регистрации
        tk.Button(registration_window, text="Зарегистрироваться", command=registration_window.destroy).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()