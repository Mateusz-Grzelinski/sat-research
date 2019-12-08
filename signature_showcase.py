from pprint import pprint

import src.generators._signatures.first_order_logic as fol
from src.ast.first_order_logic import Predicate, Functor, Variable

if __name__ == '__main__':
    v = fol.VariableNameGenerator(variable_names={'V'})
    f = fol.FunctorSignatureGenerator(variable_name_gen=v, functor_names={'f'}, arities=[0], max_recursion_depth=0)
    func_sig = list(f.generate())
    print(f'functors: {len(func_sig)}')
    pprint(func_sig)

    p = fol.PredicateSignatureGenerator(variable_name_gen=v, predicate_names={'p'}, arities=[0, 1], functor_gen=f)
    pred_sig = list(p.generate())
    print(f'predicates: {len(pred_sig)}')
    pprint(pred_sig)

    a = fol.AtomSignatureGenerator(variable_name_gen=v, connectives={''}, predicate_gen=p)
    atom_sig = list(a.generate())
    print(f'atoms: {len(atom_sig)}')
    pprint(atom_sig)

    l = fol.LiteralSignatureGenerator(atom_gen=a)
    lit_sig = list(l.generate())
    print(f'literals: {len(lit_sig)}')
    pprint(lit_sig)

    # c1 = fol.CNFClauseSignatureGenerator(clause_lengths={1}, literal_gen=l)
    # c2 = fol.CNFClauseSignatureGenerator(clause_lengths={2}, literal_gen=l)
    c3 = fol.CNFClauseSignatureGenerator(clause_lengths={3}, literal_gen=l)
    # c123 = fol.CNFClauseSignatureGenerator(clause_lengths={1, 2, 3}, literal_gen=l)
    clauses_sig = set(c3.generate())
    for clause in clauses_sig:
        for cont, i, item in clause.items(enum=True):
            if isinstance(item, Predicate):
                cont[i].name = 'p'
            elif isinstance(item, Functor):
                cont[i].name = 'f'
            elif isinstance(item, Variable):
                cont[i].name = 'V'

    print(f'clauses: {len(clauses_sig)}')
    pprint(clauses_sig)

    F = fol.CNFFormulaSignatureGenerator(clause_gens={
        c3: 3
    })

    print('formulas:')
    for f in enumerate(F.generate()):
        print(f)
        break
    # pprint(f'{next(gen)=}')
    # pprint(f'{next(gen)=}')
    # pprint(f'{next(gen)=}')

    # f1 = Functor('f', items=[Variable('V')])
    # f2 = Functor('f', items=[Variable('X')])
    # f = {f1, f2, }
    # print(f)
