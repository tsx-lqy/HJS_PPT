# HJS_PPT

让 AI 把科研内容讲清楚：图示承担结构，短句解释机制，证据支持结论。

一个可以修改和组合的科研 PPT skill，适用于论文汇报、实验室组会、系统设计、复试答辩和研究计划。保留你自己的模板，支持中文和英文。

<img src="docs/images/hajizhe-avatar.jpg" width="220" alt="哈基折">

**哈基折**

[English](README.en.md) · [安装](#安装) · [用途与例子](skills/hjs_ppt/references/usage-examples.md) · [15 种版式](skills/hjs_ppt/references/layouts.md) · [制作流程](skills/hjs_ppt/references/production.md)

## 安装

使用 [Skills CLI](https://github.com/vercel-labs/skills) 安装，需要 Node.js 和 Git：

```bash
npx skills@latest add tsx-lqy/skill --skill hjs_ppt
```

按提示选择你的 AI 工具和安装方式。默认安装到当前项目；添加 `-g` 可安装为用户级 skill。

<details>
<summary>直接安装到 Codex 或 Claude Code</summary>

Codex：

```bash
npx skills@latest add tsx-lqy/skill --skill hjs_ppt -a codex -g --copy
```

Claude Code：

```bash
npx skills@latest add tsx-lqy/skill --skill hjs_ppt -a claude-code -g --copy
```

`--copy` 使用普通文件复制，适合不方便创建符号链接的环境。安装后打开新会话，或按 AI 工具的提示刷新技能列表。

</details>

<details>
<summary>下载 ZIP 后手动安装</summary>

1. [下载仓库 ZIP](https://github.com/tsx-lqy/skill/archive/refs/heads/main.zip) 并解压。
2. 将 `skills/hjs_ppt` **整个文件夹**复制到你的工具的 skills 目录，不要只复制 `SKILL.md`。
3. Codex 可使用用户级 `~/.agents/skills/`；Claude Code 可使用 `~/.claude/skills/`。其他工具的目录参见 [Skills CLI 支持列表](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)。
4. 若已有同名 skill，先保留自己的修改，再选择替换或合并。不要同时安装多份同名 skill。

Windows 的 `~` 表示当前用户目录。

</details>

更新安装的 skill：

```bash
npx skills@latest update
```

更新可能覆盖本地编辑过的 skill，先保存自己的修改。

## 从旧名称迁移

本 skill 已从 `scu-ppt-body-style` 更名为 **`hjs_ppt`**。请执行上面的新安装命令，备份并移出旧的同名功能目录，避免同时加载两份；仅运行更新命令不保证完成名称迁移。新调用名是 `$hjs_ppt`。

名称按维护者指定保留下划线，已验证 Skills CLI 的实际发现与安装；仅接受连字符的严格 Agent Skills 命名校验器会报告不兼容，不能把本仓库校验通过理解为所有客户端均支持该名称。

## 开始使用

在 Codex 中显式调用：

```text
使用 $hjs_ppt，把这篇论文整理为 8 页中文组会 PPT。
保留我提供的蓝色模板，重点解释方法、实验对比和局限。
```

也可以直接告诉支持 skills 的 AI 工具：

```text
使用 hjs_ppt 重排这份汇报的内容页。
保持现有页数、封面和页眉页脚，让图、公式和结论之间的关系更清楚。
```

提供研究材料、已有图表，以及需要沿用的模板。这个 skill 提供内容组织、主体风格及材料整理、公式图表、逐页讲稿、渲染检查四类制作流程，并附独立的 PPTX 检查和 Windows PowerPoint 导图脚本。生成和编辑 `.pptx` 仍需要 AI 工具具备相应能力；安装 skill 不会额外安装 PowerPoint、MathType 或 PPT Master。

## 排版能解决什么问题

| 你的内容 | 可以采用的方式 | 作用 |
|---|---|---|
| 抽象公式或矩阵 | 输入 → 小算例 → 过程 → 公式 | 让变量与实际操作对应 |
| 单篇论文讲解 | 来源 → 核心机制 → 实验图 → 局限 | 让结论找到证据 |
| 多种技术路线 | 方案 × 收益 / 代价 | 按同一需求解释选择 |
| 方法演进或发展史 | 连续时间线 + 当前节点 | 跨页保持参照，避免每页重新找重点 |

例如，讲样本标准差时，先给出明确标注的教学数据 2、3、4，再展示偏差和公式，最后说明它描述样本离散。完整调用提示、约 40 秒讲稿、文献页与方案取舍例子见 [排版用途说明与示例](skills/hjs_ppt/references/usage-examples.md)。

![从具体算例到公式](skills/hjs_ppt/references/images/10-worked-principle.svg)

## 基础制作能力

- **材料整理**：来源页码、图号、数据、条件与结论对应；可提取已有 PPTX 的文字和备注。
- **MathType 公式与可编辑图表**：所有公式必须使用 MathType，并在保存后的 PPTX 中可重新用 MathType 编辑；图表优先使用原生对象，保留公式源、变量和数据。不能用 Office Math、普通文本或纯图片公式替代。缺少 MathType 时明确报告未完成项，见 [规则与例子](skills/hjs_ppt/references/mathtype.md)。
- **逐页讲稿**：按最终页序讲“看哪里、如何解释、还有什么限制”，写入备注或交付对应 Markdown。
- **渲染检查**：检查 PPTX 内部关系和对象，实际渲染后逐页看遮挡、小字、公式、图例及模板边界。

可与 [PPT Master](https://github.com/hugohe3/ppt-master) 配合进行材料转换和原生导出，主体排版由本 skill 决定。具体分工、已核对的接口及依赖见 [接入说明](skills/hjs_ppt/references/ppt-master-integration.md)。不捆绑上游引擎；本次没有整合动画、配音或视频。

## 为什么需要它

**图很多，却不知道先看哪里。** 先安排主图、编号解释和阅读顺序，再放辅助文字。

**公式放上去了，却没有讲清作用。** 将变量、图中模块和状态变化对应起来。

**结果很好看，却缺少证据链。** 将整体图、相同 ROI、测量曲线和指标按同一比较口径组织。

**换了模板，内容就失去层级。** 把主体结构与封面、校徽、页眉页脚分开，在指定模板内应用规则。

## Skill 索引

| Skill | 用途 | 包含内容 |
|---|---|---|
| [hjs_ppt](skills/hjs_ppt/SKILL.md) | 科研 PPT 主体组织与基础制作 | 字体配色、汇报节奏、15 种版式、原创 SVG、用途与例子、四类制作流程、检查脚本 |

十五种版式：系统总览、主图与公式、系统逐步拆解、结果与指标、多方法矩阵、双方案对比、闭环讲解、并列机制、文献与证据、具体算例、方案取舍、连续时间线、个人贡献与证据、研究版图、研究任务与阶段成果。

![主图与公式的主体组织示意](skills/hjs_ppt/references/images/06-concept-and-equation.svg)

## 内容与来源

风格规则来自六份去重科研汇报、共 133 页的观察与重新整理，最新加入 23 页复试与研究计划汇报；重复提供的 COME 只计一次。页数含封面和附录，提炼对象为主体内容。公开版只分发规则、原创示意、教学例子和独立脚本，不包含原始 PPT、论文截图、实验图像、机构标识或作者本机路径。项目名称不表示四川大学或原稿涉及机构的官方发布或背书。详细口径见 [提炼依据](skills/hjs_ppt/references/design-notes.md)。

仓库的简洁介绍、安装入口和技能索引组织方式参考了 [mattpocock/skills](https://github.com/mattpocock/skills)。本仓库的科研主体风格内容独立整理，未复制其技能正文。

## 维护与贡献

发现问题时，可提交 Issue，注明使用的 AI 工具、输入材料类型、预期和实际结果。提交示例前请移除不适合公开的内容。

修改后运行：

```bash
python scripts/validate_skills.py
python -B -m unittest discover -s tests
```

该检查验证目录、元数据、相对链接、SVG 和公开包文件范围；实际成片质量仍需渲染和人工检查。

## 许可证

[MIT](LICENSE)。适用于本仓库发布的规则、文档、校验脚本及原创 SVG 示意，不授予任何未随仓库发布的原稿、论文图像、字体或商标权利。
