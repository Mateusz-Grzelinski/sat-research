import math
import sys

from src.generators import IntegerRange
from src.generators.presets.first_order_logic import CNFFormulaGenerator
from src.syntax_tree.exporters.tptp import TPTPExporter

sys.setrecursionlimit(4000)

if __name__ == '__main__':
    gen = CNFFormulaGenerator(
        variable_names={f'V{i}' for i in range(10)},
        functor_names={f'f{i}' for i in range(20)}, functor_arity={i for i in range(10)}, functor_recursion_depth=0,
        predicate_names={f'p{i}' for i in range(20)}, predicate_arities={i for i in range(10)},
        atom_connectives={''},
        clause_lengths={i for i in range(7, 10)},
        number_of_clauses=IntegerRange(min=800, max=1000),
        number_of_literals=IntegerRange(min=1000, max=math.inf),
        literal_negation_chance=0.1
    ).generate()

    exporter = TPTPExporter(output_dir='./test-medium', )

    for i, formula in enumerate(gen):
        print(i, formula)
        exporter.export(expression=formula, filename=str(i))
        if i > 9:
            break
