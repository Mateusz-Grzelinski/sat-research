"""Common setting for all test in this directory. Mark this directory sources root, or add it to PYTHONPATH"""
threshold = 0.05
number_of_instances_in_set = 30
number_of_variables_without_connective = 0
clause_lengths = {i for i in range(5, 20)}
negation_probability = 0.1
variable_names = [f'V{i}' for i in range(1000)]

number_of_clauses = 20_000
number_of_variables_with_always_connectives = 100_000
number_of_variables_with_eventually_connectives = 100_000
