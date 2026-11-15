#!/usr/bin/env python3
"""
Kelly Crossover T* — reproduction script (SXS-COVENANT v1.0 applies).

Model: even-money bets (win pays 1:1). Each round, bet fraction f of bankroll.
Win (prob p): bankroll *= (1 + f). Lose: bankroll *= (1 - f).
Full Kelly fraction for even-money at win prob p is f* = 2p - 1;
"half Kelly" is f*/2. (Betting f = 1.0 is NOT Kelly; it is ruin-on-first-loss.)

Computes, for each round T, by exact binomial lattice DP:
  - first-passage hitting probability: P(bankroll reached >= target at or before T)
  - endpoint probability:             P(bankroll at exactly T >= target)

Reference case: p = 0.55, target = 2.0, full f=0.10 vs half f=0.05.
Published v1.1 reference values: first-passage crossover ~513 rounds with a
near-tie band 508-512; closed-form endpoint T_cross = 277 vs measured ~300;
full Kelly's own hitting probability at the crossover ~0.661.
Report both ledgers separately (v1.1 discipline): endpoint and first-passage
give different answers and must not be mixed.
"""
import numpy as np
from math import comb, log

P = 0.55
TARGET = 2.0
T_MAX = 600
F_FULL = 2 * P - 1          # 0.10
F_HALF = F_FULL / 2         # 0.05


def hit_curve(f: float, t_max: int = T_MAX):
    """First-passage hitting probability curve via lattice DP with absorption."""
    log_target = log(TARGET)
    lw, ll = log(1 + f), log(1 - f)
    state = {(0, 0): 1.0}
    hit = 0.0
    curve = np.zeros(t_max + 1)
    for t in range(t_max):
        new = {}
        for (w, l), mass in state.items():
            # win
            if (w + 1) * lw + l * ll >= log_target:
                hit += mass * P
            else:
                new[(w + 1, l)] = new.get((w + 1, l), 0.0) + mass * P
            # lose
            if w * lw + (l + 1) * ll >= log_target:
                hit += mass * (1 - P)
            else:
                new[(w, l + 1)] = new.get((w, l + 1), 0.0) + mass * (1 - P)
        state = new
        curve[t + 1] = hit
    return curve


def endpoint_curve(f: float, t_max: int = T_MAX):
    """P(bankroll_T >= target) from the plain binomial distribution."""
    log_target = log(TARGET)
    lw, ll = log(1 + f), log(1 - f)
    out = np.zeros(t_max + 1)
    for t in range(t_max + 1):
        s = 0.0
        for w in range(t + 1):
            if w * lw + (t - w) * ll >= log_target:
                s += comb(t, w) * (P ** w) * ((1 - P) ** (t - w))
        out[t] = s
    return out


def first_cross(low, high):
    for t in range(1, len(low)):
        if low[t] > high[t]:
            return t
    return None


if __name__ == "__main__":
    hf_full = hit_curve(F_FULL)
    hf_half = hit_curve(F_HALF)
    ep_full = endpoint_curve(F_FULL)
    ep_half = endpoint_curve(F_HALF)

    t_star = first_cross(hf_half, hf_full)
    t_end = first_cross(ep_half, ep_full)
    print(f"p={P}, target={TARGET}x, even-money; full f={F_FULL:.2f}, half f={F_HALF:.2f}")
    print(f"First-passage: half first overtakes full at T* = {t_star}")
    if t_star:
        print(f"  hitting probs at T*: full={hf_full[t_star]:.4f}  half={hf_half[t_star]:.4f}")
    print(f"First-passage hitting at T=500: full={hf_full[500]:.4f}  half={hf_half[500]:.4f}")
    print(f"Endpoint:      half first overtakes full at T  = {t_end}")
    print(f"Endpoint prob at T=500:         full={ep_full[500]:.4f}  half={ep_half[500]:.4f}")
