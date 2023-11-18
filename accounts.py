import sqlite3
import setting

class Account:
    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.conn = sqlite3.connect(setting.name_base) # Подключение к БД
        self.cursor = self.conn.cursor()
        self.loaded = False

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
            return "Error: " + str(err)
        else:
            self.conn.commit()
            return "Successfull"
    
    def load(self):
        try:
            self.cursor.execute("""
            SELECT * FROM accounts WHERE login = ?
            """, [self.login])
            account = self.cursor.fetchone()
            self.cursor.execute("""
            SELECT count(*) FROM accounts WHERE login = ?
            """, [self.login])
        except sqlite3.DatabaseError as err:
            return "Error: " + str(err)
        else:
            if self.cursor.fetchone()[0] == 0:
                return "Account not found!"

        if self.password != account[2]:
            return "Password not True!"
        else:
            self.loaded = True
            return "Successfull"