#!/usr/bin/env python3
"""Independent exhaustive tests for the bilateral-deficiency theorem ladder."""

from __future__ import annotations

import unittest
from collections import Counter
from fractions import Fraction
from itertools import combinations

from bd_core import (
    FALSE,
    TRUE,
    UNASSIGNED,
    IndexedCNF,
    assignment_to_ids,
    beta,
    bilateral_deficiency,
    conditional_expectation_complete_assignment,
    disjoint_union,
    expected_unsatisfied_clauses,
    formula_graph,
    ids_to_assignment,
    independent_dominating_sets,
    is_bilateral,
    maxsat_defect,
    partial_assignments,
    dimacs_text,
    read_dimacs,
    replicate_clauses,
    residual,
    width_lift,
)
from analyze_formula import incidence_is_forest, regular_dim_signature
from connector_search import exact_322_audit, occurrence_switch
from terminal_signature import (
    close_signature,
    compose_closed_signatures,
    glue_formulas_on_terminals,
    terminal_signature,
)
from lift_search import two_lift
from generate_enforcer_base import flip_variable
from formula_identity import identity_audit
from generate_prism_amplifier import (
    edge_enforcer_amplifier,
    prism_amplifier,
    prism_edges,
)
from generate_owest_amplifier import audit_cubic_skeleton, owest_h1_skeleton
from paired_edge_normal_form import audit_assignment_identity, paired_clause_graph


def formulas_from_clause_pool(variables: int, maximum_clauses: int):
    literals = tuple(range(1, variables + 1)) + tuple(range(-variables, 0))
    pool = [frozenset()]
    for width in range(1, min(2, len(literals)) + 1):
        pool.extend(frozenset(clause) for clause in combinations(literals, width))
    for number in range(maximum_clauses + 1):
        for indices in combinations(range(len(pool)), number):
            yield IndexedCNF.from_clauses(variables, (pool[index] for index in indices))


