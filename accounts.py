import sqlite3
import setting

conn = sqlite3.connect(setting.name_base) # Подключение к БД
cursor = conn.cursor()

def addaccount(login, password):
	if len(login) == 0:
		return print("[Error] Len login = 0"); # Error code
	if len(password) == 0:
		return print("[Error] Len password = 0"); # Error code

	cursor.execute("""
			INSERT INTO accounts (login, password)
			VALUES (?, ?)
		""", (login, password))
	conn.commit()