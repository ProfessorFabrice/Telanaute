#!/usr/bin/python3

import sys

# import local
from .LectureXml import LectureXml

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
# &lt;!ELEMENT tailletamponrobotsfils (#PCDATA)&gt;
# &lt;!ELEMENT tailletamponaranger (#PCDATA)&gt;
# &lt;!ELEMENT tailletamponatraiter (#PCDATA)&gt;
# </pre>
# le constructeur de la classe permet d'initialiser les differentes variables de classe
# @param nomFicCollection chemin et nom du fichier d'option sans l'extention ".xml"
# @param erreurLog Instance de la classe erreurLog

class CollectionGenerique(LectureXml):
	# le constructeur de la classe permet d'initialiser les differentes variables de classe
	
	def __init__(self, nomFicCollection, erreurLog):
		LectureXml.__init__(self,nomFicCollection,erreurLog,'Collection')
		# pour la lecture des greffons
		sys.path.append('./greffons')
		# lecture des données
		self.nomCollection = self.chargerNoeud('nom')
		

	##
	# methode permettand de lire et stocker les greffons de l'arpenteur
	# @param listeNomGreffons une liste des noms de greffons a telecharger dans le repertoire "greffons"
	# @return la liste des pointeurs
	def lectureGreffonsArpenteur(self,listeNomGreffons):
		liste = []
		for m in listeNomGreffons:
			try:
				self.erreurLog.log('chargement greffon '+str(m))
				tmpmodule = __import__(m,globals(),locals(),[m])
				liste.append(tmpmodule.Filtre())
			except Exception as msg:
				self.erreurLog.erreur('Collection','lectureGreffonsArpenteur','chargement greffon '+m+' impossible\n',-10,msg)
		return liste
	##
	# methode permettand de lire et stocker les greffons du traiteur
	# @param listeNomGreffons une liste des noms de greffons a telecharger dans le repertoire "greffons"
	# @return la liste des pointeurs
	def lectureGreffonsTraiteur(self,listeNomGreffons):
		liste = []
		for m in listeNomGreffons:
			try:
				self.erreurLog.log('chargement greffon '+m)
				tmpmodule = __import__(m,globals(),locals(),[m])
				liste.append(tmpmodule.Traite(self.nomCollection))
			except Exception as msg:
				raise
				self.erreurLog.erreur('Collection','lectureGreffonsTraiteur','chargement greffon '+m+' impossible\n',-10,msg)
		return liste
	##
	# methode permettant la recuperation de l'attribut
	# nomCollection            
	def getNomCollection(self):
		return self.nomCollection
		
	##
	# methode permettant la recuperation de l'attribut
	# nbRobotsFils
	def getNbRobotsFils(self) :
		return self.nbRobotsFils
				
	##
	# methode permettant la recuperation de l'attribut
	# tailleTamponUrlARanger
	def getTailleTamponARanger(self) :
		return self.tailleTamponARanger
		
	##
	# methode permettant la recuperation de l'attribut
	# tailleTamponUrlATraiter
	def getTailleTamponATraiter(self) :
		return self.tailleTamponATraiter
