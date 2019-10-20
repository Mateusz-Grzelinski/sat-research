from pprint import pprint

from src.generators.presets.liveness_safety_generator import LivenessSafetyGenerator
from src.generators.range import Range

if __name__ == '__main__':
    from src.exporters.tptp.tptp_header import TPTPHeader

    gen = LivenessSafetyGenerator(
        functor_names={'f1'}, functor_arity={0},
        predicate_names={'p1', 'p2'}, predicate_arities={0, 1},
        connectives={''},
        clause_lengths={1, 2, 3},
        variable_names={'V1', 'V2'},
        number_of_clauses=Range(min=5, max=10),
        number_of_literals=Range(min=10, max=30)
    )
    formula_gen = gen.generate()
    formula = next(formula_gen)
    formula = next(formula_gen)
    formula = next(formula_gen)
    formula = next(formula_gen)
    formula = next(formula_gen)
    formula = next(formula_gen)
    formula = next(formula_gen)
    formula = next(formula_gen)
    formula = next(formula_gen)
    formula = next(formula_gen)
    formula = next(formula_gen)
    formula = next(formula_gen)
    header = TPTPHeader()
    header.read_from(formula)
    print('generated formula:')
    print(header.get_header())
    pprint(formula)
