# -*- coding: utf-8 -*-
import os
import csv
  
def clean_up() :
    if os.path.isfile("parser.out"): os.remove("parser.out")
    if os.path.isfile("parsetab.py"): os.remove("parsetab.py")
    if os.path.isfile("asp_py_lextab.py"): os.remove("asp_py_lextab.py")
    if os.path.isfile("asp_py_lextab.pyc"): os.remove("asp_py_lextab.pyc")
    if os.path.isfile("asp_py_parsetab.py"): os.remove("asp_py_parsetab.py")
    if os.path.isfile("asp_py_parsetab.pyc"): os.remove("asp_py_parsetab.pyc")
  
    
def split_proj_id(answer) :
    'renvoie un dico avec [id : {[number,[target]]}]'
    crossroads = {}
    for element in answer :
        if element.pred() == "crossroad" : 
            id_cross = element.arg(0).replace("\"","")
            if id_cross not in crossroads.keys() :
                crossroads.update({id_cross : [0]})
                
        elif element.pred() == "subtarget" : 
            id_target = element.arg(0).replace("\"","")
            id_cross = element.arg(1)  .replace("\"","")
            if id_cross in crossroads.keys() :
                crossroads[id_cross][0] += 1
                crossroads[id_cross].append(id_target)
            else :
                crossroads.update({id_cross : [1,id_target]})
                
    return crossroads

def print_crossroad(answer, dico, file_name, option_ecriture="wt",titre="") :
        
    file = open(file_name,option_ecriture)
    writer = csv.writer(file,delimiter="\t")
    if titre != "" :
        writer.writerow([titre+" :"])
    if len(list(dico)[0]) == 2 :
        writer.writerow(['identifiant','name','compartment','number of targets','targets'])
    else :
        writer.writerow(['identifiant','name','number of targets','targets'])
        
    for element in answer.keys() :
        try :
            writer.writerow([element.replace("\"","")]+dico[element.replace("\"","")]+answer[element.replace("\"","")]) 
        except KeyError :
            writer.writerow([element.replace("\"","")]+[element.replace("\"","")]) 

    file.close()
