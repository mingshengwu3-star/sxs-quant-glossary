# DCG paired-SE + bucket computation — same inputs as compute_fixtures.py
# (football-data.co.uk 2023-24 CSVs E0/I1/SP1, Bet365 closing 1X2, proportional de-vig).
# Recompute: curl -sL -o E0.csv https://www.football-data.co.uk/mmz4281/2324/E0.csv
# (same pattern for I1, SP1), then run this file in that directory.
# Verified 2026-11-23 evening round: per-league DCG/SE reproduce the check post exactly
# (EPL +1.01/SE 2.11, Serie A -3.55/2.34, La Liga -2.10/2.31).
# Combined DCG from full precision is -1.54pp (check post printed -1.55pp: the 0.01pp
# gap is a rounding path — summing the 2dp-rounded league means — not a data error.
# Launch round: use the full-precision -1.54pp with a method note.)
import csv, math

def load(code):
    rows = list(csv.DictReader(open(f'{code}.csv', encoding='utf-8-sig')))
    ds = []
    for r in rows:
        try:
            oh, od, oa = float(r['B365H']), float(r['B365D']), float(r['B365A'])
        except (KeyError, ValueError, TypeError):
            continue
        inv = [1/oh, 1/od, 1/oa]
        p = inv[1]/sum(inv)
        ds.append((p, 1 if r['FTR'] == 'D' else 0))
    return ds

def report(ds, name):
    n = len(ds)
    rate = sum(y for _, y in ds)/n
    mean = sum(p for p, _ in ds)/n
    se = math.sqrt(rate*(1-rate)/n)
    diffs = [p-y for p, y in ds]
    md = sum(diffs)/n
    pse = math.sqrt(sum((d-md)**2 for d in diffs)/(n-1)/n)
    print(f'{name}: n={n} realized={rate:.4f} implied={mean:.4f} '
          f'DCG={100*(mean-rate):+.2f}pp SE_indep={100*se:.2f}pp paired_SE={100*pse:.2f}pp')

all_ds = []
for code, name in [('E0', 'EPL'), ('I1', 'Serie A'), ('SP1', 'La Liga')]:
    ds = load(code)
    report(ds, name)
    all_ds += ds
report(all_ds, 'COMBINED')

# Buckets by implied draw probability — boundaries declared 2026-11-23 evening round,
# frozen for the v1.0 launch table. Do not move them after seeing results.
for lo, hi, label in [(0, 0.22, '<22%'), (0.22, 0.25, '22-25%'),
                      (0.25, 0.28, '25-28%'), (0.28, 1, '>=28%')]:
    b = [(p, y) for p, y in all_ds if lo <= p < hi]
    nb = len(b)
    if not nb:
        print(f'bucket {label}: n=0')
        continue
    rb = sum(y for _, y in b)/nb
    mb = sum(p for p, _ in b)/nb
    seb = math.sqrt(rb*(1-rb)/nb)
    print(f'bucket {label}: n={nb} realized={rb:.4f} implied={mb:.4f} '
          f'DCG={100*(mb-rb):+.2f}pp SE={100*seb:.2f}pp')
