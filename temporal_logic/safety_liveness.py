import logging

from src.ast.exporters.inkresat.inkresat_exporter import InkresatExporter
from src.generators import IntegerRange
from src.generators.presets.propositional_temporal_logic.cnf_propositional_temporal_logic_generator import \
    CNFPropositionalTemporalLogicGenerator

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    threshold = 0.05
    number_of_instances_in_set = 50

    number_of_clauses_list = [50, 100, 200, 400, 500, 600, 700]
    number_of_variables_with_always_connectives = 500
    number_of_variables_with_eventually_connectives = 500
    for number_of_clauses in number_of_clauses_list:
        system_rpoperty_gen = CNFPropositionalTemporalLogicGenerator(
            variable_names={f'V{i}' for i in range(20)},
            number_of_variables_without_connective=IntegerRange(0, 0),
            number_of_variables_with_always_connectives=IntegerRange.from_relative(500, threshold),
            number_of_variables_with_eventually_connectives=IntegerRange.from_relative(500, threshold),
            number_of_clauses=IntegerRange.from_relative(number_of_clauses, threshold),
            clause_lengths={2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13})
        exporter = InkresatExporter(
            output_dir=f'./test-inkresat-cnf/{number_of_clauses}-clauses/',
            filename_handle=lambda formula_info: '',
            statistics_to_file=True
        )
        for i, formula in enumerate(system_rpoperty_gen.generate()):
            # print(str(formula))
            # print(formula.get_info())
            exporter.export(formula, filename_suffix=str(i))
            if i == number_of_instances_in_set:
                break

        # else:
        #     logging.error(f'not enoughformulas, ended at {i}, expcted {number_of_instances_in_set}')
