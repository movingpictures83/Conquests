# -*- coding: utf-8 -*-
#!/usr/bin/python2
from lxml import etree
import sys
import os
import csv

from cobra.io import read_sbml_model, write_sbml_model
from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra import *

from src import draft_without_metabolite

def stoichio_crossroad(file_draft, file_metabo, file_seed, file_target, limit, repository, file_delete='y') :
	
	parser = etree.XMLParser(remove_blank_text=True)
	#################################################################### seed
	seed = etree.parse(file_seed, parser)
	root = "}".join(seed.getroot().tag.split("}")[:-1])+"}"
	seed_tree = seed.getroot().find(root+'model/'+root+'listOfSpecies')
	listOfSeed = []
	for element in seed_tree :
			listOfSeed.append(element.attrib['id'])
	listOfSeed.sort()
			
	#################################################################### target
	target = etree.parse(file_target, parser)
	root = "}".join(target.getroot().tag.split("}")[:-1])+"}"
	target_tree = target.getroot().find(root+'model/'+root+'listOfSpecies')
	listOfTarget = []
	for element in target_tree :
			listOfTarget.append(element.attrib['id'])
	listOfTarget.sort()
	
	#################################################################### metabolite
	name_metabolite = {}
	metabo_sbml = etree.parse(file_metabo,parser)
	root = "}".join(metabo_sbml.getroot().tag.split("}")[:-1])+"}"
	listS = metabo_sbml.getroot().find(root+'model/'+root+'listOfSpecies')
	test = set()
	for specie in listS :
		id_specie = specie.attrib["id"]
		if id_specie not in listOfSeed and id_specie not in listOfTarget :
			test.add(specie.attrib["id"])
			try :
				name_metabolite.update({id_specie : [specie.attrib["name"]]})
			except KeyError :
				name_metabolite.update({id_specie : [id_specie]})
			try :
				name_metabolite[id_specie].append(specie.attrib["compartment"])
			except KeyError :
				pass
	######################################################################## 
	with open(file_draft,"r") as file :
		line0 = file.readlines()[0]
	
	file=open(repository+"stoichiometrical_crossroads.csv","w")	
	writer = csv.writer(file,delimiter="\t")
	if len(list(name_metabolite)[0]) == 2 :
		writer.writerow(['identifiant','name','compartment'])
	else :
		writer.writerow(['identifiant','name'])	
	file.close()    
        
	for removed_metabo in test :
		outFile = draft_without_metabolite.without_metabo(file_draft,removed_metabo,"new_draft.sbml")
				
		model=create_cobra_model_from_sbml_file(outFile)
		model.optimize()
		growth = model.solution.f
		
		try :
			if abs(growth) <= limit :
				file=open(repository+"stoichiometrical_crossroads.csv","a")
				writer = csv.writer(file,delimiter="\t")
				writer.writerow([removed_metabo]+name_metabolite[removed_metabo])
				file.close()
		except TypeError :
			print(removed_metabo,"\t",growth)
			
		if file_delete=="y" :
			os.remove(outFile)	
			

if __name__ == '__main__':
	file_draft = sys.argv[1]
	file_metabo =sys.argv[2]
	file_seed = sys.argv[3]
	file_target = sys.argv[4]
	limit = float(sys.argv[5])
	try :
			repository = sys.argv[6]
	except IndexError :
			repository = "/".join(file_metabo.split("/")[:-1])+"/SC"+str(limit)+".txt"
	
	file_delete=raw_input("Delete new_draft (y/n) ?")
	
	stoichio_crossroad(file_draft, file_metabo, file_seed, file_target, limit, repository, file_delete)
