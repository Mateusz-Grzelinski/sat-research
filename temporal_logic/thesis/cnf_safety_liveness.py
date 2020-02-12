import concurrent
import logging
import os
from concurrent.futures.process import ProcessPoolExecutor

from src.generators import IntegerRange
from src.generators.presets.propositional_temporal_logic.cnf_propositional_temporal_logic_generator import \
    CNFPropositionalTemporalLogicGenerator

logging.basicConfig(level=logging.DEBUG)

futures = []


def job(system_property_gen: CNFPropositionalTemporalLogicGenerator, number_of_instances_in_set: int):
    for i, formula in enumerate(system_property_gen.generate()):
        if i >= number_of_instances_in_set:
            break
        path = os.path.join(
            '_test-inkresat-cnf-atom-clause-ratio',
            f'clauses{int(system_property_gen.number_of_clauses.average)}-variables{int(system_property_gen.number_of_variables_with_eventually_connectives.average + system_property_gen.number_of_variables_with_always_connectives.average)}',
            f'{i}'
        )
        formula.save_to_file(path=path)
        formula.save_info_to_file(
            path=path + '.fml',
            additional_statistics={'number_of_names_for_variables': len(system_property_gen.variable_names)}
        )
        logging.info(
            f'Generated formula with {system_property_gen.number_of_clauses} clauses: {i + 1}/{number_of_instances_in_set}: {path}')
        # future = pool_executor.submit(formula.save_to_file, path)
        # futures.append(future)
        # future = pool_executor.submit(formula.save_info_to_file, path,
        #                               additional_statistics={'number_of_names_for_variables': len(variable_names)})
        # future.add_done_callback(lambda _ft: logging.info(
        #     f'Generated formula with {number_of_clauses} clauses: {i + 1}/{number_of_instances_in_set}: {path}'))
        # futures.append(future)


if __name__ == '__main__':
    threshold = 0.05
    number_of_instances_in_set = 30
    number_of_clauses_list = [50, 60, 70, 80, 90, 100, 200, 400, 500, 600, 7000, 8000, 9000, 10000, 11_000, 12_000,
                              13_000, 14_000, 15_000, 16_000, 17_000, 18_000, 19_000, 20_000]
    number_of_variables_with_always_connectives = 100000
    number_of_variables_with_eventually_connectives = 100000
    number_of_variables_without_connective = 00
    clause_lengths = {i for i in range(5, 20)}
    negation_probability = 0.1
    variable_names = [f'V{i}' for i in range(1000)]

    pool_executor = ProcessPoolExecutor(max_workers=7)
    # start with biggest numbers - they will probably run longest
    for number_of_clauses in sorted(number_of_clauses_list, reverse=True):
        system_property_gen = CNFPropositionalTemporalLogicGenerator(
            variable_names=variable_names,
            number_of_variables_without_connective=IntegerRange.from_relative(number_of_variables_without_connective,
                                                                              threshold),
            number_of_variables_with_always_connectives=IntegerRange.from_relative(
                number_of_variables_with_always_connectives, threshold),
            number_of_variables_with_eventually_connectives=IntegerRange.from_relative(
                number_of_variables_with_eventually_connectives, threshold),
            number_of_clauses=IntegerRange.from_relative(number_of_clauses, threshold),
            clause_lengths=clause_lengths,
            negation_probability=negation_probability
        )

        future = pool_executor.submit(job, system_property_gen, number_of_instances_in_set)
        futures.append(future)
    concurrent.futures.wait(futures)
    print(exception for future in futures if (exception := future.exception()))
    logging.info('All done')
