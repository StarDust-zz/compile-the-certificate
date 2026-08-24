# Compile the certificate

A small, stdlib-only join of two keepers.

[MemCompiler](https://github.com/StarDust-zz/compile-dont-inject) says memory is source and Brief State compiles the executable. [VERDI](https://github.com/StarDust-zz/retrieval-is-not-transfer) says a retrieved repair is a hypothesis and a certificate licenses a trial. This pack puts them on one library: **when/needs compile is not IRG.** The compiled set can still alias opposite-signed skills. Injecting that set is still inject.

This is the discrete algebra of that join, not AlfWorld and not a world-model training run.

```
python3 experiment.py
```

Last run: **7/7 passed**. Python 3.10+, stdlib + `fractions` only. No GPU, no network, no model API.

Papers under test:

- Ding et al., *MemCompiler: Compile, Don’t Inject — State-Conditioned Memory for Embodied Agents*, 8 May 2026, [arXiv:2605.07594](https://arxiv.org/abs/2605.07594)
- Wu, Nie, et al., *VERDI: Retrieval Is Not Transfer for Continual World Model Optimization*, August 2026, [arXiv:2608.09537](https://arxiv.org/abs/2608.09537). Project: [verdiwm-anno.github.io](https://verdiwm-anno.github.io/)

## Why this exists

Compile-dont-inject already showed that dumping `M` is a bad lowering. The leftover temptation is to treat the *compiled* set as transferred knowledge: you filtered on Brief State, so the survivors must be safe to reuse.

They are not. when/needs is a predicate on the current subgoal and beliefs. It does not see the Optimization Fingerprint. Two settled `cfg` rows can share `when="repair"` and `needs={drift}` and still have opposite paired effects on models that sit at the same 1-D probe coordinate. Unconditional first on that compiled set is rigid `cfg` (+3 on the source, −4 on cloth). The certificate is the second compile: it looks at φ_t, sign agreement, LCB, and protected coordinates, and it licenses a *trial*, not a claim.

If the seven assertions hold, the keeper is:

> Brief State compiles a hypothesis set. The certificate compiles a trial license against φ_t. Transfer is neither.

## The object

```
M        = settled source library (IEM rows)
b_t      = Brief State = (subgoal, beliefs, target fingerprint φ_t)
compile  = { e ∈ M | e.settled
                     ∧ e.when == b_t.subgoal
                     ∧ e.needs ⊆ b_t.beliefs }
           → hypothesis set H
C(a, φ_t) licenses a trial of a on the target
AMMI     = inject all of M (trap + screens + every when)
accept   = ΔU > τ and every protected v_j ≤ 0
```

when/needs is one compile. The certificate is a second compile against φ_t. Neither step writes target evidence. A Fold on Brief State (beliefs, or a new probe on the chart) stales `H`.

A compile that you then dump into the executor is AMMI of a smaller bag.

## Library

`M` is six rows. Only settled rows with matching when/needs enter `H`.

| skill | when | needs | source φ | ΔU | v | settled | role |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `cfg` | `repair` | `{drift}` | rigid 1-D `(2,)` | +3 | −1 | yes | aliases with cloth |
| `cfg` | `repair` | `{drift}` | cloth 1-D `(2,)` | −4 | −1 | yes | same predicate, opposite sign |
| `next_force` | `repair` | `{drift}` | cloth 1-D `(2,)` | +5 | 0 | yes | the cloth skill |
| `rep` | `repair` | `{struct}` | cosmos `(1,1)` | +10 | +3 | yes | scalar win, vector fail |
| `pick_banana` | `always` | ∅ | rigid 1-D | +1 | 0 | yes | AMMI trap |
| `self_force` | `repair` | `{artic}` | arm `(4,)` | +2 | 0 | **no** | screen, not source |

After a chart Fold the 2-D fingerprints are rigid `(2,0)` and cloth `(2,3)`. Same when/needs still selects both `cfg` rows. IRG at ε=0 keeps only the matching chart neighbor.

True target-side effects (frozen verifier, not in `M`): cloth `cfg` = −4, cloth `next_force` = +5, cloth `pick_banana` = −8, cosmos `rep` = (10, v=3).

## Run

```bash
python3 experiment.py
```

Seven numbered lines and `7/7 passed`.

| file | what it is |
| --- | --- |
| [`experiment.py`](experiment.py) | Brief State, compile, certificate, the seven assertions |
| [`DESCRIPTION.md`](DESCRIPTION.md) | short lab note (falsifier + keepers) |

## Assertions

1. **Same `M`, two executables.** AMMI keeps the trap and the screen. Compile of `repair`+`drift` is `{cfg, next_force}`. Target IEM is empty.
2. **Compile is not a claim.** The two `cfg` rows share when/needs and disagree on sign. Unconditional first is rigid. Cloth true ΔU = −4.
3. **Certificate is the second compile.** `C(cfg)` fails on sign disagreement. `C(next_force)` passes. The frozen verifier accepts it.
4. **Fold stales `H`.** drift→struct: stale `{cfg, next_force}`, recompile `{rep}`.
5. **Chart Fold splits the alias.** 2-D cloth neighbor of `cfg` is only cloth (−4), so LCB fails. `next_force` still certifies.
6. **Protected survives compile.** Scalar 10 − 3 = 7 would pass. The vector gate and the certificate refuse.
7. **Empty compile cannot mint a trial.** Idle brief: `H = ∅`. `C(cfg)` fails on `N_eff`.

## What this is not

- Not MemCompiler's trained compiler, Soft-Mem, SFT, or GRPO, and not a replay of AlfWorld.
- Not VERDI's Ctrl-World / Cosmos / RoboCoin campaigns, GPU-hour ledger, or the 0.34 → 0.06 negative-transfer number. Those are their measurements.
- Not a claim that when/needs is useless. It already drops the always-trap and the screen. It is not enough.
- Not a product integration.

If you want the empirical results, run the papers. This repo asks whether the two *contracts* still compose when you strip the nets.

## Citation

The two claims under test:

```
@article{ding2026memcompiler,
  title   = {MemCompiler: Compile, Don't Inject -- State-Conditioned Memory for Embodied Agents},
  author  = {Ding, Xin and Wang, Xinrui and Yang, Yifan and Wu, Hao and Jiang, Shiqi
             and Zhang, Qianxi and Mi, Liang and Zhu, Hanxin and Li, Kun
             and Liu, Yunxin and Chen, Zhibo and Cao, Ting},
  journal = {arXiv preprint arXiv:2605.07594},
  year    = {2026}
}

@article{wu2026verdi,
  title   = {VERDI: Retrieval Is Not Transfer for Continual World Model Optimization},
  author  = {Wu, Junyu and Nie, Shiqin and Kou, Youyi and Yin, Baohua and Yao, Guocai
             and Chen, Qingyu and Ma, Jingheng and Zhou, Shiji and Song, Hongyong
             and Zhuge, Mingchen and Cui, Sen and Zhang, Changshui},
  journal = {arXiv preprint arXiv:2608.09537},
  year    = {2026}
}
```

This repository is an independent discrete experiment. It is not affiliated with those authors.

Sibling packs: [compile-dont-inject](https://github.com/StarDust-zz/compile-dont-inject), [retrieval-is-not-transfer](https://github.com/StarDust-zz/retrieval-is-not-transfer).

## License

[MIT](LICENSE). Copyright (c) 2026 Igor Pistolyaka.

The papers and any official code keep whatever license their authors chose. Nothing here is a copy of those codebases.
