import math

import src.ast.first_order_logic as fol
from src.ast.exporters.tptp import TPTPExporter
from src.generators import IntegerRange
from src.generators.presets.first_order_logic import CNFFormulaGenerator

if __name__ == '__main__':
    number_of_items = 5

    gen = CNFFormulaGenerator(
        functor_names={'f1'}, functor_arity={0}, functor_recursion_depth=0,
        predicate_names={'p1', 'p2'}, predicate_arities={0, 1},
        atom_connectives={''},
        clause_lengths={1, 2, 3},
        variable_names={'V1', 'V2'},
        number_of_clauses=IntegerRange(min=3, max=10),
        number_of_literals=IntegerRange(min=1, max=30)
    ).generate()

    exporter = TPTPExporter(
        output_dir='./temp-out',
        filename_handle=lambda formula_info: f'clauses_{formula_info.number_of_instances[fol.CNFClause]}_'
                                             f'atoms_{formula_info.number_of_instances[fol.Atom]}_'
                                             f'predicates_{formula_info.number_of_instances[fol.Predicate]}_'
                                             f'functors_{formula_info.number_of_instances[fol.Functor]}_'
                                             f'vars_{formula_info.number_of_instances[fol.Variable]}_'
    )

    for i in range(number_of_items):
        formula = next(gen)
        exporter.export(expression=formula, filename_suffix=str(i))
