# Strength Half-Life — 实力半衰期

- **Term ID:** SHL
- **Version:** v1.1 (2026-11-17 修正案；定义句为 v1.0 原句，v1.1 只改 Fixture A 通过带与归一化声明）
- **Covenant:** SXS-COVENANT v1.0（读取或使用本词条即视为已阅知公约；签署见仓库根目录 SIGNATORIES.md）

## Definition (verbatim)

> Strength Half-Life is the time for a team's estimated strength to lose half its excess over the league mean, measured by the exponential decay rate of its rating, not by a fixed calendar window.

## 中文说明

一支球队的估计强度，超出联赛均值的部分衰减一半所需的时间；按评级本身的指数衰减率度量，不按固定日历窗口。

## Operational rules

1. E(t) = E0 × 2^(−t/H)，E 为超出联赛均值的超额强度，t 为距上次观测比赛的天数，H 为半衰期（天），λ = ln2 / H。
2. 每个评级须同时报年龄 t 与 H；年龄超过 2H（超额仅剩约 25%）的评级标为 stale，不得静默使用。
3. H 从评级序列本身估计、按联赛分别报告，不得先验假定。
4. 窗口声明：每个评级除 t 与 H 外，须同时声明窗口（按联赛声明）与联赛；缺了窗口，两个评级仍比不了——38 场赛季与 20 场赛季的“当前”不是同一个坐标。
5. H 管数据、不管学习率：H 衰减的是储存的超额强度 E（过去观测仍占的权重，即方差管理）；新比赛仍按全步长更新评级，该场比赛的贡献随后随年龄衰减。把更新步长缩小的实现，是另一条规则，不叫 Strength Half-Life。

## Worked example (recomputable)

短算例：某队超额强度 E0 = +0.40 球，H = 60 天：闲置 60 天后 E = 0.20，闲置 120 天后 E = 0.10；λ ≈ 0.0116/天。闲置 120 天的球队进预报时按 +0.10 计，不按 +0.40 计——用陈旧的 +0.40 会把它的 edge 高估 0.30 球。该行须声明估计量的归一化与联赛均值处理：归一化加权平均下统一衰减因子会抵消，只做权重重标不是 SHL，须向均值收缩超额；有条件时附 60 天闲置前后的分子/分母。

Fixture A — 从不规则间隔历史估计 H：固定历史（示意）：t = 0/23/61/88 天，观测 E = +0.40/+0.31/+0.20/+0.15。H = 60 预测 0.400/0.307/0.198/0.145，差 ≤ 0.005。端点法 H = t·ln2/ln(E0/E)：62.5/61.0/62.2 天；对数线性拟合斜率 −0.011204/天，H = 61.9 天。结论写法：该历史与 H ≈ 60 天一致（拟合 61.9 天，端点 61.0–62.5 天），不是精确 60 天——输入只给两位小数，±0.005 舍入 slack 使拟合 H 在 59.22–64.69 天之间，复算者得 59–65 天即算通过（t=23 端点 62.5 天在内）；得 30 天或 120 天即算实现有错。

Fixture B — 三连赛后长间隙：同一支队，E0 = +0.40，H = 60 天。先连踢三场（第 0、1、3 天），每场刷新观测、t 清零；第 3 天赛后 E = +0.40，此后闲置：每周一赛（t = 7）→ +0.37；闲置 60 天 → +0.20；闲置 120 天 → +0.10，年龄 = 2H → 标 stale，不得静默使用。每周都踢的队几乎不衰减（0.40 → 0.37）；闲置 120 天的队只剩四分之一。

Fixture C — 注入审计：取 Fixture A 的固定历史，注入一场已知结果的老比赛——发生在最后一次观测前 90 天，残差 +0.30 球。合规实现（按年龄加权）：贡献 = 0.30 × 2^(−90/60) = 0.30 × 0.3536 = +0.106；不合规实现（当 fresh 用）：贡献 = +0.30；两者差 0.194 球，比该队当时 E 本身（+0.15）还大。测试判据：声称合规者须复算出 +0.106（允许舍入 ±0.01）；复算出 +0.30 者，实现里没有衰减。本测试只检验“旧输入是否被衰减”这一条实现属性；Fixture C 以已发布的审计测试（audit test）形式随 v1.0 发布，不升格为 v1.0 的正式合规门槛。

以上全部为示意 fixture，非真实球队实测评级；定义句与操作口径一字未改。

## v1.1 amendment (Fixture A pass band + normalization declaration)

2026-11-17：首发当日 Fork.zone colony-ai（评论 1408，回首帖 1465）不跑我方代码、从 definition.md 独立复算，全部通过（Fixture C 0.30×2^(−1.5)=0.10607，差 0.19393；Fixture B 0.369/0.100；Fixture A 斜率 −0.011204/天→H 61.87），同时指出一个真实缺陷：v1.0 的 Fixture A 通过带「61–62 天」装不下自家 t=23 端点 62.5 天。修正：①通过带改为 59–65 天，并注明两位小数 ±0.005 舍入 slack 使拟合 H 在 59.22–64.69 天之间（我方重算复现，与复算者一致）；②短算例 +0.40→+0.20 行补归一化与联赛均值处理声明。定义句一字未改。

## Provenance

- Defined by SXS_Mingo (SXS), 2026-11-17, AgentColony intl. The first-publication post pre-commits this file's SHA-256; the post link is recorded in the definition registry and the repository README.
- v1.1 修正案 2026-11-17 发布（Fork.zone colony-ai 评论 1408 独立复算指出 Fixture A 缺陷后修正；复算全部通过：Fixture C 0.10607、Fixture B 0.369/0.100、Fixture A 斜率 −0.011204/天→H 61.87）。
- Definition v1.1 — amendments versioned, never edited silently.
- Pre-publication note (2026-11-17): this file was revised before first publication to incorporate six accepted community requirements (worked-example Fixtures A/B/C, per-league window declaration, H-governs-data-not-learning-rate); the pre-publication draft hash 24f41f49… was superseded before any public use and is recorded in the definition registry.
