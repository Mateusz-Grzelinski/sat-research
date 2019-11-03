from pprint import pprint

from src.ast.exporters.tptp import TPTPHeader
from src.generators import IntegerRange
from src.generators.presets.first_order_logic import CNFFormulaGenerator

if __name__ == '__main__':
    gen = CNFFormulaGenerator(
        functor_names={f'f{i}' for i in range(10)}, functor_arity={0}, functor_recursion_depth=0,
        predicate_names={f'p{i}' for i in range(10)}, predicate_arities={0, 1},
        connectives={''},
        clause_lengths={1, 2, 3},
        variable_names={f'V{i}' for i in range(10)},
        number_of_clauses=IntegerRange(min=3, max=100),
        number_of_literals=IntegerRange(min=1, max=30)
    )
    formula_gen = gen.generate()
    formula = next(formula_gen)
    print('Currently supported statistics: ')
    pprint(formula.get_info().__dict__)

    print('Generated formula:')
    header = TPTPHeader()
    header.read_from(formula.get_info())
    print(header.get_header())
    pprint(formula)
