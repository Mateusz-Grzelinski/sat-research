from pprint import pprint

import src.generators._signatures.first_order_logic as fol

if __name__ == '__main__':
    v = fol.VariableGenerator(variable_names={'V'})
    f = fol.FunctorGenerator(variable_gen=v, functor_names={'f'}, arities=[0], max_recursion_depth=0)
    func_sig = list(f.generate())
    print(f'functors: {len(func_sig)}')
    pprint(func_sig)

    p = fol.PredicateGenerator(variable_gen=v, predicate_names={'p', 'p2'}, arities=[0, 1], functor_gen=f)
    pred_sig = list(p.generate())
    print(f'predicates: {len(pred_sig)}')
    pprint(pred_sig)

    a = fol.AtomGenerator(variable_name_gen=v, connectives={''}, predicate_gen=p)
    atom_sig = list(a.generate())
    print(f'atoms: {len(atom_sig)}')
    pprint(atom_sig)

    l = fol.LiteralGenerator(negation_chance=0.1, atom_gen=a)
    lit_sig = list(l.generate())
    print(f'literals: {len(lit_sig)}')
    pprint(lit_sig)

    # c1 = fol.CNFClauseSignatureGenerator(clause_lengths={1}, literal_gen=l)
    # c2 = fol.CNFClauseSignatureGenerator(clause_lengths={2}, literal_gen=l)
    c3 = fol.CNFClauseGenerator(clause_lengths={3}, literal_gen=l)
    # c123 = fol.CNFClauseSignatureGenerator(clause_lengths={1, 2, 3}, literal_gen=l)
    clauses_sig = set(c3.generate())

    print(f'clauses: {len(clauses_sig)}')
    pprint(clauses_sig)

    F = fol.CNFFormulaGenerator(clause_gens={
        c3: 3
    })

    print('formulas:')
    print(F.generate())
    # pprint(f'{next(gen)=}')
    # pprint(f'{next(gen)=}')
    # pprint(f'{next(gen)=}')

    # f1 = Functor('f', items=[Variable('V')])
    # f2 = Functor('f', items=[Variable('X')])
    # f = {f1, f2, }
    # print(f)
