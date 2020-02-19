"""In this file it is measured, how amount of temporal connectives affects solution speed """
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
            OUT_PATH, '_inkresat-cnf-liveness-safety-ratio',
            f'always{int(system_property_gen.number_of_variables_with_always_connectives.average)}-eventually{int(system_property_gen.number_of_variables_with_eventually_connectives.average)}',
            f'{i}'
        )
        formula.save_to_file(path=path)
        formula.save_info_to_file(
            path=path + '.fml',
            additional_statistics={'number_of_names_for_variables': len(system_property_gen.variable_names)}
        )
        logging.info(
            f'Generated formula always connective: {system_property_gen.number_of_variables_with_always_connectives}, eventually {system_property_gen.number_of_variables_with_eventually_connectives}: {i + 1}/{number_of_instances_in_set}: {path}')


if __name__ == '__main__':
    from _common_settings import *

    number_of_clauses = 20_000
    number_of_variables = 200_000
    liveness_safety_ratios = [i / 10 for i in range(0, 11, 1)]  # every 10%

    futures = []
    pool_executor = ProcessPoolExecutor(max_workers=7)

    for liveness_safety_ratio in liveness_safety_ratios:
        number_of_variables_with_always_connectives = int(number_of_variables * liveness_safety_ratio)
        number_of_variables_with_eventually_connectives = int(
            number_of_variables - number_of_variables_with_always_connectives)
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
