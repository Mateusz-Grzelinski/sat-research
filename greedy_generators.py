from pprint import pprint

import src.generators.signatures.first_order_logic as fof
from src.generators.range import Range

if __name__ == '__main__':
    f = fof.FunctorSignatureGenerator([0], 0)
    print('functors:')
    pprint(list(f.generate()))

    p = fof.PredicateSignatureGenerator(arities=[1], functor_gen=f)
    print('predicates:')
    pprint(list(p.generate()))

    a = fof.AtomSignatureGenerator(allowed_connectives={''}, predicate_gen=p)
    print('atoms:')
    pprint(list(a.generate()))

    l = fof.LiteralSignatureGenerator(allow_positive=True, allow_negated=True, atom_gen=a)
    print('literals:')
    pprint(list(l.generate()))

    c = fof.CNFClauseSignatureGenerator(clause_lengths={1, 3}, literal_gen=l)
    print('clauses:')
    pprint(list(c.generate()))

    F = fof.CNFFormulaSignatureGenerator(clause_gen=c)
    print('formulas:')
    gen = F.generate(
        number_of_clauses=Range(min=4, max=9),
        number_of_literals=Range(min=4, max=8),
    )
    pprint(f'{next(gen)=}')
    gen.send(True)
    pprint(f'{next(gen)=}')
    pprint(f'{next(gen)=}')

    # f1 = Functor('f', items=[Variable('V')])
    # f2 = Functor('f', items=[Variable('X')])
    # f = {f1, f2, }
    # print(f)
