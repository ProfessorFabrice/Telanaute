#!/usr/bin/python3

import sys

# import local
from Commun.CollectionGenerique import CollectionGenerique

##
# cette classe sera utilisee pour lire
# les informations d'une collection. Cette classe herite de la classe <a href="pythondoc-LectureXml.html">LectureXml</a>.
# le fichier de configuration doit respecter le DTD suivante :
# <pre>
# &lt;!ELEMENT collection (nom,graine,filtres,profondeur,nbrobotsfils,tailletamponrobotsfils,tailletamponurlaranger,tailletamponurlatraiter)&gt;
# &lt;!ELEMENT nom (#PCDATA)&gt;
# &lt;!ELEMENT graine (url+)&gt;
# &lt;!ELEMENT url (#PCDATA)&gt;
# &lt;!ELEMENT listefiltres (filtre)&gt;
# &lt;!ELEMENT filtre (#PCDATA)&gt;
# &lt;!ATTLIST filtre type CDATA #REQUIRED&gt;
# &lt;!ELEMENT profondeur (#PCDATA)&gt;
# &lt;!ELEMENT nbrobotsfils (#PCDATA)&gt;
# &lt;!ELEMENT tailletamponrobotsfils (#PCDATA)&gt;
# &lt;!ELEMENT tailletamponurlaranger (#PCDATA)&gt;
# &lt;!ELEMENT tailletamponurlatraiter (#PCDATA)&gt;
# </pre>
# le constructeur de la classe permet d'initialiser les differentes variables de classe
# @param nomFicCollection chemin et nom du fichier d'option sans l'extention ".xml"
# @param erreurLog Instance de la classe erreurLog

class CollectionArpenteur(CollectionGenerique):
	# le constructeur de la classe permet d'initialiser les differentes variables de classe
	
	def __init__(self, nomFicCollection, erreurLog):
		CollectionGenerique.__init__(self,nomFicCollection,erreurLog)
		self.erreurLog.setVerboseOn()
		# chargement des greffons
		self.listeFiltreSource = self.lectureGreffonsArpenteur(self.chargerListeAttribut('listefiltres','filtre','source'))
		self.listeFiltreUrl = self.lectureGreffonsArpenteur(self.chargerListeAttribut('listefiltres','filtre','url'))
		self.listeFiltreInformations = self.lectureGreffonsArpenteur(self.chargerListeAttribut('listefiltres','filtre','informations'))
		# lecture des données
		self.graine = self.chargerListe('graine','url')
		self.profondeur = self.chargerNoeud('profondeur')
		self.maxpagesparsite = self.entier(self.chargerNoeud('maxpagesparsite'))

		
	##
	# methode permettant la recuperation de l'attribut
	# listeFiltreSource           
	def getListeFiltreSource(self):
		return self.listeFiltreSource
		
	##
	# methode permettant la recuperation de l'attribut
	# listeFiltreUrl   
	def getListeFiltreUrl(self):
		return self.listeFiltreUrl

	##
	# methode permettant la recuperation de l'attribut
	# listeFiltreUrl   
	def getListeFiltreInformations(self):
		return self.listeFiltreInformations

	##
	# methode permettant la recuperation de l'attribut
	#
	def getGraine (self):
		return self.graine

	##
	# methode permettant la recuperation de l'attribut
	# profondeur
	def getProfondeur(self) :
		return self.profondeur
		
	##
	# methode permettant la recuperation de l'attribut
	# maxpagesparsite
	def getMaxPagesParSite(self) :
		return self.maxpagesparsite
		
