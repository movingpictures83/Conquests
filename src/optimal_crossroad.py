import sys

from lxml import etree
import csv
from cobra.io import read_sbml_model, write_sbml_model
from cobra.io.sbml import create_cobra_model_from_sbml_file
from cobra import *


def optimal_crossroad(networkFile, file_seed, file_target, limit, repository) :
    
    model=create_cobra_model_from_sbml_file(networkFile)
    model.optimize()
    if (model.solution.f > limit) and file_seed != "":
        FVA_result = flux_analysis.variability.flux_variability_analysis(model, fraction_of_optimum=1.0)
        

        essential = {}
        cross_FVA = set()
        BDD_species = {}
        for id_reaction in FVA_result.keys() :
            inf = FVA_result[id_reaction]['minimum']
            sup = FVA_result[id_reaction]['maximum']
            if inf>limit and sup>limit :
                essential.update({id_reaction : "->"})
            elif inf<-limit and sup<-limit :
                essential.update({id_reaction : "<-"})
                
        parser = etree.XMLParser(remove_blank_text=True)
    #################################################################################### seed
        seed = etree.parse(file_seed, parser)
        root = "}".join(seed.getroot().tag.split("}")[:-1])+"}"
        seed_tree = seed.getroot().find(root+'model/'+root+'listOfSpecies')
        listOfSeed = []
        for element in seed_tree :
                listOfSeed.append(element.attrib['id'])
        #################################################################################### target
        target = etree.parse(file_target, parser)
        root = "}".join(target.getroot().tag.split("}")[:-1])+"}"
        target_tree = target.getroot().find(root+'model/'+root+'listOfSpecies')
        listOfTarget = []
        for element in target_tree :
                listOfTarget.append(element.attrib['id'])
    ####################################################################################
    
        draft = etree.parse(networkFile)
        sbml = draft.find('sbml')
        root = "}".join(draft.getroot().tag.split("}")[:-1])+"}"
        listOfSpecies = draft.find(root+'model/'+root+'listOfSpecies')
        for specie in listOfSpecies :
            BDD_species.update({specie.attrib["id"] : [specie.attrib["name"]]})
            try :
                BDD_species[specie.attrib["id"]].append(specie.attrib["compartment"])
            except KeyError :
                pass
            
        listOfReactions = draft.find(root+'model/'+root+'listOfReactions')
        for reaction in listOfReactions : 
            id_reac = reaction.attrib["id"]
            id_name_reac = "_".join(id_reac.split("_")[1:])
            try :
                name_reac = reaction.attrib["name"]
            except KeyError :
                name_reac = "_".join(id_reac.split("_")[1:])
                
            if id_reac in essential.keys() or name_reac in essential.keys() or id_name_reac in essential.keys():
                try :
                    direction = essential[id_reac]
                except KeyError :
                    try :
                        direction = essential[name_reac]
                    except KeyError :
                        direction = essential[id_name_reac]
                        
                listOfReactants = reaction.find(root+"listOfReactants")
                if direction == "->" :
                    try :
                        for specie in listOfReactants :
                            if specie.attrib["species"] not in listOfSeed and specie.attrib["species"] not in listOfTarget :
                                cross_FVA.add(specie.attrib["species"])
                    except :
                        pass
                elif direction == "<-" :
                    listOfProducts = reaction.find(root+"listOfProducts")
                    try :
                        for specie in listOfProducts :
                            if specie.attrib["species"] not in listOfSeed and specie.attrib["species"] not in listOfTarget :
                                cross_FVA.add(specie.attrib["species"])
                    except :
                        pass
        
        file = open(repository+"optimal_biomass_crossroads.sbml","wt")
        writer=csv.writer(file,delimiter="\t")
        if len(list(BDD_species)[0]) == 2 :
            writer.writerow(['identifiant','name','compartment'])
        else :
            writer.writerow(['identifiant','name'])
        for cross in cross_FVA :
            writer.writerow([cross]+BDD_species[cross])
        file.close()    
        
        
if __name__ == '__main__':   
    networkFile = sys.argv[1]
    file_seed = sys.argv[2]
    file_target = sys.argv[3]
    limit=float(sys.argv[4])
    try :
        repository = sys.argv[5]
    except IndexError :
        repository = "/".join(networkFile.split("/")[:-1])+"/OBC.csv"
        
    optimal_crossroad(networkFile, file_seed, file_target, limit, repository)
