/-
  Feasibility invariants shared across math-modeling tasks.

  Every `hard_errors` branch in the benchmark's `feasibility_checks.py` is one of
  six decidable forms:

  1. domain/range bound      -- probability in [0,1], thickness positive, ...
  2. integer / binary        -- decision bits, case ids, species counts
  3. ordering relation       -- q95 >= mean, peak >= spread average, low <= high
  4. exact algebraic identity-- area = count*w*h, union <= sum-of-parts
  5. finite-domain membership-- length in {16,17}, cases == 1..6, grid membership
  6. partition/sum law       -- four area counts sum to the declared grid

  All six are decidable on exact integers, so Lean core's `decide` and `omega`
  suffice -- no Mathlib, no floating-point reasoning.
-/
import Init

namespace Feasibility

/-! ## Scalar predicates -/

/-- A nonnegative physical quantity (counts, areas, thicknesses, durations). -/
def NonNeg (x : Int) : Prop := 0 ≤ x

/-- A strictly positive physical quantity. -/
def Positive (x : Int) : Prop := 0 < x

/-- `value ≤ bound`. -/
def AtMost (bound value : Int) : Prop := value ≤ bound

/-- `lower ≤ value`. -/
def AtLeast (lower value : Int) : Prop := lower ≤ value

/-- `value` lives on the unit interval scaled by `scale` (probability, share,
    accuracy). E.g. `0.83` is `InUnit 1000 830`. -/
def InUnit (scale : Int) (x : Int) : Prop := 0 ≤ x ∧ x ≤ scale

/-- A signed coefficient such as a correlation, scaled by `scale`. -/
def InSignedUnit (scale : Int) (x : Int) : Prop := -scale ≤ x ∧ x ≤ scale

/-- `lo ≤ value ≤ hi`. -/
def Bounded (lo hi : Int) (x : Int) : Prop := lo ≤ x ∧ x ≤ hi

/-- A unit-like composite index with an *explicitly declared* tolerance, scaled by
    `scale`. Needed because the O-award reference indices are not strictly in [0,1]:
    the Juneau `sustainability_score` anchor is 1.007, so a tolerance-free unit check
    would reject the reference answer itself. The declared `tol` is part of the
    modelling assumption under audit, not a hidden fudge factor. -/
def InIndex (scale tol : Int) (x : Int) : Prop := 0 ≤ x ∧ x ≤ scale + tol

/-- A binary decision value. -/
def Binary (x : Int) : Prop := x = 0 ∨ x = 1

/-! ## List predicates -/

/-- Every row satisfies `p`. Stated as a `Bool` equality so `decide` can close it
    for a concrete literal list. -/
def AllRows {α : Type} (rows : List α) (p : α → Bool) : Prop := rows.all p = true

/-- Sum of a projected column. -/
def ColSum {α : Type} (rows : List α) (f : α → Int) : Int := (rows.map f).sum

/-- The row list is nonempty. -/
def NonEmpty {α : Type} (rows : List α) : Prop := 1 ≤ rows.length

/-- The row count is one of the allowed values. -/
def LenIn {α : Type} (rows : List α) (allowed : List Nat) : Prop := rows.length ∈ allowed

/-- A declared total is partitioned by integer parts. -/
def SumEq (parts : List Int) (total : Int) : Prop := parts.sum = total

/-! ## Reusable lemmas (kernel-checked) -/

theorem atMost_trans {x b c : Int} (h : AtMost b x) (hbc : b ≤ c) : AtMost c x := by
  unfold AtMost at h ⊢; omega

theorem atLeast_mono {x l u : Int} (h : AtLeast l x) (hlu : u ≤ l) : AtLeast u x := by
  unfold AtLeast at h ⊢; omega

theorem inUnit_nonneg {s x : Int} (h : InUnit s x) : NonNeg x := h.1

theorem binary_nonneg {x : Int} (h : Binary x) : NonNeg x := by
  unfold NonNeg
  rcases h with h | h <;> omega

/-- Ordering transitivity, the shared step behind "peak ≥ average", "q95 ≥ mean",
    and every interval or product-ceiling argument. -/
theorem le_trans' {a b c : Int} (h1 : a ≤ b) (h2 : b ≤ c) : a ≤ c := by omega

/-! ## Unit-convention lemmas

A recurring failure mode: a composite index is reported on a percent/points scale
while the declared endpoint is unit-scale. These lemmas make the *exact* salvage
conditions machine-checkable instead of a prose warning. -/

/-- Above the fraction convention but within the percent convention: feasible only
    if a percent scale was explicitly declared. -/
theorem outside_fraction_within_percent {x : Int} (h : 1000 < x) (h2 : x ≤ 100000) :
    ¬ InUnit 1000 x ∧ InUnit 100000 x := by
  constructor
  · unfold InUnit; omega
  · unfold InUnit; omega

/-- Above the percent convention too: no unit convention rescues the value. -/
theorem outside_all_conventions {x : Int} (h : 100000 < x) :
    ¬ (InUnit 1000 x ∨ InUnit 100000 x) := by
  rintro (hx | hx) <;> (unfold InUnit at hx; omega)

/-- A value beyond `scale + tol` is rejected for *that* declared tolerance. -/
theorem out_of_index {scale tol x : Int} (hx : scale + tol < x) : ¬ InIndex scale tol x := by
  intro h; unfold InIndex at h; omega

/-- No tolerance within a declared budget can rescue the value: the strongest form,
  since it rules out "just widen the tolerance" as an escape. -/
theorem out_of_index_for_any_tol_within {scale budget x : Int} (hx : scale + budget < x) :
    ∀ tol, tol ≤ budget → ¬ InIndex scale tol x := by
  intro tol htol h
  unfold InIndex at h
  omega

end Feasibility
