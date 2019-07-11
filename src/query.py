# -*- coding: utf-8 -*-
import os
import tempfile
from pyasp.asp import *

root = __file__.rsplit('/', 1)[0]

producible_prg =      root + '/encodings/producible_targets.lp'
project_cross   =       root + '/encodings/proj_cross.lp'

def get_producible(draft, seeds, targets):
    draft_f = draft.to_file()
    seed_f =  seeds.to_file()
    target_f = targets.to_file()
    prg = [producible_prg, draft_f, seed_f, target_f ]
    solver = Gringo4Clasp()
    models = solver.run(prg,collapseTerms=True,collapseAtoms=False)
    assert(len(models) == 1)
    os.unlink(draft_f)
    os.unlink(seed_f)
    os.unlink(target_f)
    return models[0]


def compute_crossroad(draft, seeds, targets):
    draft_f = draft.to_file()
    seed_f =  seeds.to_file()
    target_f = targets.to_file()
    prg = [project_cross, draft_f, seed_f, target_f]
    solver = Gringo4Clasp()
    models = solver.run(prg,collapseTerms=True, collapseAtoms=False)
    assert(len(models) == 1)
    os.unlink(draft_f)
    os.unlink(seed_f)
    os.unlink(target_f)
    return models[0] 
    
