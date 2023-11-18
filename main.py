import sqlite3
import accounts
import setting
import datetime
import hashlib
import block

conn = sqlite3.connect(setting.name_base) # Подключение к БД
cursor = conn.cursor()

def MainMenu(account):
	ViewCards(account)

	while True: 
		print("==============================================")
		print("Главное меню:")
		print("1) Мои карты")
		print("2) Выпуск новой карты")
		print("3) Переводы")
		print("9) Выход")
		print("==============================================")
		n = input("-> ")
		n = int(n)
		if n == 1:
			ViewCards(account)
		if n == 2:
			CreateCard(account)
		if n == 3:
			TransferMoney(account[1])
		elif n == 9:
			break 

def CreateAccount():
	while True: # Выход из цикла если логин свободен
		print("Для создания аккаунта введите будущий логин: ")
		login = input()
		try:
			cursor.execute("""
						SELECT count(*) FROM accounts WHERE login = ?
					""", [login])
		except sqlite3.DatabaseError as err:
				print('Error: ', err)
		else:			
			if cursor.fetchone()[0] != 0:
				print("Аккаунт с таким логином уже существует!")
			else:
				break
	while True: # Выход из цикла если пароли совпадают
		print("Введите ваш будущий пароль: ")
		password = input()
		print("Повторите пароль: ")
		re_password = input()
		if password == re_password:
			break
		else:
			print("Пароли не совпадают! Попробуйте ещё раз!")
			
	accounts.addaccount(login, password)

def CreateCard(account):
	owner = account[1]
	date = datetime.datetime.now().strftime("%d-%m-%Y %H:%M") # Получение текущей даты по шаблону
	numcard = hashlib.md5(date.encode('utf-8')).hexdigest() # Хеширование даты
	try:
		cursor.execute("""
			INSERT INTO cards (numcard, owner, balance, date)
			VALUES (?, ?, ?, ?)
		""", (numcard, owner, 0.0, date))
	except sqlite3.DatabaseError as err:
			print('Error: ', err)
	else:
		print("Карта ", numcard, "успешно выпущена!")
		conn.commit()

def ViewCards(account):
	cursor.execute("""
			SELECT * FROM cards WHERE owner = ?
		""", [account[1]])
	print("Ваши карты: ")
	userсards = cursor.fetchall()
	for item in userсards:
		print("ID карты: ", item[0], "Номер карты: ", item[1], "Остаток: ", item[3])

def TransferMoney(owner):
	while True:
		cardid_from = input("Введите id карты с которой вы хотите перевести: ")

		try:
			cursor.execute("""
						SELECT count(*) FROM cards WHERE cardid = ?
					""", (cardid_from))
		except sqlite3.DatabaseError as err:
				print('Error: ', err)
		else:	
			if cursor.fetchone()[0] == 0:
				print("Карта с таким id не найдена!")
				continue
		
		try:
			cursor.execute("""
						SELECT * FROM cards WHERE cardid = ?
					""", (cardid_from))
		except sqlite3.DatabaseError as err:
				print('Error: ', err)
		else:	
			if cursor.fetchone()[2] != str(owner):
				print("Вы не владелец данной карты!")
			else:
				break


			
	while True:
		cardid_to = input("Введите id карты на которую вы хотите перевести: ")

		try:
			cursor.execute("""
						SELECT count(*) FROM cards WHERE cardid = ?
					""", (cardid_to))
		except sqlite3.DatabaseError as err:
				print('Error: ', err)
		else:	
			if cursor.fetchone()[0] == 0:
				print("Карта с таким id не найдена!")
			else:
				break
	while True:
		amount = input("Введите сколько вы хотите перевести: ")
		amount = float(amount)

		try:
			cursor.execute("""
				SELECT * FROM cards WHERE cardid = ?
			""", (cardid_from))
		except sqlite3.DatabaseError as err:
				print('Error: ', err)
		else:
			cardfrom = cursor.fetchone()
			if float(cardfrom[3]) < amount:
				print("На карте нет столько денег!")
			else:
				break

	try:
		cursor.execute("""
			SELECT * FROM cards WHERE cardid = ?
		""", (cardid_to))
	except sqlite3.DatabaseError as err:
			print('Error: ', err)
	else:
		cardto = cursor.fetchone()	

	blockinfo = {
		"title": "Transfer",
		"amount": amount,
		"cardfrom": cardfrom[1],
		"cardto": cardto[1],
		"comments": "",
		"prev_hash": ""
	}

	balancefrom = float(cardfrom[3]) - amount
	balanceto = float(cardto[3]) + amount

	print(cardid_from)
	print(cardid_to)
	print(balancefrom)
	print(balanceto)
	try:
		cursor.execute("""
			UPDATE cards SET balance = ? WHERE cardid = ?
		""", (balancefrom, cardid_from))
	except sqlite3.DatabaseError as err:
			print('Error: ', err)
			blockinfo['comments'] += 'Error: ' + err
	else:
		conn.commit()

	try:
		cursor.execute("""
			UPDATE cards SET balance = ? WHERE cardid = ?
		""", (balanceto, cardid_to))
	except sqlite3.DatabaseError as err:
			print('Error: ', err)
			blockinfo['comments'] += 'Error: ' + err
	else:
		conn.commit()
	
	if owner == "dnfive":
		blockinfo['comments'] += 'From dnfive!'
	block.writeblock(blockinfo)
	print("Перевод успешно выполнен!")


def main():
	print('Добро пожаловать в Наш Банк!')
	print('Для пользования нашими услугами вам нужно авторизоваться')
	while True:
		print('У вас есть учётная запись? (Y/N)')
		answer = input()
		if answer == 'N' or answer == 'n':
			CreateAccount()
			break
		if answer == 'Y' or answer == 'y':
			break
		if answer != 'Y':
			print("Ошибка! Попробуйте ещё раз!")
	while True:
		print("Введите свой логин: ")
		login = input()
		try:
			cursor.execute("""
				SELECT * FROM accounts WHERE login = ?
				""", [login])
			account = cursor.fetchone()
			cursor.execute("""
					SELECT count(*) FROM accounts WHERE login = ?
				""", [login])
		except sqlite3.DatabaseError as err:
			print('Error: ', err)
		else:
			if cursor.fetchone()[0] == 0:
				print("Аккаунт с таким логином не найден!")
			else:
				break
	n = 3
	print("[DEBUG]: ") # DEBUG Message
	print(account)
	while True:
		print("Введите свой пароль: ")
		password = input()
		if password != account[2]:
			print("Пароль не верен! У вас есть " + str(n) + "/3 попыток")
		else:
			break

	print("Вы успешно вошли в аккаунт!")
	MainMenu(account)

main()
