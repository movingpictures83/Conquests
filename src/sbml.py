# -*- coding: utf-8 -*-
import re
from pyasp.asp import *
import xml.etree.ElementTree as etree  
from xml.etree.ElementTree import XML, fromstring, tostring

################################################################ Reading

def get_model(sbml) :
    model_element=None
    for e in sbml :
        if e.tag[0]=="{":
            uri,tag = e.tag[1:].split("}")
        else : tag = e.tag
        
        if tag=="model" :
            model_element=e
            break
    return model_element
    
def get_listOfSpecies(model):
    listOfSpecies = None
    for e in model:
        if e.tag[0] == "{":
          uri, tag = e.tag[1:].split("}")
        else: tag = e.tag
        if tag == "listOfSpecies":
          listOfSpecies = e
          break
    return listOfSpecies 
    
def get_listOfReactions(model):
    listOfReactions = None
    for e in model:
        if e.tag[0] == "{":
          uri, tag = e.tag[1:].split("}")
        else: tag = e.tag
        if tag == "listOfReactions":
          listOfReactions = e
          break
    return listOfReactions 
    
def get_listOfReactants(reaction):
    listOfReactants = None
    for e in reaction:
        if e.tag[0] == "{":
          uri, tag = e.tag[1:].split("}")
        else: tag = e.tag
        if tag == "listOfReactants":
          listOfReactants = e
          break
    return listOfReactants
    
def get_listOfProducts(reaction):
    listOfProducts = None
    for e in reaction:
        if e.tag[0] == "{":
          uri, tag = e.tag[1:].split("}")
        else: tag = e.tag
        if tag == "listOfProducts":
          listOfProducts = e
          break
    return listOfProducts
 
   
        
############################################################## network reading    
    
def readSBMLnetwork(filename, name) :
  
   lpfacts = TermSet()
   tree = etree.parse(filename)
   sbml = tree.getroot()
   model = get_model(sbml)
   
   lpfacts.add(Term('draft',["\""+name+"\""]))
   listOfReactions = get_listOfReactions(model)
   for e in listOfReactions:
     if e.tag[0] == "{":
       uri, tag = e.tag[1:].split("}")
     else: tag = e.tag
     if tag == "reaction":
       reactionId = e.attrib.get("id")
       lpfacts.add(Term('reaction', ["\""+reactionId+"\"", "\""+name+"\""]))
       if(e.attrib.get("reversible")=="true"):  lpfacts.add(Term('reversible', ["\""+reactionId+"\""]))
       
       listOfReactants = get_listOfReactants(e)
       if listOfReactants== None : print("\n Warning:",reactionId, "listOfReactants=None")
       else: 
          for r in listOfReactants:
            lpfacts.add(Term('reactant', ["\""+r.attrib.get("species")+"\"", "\""+reactionId+"\""]))
         
       listOfProducts = get_listOfProducts(e)
       if listOfProducts== None : print("\n Warning:",reactionId, "listOfProducts=None")
       else: 
          for p in listOfProducts:
            lpfacts.add(Term('product', ["\""+p.attrib.get("species")+"\"", "\""+reactionId+"\""]))

   return lpfacts
      
def readSBMLtargets(filename) :
 
   lpfacts = TermSet()
   
   tree = etree.parse(filename)
   sbml = tree.getroot()
   model = get_model(sbml)
   
   listOfSpecies = get_listOfSpecies(model)
   for e in listOfSpecies:
     if e.tag[0] == "{":
       uri, tag = e.tag[1:].split("}")
     else: tag = e.tag
     if tag == "species":
       lpfacts.add(Term('initial_target', ["\""+e.attrib.get("id")+"\""]))
   return lpfacts
   
   
def readSBMLseeds(filename) :
   lpfacts = TermSet()
   
   tree = etree.parse(filename)
   sbml = tree.getroot()
   model = get_model(sbml)
   
   listOfSpecies = get_listOfSpecies(model)
   for e in listOfSpecies:
     if e.tag[0] == "{":
       uri, tag = e.tag[1:].split("}")
     else: tag = e.tag
     if tag == "species":
       lpfacts.add(Term('seed', ["\""+e.attrib.get("id")+"\""]))
   return lpfacts


def readSBMLname(filename) :
    tree = etree.parse(filename)
    sbml = tree.getroot()
    model = get_model(sbml)
    
    dictionnary = {}    
    
    listOfSpecies = get_listOfSpecies(model)
    for e in listOfSpecies:
        if e.tag[0] == "{":
            uri,tag = e.tag[1:].split("}")
        else: tag = e.tag
             
        if tag == "species":
            if "metacyc" in e.attrib.get("name") :
                name = e.attrib.get("name").rsplit(":")[-1].replace("\"","")
            elif e.attrib.get("name")[-1] == "]" :
                name = e.attrib.get("name").rsplit("[")[0].replace("\"","")
            else :
                name = e.attrib.get("name").replace("\"","")
            if "compartment" in e.attrib :
                dictionnary[e.attrib.get("id")] = [name,e.attrib.get("compartment")]
            else :
                dictionnary[e.attrib.get("id")] = [name]   
    return dictionnary


