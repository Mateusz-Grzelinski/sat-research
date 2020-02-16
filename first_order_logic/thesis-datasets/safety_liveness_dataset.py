import logging

from src.generators import IntegerRange
from src.generators.presets.first_order_logic import CNFSafetyLivenessPreset

logging.basicConfig(level=logging.DEBUG)

# sys.setrecursionlimit(4000)

if __name__ == '__main__':
    number_of_formulas = 50

    test_number_of_clauses = [100, 200, 300, 400, 500]
    test_number_of_literals = [1000]
    threshold = 0.05

    variable_names = [f'V{i}' for i in range(10)]
    functor_names = [f'f{i}' for i in range(20)]
    predicate_names = [f'p{i}' for i in range(20)]

    for number_of_clauses in test_number_of_clauses:
        for number_of_literals in test_number_of_literals:
            gen = CNFSafetyLivenessPreset(
                variable_names=variable_names,
                functor_names=functor_names, functor_arity={0},
                functor_recursion_depth=0,
                predicate_names=predicate_names, predicate_arities={i for i in range(5)},
                atom_connectives={None},
                clause_lengths={i for i in range(2, 11)},
                number_of_clauses=IntegerRange.from_relative(number_of_clauses, threshold),
                number_of_literals=IntegerRange.from_relative(number_of_literals, threshold),
                literal_negation_chance=0.1,
            )

            for i in range(number_of_formulas):
                out_file_path = f'./test-cnf/clauses{number_of_clauses}-literals{number_of_literals}/{i}'
                logging.info(f'generating formula {i}/{number_of_formulas}: {out_file_path}')
                formula_gen = gen.generate()
                formula = next(formula_gen)
                # print(formula.get_as_tptp().getvalue())
                formula.save_to_file(path=out_file_path, normal_form='cnf')
                formula.save_info_to_file(
                    path=out_file_path + '.p',
                    normal_form='cnf',
                    additional_statistics={
                        'number_of_variable_names': len(variable_names),
                        'number_of_predicate_names': len(predicate_names),
                        'number_of_functor_names': len(functor_names)
                    }
                )
