# Compile the certificate

Tiny, exact (rationals) join of Ding et al., *MemCompiler: Compile,
Don’t Inject* (arXiv:2605.07594) and Wu, Nie et al., *VERDI:
Retrieval Is Not Transfer* (arXiv:2608.09537).

A compile is a hypothesis set. A certificate licenses a trial on
this fingerprint. Injecting the compiled set is still inject.

```
python3 experiment.py
```

Last run: **7/7 passed**. Python 3.10+, stdlib + `fractions` only.
No GPU, no network, no model API.

MIT License. See DESCRIPTION.md for the claim, what would falsify it,
and the keepers from that run.

Also: [compile-dont-inject](https://github.com/StarDust-zz/compile-dont-inject),
[retrieval-is-not-transfer](https://github.com/StarDust-zz/retrieval-is-not-transfer).
