# AxiomCreation explanation relationship
# Incomplete axiom creation (just checking the data)

import json

from formulas import get_formulas, get_data
from explanations import get_explanations, get_prev_explanations
from formulas import get_axioms

# load the log data
json_file = open("./Task1-brenna-log.json")
data = json.loads("".join(json_file.readlines()))
formulas = get_formulas(data)

for i in range(len(formulas)):
    t1 = formulas[i - 1]["timestamp"] if i > 1 else 0
    t2 = formulas[i]["timestamp"]
    data_1 = get_data(data, t1, t2)
    explanations = get_explanations(data_1)
    num = len(explanations)
    axioms = get_axioms(data_1)
    # get explanations prior to each axiom creation
    for j in range(len(axioms)):
        axiom_explanations = get_prev_explanations(axioms, j, explanations)


x = 1
