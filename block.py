import sqlite3
import os
import hashlib
import setting


conn = sqlite3.connect(setting.name_base) # Подключение к БД
cursor = conn.cursor()

def get_hash(blockinfo):
	f = open('block.txt', 'w')
	f.write('title : ' + str(blockinfo['title']) + '\n')
	f.write('amount : ' + str(blockinfo['amount']) + '\n')
	f.write('cardfrom : ' + str(blockinfo['cardfrom']) + '\n')
	f.write('cardto : ' + str(blockinfo['cardto']) + '\n')
	f.write('comments: ' + str(blockinfo['comments']) + '\n')
	f.write('prev_hash : ' + str(blockinfo['prev_hash']) + '\n')
	f.close()
	file = open('block.txt', 'rb').read()
	h = hashlib.md5(file).hexdigest()
	path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'block.txt')
	os.remove(path)
	return h


def writeblock(blockinfo):
	cursor.execute("""
	 		SELECT MAX(nblock) FROM blockchain
	 	""")
	nblock = cursor.fetchone()[0]
	cursor.execute("""
			SELECT * FROM blockchain WHERE nblock = ?
		""", [nblock])
	prev_b = cursor.fetchone()
	prev_binfo = {'nblock': prev_b[0],
				  'title': prev_b[1],
				  'amount': prev_b[2],
				  'cardfrom': prev_b[3],
				  'cardto': prev_b[4],
				  'comments': prev_b[5],
				  'prev_hash': prev_b[6]}
	blockinfo['prev_hash'] = get_hash(prev_binfo)
	cursor.execute("""
		INSERT INTO blockchain (title, amount, cardfrom, cardto, comments, prev_hash)
		VALUES (?, ?, ?, ?, ?, ?)
	""", (blockinfo['title'], blockinfo['amount'], blockinfo['cardfrom'], blockinfo['cardto'], blockinfo['comments'], blockinfo['prev_hash']))
	conn.commit()