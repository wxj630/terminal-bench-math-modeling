/-
  Instance 2: MCM 2025-B Juneau tourism.

  Same invariant library, different task. This instance is the interesting one:
  it turns a *soft warning* in the numeric gate ("resident_acceptance_index is
  reported above 1.0, suggesting a percentage/points scale") into a machine-checked
  statement about exactly which convention can rescue each value.

  The O-award anchors are acceptance_index = 1.0 and sustainability_score = 1.007.
  The second one is why the index domain needs a *declared* tolerance rather than a
  bare [0,1] bound: a tolerance-free check rejects the reference answer itself.
-/
import FeasibilityDemo.Invariants
open Feasibility

namespace Juneau

/-- The headroom a model may declare on a unit-like composite index, on the same
    x1000 scale (50 = 5%). Declaring it is the point: the audit asks whether the
    reported value fits *any* reasonable declaration. -/
def tolBudget : Int := 50

structure Artifact where
  acceptanceIndex : Int   -- x 1000
  sustainability : Int    -- x 1000

/-- Feasible under a *declared* tolerance `tol` for the composite index, with the
    acceptance index on the exact unit interval (its anchor is 1.0). -/
def Feasible (tol : Int) (a : Artifact) : Prop :=
  InUnit 1000 a.acceptanceIndex ∧ InIndex 1000 tol a.sustainability

/-- Values read verbatim from the union-alpha artifact. -/
def ua : Artifact :=
  { acceptanceIndex := 85098      -- 85.09810789526455
  , sustainability := 118362 }    -- 118.36208669513368

/-- 85.098 is outside the fraction convention but inside the percent convention: it is
    salvageable *only* by an explicitly declared percent scale. -/
theorem ua_acceptance_percent_only :
    ¬ InUnit 1000 ua.acceptanceIndex ∧ InUnit 100000 ua.acceptanceIndex := by
  unfold ua InUnit; decide

/-- 118.362 is rejected for *every* tolerance inside the declared budget, so widening
    the tolerance is not an escape. This is the machine-checked replacement for the
    "sustainability_score exceeds 1.5 ... until explicitly converted" warning. -/
theorem ua_sustainability_out_for_any_sane_tol :
    ∀ tol, tol ≤ tolBudget → ¬ InIndex 1000 tol ua.sustainability := by
  apply out_of_index_for_any_tol_within
  unfold ua tolBudget; decide

/-- Therefore the artifact cannot satisfy the contract for any tolerance within budget. -/
theorem ua_infeasible_for_any_sane_tol :
    ∀ tol, tol ≤ tolBudget → ¬ Feasible tol ua := by
  intro tol htol h
  exact ua_sustainability_out_for_any_sane_tol tol htol h.2

end Juneau
