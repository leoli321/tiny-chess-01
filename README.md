# tiny-chess-01

8x8 international chess UCI engine in a single Python file, for
make.fun bounty tiny-chess-01 ("Build the strongest chess engine in
4 KB of Python").

- `main.py` — the engine, 3,814 bytes, under the 4,096-byte limit.
- Deterministic: fixed 40,000-node search, no clock, no randomness.
- perft 1-4 verified: 20 / 400 / 8902 / 197281.
- UCI: `uci`, `isready`, `position startpos moves ...`, `go`, `quit`.

This is the original engine as uploaded by Sato. A larger optimized
version (17,919 bytes, clock-based time control) exists in local
workspace only — it is NOT this entry: it exceeds 4,096 bytes and
its clock-based search breaks the bounty determinism rule.
