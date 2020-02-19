""" In this file is is being measured, how atom-clause ratio affects solution speed """
import concurrent
import logging
import os
from concurrent.futures.process import ProcessPoolExecutor

from logic_formula_generator.generators import IntegerRange
from logic_formula_generator.generators.presets.propositional_temporal_logic.cnf_propositional_temporal_logic_preset import \
    CNFPropositionalTemporalLogicPreset

logging.basicConfig(level=logging.DEBUG)


def job(system_property_gen: CNFPropositionalTemporalLogicPreset, number_of_instances_in_set: int):
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


if __name__ == '__main__':
    from _common_settings import *

    number_of_clauses_list = [50, 60, 70, 80, 90, 100, 200, 400, 500, 600, 7000, 8000, 9000, 10000, 11_000, 12_000,
                              13_000, 14_000, 15_000, 16_000, 17_000, 18_000, 19_000, 20_000]

    futures = []
    pool_executor = ProcessPoolExecutor(max_workers=7)
    # start with biggest numbers - they will probably run longest
    for number_of_clauses in sorted(number_of_clauses_list, reverse=True):
        system_property_gen = CNFPropositionalTemporalLogicPreset(
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
    errors = [future.exception() for future in futures]
    if any(errors):
        logging.error(e for e in errors if e)
    logging.info('All done')
