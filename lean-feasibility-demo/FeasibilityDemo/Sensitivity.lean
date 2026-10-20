/-
  Sensitivity check: the certificates are not vacuous.

  If the Juneau proofs only succeeded because the predicate was trivially true, then
  flipping an input would not change provability. These instances show that it does:
  a unit-scale artifact is provably feasible, and the *same* predicate provably
  rejects the reported value. A gate that cannot fail is not a gate.
-/
import FeasibilityDemo.Invariants
import FeasibilityDemo.Juneau
open Feasibility

namespace JuneauSensitivity
open Juneau

/-- A correctly unit-scaled policy report (acceptance 0.83, sustainability 1.007 --
    the O-award anchor, which is why the tolerance exists). -/
def corrected : Artifact :=
  { acceptanceIndex := 830
  , sustainability := 1007 }

/-- The corrected artifact is provably feasible under the declared contract. -/
theorem corrected_feasible : Feasible tolBudget corrected := by
  unfold Feasible corrected InUnit InIndex tolBudget; decide

/-- The reported artifact is provably infeasible for every in-budget tolerance.
    Both proofs are kernel-checked, so the verdict genuinely depends on the data. -/
theorem reported_infeasible :
    ∀ tol, tol ≤ tolBudget → ¬ Feasible tol ua := ua_infeasible_for_any_sane_tol

end JuneauSensitivity
