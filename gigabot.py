try:
	import requests
	import sqlite3
	import json
	import re
	import time
	from bs4 import BeautifulSoup
	from modules.headers import Headers
	from modules.banner import banner, menu
	from modules.bootstrapy import Strapy

except ImportError:
	exit("Erro ao tentar importar algum módulo")



class Gigabot():

	"""docstring for Gigabot"""
	def __init__(self, url):
		self.url = url

	def start_game(self):
		headers = Headers.headers_start
		with open('start.json', 'r') as start:
			data = start.read()
			obj = json.loads(data)
			start = requests.post("http://giga.unitel.ao/api/game/start",data=obj, headers=headers)
			print(start)
			print(start.text)
	
	def get_database(self):
		conn = sqlite3.connect('perguntas.db')
		return conn



	def get_question(self):	
		headers = Headers.headers_question
		self.re = requests.get(self.url, headers=headers)
		question = self.re
		question = question.text
		#Find(str)
		start = question.find('label')
		end = question.find('answers')

		print("=== QUESTÃO ===\n")
		print(question[start+8:end-3].upper())
		self.find_question = question[start+8:end-3]
		#:{"moveId":4628870481,"stageIndex":1
		movstart = question.find('moveId')
		movend = question.find('stageIndex')
		self.moveId = question[movstart+8:movend-2]

	def answered(self,answer):
		headers = Headers.answer
		payload = {
			"moveId":int(self.moveId),
			"index":int(answer),
			"help":None,
			"time": 20,
			"optional":None
		}
		with open('answer.json', 'r') as answer:
			data = answer.read()
			obj = json.loads(data)
		#print(payload)
		answer = requests.post("http://giga.unitel.ao/api/game/answer",data=obj, headers=headers)
		print(answer)


	def get_answers(self):
		headers = Headers.headers_question
		answers = self.re
		answers = answers.text
		an1 = answers.find("\"index\":0")
		an2 = answers.find('\"index\":1')
		an3 = answers.find('\"index\":2')
		an4 = answers.find('\"index\":3')
		an5 = answers.find('timeToAnswer')
		#Answers {a, b, c, d}
		self.a = answers[an1+19:an2-4]
		self.b = answers[an2+19:an3-4]
		self.c = answers[an3+19:an4-4]
		self.d = answers[an4+19:an5-5]
		print("\n\n=== RESPOSTAS ===")		
		print(f"A - {self.a}\nB - {self.b}\nC - {self.c}\nD - {self.d}\n".upper())
		self.answers_list= [self.a,self.b,self.c,self.d]
		
	def get_all_questions_in_db(self):
		conn = sqlite3.connect('quizdeomilhao.db')
		cursor = conn.cursor()
		cursor = conn.execute('SELECT * FROM quizdeomilhao')
		for row in cursor:
			print(f"{row[0]} - {row[1]} \n {row[2]}")

		#print(Strapy.RUN+"A pesquisar perguntas no banco de dados..."+Strapy.END)

		#print(Strapy.GOOD+"Pergunta(s) encontrada(s) no banco de dados!"+Strapy.END)
		#for row in cursor:
		#	print(f"Id: {row[0]} \nPergunta: {row[1]} \nResposta: {row[2]}")

		#if not str in cursor:
		#	print(Strapy.BAD+"Pergunta(s) não encontrada(s) no banco de dados!"+Strapy.END)
		#	return False

		conn.close()


	def get_question_in_db(self):
		#cursor = self.get_question_in_db()
		conn = self.get_database()
		cursor = conn.cursor()
		question = self.find_question.split("\\")
		cursor = conn.execute('SELECT * FROM Quiz WHERE question ==« "{}"'.format(question))

		print(Strapy.RUN+"A pesquisar resposta no banco de dados..."+Strapy.END)

		for row in cursor:
			if row[1]:
				print(Strapy.GOOD+"Resposta encontrada no banco de dados!"+Strapy.END)
				print(f"Id: {row[0]} \nPergunta: {row[1]} \nResposta: {row[2]}\n")
				self.verify_db = True

		if not str in cursor:
			print(Strapy.BAD+"Resposta não encontra no banco de dados!"+Strapy.END)
			self.verify_db = False

	def get_question_in_db2(self):
		question = self.find_question.split("\\")
		conn = sqlite3.connect('quizdeomilhao.db')
		cursor = conn.cursor()
		cursor = conn.execute('SELECT * FROM quizdeomilhao WHERE question = "{}"'.format(question))
		print("«««BUSCANDO NO QUIZDOMILHÃO»»»")
		for row in cursor:
			print(f"{row[0]} - {row[1]} \n {row[2]}")

		#print(Strapy.RUN+"A pesquisar resposta no banco de dados 2 ..."+Strapy.END)

		#for row in cursor:
		#	print(Strapy.GOOD+"Resposta encontrada no banco de dados!"+Strapy.END)
		#	print(f"Id: {row[0]} \nPergunta: {row[1]} \nResposta: {row[2]}\n")
		#	self.verify_db2 = True

		#if not str in cursor:
		#	print(Strapy.BAD+"Resposta não encontra no banco de dados!"+Strapy.END)
		#	self.verify_db2 = True


	def search_in_google(self):
		#search = requests.get("https://www.google.com/search?q="+self.find_question)
		search = requests.get("https://www.google.com/search?q="+self.find_question)
		soup = BeautifulSoup(search.text, 'html.parser')
		
		#print(self.answers_list)
		#924482776
		for answer in self.answers_list:
			#a = soup.find(answer)
			#print("BeautifulSoup")
			#a=soup.body.find_all(text=answer)
			#print(a)
			#print("Regex")
			result = re.search(r''+answer, soup.prettify()) 
			print("«««BUSCANDO NO GOOGLE»»»")
			print(result)
			#if result.group() in self.answers_list:
			#	print("Respostas achada pelo google:")
			#	print(result.group())
			#	self.verify_google = True
		#self.verify_google = True

	def save_question_in_db(self):

		print(Strapy.RUN+"Salvando a resposta manualmente..."+Strapy.END)

		verify_in_db = self.verify_db
		verify_in_db2 = self.verify_db2
		if verify_in_db == False | verify_in_db2 == False:
			print(Strapy.INFO+"Insere a resposta manualmente, somente a resposta\n Exemplo: \"Manteiga\" e não \"b) Manteiga\"\n"+Strapy.END)
			my_answer = str(input("Porfavor insere a resposta ex:(Macaco) "))
			
			while not my_answer:
				print(Strapy.BAD+"Insere uma resposta, verfica a resposta do portal :("+Strapy.END)
				my_answer
				if my_answer:
					print(Strapy.RUN+"Salvando a resposta..."+Strapy.END)
					conn = self.get_database()
					cursor = conn.cursor()
					cursor.execute('INSERT INTO Quiz(question,answer) VALUES(?,?)',
									(self.find_question, my_answer))
					conn.commit()
					conn.close()
					print(Strapy.GOOD+"Resposta salva no banco!"+Strapy.END)


def main():
	banner()
	url = "http://giga.unitel.ao/api/game/question"
	gb = Gigabot(url)
	#bg.start_game()
	#bg.start_game()
	#gb.get_question()
	#gb.get_answers()
	#gb.get_question_in_db()
	#gb.get_question_in_db2()
	#resposta = input("\nInsere a resposta:")
	#bg.answered(resposta)
	#bg.search_in_google()
	#bg.save_question_in_db()
	gb.get_question()
	gb.get_answers()
	#gb.get_question_in_db()
	#gb.get_question_in_db2()
	gb.search_in_google()
	
	#menu()
	#bg.get_all_questions_in_db()
	"""
	try:
		opt = int(input(">>>"))
	except ValueError:
		print("Somente números!")
	if opt == 1:
		bg.start_game()
	elif opt == 2:
		bg.get_all_questions_in_db()
	
	elif opt == 3:
		bg.save_question_in_db()


	elif opt == 4:
		bg.get_question()
		bg.get_answers()
		bg.get_question_in_db()
		bg.get_question_in_db2()
		bg.search_in_google()
		#bg.save_question_in_db()
	else:
		exit("Saindo!")
	"""
if __name__ == '__main__':
	main()
