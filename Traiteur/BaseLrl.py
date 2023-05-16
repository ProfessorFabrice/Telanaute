#!/usr/bin/python
# -*- coding: utf-8

##
# projet Telanaute
# LLI 2004
# Classe BaseLrl
##

import sys
import re
import string

from Lrl import Lrl

try :
	import pgdb
except :
	try:
		import psycopg as pgdb
	except:
		print "Chargement module de connexion à postgres impossible => ARRET"
		sys.exit(1)

##
# cette classe est utilise pour l'interaction entre RobotBroute et la base
# @param collection Instance de la classe Collection
# @param option Instance de la classe Option
# @param erreurLog Instance de la classe ErreurLog

class BaseLrl :

	# constructeur
	def __init__(self,option,collectionTraiteur,erreurLog):
		self.erreurLog=erreurLog
		self.nomCollection= collectionTraiteur.getNomCollection()
		self.racine = option.getRacine()
		self.add_sep = re.compile("(...)(...)(...)")
		self.date=re.compile("(..)(..)-(..)-(..)")
		self.db = None
		try:
			self.db = pgdb.connect("dbname="+option.getNomBase()+" host="+option.getMachine()+" port="+str(option.getPort())+" user="+option.getUtilisateur()+" password="+option.getMdp())
			#self.db = pgdb.connect(database=option.getNomBase(),host=option.getMachine(),user=option.getUtilisateur(),password=option.getMdp())
		except Exception,msg:
			self.erreurLog.erreur(self.__class__.__name__,__name__,"pb connexion base",1,msg)            

	##
	# methode permettant de couper l'acces a la base
	def bdFin(self):
		self.db.close()
                
	##
	# methode permettant de convertir un enregistrement postgres vers un objet url
	# @param enr l'enregistrement issu de la base
	# @return une instance de l'objet url
	def __convertEnrToLrl(self,enr):
		idLrl="0"*(9-len(str(enr[1])))+str(enr[1])
		lrlName=self.racine+'/datatraite/'+string.strip(enr[2])+self.add_sep.sub("/\g<1>/\g<2>/\g<3>/",idLrl)+self.date.sub("\g<4>-\g<3>-\g<2>",enr[3].date)    
		return Lrl(enr[0],enr[1],lrlName,enr[2],enr[3].date,None,self.erreurLog)

        

	##
	# methode permettant de recuperer de la base un ensemble d'url a traiter
	# @param nbLrlATraiter nombre d'element a extraire de la base
	# @return tabLrl un tableau d'instance de la classe Lrl
	def getATraiter(self,nbLrlATraiter,tamponLrlATraiter) :
		# Creation de la requete SQL
		self.erreurLog.log(" SELECT * FROM "+self.nomCollection+" WHERE etat_collection=1 LIMIT "+str(nbLrlATraiter)+";")
		requeteSql = """ SELECT * FROM """+self.nomCollection+""" WHERE etat_collection=1 LIMIT """+str(nbLrlATraiter)+""" ; """
        
		# creation des cursors
		curs=self.db.cursor()
        
		# lancement de la requete
		try :
			curs.execute(requeteSql)
			self.db.commit()
		except Exception,msg:
			self.erreurLog.erreur(self.__class__.__name__,__name__,"erreur recuperation LrlATraiter",1,msg)
        
		# recuperation du resultat
		tab=[]
		for enr in curs.fetchall():
			tab.append(enr[0])
			tamponLrlATraiter.put(self.__convertEnrToLrl(enr),1)
        
		# liberation curseur
		curs.close()

		# maj dans la base
		self.setEtats(tab,2)
                
	##
	# methode permettant de mettre les etats a une certaine valeur
	# @param etatLrl la valeur a mettre pour etat_url
	# @param etatCollection la valeur a mettre pour etat_collection
	# @param tabIdLrl un tableau contenant les id_url
	def setEtats(self,tabLrl,etatCollection) :
		if len(tabLrl) > 0 :
			listeid =""
			idfin = tabLrl.pop()
			for idlrl in tabLrl:
				listeid = listeid + "id_base="+str(idlrl)+" OR "
			listeid = listeid + "id_base="+str(idfin)
			curs=self.db.cursor()
			try :
				curs.execute("UPDATE "+self.nomCollection+" SET etat_collection="+str(etatCollection)+" WHERE "+listeid)
			except Exception,msg:
				self.erreurLog.erreur(self.__class__.__name__,__name__,req,-1,"")
			self.db.commit()
			curs.close()
			
			#self.__executemany("UPDATE "+self.nomCollection+" SET etat_collection="+str(etatCollection)+" WHERE id_base=%d"+(" OR id_base=%d"*(len(tabLrl)-1)),[tabLrl])
    

	##
	# methode permettant de faire un executemany
	# @param req la requete SQL
	# @param tab la liste de liste pour l'excutemany
	def __executemany(self,req,tab) :
		if len(tab) > 0:
			curs=self.db.cursor()
			try :
				curs.executemany(req,tab)
			except Exception,msg:
				self.erreurLog.erreur(self.__class__.__name__,__name__,req,-1,msg)
			self.db.commit()
			curs.close()
        
	##
	# methode permettant de mettre a jour les lrl traites correctement
	# @param tab une liste contenant des id des lrl
	def putARangerOK(self,tab) :
		self.setEtats(tab,0)
        
	##
	# methode permettant de mettre a jour les url dont le traitement s'est termine par une erreuur
	# @param tab une liste contenant des id des lrl
	def putARangerE(self,tab) :
		self.setEtats(tab,3)

	##
	# methode permettant de mettre a jour les url dont le traitement est a faire (arret traitement)
	# @param tab une liste contenant des id des lrl
	def putAFaire(self,tab) :
		self.setEtats(tab,1)

