import logging
import logging
import os

from src.generators import IntegerRange
from src.generators.presets.propositional_temporal_logic.cnf_propositional_temporal_logic_generator import \
    CNFPropositionalTemporalLogicGenerator

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    threshold = 0.5
    number_of_instances_in_set = 2
    number_of_clauses_list = [50, 60, 70, 80, 90, 100, 200, 400, 500, 600, 700, 800, 900, 1000]
    number_of_variables_with_always_connectives = 100
    number_of_variables_with_eventually_connectives = 100
    number_of_variables_without_connective = 100
    clause_lengths = {i for i in range(5, 40)}
    negation_probability = 0.1
    variable_names = [f'V{i}' for i in range(50)]

    # pool_executor = ProcessPoolExecutor(max_workers=7)
    # futures = []
    for number_of_clauses in number_of_clauses_list:
        system_rpoperty_gen = CNFPropositionalTemporalLogicGenerator(
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

        for i, formula in enumerate(system_rpoperty_gen.generate()):
            path = os.path.join(
                '_test-inkresat-cnf-atom-clause-ratio',
                f'clauses{number_of_clauses}-variables{number_of_variables_with_eventually_connectives + number_of_variables_with_always_connectives}',
                f'{i}')
            formula.save_to_file(path=path)
            formula.save_info_to_file(path=path,
                                      additional_statistics={'number_of_names_for_variables': len(variable_names)})
            logging.info(
                f"Done generating formulas with {number_of_clauses} variables: {i}/{number_of_instances_in_set}")
            if i >= number_of_instances_in_set:
                break

            # future = pool_executor.submit(formula.save_to_file, path)
            # future = pool_executor.submit(formula.save_info_to_file, path,
            #                               additional_statistics={'number_of_names_for_variables': len(variable_names)})
            # future.add_done_callback(lambda _ft: logging.info(
            #     f"Done generating {number_of_instances_in_set} formulas with {number_of_clauses} variables"))
            # futures.append(future)
            # concurrent.futures.wait(futures)
    logging.info('All done')
