#!/usr/bin/python3

import sys

# import local
from xml.dom.minidom import parse, parseString
from .ErreurLog import ErreurLog

##
# cette classe sera utilisee pour lire
# les informations stockées dans des fichiers xml.
# le constructeur de la classe prend les parametres suivants
# @param nom chemin et nom du fichier a lire sans l'extention ".xml"
# @param erreurlog Instance de la classe ErreurLog
# @param log Nom de la classe appelante a ajouter pour les log

class LectureXml:

	def __init__(self, nom, erreurLog,log):
		self.erreurLog = erreurLog
		self.log = log
		# lecture du fichier xml
		try :
			d = parse(nom+'.xml')
		except Exception as msg:
			if self.erreurLog:
				 self.erreurLog.erreur(self.log,"__init__","Erreur de lecture du fichier : "+nom+".xml ",-1,msg)
			else:
				sys.stderr.write(self.log+" __init__ Erreur de lecture du fichier : "+nom+".xml "+str(msg)+"\n")
				sys.exit(0)
		try :
			self.racine = d.childNodes[1]
		except Exception as msg:
			if self.erreurLog:
				self.erreurLog.erreur(self.log,"__init__","Erreur d'analyse du fichier : "+nom+".xml",-1,msg)
			else:
				sys.stderr.write(self.log+" __init__ Erreur d'analyse du fichier : "+nom+".xml "+str(msg)+"\n")
				sys.exit(0)

	##   
	# methode qui permet de charger une liste d'informations
	# stockes dans un fichier "collection" au format xml.
	# @param pere nom de la balise encadrant la liste
	# @param fils nom de la balise d'un element d'une liste
	# @return un tableau de string
	
	def chargerListe(self,pere,fils):
		resultat = []              
		try :
			balise_pere = self.racine.getElementsByTagName(pere)
		except Exception as msg:
			# le fichier specifie est mal forme
			if self.erreurLog:
				self.erreurLog.erreur(self.log,"chargerListe","Erreur dans la structure du fichier xml : "+pere,-1,msg)
		# pour tous les elements sous le pere
		for a in balise_pere:
			#on recupere un element
			try :
				tab_node = a.getElementsByTagName(fils)
				tableau = []
				for noeud in tab_node :
					tableau.append(noeud.childNodes[0].data.encode('utf8'))
				resultat = tableau
			except Exception as msg:
				# noeud vide donc retour d'un tableau vide
				if self.erreurLog:
					self.erreurLog.erreur(self.log,'chargerListe','PB lecture des '+fils,-1,msg)
		return resultat
	
		##
	# methode qui permet de lire la valeur d'une balise
	# stockee dans un fichier collection au format xml
	# @param noeud nom de la balise a lire
	# @return un string
	
	def chargerNoeud(self,noeud):
		try :
			n = self.racine.getElementsByTagName(noeud)
			if len(n[0].childNodes)>0:
				return n[0].childNodes[0].data.encode('utf8')
		except Exception as msg:
			# le fichier filtre specifie est mal forme
			if self.erreurLog:
				self.erreurLog.erreur(self.log,"chargerListe","Warning dans la structure du fichier xml au niveau du noeud : "+noeud,-1,msg)
		return ''


	##
	# methode permettant de lire la valeur d'une balise 
	# en fonction de la valeur de la balise et d'un attribut
	# @param pere nom de la balise encadrant la liste
	# @param fils nom de la balise d'un element d'une liste
	# @param attibut nom de l'attribut
	# @return un tableau de string
	def chargerListeAttribut(self,pere,fils,attribut):
		resultat = []
		try :
			balise_pere = self.racine.getElementsByTagName(pere)
		except Exception as msg:
			# le fichier specifie est mal forme
			if self.erreurLog:
				self.erreurLog.erreur(self.log,'chargerListeAttribut','Erreur dans la structure du fichier xml : '+pere,-1,msg)
		# pour tous les elements sous le pere
		for a in balise_pere:
			#on recupere un element
			try :
				tab_node = a.getElementsByTagName(fils)
				tableau = []
				for noeud in tab_node :
					if noeud.attributes['type'].value == attribut:
						tableau.append(noeud.childNodes[0].data.encode('utf8'))
				resultat = tableau
			except Exception as msg:
				# noeud vide donc retour d'un tableau vide
				if self.erreurLog:
					self.erreurLog.erreur(self.log,'chargerListeAttribut','PB lecture des '+fils,-1,msg)
		return resultat
		

	##
	# methode permettant de gerer le cas ou une chaine est vide
	# @param chaine une chaine de caracteres
	# @return -1 si la chaine est vide, un entier correspondant au transcodage de la chaine sinon
	def entier(self,chaine):
		if chaine == '':
			return -1
		else:
			return int(chaine.decode('utf8'))
