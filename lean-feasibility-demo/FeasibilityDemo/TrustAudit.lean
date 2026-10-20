/-
  Trust audit.

  A feasibility *certificate* is only worth more than a numeric check if it is
  kernel-checked. `sorryAx` (an admitted gap) or `Lean.ofReduceBool` (trusting the
  compiler rather than the kernel, as `native_decide` does) would silently destroy
  that guarantee. This file makes each certificate's dependency set explicit.
-/
import FeasibilityDemo.Invariants
import FeasibilityDemo.CropPlanting
import FeasibilityDemo.Juneau
import FeasibilityDemo.Sensitivity

-- Shared library lemmas: no computational trust, only classical logic.
#print axioms Feasibility.atMost_trans
#print axioms Feasibility.atLeast_mono
#print axioms Feasibility.le_trans'
#print axioms Feasibility.out_of_index

-- Worked task instances.
#print axioms CropPlanting.ua_feasible
#print axioms CropPlanting.ua_in_interpretation_gap
#print axioms CropPlanting.gap_is_real
#print axioms Juneau.ua_acceptance_percent_only
#print axioms Juneau.ua_sustainability_out_for_any_sane_tol
#print axioms JuneauSensitivity.corrected_feasible
#print axioms JuneauSensitivity.reported_infeasible
