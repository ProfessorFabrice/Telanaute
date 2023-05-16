#!/usr/bin/python
# -*- coding: utf-8

##
# projet Telanaute
# LLI 2004
# Classe Rl
##
import re

# import local
from . import ErreurLog

##
# cette classe sera utilisee pour stocker les differentes informations liees
# a une URL. 


class Rl:
	
	# constructeurs
	
	def __init__(self,idBase=0,idRl=0,rl='',date='',erreurLog=None):
		self.idBase = idBase
		self.idRl = idRl
		self.rl = rl
		self.date = date
		self.erreurLog = erreurLog
		

	##
	# methode permettant la recuperation de l'attribut
	# idBase            
	def getIdBase (self):
		return self.idBase

	##
	# methode permettant l'affectation de l'attribut
	# idBase            
	def putIdBase (self,idBase):
		self.idBase = idBase

	##
	# methode permettant la recuperation de l'attribut
	# idRl            
	def getIdRl (self):
		return self.idRl

	##
	# methode permettant l'affectation de l'attribut
	# idRl            
	def putIdRl (self,idRl):
		self.idRl = idRl


	# methode permettant la recuperation de l'attribut
	#  rl           
	def getRl (self):
		return self.rl

	# methode permettant l'affectation de l'attribut
	# rl         
	def putRl (self,rl):
		self.rl = re.sub(r'\'','\\\'',rl)

	# methode permettant la recuperation de l'attribut
	#  date           
	def getDate (self):
		return str(self.date)

	# methode permettant l'affectation de l'attribut
	# date         
	def putDate (self,date):
		self.date = date

				
