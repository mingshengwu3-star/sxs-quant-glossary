# 约定 1 · 修正日志（Correction Log）

适用：任何已发布数字、定义、结论的事后修正。原则：**修正只发新版，永不静默改旧版。**

每条修正记录必填字段：

| field | meaning |
|---|---|
| `item` | 被修正的对象（词条/数字/帖子，附链接） |
| `old_value` / `new_value` | 修正前后的值 |
| `reason` | 为什么错（口径、端点、样本、计算） |
| `discovered_by` | 谁发现的（自己/他方署名） |
| `scope` | 影响范围：哪些下游结论受影响 |
| `threshold_set_by` | 相关阈值由谁设定（DSS 第五字段纪律） |
| `version_stamp` | 修正后版本号与日期 |

样例：T* v1.1——端点计数与首达计数在 500 轮给出相反答案；旧报法只报单点，新报法两本账分开、交叉只给区间。发现者：OrionMuse、IsiosParea、Jamir 三方独立指出。
