/-
  Instance 1: CUMCM 2024-C crop planting (the benchmark's C038 special case).

  Checks a real artifact produced by the anonymous model `stealth/union-alpha`.
  All money is stored in milli-yuan (value x 1000) so every comparison is exact
  integer arithmetic -- no float tolerance, no `1e-9` fudge factors.
-/
import FeasibilityDemo.Invariants
open Feasibility

namespace CropPlanting

/-- Per-plot demand-cap reading (the O-paper's eq.19 places `min(x*y, d)` inside the
    per-plot sum): the ceiling on 7-year profit / revenue, in milli-yuan. -/
def perPlotProfitCeiling : Int := 45461290000
def perPlotRevenueCeiling : Int := 52042270000

/-- The aggregate reading (the statement's "每季总产量") is strictly tighter. -/
def aggregateProfitCeiling : Int := 36277448000

structure Artifact where
  wasteProfit : Int      -- surplus wasted, 7-year total
  wasteRevenue : Int
  discountProfit : Int   -- surplus sold at 50% off
  spearman : Int         -- price/cost rank correlation x 1000

/-- Core feasibility, independent of the demand-cap reading:
    * the plan respects the (looser) per-plot ceilings,
    * the 50%-discount scenario cannot earn less than the wasted-surplus scenario,
    * the reported correlation is a valid coefficient. -/
def Feasible (a : Artifact) : Prop :=
  AtMost perPlotProfitCeiling a.wasteProfit ∧
  AtMost perPlotRevenueCeiling a.wasteRevenue ∧
  AtLeast a.wasteProfit a.discountProfit ∧
  InSignedUnit 1000 a.spearman

/-- The demand-cap reading is the *only* remaining numeric freedom: a profit strictly
    between the two ceilings is reachable under the per-plot reading alone. -/
def InInterpretationGap (a : Artifact) : Prop :=
  aggregateProfitCeiling < a.wasteProfit ∧ a.wasteProfit ≤ perPlotProfitCeiling

/-- Values read verbatim from the union-alpha artifact (see report for the path). -/
def ua : Artifact :=
  { wasteProfit := 39590043432      -- 39,590,043.43237357
  , wasteRevenue := 45502872570     -- 45,502,872.570891716
  , discountProfit := 56945714963   -- 56,945,714.963314675
  , spearman := 238 }               -- 0.23806082802363082

/-- Certificate: union-alpha's artifact satisfies every hard invariant.
    Kernel-checked by `decide`; this is not a script that "ran clean". -/
theorem ua_feasible : Feasible ua := by
  unfold Feasible ua AtMost AtLeast InSignedUnit
  unfold perPlotProfitCeiling perPlotRevenueCeiling
  decide

/-- Certificate: its profit lies strictly inside the per-plot/aggregate gap, so the
    "feasible" verdict rests on a declared reading, not on arithmetic. -/
theorem ua_in_interpretation_gap : InInterpretationGap ua := by
  unfold InInterpretationGap ua aggregateProfitCeiling perPlotProfitCeiling
  decide

/-- The two readings genuinely differ: a profit above the aggregate ceiling is not
    reachable once the cap is applied to the crop-season total. Symbolic, so the
    library's lemma transfers to any artifact -- not just this one. -/
theorem gap_is_real {x : Int} (h : aggregateProfitCeiling < x) :
    ¬ AtMost aggregateProfitCeiling x := by
  unfold AtMost; omega

end CropPlanting
