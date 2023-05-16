#!/usr/bin/python3

import re

##
##
# decoupe mot
class Traite(object):
	def __init__(self,nomCollection=''):
		# init
		self.mavariable=0
		self.nom = 'decoupeMot'
		self.decoupe = re.compile(r'[^-A-zàâéèêëîïôûùçÂÀÉÊÈËÎÏÔÛÙÇ]+')
		self.tr = str.maketrans('ABCDEFGHIJKLMNOPQRSTUVWXYZÂÀÉÊÈËÎÏÔÛÙÇ','abcdefghijklmnopqrstuvwxyzàâéèêëîïôûùç')
		self.sep = '\n'

		
	def traite(self,texte,nomfic):
		res = ''
		listemot = self.decoupe.split(texte)
		for mot in listemot:
			res = res + mot.translate(self.tr) + '\t' +mot + '\n'  
		return res
