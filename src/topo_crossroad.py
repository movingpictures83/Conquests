# -*- coding: utf-8 -*-
from pyasp.asp import *
from optparse import OptionParser
from src import query, utils, sbml
import sys

def topological_crossroad(draft_sbml, seeds_sbml, targets_sbml, directory_name) :
    
    name_metabolites = {}
    
    draftnet = sbml.readSBMLnetwork(draft_sbml, 'draft') 
    seeds = sbml.readSBMLseeds(seeds_sbml)
    initial_targets = sbml.readSBMLtargets(targets_sbml)
    
    name_metabolites = sbml.readSBMLname(draft_sbml)
  
#####################################################################
    seed_name = []
    for s in seeds :
        seed_name.append(s.arg(0))
    targets = TermSet()
    for t in initial_targets :
        if t.arg(0) not in seed_name :
            targets.add(t)  
    productible_targets = query.get_producible(draftnet, seeds, targets)
    
#####################################################################
    answer= query.compute_crossroad(draftnet,seeds,productible_targets)
    crossroads = utils.split_proj_id(answer)
                
    if not os.path.isdir(directory_name):            
            os.makedirs(directory_name)
    
    if len(crossroads.keys())!=0 :
        utils.print_crossroad(crossroads,name_metabolites,directory_name+'topological_crossroads.csv')
        print(directory_name+'topological_crossroads.csv')
    else :
        print("no crossroad")

if __name__ == '__main__':
    usage = "usage: %prog [options] draftnetwork seedfile targetfile" 
    parser = OptionParser(usage)
    parser.add_option("-D","--directory",dest="directory",default= "",help="directory answer")
    (options, args) = parser.parse_args()
    
    if len(args) < 3:
        parser.error("incorrect number of arguments")

    draft_sbml = args[0]
    seeds_sbml = args[1]
    targets_sbml =  args[2]
    directory_name = options.directory
    
    if directory_name != "" and directory_name[-1]!="/" : directory_name += "/"
    elif "/" in draft_sbml : directory_name = draft_sbml.rsplit('/',1)[0]
            
    
    topological_crossroad(draft_sbml, seeds_sbml, targets_sbml, directory_name)    
