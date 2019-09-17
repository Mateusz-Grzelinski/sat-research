from src.exporters.tptp_exporter import TPTPHeader
from src.generators import WeightedSequence
from src.generators.factories import FunctorFactory, PredicateFactory, AtomFactory, LiteralFactory, CNFClauseFactory
from src.generators.randomcnfgenerator import RandomCNFGenerator
from src.generators.thresholdregulator import ThresholdRegulator


def dataset1():
    functors = FunctorFactory.generate_functors(names=['f'], arities=[0, 1], max_recursion_depth=1)
    functors = WeightedSequence.from_weighted_values(functors)
    predicates = PredicateFactory.generate_predicates(names=['p'], arities=[1, 2])
    predicates = WeightedSequence.from_weighted_values(predicates)
    atoms = AtomFactory.generate_atoms({''})
    atoms = WeightedSequence.from_weighted_values(atoms)
    literals = LiteralFactory.generate_literals()
    literals = WeightedSequence.from_weighted_values(literals)
    clauses = CNFClauseFactory.generate_clauses(lengths=[1, 2, 3, 4])
    clauses = WeightedSequence.from_weighted_values(clauses)

    g = RandomCNFGenerator(
        functors=functors.values,
        functor_weights=functors.weights,
        predicates=predicates.values,
        predicate_weights=predicates.weights,
        atoms=atoms.values,
        atom_weights=atoms.weights,
        literals=literals.values,
        literal_weights=literals.weights,
        clauses=clauses.values,
        clause_weights=clauses.weights
    )

    print(f'{g.functors=}')
    print(f'{g.predicates=}')
    print(f'{g.atoms=}')
    print(f'{g.literals=}')
    print(f'{g.clauses=}')

    formula = g.generate_cnf_formula(number_of_clauses=2)
    tr = ThresholdRegulator(
        number_of_clauses=ThresholdRegulator.range(10, threshold=0.5, delta=5),
        number_of_literals=ThresholdRegulator.range(10, threshold=0.5, delta=5),
        number_of_atoms=ThresholdRegulator.range(10, threshold=0.5, delta=5),
        number_of_predicates=ThresholdRegulator.range(10, threshold=0.5, delta=5),
        number_of_functors=ThresholdRegulator.range(10, threshold=0.5, delta=5),
        number_of_variables=ThresholdRegulator.range(10, threshold=0.5, delta=5)
    )
    tr.tune_cnf_formula(generator=g, initial_cnf_formula=formula)
    t = TPTPHeader()
    t.read_from(formula)
    print(t.get_header())
    print(formula)


if __name__ == '__main__':
    # f = FunctorFactory.generate_functors(names=['f'], arities=[0, 1, 2], max_recursion_depth=1)
    # f2 = FunctorFactory.generate_liveness_functors(names=['f'])
    # print(f)
    # print(f2)
    dataset1()
