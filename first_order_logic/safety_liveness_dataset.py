import sys

from src.ast.exporters.tptp import TPTPExporter
from src.generators import IntegerRange
from src.generators.presets.first_order_logic import CNFSafetyLivenessGenerator

sys.setrecursionlimit(4000)

if __name__ == '__main__':
    number_of_formulas = 50
    number_of_variables = 10

    test_number_of_clauses = [100, 200, 300, 400, 500]
    test_number_of_literals = [1000]
    threshold = 0.05

    for number_of_clauses in test_number_of_clauses:
        for number_of_literals in test_number_of_literals:
            gen = CNFSafetyLivenessGenerator(
                variable_names={f'V{i}' for i in range(number_of_variables)},
                functor_names={f'f{i}' for i in range(20)}, functor_arity={0},
                functor_recursion_depth=0,
                predicate_names={f'p{i}' for i in range(20)}, predicate_arities={i for i in range(5)},
                atom_connectives={''},
                clause_lengths={i for i in range(2, 11)},
                number_of_clauses=IntegerRange.from_relative(number_of_clauses, threshold),
                number_of_literals=IntegerRange.from_relative(number_of_literals, threshold),
                literal_negation_chance=0.1,
            )

            exporter = TPTPExporter(
                output_dir=f'./test-cnf/clauses{number_of_clauses}-literals{number_of_literals}',
                filename_handle=lambda formula_info: ''
            )

            for i in range(number_of_formulas):
                # print(i, formula)
                formula = gen.generate()
                exporter.export(expression=next(formula), filename_suffix=str(i))
