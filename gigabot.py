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


def main():
	banner()
	url = "http://giga.unitel.ao/api/game/question"
	gb = Gigabot(url)
	gb.get_question()
	gb.get_answers()
	gb.search_in_google()
	
if __name__ == '__main__':
	main()
