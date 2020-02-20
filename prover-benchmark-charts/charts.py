import json

import matplotlib.pyplot as plt

from logic_formula_generator.data_model import ConjunctiveNormalFormPropositionalTemporalLogicFormulaInfo
from provers_benchmark.statistics.stats import Statistics

with open('../prover-benchmark-results/results-inkresat.json') as inkresat_results:
    x = json.load(inkresat_results)

stat = Statistics.from_dict(x)
stat: Statistics


def get_test_runs_for_input_name(input_name: str):
    for test_suite in stat.test_suites:
        for test_run in test_suite.test_run:
            if test_run.minimal_input_statistics.name != input_name:
                continue
            yield test_run


inkresat_cnf_liveness_safety_ratio = list(get_test_runs_for_input_name('set_1'))

for i in inkresat_cnf_liveness_safety_ratio:
    i.input_statistics = ConjunctiveNormalFormPropositionalTemporalLogicFormulaInfo.from_dict(i.input_statistics)

exec_time = [test_run.execution_statistics.execution_time for test_run in inkresat_cnf_liveness_safety_ratio]
peak_mem = [test_run.execution_statistics.peak_memory for test_run in inkresat_cnf_liveness_safety_ratio]
num_of_clauses = [test_run.input_statistics.number_of_clauses for test_run in inkresat_cnf_liveness_safety_ratio]
num_of_var = [test_run.input_statistics.number_of_variables for test_run in inkresat_cnf_liveness_safety_ratio]

plt.scatter(num_of_clauses, exec_time)
# plt.plot(exec_time)
plt.ylabel('execution time')
plt.xlabel('number of clauses')
plt.show()
