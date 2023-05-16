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

class CollectionTraiteur(CollectionGenerique):
	# le constructeur de la classe permet d'initialiser les differentes variables de classe
	
	def __init__(self, nomFicCollection,erreurLog):
		CollectionGenerique.__init__(self,nomFicCollection,erreurLog)
		# chargement des greffons
		self.listeFiltreTraite = self.lectureGreffonsTraiteur(self.chargerListeAttribut('listetraitements','traitement','traite'))
		# lecture des données

		
	##
	# methode permettant la recuperation de l'attribut
	# listeFiltreSource           
	def getListeFiltreTraite(self):
		return self.listeFiltreTraite
		
