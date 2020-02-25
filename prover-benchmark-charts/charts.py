import json
import os

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from logic_formula_generator.data_model import ConjunctiveNormalFormPropositionalTemporalLogicFormulaInfo
from provers_benchmark.statistics.stats import Statistics

with open('../prover-benchmark-results/results-inkresat1.json') as inkresat_results:
    x = json.load(inkresat_results)

stat = Statistics.from_dict(x)
stat: Statistics


def get_test_runs_for_input_name(input_name: str):
    for test_suite in stat.test_runs:
        for test_run in test_suite.test_run:
            if test_run.minimal_input_statistics.name != input_name:
                continue
            yield test_run


input_set_name = 'set_1'
inkresat_cnf_liveness_safety_ratio = list(get_test_runs_for_input_name(input_set_name))

for i in inkresat_cnf_liveness_safety_ratio:
    i.input_statistics = ConjunctiveNormalFormPropositionalTemporalLogicFormulaInfo.from_dict(i.input_statistics)

exec_time = [test_run.execution_statistics.execution_time for test_run in inkresat_cnf_liveness_safety_ratio]
peak_mem = [test_run.execution_statistics.peak_memory for test_run in inkresat_cnf_liveness_safety_ratio]
num_of_clauses = [test_run.input_statistics.number_of_clauses for test_run in inkresat_cnf_liveness_safety_ratio]
num_of_var = [test_run.input_statistics.number_of_variables for test_run in inkresat_cnf_liveness_safety_ratio]

fig = plt.figure()
fig: Figure
plt.title('Execution time of variable clause-variable ratio')
plt.scatter(num_of_clauses, exec_time, label='execution time')
# plt.plot(exec_time)
# ax = fig.gca()
# ax.yaxis.set_major_locator(MaxNLocator(integer=True))
plt.grid(True)
plt.ylabel('execution time [seconds]')
plt.xlabel('number of clauses')
fig.autofmt_xdate()

plt.xticks([i for i in range(0, max(num_of_clauses), 1000) if min(num_of_clauses) < i < max(num_of_clauses)],
           rotation=45)
# plt.xticks([7000, 8000, 9000, 10000, 11_000, 12_000,
#             13_000, 14_000, 15_000, 16_000, 17_000, 18_000, 19_000, 20_000],
#            rotation=45, ha='right'
#            )
plt.yticks(list({i for i in range(0, max(200, *exec_time), 25)}))
plt.legend()

prefix_path = os.path.join('_generated', input_set_name)
os.makedirs(prefix_path, exist_ok=True)
plt.savefig(os.path.join(prefix_path, 'numOfClausesVsExecTime.png'))
# plt.show()
