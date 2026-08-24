# Compile the certificate

A compile is a hypothesis set. A certificate licenses a trial on
this fingerprint. Injecting the compiled set is still inject.

**Falsifier:** AMMI and compile emit the same rows over this M;
unsettled screens appear in the compiled set; the two `cfg` rows
with the same when/needs have the same sign; unconditional first
on that compiled `cfg` set has nonnegative true ΔU on cloth;
the certificate over that set passes for `cfg`; Fold drift→struct
leaves H unchanged; a 2-D cloth fingerprint still treats rigid
`cfg` as a neighbor with passing LCB; compiled `rep` is accepted
as a vector; or an idle brief still certifies `cfg`.

## Sources

Ding et al. *MemCompiler: Compile, Don’t Inject.* arXiv:2605.07594,
8 May 2026. https://arxiv.org/abs/2605.07594

Wu, Nie, et al. *VERDI: Retrieval Is Not Transfer for Continual
World Model Optimization.* arXiv:2608.09537, August 2026.
https://arxiv.org/abs/2608.09537

Public packs: [compile-dont-inject](https://github.com/StarDust-zz/compile-dont-inject),
[retrieval-is-not-transfer](https://github.com/StarDust-zz/retrieval-is-not-transfer).

## Object

```
M        = settled source library (IEM rows)
b_t      = Brief State (subgoal + beliefs + target fingerprint φ_t)
compile  = { e in M | e.settled
                     and e.when == b_t.subgoal
                     and e.needs ⊆ b_t.beliefs }
           → hypothesis set H
C(a, φ_t) licenses a trial of a on the target
AMMI     = inject all of M (trap + screens + every when)
accept   = ΔU > τ and every protected v_j ≤ 0
```

when/needs is one compile. The certificate is a second compile
against φ_t. Neither step writes target evidence. A Fold on Brief
State (beliefs or chart) stales H.

Same when/needs aliases rigid cfg (ΔU = +3) and cloth cfg
(ΔU = −4). `next_force` is the cloth skill. `rep` is ΔU = 10
with v = 3. `pick_banana` is the always-trap. A screen
`self_force` is unsettled.

## What ran (7/7)

1. **Same M, two executables.** AMMI keeps trap and screen.
   Compile of repair+drift is {cfg, next_force}. Target IEM empty.
2. **Compile is not a claim.** Two cfg rows share when/needs and
   disagree on sign. Unconditional first is rigid; cloth true
   ΔU = −4.
3. **Certificate is the second compile.** C(cfg) fails on sign
   disagreement. C(next_force) passes. Frozen V accepts it.
4. **Fold stales H.** drift→struct: stale {cfg, next_force},
   recompile {rep}.
5. **Chart Fold splits the alias.** 2-D cloth neighbor of cfg is
   only cloth (−4), so LCB fails. next_force still certifies.
6. **Protected survives compile.** Scalar 10 − 3 = 7 would pass.
   Vector gate and certificate refuse.
7. **Empty compile cannot mint a trial.** Idle brief: H = ∅.
   C(cfg) fails on N_eff.

## Keepers

If 7/7 pass, the object that is now a fact is: **Brief State
compiles a hypothesis set; the certificate compiles a trial
license against φ_t; transfer is neither.** when/needs is not
IRG. A compiled alias is still an alias. Averaging a protected
violation into ΔU is a different lowering. A screen is not
source. An empty compile is noaction.

Nothing here is AlfWorld, Ctrl-World, Cosmos, a GPU-hour ledger,
or either paper's headline number. Those are their measurements.
This pack is the discrete join of the two contracts.
