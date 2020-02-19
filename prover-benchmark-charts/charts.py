# import matplotlib.pyplot as plt
import json
from typing import Dict, List

from logic_formula_generator.data_model import ConjunctiveNormalFormPropositionalTemporalLogicFormulaInfo

with open('../prover-benchmark-results/results-inkresat.json') as inkresat_results:
    x = json.load(inkresat_results)

cnf_ptl_infos: Dict[str, List[ConjunctiveNormalFormPropositionalTemporalLogicFormulaInfo]] = {}
# data is type of Statistics, but represented as dict
for test_suite in x['test_suites']:
    for test_run in test_suite['test_run']:
        test_input_name = test_run['minimal_input_statistics']['name']
        if not cnf_ptl_infos.get(test_input_name):
            cnf_ptl_infos[test_input_name] = []
        info = ConjunctiveNormalFormPropositionalTemporalLogicFormulaInfo()
        for key, value in x.items():
            if key == 'clause_sizes':
                setattr(info, int(key), value)
            else:
                setattr(info, key, value)
        cnf_ptl_infos[test_input_name].append(info)

print(cnf_ptl_infos)

# plt.plot([1, 2, 3, 4])
# plt.ylabel('some numbers')
# plt.show()
