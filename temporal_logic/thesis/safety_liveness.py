import concurrent.futures.process
import logging
from concurrent.futures.process import ProcessPoolExecutor

from src.ast.exporters.inkresat.inkresat_exporter import InkresatExporter
from src.generators import IntegerRange
from src.generators.presets.propositional_temporal_logic.cnf_propositional_temporal_logic_generator import \
    CNFPropositionalTemporalLogicGenerator

logging.basicConfig(level=logging.DEBUG)


def job(exporter, generator, max_runs):
    i = 0
    for i, formula in enumerate(generator.generate()):
        exporter.export(formula, filename=str(i))
        if i == max_runs:
            return
    logging.error(f'not enough formulas, ended at {i}, expected {max_runs}')


if __name__ == '__main__':
    threshold = 0.05
    number_of_instances_in_set = 50
    number_of_clauses_list = [50, 60, 70, 80, 90, 100, 200, 400, 500, 600, 700, 800, 900, 1000]
    number_of_variables_with_always_connectives = 10000
    number_of_variables_with_eventually_connectives = 10000
    variable_names = [f'V{i}' for i in range(1000)]

    pool_executor = ProcessPoolExecutor(max_workers=7)
    futures = []
    for number_of_clauses in number_of_clauses_list:
        system_rpoperty_gen = CNFPropositionalTemporalLogicGenerator(
            variable_names=variable_names,
            number_of_variables_without_connective=IntegerRange(0, 0),
            number_of_variables_with_always_connectives=IntegerRange.from_relative(
                number_of_variables_with_always_connectives, threshold),
            number_of_variables_with_eventually_connectives=IntegerRange.from_relative(
                number_of_variables_with_eventually_connectives, threshold),
            number_of_clauses=IntegerRange.from_relative(number_of_clauses, threshold),
            clause_lengths={i for i in range(10, 40)},
            negation_probability=0.1)
        exporter = InkresatExporter(
            output_dir=f'test-inkresat-cnf-atom-clause-ratio/clauses{number_of_clauses}-variables{number_of_variables_with_eventually_connectives + number_of_variables_with_always_connectives}/',
            statistics_to_file=True,
            additional_statistics={'number_of_names_for_variables': len(variable_names)}
        )

        future = pool_executor.submit(job, exporter, system_rpoperty_gen, number_of_instances_in_set)
        future.add_done_callback(lambda _ft: logging.info(
            f"Done generating {number_of_instances_in_set} formulas with {number_of_clauses} variables"))
        futures.append(future)
    concurrent.futures.wait(futures)
    logging.info('All done')
