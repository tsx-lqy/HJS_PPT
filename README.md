# Skills for Research Presentations

让 AI 把科研内容讲清楚：图示承担结构，短句解释机制，证据支持结论。

一组小而独立、可以修改和组合的 Agent Skills。当前收录一个科研 PPT 主体风格 skill，适用于论文汇报、实验室组会和系统设计讲解。保留你自己的模板，也支持中文和英文内容。

[English](README.en.md) · [安装](#安装) · [Skill 索引](#skill-索引) · [版式配方](skills/scu-ppt-body-style/references/layouts.md)

## 安装

使用 [Skills CLI](https://github.com/vercel-labs/skills) 安装，需要 Node.js 和 Git：

```bash
npx skills@latest add tsx-lqy/skill --skill scu-ppt-body-style
```

按提示选择你的 AI 工具和安装方式。默认安装到当前项目；添加 `-g` 可安装为用户级 skill。

<details>
<summary>直接安装到 Codex 或 Claude Code</summary>

Codex：

```bash
npx skills@latest add tsx-lqy/skill --skill scu-ppt-body-style -a codex -g --copy
```

Claude Code：

```bash
npx skills@latest add tsx-lqy/skill --skill scu-ppt-body-style -a claude-code -g --copy
```

`--copy` 使用普通文件复制，适合不方便创建符号链接的环境。安装后打开新会话，或按 AI 工具的提示刷新技能列表。

</details>

<details>
<summary>下载 ZIP 后手动安装</summary>

1. [下载仓库 ZIP](https://github.com/tsx-lqy/skill/archive/refs/heads/main.zip) 并解压。
2. 将 `skills/scu-ppt-body-style` **整个文件夹**复制到你的工具的 skills 目录，不要只复制 `SKILL.md`。
3. Codex 可使用用户级 `~/.agents/skills/`；Claude Code 可使用 `~/.claude/skills/`。其他工具的目录参见 [Skills CLI 支持列表](https://github.com/vercel-labs/skills/blob/main/docs/agents.md)。
4. 若已有同名 skill，先保留自己的修改，再选择替换或合并。不要同时安装多份同名 skill。

Windows 的 `~` 表示当前用户目录。

</details>

更新安装的 skill：

```bash
npx skills@latest update
```

更新可能覆盖本地编辑过的 skill，先保存自己的修改。

## 开始使用

在 Codex 中显式调用：

```text
使用 $scu-ppt-body-style，把这篇论文整理为 8 页中文组会 PPT。
保留我提供的蓝色模板，重点解释方法、实验对比和局限。
```

也可以直接告诉支持 skills 的 AI 工具：

```text
使用 scu-ppt-body-style 重排这份汇报的内容页。
保持现有页数、封面和页眉页脚，让图、公式和结论之间的关系更清楚。
```

提供研究材料、已有图表，以及需要沿用的模板。这个 skill 负责内容组织和视觉规则；生成、编辑及渲染 `.pptx` 仍需要 AI 工具具备相应文件处理能力。仅安装 skill 不会额外安装 PowerPoint，也不会自动生成演示文稿。

## 为什么需要它

**图很多，却不知道先看哪里。** 先安排主图、编号解释和阅读顺序，再放辅助文字。

**公式放上去了，却没有讲清作用。** 将变量、图中模块和状态变化对应起来。

**结果很好看，却缺少证据链。** 将整体图、相同 ROI、测量曲线和指标按同一比较口径组织。

**换了模板，内容就失去层级。** 把主体结构与封面、校徽、页眉页脚分开，在指定模板内应用规则。

## Skill 索引

| Skill | 用途 | 包含内容 |
|---|---|---|
| [scu-ppt-body-style](skills/scu-ppt-body-style/SKILL.md) | 科研 PPT 主体组织与重排 | 字体配色、三种汇报节奏、8 种版式配方、可编辑 SVG 示意、交付核对 |

八种版式：系统总览、主图与公式、系统逐步拆解、结果与指标、多方法矩阵、双方案对比、闭环讲解、并列机制。

![主图与公式的主体组织示意](skills/scu-ppt-body-style/references/images/06-concept-and-equation.svg)

## 内容与来源

风格规则来自三份科研汇报的主体页观察与重新整理。公开版只分发文字规则和原创版式示意，不包含原始 PPT、论文截图、实验图像、机构标识或作者本机路径。`scu` 保留为 skill 标识，不表示四川大学官方发布或背书。

仓库的简洁介绍、安装入口和技能索引组织方式参考了 [mattpocock/skills](https://github.com/mattpocock/skills)。本仓库的科研主体风格内容独立整理，未复制其技能正文。

## 维护与贡献

发现问题时，可提交 Issue，注明使用的 AI 工具、输入材料类型、预期和实际结果。提交示例前请移除不适合公开的内容。

修改后运行：

```bash
python scripts/validate_skills.py
```

该检查验证目录、元数据、相对链接、SVG 和公开包文件范围；实际成片质量仍需渲染和人工检查。

## 许可证

[MIT](LICENSE)。适用于本仓库发布的规则、文档、校验脚本及原创 SVG 示意，不授予任何未随仓库发布的原稿、论文图像、字体或商标权利。
