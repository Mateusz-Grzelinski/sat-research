from src.generators.presets.first_order_logic import FormulaGenerator

if __name__ == '__main__':
    gen = FormulaGenerator(
        functor_names={f'f{i}' for i in range(10)}, functor_arity={0}, functor_recursion_depth=0,
        predicate_names={f'p{i}' for i in range(10)}, predicate_arities={0, 1},
        variable_names={f'V{i}' for i in range(10)},
        atom_connectives={None},
        atom_negation_chance=0.1,
        number_of_atoms=10,
        quantifier_number_of_atoms=set(),
        number_of_existential_quantifiers=0,
        number_of_universal_quantifiers=0,
    )
    formula = gen.generate()

    print('Generated formula:')
    print(str(formula))
