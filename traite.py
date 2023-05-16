#!/usr/bin/python3

import sys
import time
from urllib.parse import urlparse
import re

from Commun.ErreurLog import ErreurLog
from Traiteur.TraiteLrl import *
from Traiteur.CollectionTraiteur import *

nomcollection = re.sub("\.xml$","",sys.argv[1])
add_sep = re.compile("(...)(...)(...)")
el = ErreurLog("traiteur.log")
el.setLogFichier()
collection = CollectionTraiteur(nomcollection,el)
tr = TraiteLrl(collection,el)
for elt in open("run/"+collection.getNomCollection()+".res"):
	[idstr,date] = elt.rstrip().split("\t")
	print(idstr,date)
	try:
		identificateur = int(idstr)
		rep='data/'+add_sep.sub("\g<1>/\g<2>/\g<3>/","0"*(9-len(idstr))+idstr)
		l = Lrl(0,identificateur,rep+date,'',date,0,el)
		tr.traite(l)
	except:
		raise
		print("Pb")
tr.close()