class BilateralDeficiencyTests(unittest.TestCase):
    def test_residual_and_bilateral_definition(self):
        formula = IndexedCNF.from_clauses(3, [(1, 2), (-1, 3), (-2, -3)])
        assignment = (UNASSIGNED, TRUE, FALSE)
        r = residual(formula, assignment)
        self.assertEqual(r.clause_indices, (1,))
        self.assertEqual(r.clauses, (frozenset({-1}),))
        self.assertFalse(is_bilateral(formula, assignment))

    def test_master_bijection_and_size_polynomial_exhaustively(self):
        # This includes empty, unit, binary, tautological, and absent-variable cases.
        checked = 0
        for formula in formulas_from_clause_pool(2, 3):
            graph_sets = set(independent_dominating_sets(formula_graph(formula)))
            assignment_sets = {
                assignment_to_ids(formula, assignment)
                for assignment in partial_assignments(formula.variables)
                if is_bilateral(formula, assignment)
            }
            self.assertEqual(graph_sets, assignment_sets, formula)
            for selected in graph_sets:
                assignment = ids_to_assignment(formula, selected)
                self.assertEqual(assignment_to_ids(formula, assignment), selected)
                self.assertEqual(
                    len(selected),
                    formula.variables + bilateral_deficiency(formula, assignment),
                )
            graph_spectrum = Counter(map(len, graph_sets))
            beta_spectrum = Counter(
                {
                    formula.variables + deficiency: multiplicity
                    for deficiency, multiplicity in beta(formula).spectrum
                }
            )
            self.assertEqual(graph_spectrum, beta_spectrum)
            checked += 1
        self.assertGreater(checked, 100)

    def test_width_two_equals_maxsat_defect_exhaustively(self):
        for formula in formulas_from_clause_pool(2, 4):
            self.assertEqual(beta(formula).value, maxsat_defect(formula), formula)

    def test_width_lift_preserves_beta(self):
        seeds = [
            IndexedCNF.from_clauses(1, [(1,), (-1,)]),
            IndexedCNF.from_clauses(2, [(1, 2), (-1, -2)]),
            IndexedCNF.from_clauses(2, [(1, -1), (), (2,)]),
        ]
        for formula in seeds:
            self.assertEqual(beta(width_lift(formula)).value, beta(formula).value)

    def test_additivity_and_multiplicative_spectrum(self):
        positive = IndexedCNF.from_clauses(1, [(1,), (-1,)])
        negative = IndexedCNF.from_clauses(3, [(1, 2, 3), (-1, -2, -3)])
        combined = disjoint_union(positive, negative)
        self.assertEqual(beta(positive).value, 1)
        self.assertEqual(beta(negative).value, -1)
        self.assertEqual(beta(combined).value, 0)

        expected: Counter[int] = Counter()
        for left, left_count in beta(positive).spectrum:
            for right, right_count in beta(negative).spectrum:
                expected[left + right] += left_count * right_count
        self.assertEqual(dict(beta(combined).spectrum), dict(expected))

    def test_replication_recovers_maxsat_optimum(self):
        seeds = [
            IndexedCNF.from_clauses(1, [(1,), (-1,)]),
            IndexedCNF.from_clauses(2, [(1, 2), (-1,), (-2,)]),
            IndexedCNF.from_clauses(3, [(1, 2, 3), (-1, -2, -3)]),
        ]
        for formula in seeds:
            copies = formula.variables + 1
            amplified = replicate_clauses(formula, copies)
            recovered = -(-beta(amplified).value // copies)
            self.assertEqual(recovered, maxsat_defect(formula))

    def test_conditional_expectation_constructs_complete_beta_witness(self):
        formulas = [
            IndexedCNF.from_clauses(0, [()]),
            IndexedCNF.from_clauses(2, [(1, -1), (2, -2)]),
            IndexedCNF.from_clauses(3, [(1, 2, 3), (-1, -2, -3)]),
            read_dimacs(
                __import__("pathlib").Path(__file__).with_name("instances")
                / "negative_322.cnf"
            ),
            read_dimacs(
                __import__("pathlib").Path(__file__).with_name("instances")
                / "txgraffiti_15_20.cnf"
            ),
        ]
        for formula in formulas:
            initial = expected_unsatisfied_clauses(
                formula, (UNASSIGNED,) * formula.variables
            )
            assignment, unsatisfied, trace = (
                conditional_expectation_complete_assignment(formula)
            )
            self.assertTrue(is_bilateral(formula, assignment))
            self.assertEqual(len(residual(formula, assignment).clauses), unsatisfied)
            self.assertLessEqual(unsatisfied, initial.numerator // initial.denominator)
            self.assertEqual(trace[0], initial)
            self.assertEqual(trace[-1], Fraction(unsatisfied))
            self.assertTrue(
                all(right <= left for left, right in zip(trace, trace[1:]))
            )

        positive = formulas[-1]
        assignment, unsatisfied, _ = conditional_expectation_complete_assignment(
            positive
        )
        self.assertEqual(regular_dim_signature(positive), 3)
        self.assertLessEqual(unsatisfied, len(positive.clauses) // 8)
        self.assertEqual(
            bilateral_deficiency(positive, assignment), unsatisfied
        )

    def test_beta_is_not_ordinary_deficiency_or_satisfiability(self):
        satisfiable = IndexedCNF.from_clauses(2, [(1,), (2,), (1, 2)])
        unsatisfiable = IndexedCNF.from_clauses(2, [(1,), (2,), (-1, -2)])
        self.assertEqual(len(satisfiable.clauses) - satisfiable.variables, 1)
        self.assertEqual(len(unsatisfiable.clauses) - unsatisfiable.variables, 1)
        self.assertEqual(beta(satisfiable).value, 0)
        self.assertEqual(beta(unsatisfiable).value, 1)

        negative_but_satisfiable = IndexedCNF.from_clauses(
            3, [(1, 2, 3), (-1, -2, -3)]
        )
        self.assertEqual(maxsat_defect(negative_but_satisfiable), 0)
        self.assertEqual(beta(negative_but_satisfiable).value, -1)

    def test_dimacs_round_trip_preserves_indexed_duplicates(self):
        formula = IndexedCNF.from_clauses(2, [(1, -1), (2,), (2,), ()])
        path = __import__("pathlib").Path(__file__).with_name(".roundtrip-test.cnf")
        try:
            path.write_text(dimacs_text(formula), encoding="ascii")
            self.assertEqual(read_dimacs(path), formula)
        finally:
            path.unlink(missing_ok=True)

    def test_structural_algorithm_signatures(self):
        tree_formula = IndexedCNF.from_clauses(3, [(1, 2), (-2, 3)])
        cycle_formula = IndexedCNF.from_clauses(2, [(1, 2), (-1, -2)])
        self.assertTrue(incidence_is_forest(tree_formula))
        self.assertFalse(incidence_is_forest(cycle_formula))

        exact_322 = read_dimacs(
            __import__("pathlib").Path(__file__).with_name("instances") / "negative_322.cnf"
        )
        self.assertEqual(regular_dim_signature(exact_322), 3)

        # Tautological clauses arise legitimately when an unmatched graph
        # vertex sees both endpoints of one distinguished matching edge.
        tautological_regular = IndexedCNF.from_clauses(2, [(1, -1), (2, -2)])
        self.assertEqual(regular_dim_signature(tautological_regular), 2)

    def test_occurrence_switch_preserves_exact_322_and_connects(self):
        component = read_dimacs(
            __import__("pathlib").Path(__file__).with_name("instances")
            / "negative_322.cnf"
        )
        left_literal = min(component.clauses[0], key=lambda value: abs(value))
        right_literal = min(component.clauses[0], key=lambda value: abs(value))
        joined = occurrence_switch(
            component, component, 0, left_literal, 0, right_literal
        )
        self.assertTrue(all(exact_322_audit(joined).values()))

    def test_terminal_min_plus_composition_is_exact(self):
        left = IndexedCNF.from_clauses(
            2, [(1, 2), (-1, -2), (1, -2)]
        )
        right = IndexedCNF.from_clauses(
            2, [(1, 2), (-1, -2), (-1, 2)]
        )
        left_signature = terminal_signature(left, (1,))
        right_signature = terminal_signature(right, (1,))
        self.assertEqual(close_signature(left_signature)[0], beta(left).value)
        self.assertEqual(close_signature(right_signature)[0], beta(right).value)

        composed_value, _, _ = compose_closed_signatures(
            left_signature, right_signature
        )
        glued = glue_formulas_on_terminals(left, (1,), right, (1,))
        self.assertEqual(composed_value, beta(glued).value)

    def test_two_lift_preserves_exact_322(self):
        component = read_dimacs(
            __import__("pathlib").Path(__file__).with_name("instances")
            / "negative_322.cnf"
        )
        lifted = two_lift(component, frozenset({0, 3, 7}))
        audit = exact_322_audit(lifted)
        self.assertTrue(audit["proper"])
        self.assertTrue(audit["simple"])
        self.assertTrue(audit["exact_322"])

    def test_enforcer_flip_composition_has_value_one(self):
        enforcer = read_dimacs(
            __import__("pathlib").Path(__file__).with_name("instances")
            / "sat2024_e322_enforcer.cnf"
        )
        flipped = flip_variable(enforcer, 1)
        left = terminal_signature(enforcer, (1,))
        right = terminal_signature(flipped, (1,))
        value, _, _ = compose_closed_signatures(left, right)
        composed = glue_formulas_on_terminals(enforcer, (1,), flipped, (1,))
        self.assertEqual(value, 1)
        self.assertTrue(all(exact_322_audit(composed).values()))

    def test_formula_identity_allows_terminal_sign_switch(self):
        source = __import__("pathlib").Path(__file__).with_name("instances") / (
            "sat2024_e322_enforcer.cnf"
        )
        with __import__("tempfile").TemporaryDirectory() as temporary:
            target = __import__("pathlib").Path(temporary) / "flipped.cnf"
            formula = read_dimacs(source)
            target.write_text(dimacs_text(flip_variable(formula, 1)), encoding="ascii")
            audit = identity_audit(source, target)
            self.assertTrue(audit["plain_formula_graph_isomorphic"])
            self.assertTrue(audit["colored_formula_graph_isomorphic"])

    def test_prism_amplifier_has_declared_exact_structure(self):
        enforcer = read_dimacs(
            __import__("pathlib").Path(__file__).with_name("instances")
            / "sat2024_e322_enforcer.cnf"
        )
        self.assertEqual(len(prism_edges(3)), 9)
        formula = prism_amplifier(enforcer, 3)
        self.assertEqual(formula.variables, 72)
        self.assertEqual(len(formula.clauses), 96)
        self.assertTrue(all(exact_322_audit(formula).values()))

    def test_owest_skeleton_and_amplifier_have_declared_structure(self):
        enforcer = read_dimacs(
            __import__("pathlib").Path(__file__).with_name("instances")
            / "sat2024_e322_enforcer.cnf"
        )
        for expansions in range(3):
            order, edges = owest_h1_skeleton(expansions)
            self.assertEqual(order, 16 + 18 * expansions)
            skeleton_audit = audit_cubic_skeleton(order, edges)
            self.assertTrue(skeleton_audit["simple"])
            self.assertTrue(skeleton_audit["cubic"])
            self.assertTrue(skeleton_audit["connected"])
            formula = edge_enforcer_amplifier(enforcer, order, edges)
            self.assertTrue(all(exact_322_audit(formula).values()))
            self.assertEqual(formula.variables, 12 * order)
            self.assertEqual(len(formula.clauses), 16 * order)

    def test_paired_edge_normal_form_matches_every_assignment(self):
        formula = read_dimacs(
            __import__("pathlib").Path(__file__).with_name("instances")
            / "negative_322.cnf"
        )
        graph = paired_clause_graph(formula)
        self.assertEqual(graph.vertices, 8)
        self.assertEqual(len(graph.pairs), 6)
        self.assertEqual(len(graph.edges), 12)
        for assignment in partial_assignments(formula.variables):
            audit_assignment_identity(formula, assignment)


if __name__ == "__main__":
    unittest.main(verbosity=2)
