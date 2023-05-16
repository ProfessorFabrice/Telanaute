#!/usr/bin/python3

import time
import string
import os
import re
import sys
import inspect

# import local
from Commun.ErreurLog import ErreurLog
from Commun.Lrl import *


##
# Cette classe effectue les differents traitements lies a une url, c'est-a-dire :
# <ul>
# <li>repérage des traitements a effectuer</li>
# <li>application des traitements</li>
# <li>sauvegarde des resultats dans le systeme de fichier</li>
# </ul>

class TraiteLrl:
	# constructeur
	def __init__(self,configCollection,erreurLog):
		self.erreurLog = erreurLog
		self.listeTraitements = configCollection.getListeFiltreTraite()
		self.nomCollection = configCollection.getNomCollection()
		
	##
	# Cette methode lance l'ensemble des traitements sur un fichier source.
	# @param lrlObjet un objet Lrl contenant le chemin vers le fichier a traiter (chemin+date)
	def traite(self,lrlObjet):
		precedentTraitement = ''
		lrlBase = lrlObjet.getLrl()+'_source'
		self.erreurLog.log("traitement de "+lrlBase)
		for m in self.listeTraitements:
			self.erreurLog.log("\tgreffon : "+m.nom)
			lrlPrecedent = lrlBase
			# ajout du nom du greffon
			lrlBase = lrlBase + '.' + m.nom
			if os.path.isfile(lrlBase):
				continue
			else: # le traitement n'a pas ete fait
				if precedentTraitement == '': # Si le resultat du precedent traitement n'est pas connu
					ficResPrecedent = open (lrlPrecedent)
					precedentTraitement = ficResPrecedent.read()
				fichierResultat = open (lrlBase,'w')
				# appel du greffon
				precedentTraitement = m.traite(precedentTraitement,lrlPrecedent)
				fichierResultat.write(precedentTraitement)
				fichierResultat.close()
		lrlObjet.putErreurTraite(0)
		return lrlObjet
		
	##
	# fermeture des greffons
	def close(self):
		for m in self.listeTraitements:
			m.close()

		
		
