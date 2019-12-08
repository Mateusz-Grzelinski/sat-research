import math
import sys

from src.ast.exporters.tptp import TPTPExporter
from src.generators import IntegerRange
from src.generators.presets.first_order_logic import CNFFormulaGenerator

sys.setrecursionlimit(4000)

if __name__ == '__main__':
    gen = CNFFormulaGenerator(
        variable_names={f'V{i}' for i in range(10)},
        functor_names={f'f{i}' for i in range(20)}, functor_arity={i for i in range(10)}, functor_recursion_depth=0,
        predicate_names={f'p{i}' for i in range(20)}, predicate_arities={i for i in range(10)},
        atom_connectives={''},
        clause_lengths={i for i in range(7, 10)},
        number_of_clauses=IntegerRange(min=800, max=1000),
        number_of_literals=IntegerRange(min=1000, max=math.inf)
    ).generate()

    exporter = TPTPExporter(
        output_dir='./test-medium',
        filename_handle=lambda formula_info: ''
    )

    for i, formula in enumerate(gen):
        # print(i, formula)
        offset = 0
        exporter.export(expression=formula, filename_suffix=str(i + offset))
        if i + offset > 99:
            break
