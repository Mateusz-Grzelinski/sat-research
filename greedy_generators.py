from pprint import pprint

from src.generators.first_order_logic.atom_generator import AtomGenerator
from src.generators.first_order_logic.conjunctive_normal_form.cnf_clause_generator import CNFClauseGenerator
from src.generators.first_order_logic.conjunctive_normal_form.cnf_formula_generator import CNFFormulaGenerator
from src.generators.first_order_logic.conjunctive_normal_form.literal_generator import LiteralGenerator
from src.generators.first_order_logic.functor_generator import FunctorGenerator
from src.generators.first_order_logic.predicate_generator import PredicateGenerator

f = FunctorGenerator([0], 0)
print('functors:')
pprint(list(f.generate()))

p = PredicateGenerator(arities=[1], functor_gen=f)
print('predicates:')
pprint(list(p.generate()))

a = AtomGenerator(allowed_connectives={''}, predicate_gen=p)
print('atoms:')
pprint(list(a.generate()))

l = LiteralGenerator(allow_positive=True, allow_negated=True, atom_gen=a)
print('literals:')
pprint(list(l.generate()))

c = CNFClauseGenerator(clause_lengths={1, 3}, literal_gen=l)
print('clauses:')
pprint(list(c.generate()))

F = CNFFormulaGenerator(clause_gen=c)
print('formulas:')
pprint(list(F.generate(1)))

# f1 = Functor('f', items=[Variable('V')])
# f2 = Functor('f', items=[Variable('X')])
# f = {f1, f2, }
# print(f)
