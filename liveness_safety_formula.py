from pprint import pprint

from src.ast.first_order_logic import CNFFormula
from src.generators._range import IntegerRange
from src.generators.presets.first_order_logic import CNFFormulaGenerator

if __name__ == '__main__':
    gen = CNFFormulaGenerator(
        functor_names={'f1'}, functor_arity={0}, functor_recursion_depth=0,
        predicate_names={'p1', 'p2'}, predicate_arities={0, 1},
        connectives={''},
        clause_lengths={1, 2, 3},
        variable_names={'V1', 'V2'},
        number_of_clauses=IntegerRange(min=3, max=10),
        number_of_literals=IntegerRange(min=1, max=30)
    )
    formula_gen = gen.generate()
    formula = next(formula_gen)
    formula = next(formula_gen)
    formula: CNFFormula
    # header = TPTPHeader()
    # header.read_from(formula)
    # print(header.get_header())
    print('stats: ')
    pprint(formula.get_info().__dict__)
    print('generated formula:')
    pprint(formula)
