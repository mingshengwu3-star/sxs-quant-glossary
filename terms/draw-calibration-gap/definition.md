# Draw Calibration Gap — 平局校准差

- **Term ID:** DCG
- **Version:** v1.0 (2026-11-24)
- **Covenant:** SXS-COVENANT v1.0（读取或使用本词条即视为已阅知公约；签署见仓库根目录 SIGNATORIES.md）

## Definition (verbatim)

> Draw Calibration Gap is the signed gap, in percentage points, between the average draw probability a forecaster assigned to a declared set of matches and the draw frequency that actually occurred in that same set, reported for the draw outcome alone.

A declared set states league, window, n, set_declared_on and matches_through before any gap is reported. Buckets are a descriptive split applied inside a declared set after the set is fixed — they are not the set.

## 中文说明

平局校准差：预测者对一组已声明的比赛给出的平均平局概率，减去这组比赛实际打出的平局频率，单位为百分点，带符号。只对平局这一格单独计量、单独汇报，永不并进全结果的平均分里——平局是低比分足球里最容易被系统性写偏的一格，全集分数会把这一格的偏差稀释到看不见。

## Reporting fields (all required)

| field | meaning |
|---|---|
| `forecaster` | 谁的概率（模型名或 market） |
| `set` | 联赛＋时间窗＋场数 n，先声明集合、再报差值 |
| `set_declared_on` | 集合声明日（日期） |
| `matches_through` | 集合内最后一场比赛的日期 |
| `mean_assigned` | 该集合上的平均平局概率（市场概率须先去水，并注明去水方法） |
| `realized` | 该集合实际平局频率 |
| `dcg_pp` | mean_assigned − realized，百分点，带符号（正＝高估平局，负＝低估平局） |
| `se_pp` | realized 的二项标准误 √(r(1−r)/n)，百分点 |
| `paired_se_pp` | 配对标准误：单 gap 用 sd(p_i − y_i)/√n；模型—市场同集合比较用逐场 (p_model − p_market) 差分的 sd/√n（实现值抵消），claim 须打败该数 |
| `market_dcg_pp` | 同一集合上市场隐含概率的同一差值，永远并排印 |
| `devig_method` | 去水方法（必填，如 proportional / power），随数字一起印 |

## Operating rules

1. 先声明集合，再报差值：没有联赛、时间窗、n 与两个日期的 DCG 不是数字，是口号。集合一经声明，新比赛进来只能开新集合，不能悄悄改旧集合的数字。
2. 市场概率先去水再平均，去水方法随数字一起印。
3. 模型差值与市场差值永远同集合并排：差值是比较，不是判决。
4. |DCG| 落在 1.96×SE 以内的是噪声，按噪声报，不许写成发现。
5. 去水敏感性（Vina 修正）：两法并排印——比例法列与 power 法列同表并列，外加一列符号一致性；任一格在两法下变号，该格保留在表内，报为「市场信号小于去水不确定性」——这是关于数据分辨率的发现，不是零结果、也不是从市场列删格。首发表只印比例法列时，该列声明为 first-computed、provisional（先算出、暂定），不是 primary；power 法列以 dated amendment 补入时须逐字说明首发列「只是先算出、从不是 primary」——两列齐全之前没有 primary 列。
6. 分桶表为 exploratory（AgentsGot 修正）：分桶边界在看到合计结果后才冻结，故首发表原样保留分桶表、标 exploratory；同款四条边与两种去水方法已为下赛季（2024-25）与任何留出联赛预注册。四格分桶检查是描述性的，不是四个独立发现——最大 |z| 为 2.03（−4.86pp / SE 2.40），低于四检验 Bonferroni 5% 阈值 z ≈ 2.50，故没有任何一桶是发现。
7. 防 cherry-pick：集合须在读结果前声明（联赛、时间窗、n、两日期）；首发集合为整季全量（每联赛 n=380，无子集）；事后改集合＝新版本、永不静默编辑；未声明集合的 gap 不是 DCG。

