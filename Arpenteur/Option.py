#!/usr/bin/python3

# import local
from .LectureXml import LectureXml

##
# Cette classe sera utilisee pour lire
# les informations lies au stockage des donnees recuperees.
# Cette classe herite de la classe <a href="pythondoc-LectureXml.html">LectureXml</a>.
# le fichier d'options doit respecter le DTD suivante :
# <pre>
# &lt;!ELEMENT option (base,sf)&gt;
# &lt;!ELEMENT base (nom,machine,port,utilisateur,mdp)&gt;
# &lt;!ELEMENT nom (#PCDATA)&gt;
# &lt;!ELEMENT machine (#PCDATA)&gt;
# &lt;!ELEMENT port (#PCDATA)&gt;
# &lt;!ELEMENT utilisateur (#PCDATA)&gt;
# &lt;!ELEMENT mdp (#PCDATA)&gt;
# &lt;!ELEMENT sf (base)&gt;
# &lt;!ELEMENT base (#PCDATA)&gt;
# &lt;!ELEMENT crawl (nbtry)&gt;
# &lt;!ELEMENT nbtry (#PCDATA)&gt;
# </pre>
# le constructeur de la classe permet d'initialiser les differentes variables de classe
# @param nomFicOption chemin et nom du fichier d'option sans l'extention ".xml"
# @param erreurLog Instance de la classe erreurLog


class Option(LectureXml):

	def __init__(self, nomFicOption, erreurLog):
		erreurLog.setVerboseOn()
		LectureXml.__init__(self,nomFicOption,erreurLog,'Option')
		# lecture des données
		self.nomBase = self.chargerNoeud('nom')
		self.machine = self.chargerNoeud('machine')
		self.port = int(self.chargerNoeud('port'))
		self.utilisateur = self.chargerNoeud('utilisateur')
		self.mdp = self.chargerNoeud('mdp')
		self.racineSf = self.chargerNoeud('racine')
		self.nbTry = self.chargerNoeud('nbtry')

	##
	# methode permettant la recuperation de l'attribut
	# nomBase            
	def getNomBase(self):
		return self.nomBase

	##
	# methode permettant la recuperation de l'attribut
	# machine            
	def getMachine (self):
		return self.machine

	##
	# methode permettant la recuperation de l'attribut
	# port            
	def getPort (self):
		return self.port

	##
	# methode permettant la recuperation de l'attribut
	# utilisateur            
	def getUtilisateur (self):
		return self.utilisateur

	##
	# methode permettant la recuperation de l'attribut
	# mdp            
	def getMdp (self):
		return self.mdp

	##
	# methode permettant la recuperation de l'attribut
	# racineSf            
	def getRacine (self):
		return self.racineSf

	##
	# methode permettant la recuperation de l'attribut
	# nbTry            
	def getNbTry (self):
		return self.nbTry

