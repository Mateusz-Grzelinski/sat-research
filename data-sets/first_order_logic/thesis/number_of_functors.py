import concurrent
import logging
import os
from concurrent.futures.process import ProcessPoolExecutor

from logic_formula_generator.generators.presets.first_order_logic import CNFSafetyLivenessPresetNoSolver

logging.basicConfig(level=logging.DEBUG)

OUT_PATH = '../../_generated'

ATOM_CLAUSE_RATIO_PATH = "_fol-tptp-cnf-number-of-functors"

literal_negation_chance = 0.5
number_of_formula_instances = 30

variable_names = [f'V{i}' for i in range(50)]
predicate_names = [f'p{i}' for i in range(50)]


def job(system_property_gen: CNFSafetyLivenessPresetNoSolver):
    for i in range(number_of_formula_instances):
        out_file_path = os.path.join(
            OUT_PATH, ATOM_CLAUSE_RATIO_PATH,
            f'functor_names{len(system_property_gen.functor_names)}', f'{i}'
        )
        logging.info(f'generating formula {i}/{number_of_formula_instances}: {out_file_path}')
        formula = system_property_gen.generate()
        formula.save_to_file(path=out_file_path, normal_form='cnf')
        formula.save_info_to_file(
            path=out_file_path + '.p',
            normal_form='cnf',
            additional_statistics={
                'number_of_variable_names': len(system_property_gen.variable_names),
                'number_of_predicate_names': len(system_property_gen.predicate_names),
                'number_of_functor_names': len(system_property_gen.functor_names)
            }
        )


if __name__ == '__main__':
    test_number_of_functors = [10, 25, 50, 100, 250, 500, 1000]
    number_of_clauses = 1000
    number_of_literals = 5000
    clause_lengths = [i for i in range(2, 10)]
    clause_weights = [1] * len(clause_lengths)

    predicate_arities = [i for i in range(5)]

    futures = []
    pool_executor = ProcessPoolExecutor(max_workers=7)
    for number_of_functors in test_number_of_functors:
        functor_names = [f'f{i}' for i in range(number_of_functors)]
        gen = CNFSafetyLivenessPresetNoSolver(
            variable_names=variable_names,
            functor_names=functor_names, functor_arity={0},
            functor_recursion_depth=0,
            predicate_names=predicate_names, predicate_arities=predicate_arities,
            atom_connectives={None},
            clause_lengths=clause_lengths,
            clause_lengths_weights=clause_weights,
            min_number_of_clauses=number_of_clauses,
            min_number_of_literals=number_of_literals,
            literal_negation_chance=literal_negation_chance,
        )
        future = pool_executor.submit(job, gen)
        futures.append(future)
    concurrent.futures.wait(futures)
    errors = [future.exception() for future in futures]
    if any(errors):
        logging.error([e for e in errors if e])
    logging.info('All done')
