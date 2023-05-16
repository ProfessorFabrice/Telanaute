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
		self.nom = 'InformationsReject'
		# init
		self.tailleMax=4096000
	
	##
	# methode de test
	def test(self,info):
		if info.has_key('content-length') :
			if int(info['content-length']) > self.tailleMax :
				return False            
		return True
