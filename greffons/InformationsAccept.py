#!/usr/bin/python
# -*- coding: latin-1

##
# projet Telanaute
# LLI 2004
# Classe UrlReject
##

import re

##
# exemple de classe filtre url
class Filtre:
	def __init__(self):
		self.nom = 'InformationsAccept'
		# init
		self.filtreTypeAccept=[]
		for mime in ['text/html','text/plain']:
			self.filtreTypeAccept.append(re.compile(mime))
	
	##
	# methode de test
	def test(self,info):
		if info.has_key('Content-Type'):
			contentType = info['Content-Type']
			for filtre in self.filtreTypeAccept:
				if filtre.search(contentType):
					return True
		return False
