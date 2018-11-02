#!python
# -*- coding: utf-8 -*-
import argparse
import sys
import os.path

from src import seed_target_sbml,topo_crossroad,stoichio_crossroad,optimal_crossroad


class ConquestsPlugin:
   def input(self, filename):
      inputfile = open(filename, 'r')
      self.draft = inputfile.readline().strip()
      self.seed_cofactor = inputfile.readline().strip()
      self.biomass_id = inputfile.readline().strip()

   def run(self):
      pass   # Execution and output are merged

   def output(self, filename):
      repository = filename+"/"
      seed_target_sbml.seed_target_from_sbml(self.draft, self.biomass_id, repository)
      seed = repository+"seeds_from_sbml.sbml"
      target = repository+"targets_from_sbml.sbml"
      if self.seed_cofactor == "" :
         topo_crossroad.topological_crossroad(self.draft, seed, target, repository)
      else:
         topo_crossroad.topological_crossroad(self.draft, self.seed_cofactor, target, repository)
      stoichio_crossroad.stoichio_crossroad(self.draft, self.draft, seed, target, 1e-5, repository)
      optimal_crossroad.optimal_crossroad(self.draft, seed, target, 1e-5, repository)

