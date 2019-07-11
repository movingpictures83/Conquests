# -*- coding: utf-8 -*-
from lxml import etree 
import sys
import os

def seed_target_from_sbml(draft,biomass_name,repository) :
        
        if not os.path.isdir(repository) :
            os.makedirs(repository)
    
        seeds = set()
        bio_reac = set()
        BDD_species = {}

        draft_parse = etree.parse(draft)
        sbml = draft_parse.find('sbml')
        root = "}".join(draft_parse.getroot().tag.split("}")[:-1])+"}"
        
        listOfSpecies = draft_parse.find(root+'model/'+root+'listOfSpecies')
        for specie in listOfSpecies :
                BDD_species.update({specie.attrib["id"] : specie})
                if specie.attrib["boundaryCondition"] == "true" :
                        seeds.add(specie)
                
                
        listOfReactions = draft_parse.find(root+'model/'+root+'listOfReactions')
        for reaction in listOfReactions : 
                try :
                        id_reac = reaction.attrib["id"]
                except KeyError :
                        id_reac = ""
                try :
                        id_name_reac = "_".join(id_reac.split("_")[1:])
                except KeyError :
                        id_name_reac = ""
                try :
                        name_reac = reaction.attrib["name"]
                except KeyError :
                        name_reac = ""
                if (biomass_name in id_reac) or (biomass_name in id_name_reac) or (biomass_name in name_reac) :
                        Reactants = reaction.find(root+'listOfReactants')
                        for specie in Reactants :
                                bio_reac.add(BDD_species[specie.attrib["species"]])
                                
        with open(draft,"r") as file :
                line0 = file.readlines()[0]
        ################################################################ seed

        seed_doc = draft_parse
        root = "}".join(seed_doc.getroot().tag.split("}")[:-1])+"}"
        model = seed_doc.find(root+'model')
        listR = model.find(root+"listOfReactions")
        model.remove(listR)
        
        listS = model.find(root+"listOfSpecies")
        listS.clear()
        for element in seeds :
                listS.append(element)
        outFile=open(repository+'/seeds_from_sbml.sbml','wb')
        outFile.write(line0.encode('utf-8'))
        seed_doc.write(outFile, pretty_print=True)

        ################################################################ target

        target_doc = draft_parse
        root = "}".join(target_doc.getroot().tag.split("}")[:-1])+"}"
        model = target_doc.find(root+'model')
        try :
                listR = model.find(root+"listOfReactions")
                model.remove(listR)
        except TypeError :
                pass
        listS = model.find(root+"listOfSpecies")
        listS.clear()
        for element in bio_reac :
                listS.append(element)
        outFile=open(repository+'/targets_from_sbml.sbml','wb')
        outFile.write(line0.encode('utf-8'))
        target_doc.write(outFile, pretty_print=True)
        
if __name__ == '__main__':        

        draft = sys.argv[1]
        biomass_name = sys.argv[2]
        try :
                repository = sys.argv[3]
        except IndexError :
                repository = "/".join(file_read.split("/")[:-1])        
        
        seed_target_from_sbml(draft,biomass_name,repository)
