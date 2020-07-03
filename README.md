# Conquests
# Language: Python
# Input: TXT (list of files and target)
# Output: PREFIX (repository directory name)
# Tested with: PluMA 1.1, Python 3.6

PluMA plugin that applies the Conquests algorithm (Laniau et al, 2017)
to find Phenotypically Essential Metabolites (PEMs) within a metabolic network.

The input TXT file contains three lines:

(Name of SBML Metabolic Network File)
(Name of SBML Boundary Seed File)
(Name of Target) 

The output file is a prefix, which contains the name of a repository
into which several files will be deposited (if the directory does not exist
it will be created automatically):

optimal_biomass_crossroads.sbml
seeds_from_sbml.sbml
targets_from_sbml.sbml
stoichoimetrical_crossroads.csv
topological_crossroads.csv

The CSV files include Essential metabolites from the perspectives of
underlying chemical reaction properties, and network structure.

Note: This plugin acts as a wrapper around the original Conquests software
package, available at https://github.com/jlaniau/conquests and under
the GNU Public License (we have included a copy).  
All original source code that we used from this package is in data/
and src/, and has been unmodified from its original version.