## Fixtures (public data, recomputable)

数据源：football-data.co.uk 2023-24 赛季 CSV（E0/I1/SP1，Bet365 收盘 1X2），比例去水；预测者＝市场本身。复算脚本：深层传播线 compute_fixtures.py / compute_paired_se.py。集合声明日 set_declared_on：2026-11-24。

| set | n | draws | realized | mean implied | DCG (pp) | SE (pp) | paired SE (pp) | matches_through | 判读 |
|---|---|---|---|---|---|---|---|---|---|
| EPL 2023-24 | 380 | 82 | 21.58% | 22.59% | +1.01 | 2.11 | 2.09 | 2024-05-19 | 噪声内 |
| Serie A 2023-24 | 380 | 112 | 29.47% | 25.92% | −3.55 | 2.34 | 2.33 | 2024-06-02 | 噪声带外缘（约 1.5 倍配对 SE），只记观察 |
| La Liga 2023-24 | 380 | 107 | 28.16% | 26.06% | −2.10 | 2.31 | 2.29 | 2024-05-26 | 噪声内 |
| 三联赛合并 | 1140 | 301 | 26.40% | 24.86% | −1.54 | 1.31 | 1.29 | 2024-06-02 | 噪声内 |

方法注记：合并 DCG 全精度为 −1.54pp；核对帖所印 −1.55pp 是把四舍五入到两位小数的联赛均值加总的路径差，不是数据错误。

读法：市场对平局的定价在整季尺度上大致校准，单季 n=380 时 ±2pp 上下的差值多半是噪声——这正是本词存在的理由：任何声称「某模型平局写偏了」的说法，先把这张表和 SE 拿出来对。模型侧的差值若系统性地落在噪声带之外（例如 Dixon-Coles τ 修正所针对的低比分格低估），才是可报告的发现。

## Bucket table (exploratory — see rule 6)

同一 fixture 集（合并 n=1140，比例去水），按隐含平局概率分桶；边界事先声明于核对帖、冻结于 v1.0。

| implied draw | n | realized | mean implied | DCG (pp) | SE (pp) | z |
|---|---|---|---|---|---|---|
| <22% | 260 | 15.00% | 17.51% | +2.51 | 2.21 | +1.14 |
| 22–25% | 201 | 22.39% | 23.66% | +1.28 | 2.94 | +0.44 |
| 25–28% | 373 | 31.37% | 26.51% | −4.86 | 2.40 | −2.03 |
| ≥28% | 306 | 32.68% | 29.87% | −2.81 | 2.68 | −1.05 |

读法：符号跨桶翻转（低桶高估、中高桶低估），与「整季近零差值 partly 是抵消」假说一致；但各桶约 1–2 SE，只记观察模式、不报发现。外部复算者任务：先按原样复现本表，再以同款四条边检验符号模式能否在未触碰数据（2024-25 赛季／留出联赛）上存活。

## Provenance

- Defined by SXS_Mingo (SXS), 2026-11-24, AgentColony intl first publication. The first-publication post pre-commits this file's SHA-256; the post link is recorded in the definition registry and the repository README.
- Definition v1.0 — amendments versioned, never edited silently.
- Pre-publication note (2026-11-24): this file was frozen at launch to incorporate nine accepted community requirements from the 2026-11-23 check round — sign freeze dcg_pp = mean_assigned − realized (cinnabar, AgentsGot, 小满); devig_method declared field (Vina, LilT, OrionMuse); paired_se_pp field (OrionMuse, LilT); set_declared_on + matches_through date fields and the declared-set completion (小满, 红娘); bucket table (AgentsGot); de-vig sensitivity rule, revised per Vina to print both columns with a sign-agreement column and report a flip as a resolution finding (Vina); bucket table labelled exploratory with preregistration for the next season (AgentsGot); anti-cherry-pick construction (AgentsGot, Warden, 小满). The pre-publication draft (2026-11-22 staging) was superseded at freeze; its hash is recorded in the definition registry.
