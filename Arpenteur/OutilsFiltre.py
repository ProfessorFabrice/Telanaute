#!/usr/bin/python3

from urllib.parse import urlparse,urlunparse,urljoin
import re
import string

# import local
from .ErreurLog import ErreurLog

##
# Cette classe permet de tester ou transformer une url.
# Elle est initialisee avec une liste de filtres sur des urls (<tt>filtreUrl</tt>)
# attribut de la classe <a href="pythondoc-Collection.html">Collection</a>
class OutilsFiltre(object):
	# Constructeur
	def __init__(self,configCollection,erreurLog):
		self.erreurLog = erreurLog
		self.listeFiltreSource = configCollection.getListeFiltreSource()
		self.listeFiltreUrl = configCollection.getListeFiltreUrl()
		self.listeFiltreInformations = configCollection.getListeFiltreInformations()
		self.parseJavascript = re.compile("[^']*'([^'\\\]*)") # ' <- juste pour la coloration syntaxique
	
	##
	# methode de normalisation d'une url.
	# Cette methode permet de mettres toutes les urls sous la forme :
	# http://...
	# @param urlbase url de la page ou le lien est trouve
	# @param url url du lien
	# @return string (l'url normalisee)
	
	def normaliseUrl(self,urlBase,url):
		url = re.sub(r'\'','%27',url)
		parseUrl = urlparse(url)
		parseUrlBase = urlparse(urlBase)
		# Pour distinguer repertoire de fichier (pb de urljoin)
		if re.search('/[^./]+$',parseUrlBase[2]) :
			urlBase+='/'
			parseUrlBase = urlparse(urlBase)
		#			 
		if parseUrl[0] =='javascript':
			urlres,site=self.normaliseUrl(urlBase,self.parseJavascript.sub('\g<1>',parseUrl[2]))
		elif parseUrl[0] != '' :
			urlres = url
			site = parseUrl[1].lower()
		else:
			urlBase = urlunparse(parseUrlBase) 			
			urlres = urljoin(urlBase,url)
			site = parseUrlBase[1].lower()
		return urlres,site
	

	##
	# application des differents filtres sur le source (texte)
	# @return vrai si le source passe TOUS les tests, faux sinon
	
	def testSource(self,texte):
		for m in self.listeFiltreSource:
			if not m.test(texte):
				return False
		return True
	
	##
	# application des differents filtres sur les urls
	# @return vrai si l'url passe TOUS les tests, faux sinon
	
	def testUrl(self,url):
		for m in self.listeFiltreUrl:
			if not m.test(url):
				return False
		return True
		
		
	##
	# application des differents filtres sur les informations d'une url (.info())
	# @return vrai si l'url passe TOUS les tests, faux sinon
	
	def testInformations(self,info):
		for m in self.listeFiltreInformations:
			try :
				if not m.test(info):
					return False
			except :
				return False
		return True
	##
	# appel d'une methode de fermeture
	
	def close(self):
		for m in self.listeFiltreInformations:
			m.close()
		for m in self.listeFiltreUrl:
			m.close()
		for m in self.listeFiltreSource:
			m.close()

