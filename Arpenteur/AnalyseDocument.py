#!/usr/bin/python3

from html.parser import HTMLParser
import string
import types
import re

##
# Classe permettant d'analyser une page HTML
# pour en extraire les liens et le texte
#
# La variable ok permet de ne pas analyser des parties du document (entete p. ex.)

class AnalyseDocument(HTMLParser):

	def __init__(self,document,documentType,erreurLog,strict=False):
		super().__init__(strict)
		self.erreurLog = erreurLog
		self.ancre={}
		self.texte=''
		self.ok = True;
		self.analyse(document,documentType)

	############ methodes d'analyse

	def handle_starttag(self,tag, attrs):
		if tag in ['a','base','link','area','frame','iframe']:
			href = [v for k, v in attrs if k=='href' or k=='src']
			if href:
				self.ancre[href[0]]=1
		if tag == "script":
			self.ok = False
		
	def handle_endtag(self, tag):
		if tag == "script":
			self.ok = True
	##
	# Recuperation du texte	du document
	def handle_data(self,text):
		if self.ok:
			self.texte+=text
			
	############ fin methodes d'analyse
	
	##
	# methode qui choisi le type d'analyse a effectuer sur le document source
	# le transcodage des differents formats se fait ici (pdf -> texte, ps -> texte) (non implante)
	# @param source source du document a analyser
	# @param typeDocument du document
	def analyse(self,source,typeDocument):
		if (re.search('text/html',typeDocument)):
			self.feed(source)
		elif (re.search('text/plain',typeDocument)):
			self.texte = source
	
	
	##
	# methode permettant la recuperation de l'attribut
	# texte
	def getTexte(self):
		# ajout blanc en debut et en fin comme separateur pour la recherche des mots
		return str(' '+self.texte+' ')
				
	##
	# methode permettant la recuperation de l'attribut
	# ancre
	def getAncre(self):
		return self.ancre

if __name__ == '__main__':
	res = open("../data/000/000/001/28-12-11_source").read()
	res = re.sub("<script(.|\n)*?</script>","",res,flags=re.I)
	parser = AnalyseDocument(res,"text/html",None)

