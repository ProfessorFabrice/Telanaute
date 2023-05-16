#!/usr/bin/python3

##
# projet Telanaute
# LLI 2004
# Classe Lrl
##


# import local
#from Commun.ErreurLog import ErreurLog
from Commun.Rl import Rl

##
# cette classe sera utilisee pour stocker les differentes informations liees
# a une "Local Ressource Locator" (LRL). 
# On trouve les attributs suivants :
# <ul>
# <li> <tt>idBase</tt> : identifiant de la base de donnees
# <li> <tt>idLrl</tt> : identificateur unique de l'url dans le systeme de fichier</li>
# <li> <tt>lrl</tt> : local ressource locator sans "_source"</li>
# <li> <tt>prefixe</tt> : nature de la source des documents (WEB : web, LM:LeMonde, ...) limite a 4 caracteres</li>
# <li> <tt>date</tt> : une date associe a l'lrl</li>
# <li> <tt>erreurTraite</tt> : code d'erreur des traitements</li>
# <li> <tt>erreurLog</tt> : pointeur gestion log et erreur</li>
# </ul>

class Lrl(Rl):
	
	# constructeurs
	
	def __init__(self,idBase=0,idLrl=0,lrl='',prefixe='',date='',erreurTraite=0,erreurLog=None):
		Rl.__init__(self,idBase,idLrl,lrl,date,erreurLog)
		self.erreurTraite = erreurTraite

	# methode permettant la recuperation de 
	#  idLrl           
	def getIdBase(self):
		return Rl.getIdBase(self)
	
	# methode permettant l'affectation de 
	#  idUrl
	def putIdBase(self,idBase):
		Rl.putIdBase(self,idBase)         

	# methode permettant la recuperation de 
	#  idLrl           
	def getIdLrl(self):
		return Rl.getIdRl(self)
	
	# methode permettant l'affectation de 
	#  idUrl
	def putIdLrl(self,idLrl):
		Rl.putIdRl(self,idUrl)         

	# methode permettant la recuperation de 
	#  url           
	def getLrl(self):
		return Rl.getRl(self)

	# methode permettant l'affectation de 
	#  Url
	def putLrl(self,url):
		Rl.putRl(self,url)         
		
	# methode permettant la recuperation de 
	#  prefixe           
	def getPrefixe(self):
		return self.prefixe

	# methode permettant l'affectation de 
	#  prefixe
	def putPrefixe(self,prefixe):
		self.prefixe = prefixe

	# methode permettant la recuperation de l'attribut
	#  erreurTraite           
	def getErreurTraite (self):
		return self.erreurTraite

	# methode permettant l'affectation de l'attribut
	# nbTry         
	def putErreurTraite (self,erreurTraite):
		self.erreurTraite = erreurTraite

