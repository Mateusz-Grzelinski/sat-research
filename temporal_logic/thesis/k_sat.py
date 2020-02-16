"""In this file it is measured, how different clauses lengths combination affects solution speed """
import concurrent
import logging
import os
from concurrent.futures.process import ProcessPoolExecutor

from src.generators.presets.propositional_temporal_logic.cnf_propositional_temporal_logic_preset_no_solver import \
    CNFPropositionalTemporalLogicPresetNoSolver

logging.basicConfig(level=logging.DEBUG)


def job(system_property_gen: CNFPropositionalTemporalLogicPresetNoSolver, number_of_instances_in_set: int):
    for i in range(number_of_instances_in_set):
        formula = system_property_gen.generate()
        if i >= number_of_instances_in_set:
            break
        k_sat_name = "-".join(str(i) for i in sorted(system_property_gen.clause_lengths)) + '=' + "-".join(
            str(i) for i in sorted(system_property_gen.clause_lengths_weights))
        path = os.path.join(
            '_test-inkresat-cnf-k-sat',
            f'sat{k_sat_name}',
            f'{i}'
        )
        formula.save_to_file(path=path)
        formula.save_info_to_file(
            path=path + '.fml',
            additional_statistics={'number_of_names_for_variables': len(system_property_gen.variable_names)}
        )
        logging.info(
            f'Generated formula k-sat {system_property_gen.clause_lengths}, weights: {system_property_gen.clause_lengths_weights}: {i + 1}/{number_of_instances_in_set}: {path}')


if __name__ == '__main__':
    from _common_settings import *

    k_sat_sets = [
        ([1, 5, 10, 20], [25, 25, 25, 25]),
        ([1, 5, 10, 20], [1, 33, 33, 33]),
        ([1, 5, 10, 20], [33, 33, 33, 1]),
        ([1, 5, 10], [1, 1, 1]),
        ([5, 10, 20], [1, 1, 1]),
    ]

    futures = []
    pool_executor = ProcessPoolExecutor(max_workers=7)

    for clause_lengths, clause_lengths_weights in k_sat_sets:
        system_property_gen = CNFPropositionalTemporalLogicPresetNoSolver(
            variable_names=variable_names,
            variable_without_connective_probability=0,
            variable_with_always_connective_probability=0.5,
            variable_with_eventually_connective_probability=0.5,
            min_number_of_clauses=0,
            min_number_of_variables=200_000,
            clause_lengths=clause_lengths,
            clause_lengths_weights=clause_lengths_weights,
            variable_negation_probability=negation_probability
        )

        future = pool_executor.submit(job, system_property_gen, number_of_instances_in_set)
        futures.append(future)
    concurrent.futures.wait(futures)
    if any_errors := [exception for future in futures if (exception := future.exception())]:
        logging.error(any_errors)
    logging.info('All done')
