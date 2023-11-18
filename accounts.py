import sqlite3
import setting



class Account:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.conn = sqlite3.connect(setting.name_base) # Подключение к БД
        self.cursor = self.conn.cursor()

    def create(self):
        if len(self.login) == 0:
            return "[Error] Len login"
        if len(self.password) == 0:
            return "[Error] Len password"
        try:
            self.cursor.execute("""
            INSERT INTO accounts (login, password)
            VALUES (?, ?)
            """, (login, password))
        except sqlite3.DatabaseError as err:
            return "Error: " + err
        else:
            self.conn.commit()
            return "Successfull"


def LoadAccount(login, password):
	conn = sqlite3.connect(setting.name_base) # Подключение к БД
	cursor = conn.cursor()
	try:
		cursor.execute("""
		SELECT * FROM accounts WHERE login = ?
		""", [login])
		account = cursor.fetchone()
		cursor.execute("""
			SELECT count(*) FROM accounts WHERE login = ?
		""", [login])
	except sqlite3.DatabaseError as err:
		return "Error: " + err
	else:
		if cursor.fetchone()[0] == 0:
			return "Account not found!"

	if password != account[2]:
		return "Password not True!"
	else:
		return "Successfull"