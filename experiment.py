#!/usr/bin/env python3
"""Compile the certificate.

Join of Ding et al. MemCompiler (arXiv:2605.07594) and Wu, Nie et al.
VERDI (arXiv:2608.09537). Brief State compiles a hypothesis set from
the source library. A certificate licenses a target-side trial.
Injecting the compiled set is still inject.

Stdlib + fractions only. Run: python3 experiment.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from fractions import Fraction
from typing import FrozenSet, List, Optional, Sequence, Tuple

F = Fraction


# ---------------------------------------------------------------------------
# Fingerprint / effect / certificate (VERDI, discrete)
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Fingerprint:
    j: Tuple[F, ...]
    hooks: Tuple[str, ...] = ()
    support: Tuple[str, ...] = ()


def dist_irg(a: Fingerprint, b: Fingerprint) -> F:
    if len(a.j) != len(b.j):
        raise ValueError("shared chart required")
    return sum((x - y) ** 2 for x, y in zip(a.j, b.j))


def overlap(a: Fingerprint, b: Fingerprint) -> F:
    sa, sb = set(a.support), set(b.support)
    if not sa or not sb:
        return F(0)
    return F(len(sa & sb), len(sa | sb))


@dataclass(frozen=True)
class Effect:
    delta_u: F
    violations: Tuple[F, ...] = ()

    def accepted(self, tau: F = F(0)) -> bool:
        return self.delta_u > tau and all(v <= 0 for v in self.violations)

    def scalar_average(self) -> F:
        return self.delta_u - sum(self.violations)


@dataclass(frozen=True)
class Record:
    """Settled source row. when/needs are MemCompiler predicates."""

    skill: str
    when: str
    needs: FrozenSet[str]
    source: Fingerprint
    effect: Effect
    settled: bool


@dataclass(frozen=True)
class Certificate:
    compile_ok: bool
    overlap_ok: bool
    n_eff_ok: bool
    sign_agree: bool
    lcb_ok: bool
    protected_ok: bool

    def pass_(self) -> bool:
        return (
            self.compile_ok
            and self.overlap_ok
            and self.n_eff_ok
            and self.sign_agree
            and self.lcb_ok
            and self.protected_ok
        )


# ---------------------------------------------------------------------------
# Brief State compile (MemCompiler, discrete)
# ---------------------------------------------------------------------------

@dataclass
class BriefState:
    subgoal: str
    beliefs: set[str] = field(default_factory=set)
    fingerprint: Optional[Fingerprint] = None

    def fold(
        self,
        next_subgoal: Optional[str] = None,
        new_beliefs: FrozenSet[str] = frozenset(),
        fingerprint: Optional[Fingerprint] = None,
    ) -> None:
        if next_subgoal is not None:
            self.subgoal = next_subgoal
        self.beliefs.update(new_beliefs)
        if fingerprint is not None:
            self.fingerprint = fingerprint


def applicable(row: Record, brief: BriefState) -> bool:
    return row.settled and row.when == brief.subgoal and row.needs <= brief.beliefs


def inject_all(memory: Sequence[Record]) -> Tuple[Record, ...]:
    return tuple(memory)


def compile_hypotheses(memory: Sequence[Record], brief: BriefState) -> Tuple[Record, ...]:
    """SCMC: same M, only what Brief State justifies. Still hypotheses."""
    return tuple(r for r in memory if applicable(r, brief))


def neighbors(target: Fingerprint, rows: Sequence[Record], skill: str, eps: F) -> List[Record]:
    return [
        r
        for r in rows
        if r.skill == skill and r.settled and dist_irg(target, r.source) <= eps
    ]


def sign_agreement(rows: Sequence[Record]) -> bool:
    signs = []
    for r in rows:
        if r.effect.delta_u > 0:
            signs.append(1)
        elif r.effect.delta_u < 0:
            signs.append(-1)
    return bool(signs) and all(s == signs[0] for s in signs)


def predicted(rows: Sequence[Record]) -> Optional[Effect]:
    if not rows:
        return None
    n = F(len(rows))
    du = sum((r.effect.delta_u for r in rows), F(0)) / n
    k = max((len(r.effect.violations) for r in rows), default=0)
    viol = []
    for j in range(k):
        s = F(0)
        for r in rows:
            v = r.effect.violations[j] if j < len(r.effect.violations) else F(0)
            s += v
        viol.append(s / n)
    return Effect(du, tuple(viol))


def certify(
    target: Fingerprint,
    skill: str,
    pool: Sequence[Record],
    *,
    eps: F,
    rho_min: F = F(1, 2),
    n_min: int = 1,
    tau: F = F(0),
) -> Certificate:
    compile_ok = skill in target.hooks
    rows = neighbors(target, pool, skill, eps)
    ov = max((overlap(target, r.source) for r in rows), default=F(0))
    pred = predicted(rows)
    return Certificate(
        compile_ok=compile_ok,
        overlap_ok=ov >= rho_min,
        n_eff_ok=len(rows) >= n_min,
        sign_agree=sign_agreement(rows),
        lcb_ok=pred is not None and pred.delta_u > tau,
        protected_ok=pred is not None and all(v <= 0 for v in pred.violations),
    )


def first_unconditional(rows: Sequence[Record]) -> Optional[Record]:
    """Illegal lowering: treat the compiled set as a ranked recipe list."""
    settled = [r for r in rows if r.settled]
    return settled[0] if settled else None


# ---------------------------------------------------------------------------
# Library
# ---------------------------------------------------------------------------

RIGID_1D = Fingerprint(j=(F(2),), hooks=("cfg",), support=("drift",))
CLOTH_1D = Fingerprint(j=(F(2),), hooks=("cfg", "next_force"), support=("drift",))
RIGID_2D = Fingerprint(j=(F(2), F(0)), hooks=("cfg",), support=("drift",))
CLOTH_2D = Fingerprint(j=(F(2), F(3)), hooks=("cfg", "next_force"), support=("drift",))
COSMOS = Fingerprint(j=(F(1), F(1)), hooks=("rep",), support=("struct",))
ARM = Fingerprint(j=(F(4),), hooks=("self_force",), support=("artic",))

# Same when/needs: Brief State cannot tell these cfg rows apart.
CFG_RIGID = Record("cfg", "repair", frozenset({"drift"}), RIGID_1D, Effect(F(3), (F(-1),)), True)
CFG_CLOTH = Record("cfg", "repair", frozenset({"drift"}), CLOTH_1D, Effect(F(-4), (F(-1),)), True)
NF_CLOTH = Record("next_force", "repair", frozenset({"drift"}), CLOTH_1D, Effect(F(5), (F(0),)), True)
CFG_RIGID_2D = Record("cfg", "repair", frozenset({"drift"}), RIGID_2D, Effect(F(3), (F(-1),)), True)
CFG_CLOTH_2D = Record("cfg", "repair", frozenset({"drift"}), CLOTH_2D, Effect(F(-4), (F(-1),)), True)
NF_CLOTH_2D = Record("next_force", "repair", frozenset({"drift"}), CLOTH_2D, Effect(F(5), (F(0),)), True)
TRAP = Record("pick_banana", "always", frozenset(), RIGID_1D, Effect(F(1), (F(0),)), True)
REP = Record("rep", "repair", frozenset({"struct"}), COSMOS, Effect(F(10), (F(3),)), True)
SCREEN = Record("self_force", "repair", frozenset({"artic"}), ARM, Effect(F(2), (F(0),)), False)

M: Tuple[Record, ...] = (
    TRAP,
    CFG_RIGID,
    CFG_CLOTH,
    NF_CLOTH,
    REP,
    SCREEN,
)

TRUE = {
    ("cloth", "cfg"): Effect(F(-4), (F(-1),)),
    ("cloth", "next_force"): Effect(F(5), (F(0),)),
    ("cloth", "pick_banana"): Effect(F(-8), (F(0),)),
    ("cosmos", "rep"): Effect(F(10), (F(3),)),
}


def apply_true(kind: str, skill: str) -> Effect:
    return TRUE[(kind, skill)]


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------

def test_1_same_m_two_executables() -> None:
    """AMMI dumps M. Compile keeps only settled repair+drift. Target IEM empty."""
    brief = BriefState("repair", {"drift"}, CLOTH_1D)
    ammi = inject_all(M)
    hyp = compile_hypotheses(M, brief)
    assert {r.skill for r in ammi} == {r.skill for r in M}
    assert {r.skill for r in hyp} == {"cfg", "next_force"}
    assert TRAP in ammi and TRAP not in hyp
    assert SCREEN in ammi and SCREEN not in hyp  # unsettled is not source
    target_iem: List[Record] = []
    assert target_iem == []
    print("1. Same M, two executables. Compile={cfg, next_force}; AMMI keeps trap+screen.")


def test_2_compile_is_not_a_claim() -> None:
    """when/needs compile still aliases rigid and cloth cfg. Injecting H hurts."""
    brief = BriefState("repair", {"drift"}, CLOTH_1D)
    hyp = compile_hypotheses(M, brief)
    cfgs = [r for r in hyp if r.skill == "cfg"]
    assert len(cfgs) == 2
    assert {r.effect.delta_u for r in cfgs} == {F(3), F(-4)}
    stolen = first_unconditional(cfgs)  # insertion order: rigid first
    assert stolen is CFG_RIGID
    got = apply_true("cloth", stolen.skill)
    assert got.delta_u < 0
    print("2. Compiled cfg set aliases +3 and −4. Unconditional first is rigid; cloth ΔU=−4.")


def test_3_certificate_is_the_second_compile() -> None:
    """Certificate over the compiled set abstains on sign disagreement."""
    brief = BriefState("repair", {"drift"}, CLOTH_1D)
    hyp = compile_hypotheses(M, brief)
    cert_cfg = certify(brief.fingerprint, "cfg", hyp, eps=F(0))
    assert not cert_cfg.sign_agree
    assert not cert_cfg.pass_()
    cert_nf = certify(brief.fingerprint, "next_force", hyp, eps=F(0))
    # next_force has one 1-D neighbor (cloth); LCB +5, protected ok
    assert cert_nf.pass_()
    assert apply_true("cloth", "next_force").accepted()
    print("3. Certificate abstains on cfg (sign split). next_force licenses a trial.")


def test_4_fold_stales_the_hypothesis_set() -> None:
    """Fold beliefs off drift onto struct. Stale H still offers cfg; recompile does not."""
    brief = BriefState("repair", {"drift"}, CLOTH_1D)
    stale = compile_hypotheses(M, brief)
    brief.fold(new_beliefs=frozenset({"struct"}))
    brief.beliefs.discard("drift")
    now = compile_hypotheses(M, brief)
    assert {r.skill for r in stale} == {"cfg", "next_force"}
    assert {r.skill for r in now} == {"rep"}
    assert stale != now
    print("4. Fold drift→struct. Stale H={cfg, next_force}; recompile={rep}.")


def test_5_chart_fold_splits_the_alias() -> None:
    """Fingerprint Fold (new probe) is a compile against a new chart."""
    m2 = (CFG_RIGID_2D, CFG_CLOTH_2D, NF_CLOTH_2D)
    brief = BriefState("repair", {"drift"}, CLOTH_2D)
    hyp = compile_hypotheses(m2, brief)
    # when/needs still selects both cfg rows
    assert sum(1 for r in hyp if r.skill == "cfg") == 2
    cert_cfg = certify(brief.fingerprint, "cfg", hyp, eps=F(0))
    # 2-D: only cloth cfg is a neighbor; its ΔU is −4 so LCB fails
    assert cert_cfg.sign_agree and not cert_cfg.lcb_ok
    cert_nf = certify(brief.fingerprint, "next_force", hyp, eps=F(0))
    assert cert_nf.pass_()
    print("5. Chart Fold: 2-D neighbor of cfg is only cloth (−4). next_force still certifies.")


def test_6_protected_survives_compile() -> None:
    """Compile selects rep. Scalar 7 would pass. Certificate keeps the vector."""
    brief = BriefState("repair", {"struct"}, COSMOS)
    hyp = compile_hypotheses(M, brief)
    assert tuple(r.skill for r in hyp) == ("rep",)
    e = hyp[0].effect
    assert e.scalar_average() == F(7)
    assert not e.accepted(F(1))
    cert = certify(brief.fingerprint, "rep", hyp, eps=F(0), tau=F(1))
    assert cert.lcb_ok and not cert.protected_ok
    assert not cert.pass_()
    assert not apply_true("cosmos", "rep").accepted(F(1))
    print("6. Compiled rep is a scalar win and a vector fail. Certificate refuses.")


def test_7_empty_compile_cannot_mint_a_trial() -> None:
    """Idle brief: noaction. Certificate on a missing skill cannot pass."""
    brief = BriefState("idle", {"drift"}, CLOTH_1D)
    hyp = compile_hypotheses(M, brief)
    assert hyp == ()
    cert = certify(brief.fingerprint, "cfg", hyp, eps=F(0))
    assert not cert.n_eff_ok and not cert.pass_()
    print("7. Empty compile is noaction. No certificate over ∅ licenses a trial.")


def main() -> None:
    tests = [
        test_1_same_m_two_executables,
        test_2_compile_is_not_a_claim,
        test_3_certificate_is_the_second_compile,
        test_4_fold_stales_the_hypothesis_set,
        test_5_chart_fold_splits_the_alias,
        test_6_protected_survives_compile,
        test_7_empty_compile_cannot_mint_a_trial,
    ]
    for t in tests:
        t()
    print(f"\n{len(tests)}/{len(tests)} passed.")


if __name__ == "__main__":
    main()
