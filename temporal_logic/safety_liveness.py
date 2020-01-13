import sys

from src.ast.exporters.inkresat.inkresat_exporter import InkresatExporter
from src.generators import IntegerRange
from src.generators.presets.propositional_temporal_logic.cnf_propositional_temporal_logic_generator import \
    CNFPropositionalTemporalLogicGenerator

sys.setrecursionlimit(4000)

if __name__ == '__main__':
    system_rpoperty_gen = CNFPropositionalTemporalLogicGenerator(
        variable_names={f'V{i}' for i in range(10)},
        number_of_variables_without_connective=IntegerRange(0, 0),
        number_of_variables_with_always_connectives=IntegerRange(1, 3),
        number_of_variables_with_eventually_connectives=IntegerRange(1, 3),
        number_of_clauses=IntegerRange(2, 10),
        clause_lengths={1})
    exporter = InkresatExporter(
        output_dir='./test-inkresat-cnf/',
        filename_handle=lambda formula_info: '',
        statistics_to_file=True
    )
    for i, formula in enumerate(system_rpoperty_gen.generate()):
        print(str(formula))
        print(formula.get_info())
        exporter.export(formula, filename_suffix=str(i))
        break
