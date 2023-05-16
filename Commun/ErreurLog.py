#!/usr/bin/python3

import sys
import os
import time
import re

# import local

#from LectureXml import LectureXml

##
# cette classe implemente des methode permettant de gerer 
# les erreurs et les fichiers de log.
# Les methodes <tt>setVerboseOn</tt> et <tt>setVerboseOff</tt> permettent
# d'activer ou non l'affichage des messages de python.
# cette classe fait appel a la classe <a href="pythondoc-LectureXml.html">LectureXml</a>
# ou la gestion des erreurs sera desactive.
# @param nomOption chemin et nom du fichier d'option sans l'extention ".xml"
# @param nomCollection chemin et nom du fichier de la collection sans l'extention ".xml"

class ErreurLog:
	
	# constructeur
	def __init__(self,nomficlog='telanaute.log'):
		self.verbose = 0
		self.nomficlog = nomficlog
		# par defaut sortie des logs sur ecran
		self.setLogEcran()

	##
	# methode permettant de gerer les fichiers de log et les erreurs
	# @param nomClasse Nom de la classe ou l'erreur s'est produite
	# @param nomMethode Nom de la methode ou l'erreur s'est produite
	# @param commentaire Commentaire sur l'erreur
	# @param numErreur Code de sortie de l'erreur (superieur a 0 sortie du programme)
	# @param msg message de python
	
	def erreur(self,nomClasse,nomMethode,commentaire,numErreur,msg):
		texteSortie = time.asctime(time.localtime())
		if numErreur == 0:
			texteSortie = '=INFO=' + texteSortie 
		texteSortie = texteSortie+':'+nomClasse+"/"+nomMethode+" ** "+commentaire
		self.sortieLog.write(texteSortie)
		if self.verbose :
			self.sortieLog.write(' '+str(msg)+'\n')
		if numErreur > 0:
			sys.exit(0)
	
	##
	# methode permettant d'afficher un message dans le fichier de log
	# @param message message a afficher
	
	def log(self,message):
		texteSortie = time.asctime(time.localtime())
		self.sortieLog.write(texteSortie+'=LOG='+message+'\n')
	
	##
	# methode activant le mode verbose
	
	def setVerboseOn(self):
		self.verbose = 1
	
	##
	# methode desactivant le mode verbose

	def setVerboseOff(self):
		self.verbose = 0

	##
	# methode permettant l'affichage des logs a l'ecran
	def setLogEcran(self):
		self.sortieLog = sys.stderr
		
	##
	# methode permettant l'affichage des logs dans un fichier
	def setLogFichier(self):
		self.sortieLog = open(self.nomficlog,"a")
		
		
		
