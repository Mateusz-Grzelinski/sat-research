import math
import sys

from src.ast.exporters.tptp import TPTPExporter
from src.generators import IntegerRange
from src.generators.presets.first_order_logic import CNFFormulaGenerator

sys.setrecursionlimit(1500)

if __name__ == '__main__':
    gen = CNFFormulaGenerator(
        functor_names={'f1', 'f2', 'f3'}, functor_arity={0}, functor_recursion_depth=0,
        predicate_names={'p1', 'p2', 'p3'}, predicate_arities={0, 1},
        atom_connectives={''},
        clause_lengths={1, 2, 3, 4, 5, 6, 7, 8, 9},
        variable_names={'V1', 'V2'},
        number_of_clauses=IntegerRange(min=500, max=1000),
        number_of_literals=IntegerRange(min=100, max=math.inf)
    ).generate()

    exporter = TPTPExporter(
        output_dir='./test-big',
        filename_handle=lambda formula_info: ''
    )

    for i, formula in enumerate(gen):
        # print(i, formula)
        exporter.export(expression=formula, filename_suffix=str(i))
        if i >= 1:
            break
