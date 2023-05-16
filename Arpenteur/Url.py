#!/usr/bin/python3


# import local
from .ErreurLog import ErreurLog
from .Rl import Rl


##
# cette classe sera utilisee pour stocker les differentes informations liees
# a une URL. 
# On trouve les attributs suivants :
# <ul>
# <li> <tt>idUrl</tt> : identificateur unique de l'url dans le systeme de fichier</li>
# <li> <tt>url</tt> : l'url precede du protocole (http:// ou file:// p. ex.)</li>
# <li> <tt>nbTry</tt> : nombre d'essais avant telechargement</li>
# <li> <tt>date</tt> : une date associe a l'url</li>
# <li> <tt>erreurUrl</tt> : code d'erreur de telechargement, O pas de probleme, > 0 (p. ex. 404) erreur</li>
# <li> <tt>erreurFiltre</tt> : code d'erreur du filtre, 0 non filtre, != 0 filtre</li>
# <li> <tt>stable</tt> : indice de stabilite de la page (la page est elle suseptible d'etre modifie) (Non implante)</li>
# <li> <tt>erreurLog</tt> : pointeur gestion log et erreur</li>
# </ul>

class Url(Rl):
	
	# constructeurs
	
	def __init__(self,idUrl=0,url='',nbTry=0,date='',erreurUrl=0,erreurFiltre=0,stable=0,erreurLog=None):
		Rl.__init__(self,idUrl,idUrl,url,date,erreurLog)
		self.nbTry = nbTry
		self.erreurFiltre = erreurFiltre
		self.erreurUrl = erreurUrl
		self.stable = stable
	
	# methode permettant la recuperation de 
	#  idUrl           
	def getIdUrl(self):
		return Rl.getIdRl(self)
	
	# methode permettant l'affectation de 
	#  idUrl
	def putIdUrl(self,idUrl):
		Rl.putIdRl(self,idUrl)         

	# methode permettant la recuperation de 
	#  url           
	def getUrl(self):
		return Rl.getRl(self)

	# methode permettant l'affectation de 
	#  Url
	def putUrl(self,url):
		Rl.putRl(self,url)         
		
		
	# methode permettant la recuperation de l'attribut
	#  nbTry           
	def getNbTry (self):
		return self.nbTry

	# methode permettant l'affectation de l'attribut
	# nbTry         
	def putNbTry (self,nbTry):
		self.nbTry = nbTry
		
	##
	# methode permettant la recuperation de l'attribut
	# stable      
	def getStable (self):
		return self.stable

	##
	# methode permettant l'affectation de l'attribut
	# stable            
	def putStable (self,stable):
		self.stable = stable
		
	##
	# methode permettant la recuperation de l'attribut
	# erreurFiltre            
	def getErreurFiltre (self):
		return self.erreurFiltre

	##
	# methode permettant la recuperation de l'attribut
	# erreurUrl          
	def getErreurUrl (self):
		return self.erreurUrl

	##
	# methode permettant la recuperation de l'attribut
	# erreurFiltre            
	def putErreurFiltre (self,erreurFiltre):
		self.erreurFiltre = erreurFiltre

	##
	# methode permettant l'affectation de l'attribut
	# erreurUrl         
	def putErreurUrl (self,erreurUrl):
		self.erreurUrl = erreurUrl 
