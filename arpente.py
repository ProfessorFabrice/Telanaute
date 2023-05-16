#!/usr/bin/python3

import sys
import time
from urllib.parse import urlparse
import random
import re
import os.path

from Commun.ErreurLog import ErreurLog
from Arpenteur.FiltreUrl import *
from Arpenteur.CollectionArpenteur import *

param = {}
for elt in sys.argv:
	if elt[0] == "-":
		param[elt[1:]] = True
	else:
		nomcollection = re.sub("\.xml$","",elt)
el = ErreurLog("arpenteur.log")
el.setLogFichier()
collectionArpente = CollectionArpenteur(nomcollection,el)
ficres = open("run/"+collectionArpente.getNomCollection()+".res","w")
mpps = collectionArpente.getMaxPagesParSite()
ar = FiltreUrl(collectionArpente,el)
tabUrl = []
tabUrlFait = {}
tabUrlKeys = {}
tabSite = {}
if os.path.isfile(".idfile") and not ("init" in param):
	id = int(open(".idfile").read())
else:
	id = 0
lastId = id
for elt in collectionArpente.getGraine():
	if elt[0:4] == 'file':
		for l in open(elt[7:]):
			tabUrl.append(Url(id,l.rstrip(),1,time.strftime("%d-%m-%y",time.localtime(time.time()))))
			tabUrlKeys[l.rstrip()] = 1
			id += 1
	else:
		tabUrl.append(Url(id,elt,1,time.strftime("%d-%m-%y",time.localtime(time.time()))))
		tabUrlKeys[elt] = 1
		id += 1
fin = False
nbpr = 0
while not fin:
	#time.sleep(random.randint(0,50)/100)
	url = tabUrl.pop(0)
	print(len(tabUrl),url.getUrl())
	tabUrlFait[url.getUrl()] = url
	try:
		codeRetour,res = ar.arpente(url,mpps)
		if codeRetour:
			ficres.write((str(url.getIdUrl())+"\t"+url.getDate())+"\n")
			nbpr += 1
			lastId = url.getIdUrl()
		for elt in res:
			site = urlparse(elt.getUrl()).netloc
			if not site in tabSite:
				tabSite[site] = 0	
			if elt.getUrl() not in tabUrlFait and elt.getUrl() not in tabUrlKeys:
				id += 1
				elt.putIdUrl(id)
				tabUrl.append(elt)
				tabUrlKeys[elt.getUrl()] = 1
				tabSite[site] +=1
	except:
		raise
		pass
	if mpps == ar.getNbPageSave() or len(tabUrl) == 0:
	#if len(tabUrl) == 0:
		fin = True
ficres.close()
open(".idfile","w").write(str(lastId+1))
