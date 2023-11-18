import sqlite3
import setting

conn = sqlite3.connect(setting.name_base) # Подключение к БД
cursor = conn.cursor()

# Создание таблицы
cursor.execute("""
		CREATE TABLE blockchain
		(nblock integer primary key autoincrement, title text, amount real, cardfrom text, 
		cardto text, prev_hash text)
	""") 

# Генезис блок
 cursor.execute("""
		INSERT INTO blockchain
		VALUES ('Init', 10000.0, 'b9445fd413438e890f4de2cfac1766a2', 'b9445fd413438e890f4de2cfac1766a2', '0')
	""")

# Таблица с картами
cursor.execute("""
		CREATE TABLE cards
		(numcard text, owner text, balance real)
	""")
# Генезис карта
cursor.execute("""
		INSERT INTO cards
		VALUES ('b9445fd413438e890f4de2cfac1766a2', 'dnfive', 10000.0)
	""")
conn.commit()