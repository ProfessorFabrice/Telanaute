#!/usr/bin/python3

import urllib.request, urllib.error, urllib.parse
from urllib.parse   import quote
import time
import string
import os
import re
import sys
import random

# import local
from .ErreurLog import ErreurLog
from .Url import Url
from .CollectionArpenteur import CollectionArpenteur
from .AnalyseDocument import AnalyseDocument
from .OutilsFiltre import OutilsFiltre
from .Option import Option

##
# Cette classe effectue les differents traitements lies a une url, c'est-a-dire :
# <ul>
# <li>telechargement de la page correspondante</li>
# <li>recherche des liens dans la page</li>
# <li>application des filtres</li>
# <li>sauvegarde de la page dans le systeme de fichier local</li>
# </ul>

class FiltreUrl:
	# constructeur
	def __init__(self,configCollection,erreurLog):
		self.erreurLog = erreurLog
		self.outilsFiltre = OutilsFiltre(configCollection,erreurLog)
		self.racine = "."
		self.nomCollection = configCollection.getNomCollection()
		# pour la creation du fichier
		self.add_sep = re.compile("(...)(...)(...)")
		self.nbPagesSave = 0
		try:
			self.useragent = [x.rstrip() for x in open("useragent.txt")]
		except:
			self.useragent = []
			hk = "dans la vieille mare une grenouille saute le bruit de l'eau".split()
			for i in range(0,50):
				random.shuffle(hk)
				self.useragent.append(" ".join(hk)) 
		
		
		
	##
	# methode permettant le traitement d'une url
	# cette methode est appelé par la calsse <a href="pythondoc-RobotPere.html">RobotPere</a>
	# @param urlObject url a traiter (objet <a href="pythondoc-Url.html">Url</a>)
	# @param nbPageSite dictionnaire du nombre de page par sites site:[nb,nb max,id base site,nb orig]
	# @return un tableau d'<a href="pythondoc-Url.html">Url</a> ou le premier element est 
	# l'url donnee en parametre associe le cas echeant a un code d'erreur si le telechargement 
	# a echoue
	def arpente(self,urlObjet,nbPageSite):
		codeRetour = True
		urlBase = urlObjet.getUrl()
		nbTry = urlObjet.getNbTry()
		idUrl = urlObjet.getIdUrl()
		listeUrlNormalise = []
		dateCourante = time.strftime("%d-%m-%y",time.localtime(time.time()))
		try:
			document,contentType = self.recupPage(urlBase)
			document = re.sub("<script(\n|.)*?</script>","",document,flags=re.I)
			documentAnalyse = self.analyseDocument(document,contentType)
			if documentAnalyse != None:
				listeUrl = list(documentAnalyse.getAncre().keys())
				documentTexte = documentAnalyse.getTexte()
				if self.outilsFiltre.testSource(document):
					self.ecritureSource(idUrl,document,dateCourante)
					self.ecritureMeta(idUrl,urlBase,listeUrl,dateCourante,contentType)
					self.ecritureTexte(idUrl,documentTexte,dateCourante)
					self.nbPagesSave += 1
					listeUrlNormalise.append(Url(idUrl,urlBase,0,dateCourante,0,0,None,self.erreurLog))
					for url in listeUrl:
						urlNormalise,site = self.outilsFiltre.normaliseUrl(urlBase,url)
						self.erreurLog.log("test url "+urlNormalise);
						valeur = self.outilsFiltre.testUrl(urlNormalise)
						if valeur:
							listeUrlNormalise.append(Url(-1,urlNormalise,0,dateCourante,None,None,None,self.erreurLog))
							self.erreurLog.log("Acceptation url : "+urlNormalise)
						else:
							self.erreurLog.log("Rejet url : "+urlNormalise)
				else:
					listeUrlNormalise.append(Url(idUrl,urlBase,0,dateCourante,0,-1,None,self.erreurLog))
					self.erreurLog.log("Rejet url testSource "+urlBase)
					codeRetour = False
		except ErreurUrl as xxx_todo_changeme1:
			(msg) = xxx_todo_changeme1
			codeRetour = False
			listeUrlNormalise.append(Url(idUrl,urlBase,nbTry + 1,dateCourante,msg.getErr(),None,None,self.erreurLog))
		return codeRetour,listeUrlNormalise
		
	##
	# Methode permettant de recuperer une page a partir de son url.	
	# @param url url de la page a recuperer
	# @return un string contenant tout le document (ou une erreur explicitement note de la forme "Erreur<num>")
	def recupPage(self,url):
		pageUrl = ''
		# ouverture url
		try:
			ua = random.choice(self.useragent)
			requestHeaders = {'User-Agent': ua}
			url = 'http://'+quote(re.sub('^http://','',url))
			request = urllib.request.Request(url,None, requestHeaders)
			ptrPage = urllib.request.urlopen(request,None,10)
		#except Commun.timeoutsocket.Timeout as xxx_todo_changeme2:
		#	(msg) = xxx_todo_changeme2
		#	self.erreurLog.erreur('FiltreUrl','recupPage',"PB d acces a l'url <"+url+">",-1,msg)
		#	raise ErreurUrl(2)
		except urllib.error.URLError as xxx_todo_changeme3:
			(msg) = xxx_todo_changeme3
			self.erreurLog.erreur('FiltreUrl','recupPage',"PB d acces a l'url <"+url+">",-1,msg)
			if re.search('HTTP Error 404',str(msg)): # erreur 404
				raise ErreurUrl(404)
			elif re.search('HTTP Error 403',str(msg)): # erreur 403
				raise ErreurUrl(403)
			else:
				raise ErreurUrl(400)
		except Exception as xxx_todo_changeme4:
			(msg) = xxx_todo_changeme4
			self.erreurLog.erreur('FiltreUrl','recupPage',"PB d acces a l'url <"+url+">",-1,msg)
			raise ErreurUrl(1)
		# test infos (greffon)
		contentType = ''
		if 'Content-Type' in ptrPage.info():
			contentType = ptrPage.info()['Content-Type']
		if self.outilsFiltre.testInformations(ptrPage.info()):
			# recuperation du document
			pageUrl = ptrPage.read()#.decode('utf-8', 'replace')
			try:
				pageUrl = pageUrl.decode('utf8')
			except UnicodeDecodeError:
				pageUrl = pageUrl.decode('latin1', 'replace')
			ptrPage.close()
		else:
			raise ErreurUrl(900) # document rejete par le greffon
		ptrPage.close()
		return pageUrl,contentType
		
		
	##
	# Analyse d'une page HTML pour en extraire les liens.
	# Cette analyse fait aussi une verification du contenu textuel
	# par rapport a (<tt>filtreSource</tt>),
	# attribut de la classe <a href="pythondoc-Collection.html">Collection</a>
	# @param document le source du document
	# @param type du document a analyser
	# @return un pointeur sur un objet de type <a href="pythondoc-AnalyseDocument.html">AnalyseDocument</a>
	def analyseDocument(self,source,typeDocument):
		# etrange mais force le reset
		document = None
		try:
			document=AnalyseDocument(source,typeDocument,self.erreurLog)
		except Exception as msg:
			raise
			self.erreurLog.erreur('FiltreUrl','recupPage',"PB avec l'analyse HTML de la page",-1,msg)
			exit
		return document
		
	##
	# Creation dans le systeme de fichier d'un fichier 
	# contenant la source du document
	# @param identificateur identificateur associe a l'url
	# @param source source a sauvegarder
	def ecritureSource(self,identificateur,source,dateCourante):
		# completion avec des zeros devant
		fichier="0"*(9-len(str(identificateur)))+str(identificateur)
		# ajout / par groupe de 3
		rep=self.add_sep.sub("\g<1>/\g<2>/\g<3>/",fichier)
		# creation du repertoire
		try:
			os.makedirs(self.racine+'/data/'+rep)
		except: # si il existe deja on ne fait rien
			pass
		try:
			ficres = open (self.racine+'/data/'+rep+'/'+dateCourante+'_source','w')
			ficres.write(source)
			ficres.close()
		except:
			self.erreurLog.erreur('FiltreUrl','ecritureSource id='+identificateur,"PB d'ecriture",-1,'')
		
	##
	# Creation dans le systeme de fichier d'un fichier 
	# contenant la version texte du source du document
	# @param identificateur identificateur associe a l'url
	# @param source source a sauvegarder
	def ecritureTexte(self,identificateur,texte,dateCourante):
		# completion avec des zeros devant
		fichier="0"*(9-len(str(identificateur)))+str(identificateur)
		# ajout / par groupe de 3
		rep=self.add_sep.sub("\g<1>/\g<2>/\g<3>/",fichier)
        	# creation du repertoire
		try:
			os.makedirs(self.racine+'/data/'+rep)
		except: # si il existe deja on ne fait rien
			pass
		try:
			ficres = open (self.racine+'/data/'+rep+'/'+dateCourante+'_source.texte','w')
			ficres.write(texte)
			ficres.close()
		except:
			erreurLog.erreur('FiltreUrl','ecritureTexte id='+identificateur,"PB d'ecriture",-1,'')

	##
	# Creation dans le systeme de fichier d'un fichier 
	# contenant des meta-informations sur le document
	# @param identificateur identificateur associe a l'url
	# @param source source a sauvegarder
	def ecritureMeta(self,identificateur,url,liens,dateCourante,typeFichier):
	       	# completion avec des zeros devant
		fichier="0"*(9-len(str(identificateur)))+str(identificateur)
        	# ajout / par groupe de 3
		rep=self.add_sep.sub("\g<1>/\g<2>/\g<3>/",fichier)
        	# creation du repertoire
		try:
			os.makedirs(self.racine+'/data/'+rep)
		except: # si il existe deja on ne fait rien
			pass
		try:
			ficmeta = open (self.racine+'/data/'+rep+'/'+dateCourante+'_meta.xml','w')
			ficmeta.write('<meta>\n\t<url>'+url+'</url>\n')
			ficmeta.write('<type>'+typeFichier+'</type>\n')
			#ficmeta.write('<contenttype>'++'</contenttype>')
			if len(liens)>0:
				ficmeta.write('\t<liens>\n')
				for lien in liens:
					ficmeta.write('\t\t<lien>'+lien+'</lien>\n')
				ficmeta.write('\t</liens>\n')
			ficmeta.write('</meta>')
			ficmeta.close()
		except:
			erreurLog.erreur('FiltreUrl','ecritureMeta id='+identificateur,"PB d'ecriture",-1,'')
			
	# récupération du nombre de pages déjà sauvegardées
	def getNbPageSave(self):
		return self.nbPagesSave
		

##
# classe permettant de gerer les erreurs de telechargement
# On trouve les valeurs de code suivants :
# <ul>
# <li> <tt>1</tt> : erreur generique</li>
# <li> <tt>400</tt> : pb telechargement</li>
# <li> <tt>404</tt> : page absente du site</li>
# <li> <tt>403</tt> : acces interdit</li>
# <li> <tt>900</tt> : document rejete par greffon</li>
# <li> <tt>2</tt> : timeout</li>
class ErreurUrl(Exception):
    def __init__(self,code):
        self.code = code
    
    def getErr(self):
        return self.code
