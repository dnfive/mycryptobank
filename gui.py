import tkinter as tk
from tkinter import messagebox
from accounts import *

class LoginApp:
	def __init__(self, root):
		self.root = root
		self.root.title("LegionBank - авторизация")
		self.root.geometry("400x400")
		self.conn = sqlite3.connect(setting.name_base) # Подключение к БД
		self.cursor = self.conn.cursor()

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

		result = Account(username, password).load()
		# Здесь можно добавить логику для проверки введенных данных
		# Например, проверить их с базой данных пользователей
		if result != "Successfull":
			messagebox.showerror("Ошибка входа", result)
		else:
			self.account = Account(username, password)
			messagebox.showinfo("Успешный вход", "Добро пожаловать, {}".format(username))
			root.destroy
			self.open_main_window()


	def registration(self):
		reg_login = self.reg_login_var.get()
		reg_pass = self.reg_pass_var.get()
		reg_pass_2 = self.reg_pass_2_var.get()
		try:
			self.cursor.execute("""
			SELECT count(*) FROM accounts WHERE login = ?
			""", [reg_login])
		except sqlite3.DatabaseError as err:
			messagebox.showerror("Ошибка базы данных", err)
		else:			
			if self.cursor.fetchone()[0] != 0:
				messagebox.showerror("Ошибка регистрации", "Аккаунт с таким логином уже существует!")
				return
		if reg_pass != reg_pass_2:
			messagebox.showerror("Ошибка регистрации", "Пароли не совпадают!")
			return
		else:
			self.account = Account(reg_login, reg_pass)
			result = self.account.create()
			if result != "Successfull":
				messagebox.showerror("Ошибка регистрации", result)
			else:
				messagebox.showinfo("Успешная регистрация!", "Добро пожаловать, {}".format(reg_login))
				registration_window.destroy

	def open_registration_window(self):
		# Создание нового окна для регистрации
		self.reg_login_var = tk.StringVar()
		self.reg_pass_var = tk.StringVar()
		self.reg_pass_2_var = tk.StringVar()
		registration_window = tk.Toplevel(self.root)
		registration_window.title("LegionBank - регистрация")
		registration_window.geometry("400x400")

		# Здесь можно добавить виджеты для ввода данных при регистрации
		# Например, поля для ввода логина, пароля, подтверждения пароля и т.д.

		tk.Label(registration_window, text="Логин:").pack(pady=10)
		tk.Entry(registration_window, textvariable=self.reg_login_var).pack(pady=5)

		tk.Label(registration_window, text="Пароль:").pack(pady=10)
		tk.Entry(registration_window, textvariable=self.reg_pass_var, show="*").pack(pady=5)

		tk.Label(registration_window, text="Подтвердите пароль:").pack(pady=10)
		tk.Entry(registration_window, textvariable=self.reg_pass_2_var, show="*").pack(pady=5)

		# Кнопка для завершения регистрации
		tk.Button(registration_window, text="Зарегистрироваться", command=self.registration).pack(pady=10)

	def open_main_window(self):
		self.main_window = tk.Toplevel(self.root)
		self.main_window.title("LegionBank - главная")
		self.main_window.geometry("500x500")

		# Создание метки с заголовком
		label = tk.Label(self.main_window, text="Личный кабинет - dnfive", font=("Arial", 20))
		label.pack(pady=10)

		# Создание кнопок
		button1 = tk.Button(self.main_window, text="Мои карты", command=self.open_my_cards)
		button1.pack(pady=5)

		button2 = tk.Button(self.main_window, text="Выпуск новой карты", command=self.issue_new_card)
		button2.pack(pady=5)

		button3 = tk.Button(self.main_window, text="Переводы", command=self.open_transfers)
		button3.pack(pady=5)

		button4 = tk.Button(self.main_window, text="Выход", command=self.exit_app)
		button4.pack(pady=5)

	def open_my_cards(self):
		my_cards = tk.Toplevel(self.root)
		my_cards.title("LegionBank - Мои карты")
		my_cards.geometry("600x400")

		self.cursor.execute("""
			SELECT * FROM cards WHERE owner = ?
		""", [self.account.login])
		userсards = self.cursor.fetchall()
		for item in userсards:
			label = tk.Label(my_cards, text="ID карты: " + str(item[0]) + " Номер карты: " + str(item[1]) + "Остаток: " + str(item[3]), font=("Arial", 8))
			label.pack(pady=10)


	def issue_new_card(self):
		owner = self.account.login
		date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M") # Получение текущей даты по шаблону
		numcard = hashlib.md5(date.encode('utf-8')).hexdigest() # Хеширование даты
		try:
			self.cursor.execute("""
				INSERT INTO cards (numcard, owner, balance, date)
				VALUES (?, ?, ?, ?)
			""", (numcard, owner, 0.0, date))
		except sqlite3.DatabaseError as err:
				messagebox.showerror("Ошибка базы данных", err)
		else:
			messagebox.showinfo("Выпуск карты", "Карта {} успешно выпущена".format(numcard))
			self.conn.commit()

	def open_transfers(self):
		print("Открытие страницы 'Переводы'")
		# Добавьте свой код открытия страницы "Переводы" здесь

	def exit_app(self):
		print("Выход из приложения")
		messagebox.showinfo("Выход", "До свидания, {}".format(self.account.login))
		self.main_window.destroy()


if __name__ == "__main__":
	root = tk.Tk()
	app = LoginApp(root)
	root.mainloop()