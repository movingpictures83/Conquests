# -*- coding: utf-8 -*-
#!/usr/bin/python2
from lxml import etree 
import sys
import os

from cobra.io import read_sbml_model, write_sbml_model
from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra import *

def without_metabo(file_draft,metabo,outFile) :

	parser = etree.XMLParser(remove_blank_text=True)
	
	with open(file_draft,"r") as file :
		line0 = file.readlines()[0]	

	draft = etree.parse(file_draft,parser)
	root = "}".join(draft.getroot().tag.split("}")[:-1])+"}"

	listR = draft.getroot().find(root+'model/'+root+"listOfReactions")
	for reaction in listR :
		remove_reac = False
		reversible = reaction.attrib["reversible"]
		listOfReactant = reaction.find(root+"listOfReactants")
		try :
			for specie in listOfReactant :
				if specie.attrib['species'] == metabo :
					listR.remove(reaction)
					remove_reac = True
					break
		except :
			pass
		if remove_reac==False and reversible == "true" :
			listOfProduct = reaction.find(root+"listOfProducts")
			try :
				for specie in listOfProduct :
					if specie.attrib['species'] == metabo :
						listR.remove(reaction)
						break
			except :
				pass
						

	new_file = "/".join(file_draft.split("/")[:-1])+"/"+outFile
	with open(new_file,"wb") as file :
		file.write(line0.encode('utf-8'))
		draft.write(file, pretty_print=True)
		
	return new_file
	 


if __name__ == '__main__':
	file_draft = sys.argv[1]
	metabo = sys.argv[2]
	try :
			outFile = sys.argv[3]		
	except IndexError :
			outFile = "new_draft.sbml"
			
	new_file = without_metabo(file_draft,metabo,outFile)
	print(new_file)
