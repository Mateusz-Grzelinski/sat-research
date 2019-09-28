from src.exporters.tptp_exporter import TPTPHeader
from src.generators.factories import FunctorFactory, PredicateFactory, AtomFactory, LiteralFactory, CNFClauseFactory
from src.generators.randomcnfgenerator import RandomCNFGenerator


def dataset1():
    functors = FunctorFactory.generate_functors(names=['f'], arities=[0, 1], max_recursion_depth=1)
    predicates = PredicateFactory.generate_predicates(names=['p'], arities=[1, 2])
    atoms = AtomFactory.generate_atoms({''})
    literals = LiteralFactory.generate_literals()
    clauses = CNFClauseFactory.generate_clauses(lengths=[1, 2, 3, 4])

    g = RandomCNFGenerator(
        functors=functors,
        predicates=predicates,
        atoms=atoms,
        literals=literals,
        clauses=clauses,
    )

    from pprint import pprint
    print('Elements in generator: ')
    pprint(g.ast_elements)

    formula = g.random_cnf_formula(number_of_clauses=4)
    g.recursive_generate(formula)
    # tr = ThresholdRegulator(
    #     number_of_clauses=ThresholdRegulator.range(10, threshold=0.5, delta=5),
    #     number_of_literals=ThresholdRegulator.range(10, threshold=0, delta=2),
    #     number_of_atoms=ThresholdRegulator.range(10, threshold=0.5, delta=5),
    #     number_of_predicates=ThresholdRegulator.range(10, threshold=0.5, delta=5),
    #     number_of_functors=ThresholdRegulator.range(10, threshold=0.5, delta=5),
    #     number_of_variables=ThresholdRegulator.range(10, threshold=0.5, delta=5)
    # )
    # tr.tune_cnf_formula(generator=g, initial_cnf_formula=formula)
    t = TPTPHeader()
    t.read_from(formula)
    print(t.get_header())
    print(formula)


def hash_test():
    clauses = CNFClauseFactory.generate_clauses(lengths=[1, 2, 3, 4], default_weight=2)
    clauses_dict = {c.value: c.weight for c in clauses}
    print(clauses_dict)
    for c in clauses:
        print(clauses_dict[c.value])
        clauses_dict[c.value] = 3
        print(clauses_dict[c.value])


if __name__ == '__main__':
    # f = FunctorFactory.generate_functors(names=['f'], arities=[0, 1, 2], max_recursion_depth=1)
    # f2 = FunctorFactory.generate_liveness_functors(names=['f'])
    # print(f)
    # print(f2)
    dataset1()
    # hash_test()
