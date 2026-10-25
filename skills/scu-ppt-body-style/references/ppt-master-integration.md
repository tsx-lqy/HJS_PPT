# 与 PPT Master 配合

本 skill 集成的是科研场景的制作流程及后端交接规则。风格来自参考稿；复杂的 PDF 转换、原生 Office Math 和 SVG → PPTX 转换使用环境中已有的工具。**没有捆绑 PPT Master 引擎，也不把安装本 skill 等同于安装该引擎。**

## 能力分工

| 能力 | 本 skill 提供 | 可用 PPT Master 时 |
|---|---|---|
| 主体排版 | 12 种配方、图文关系和用户模板边界 | 使用本 skill 的主体设计；不自动采用上游布局库 |
| 材料整理 | 来源与证据记录；PPTX 文字/备注读取 | 调用 `source_to_md.py` 及适用转换器处理更多格式 |
| 公式与图表 | 精确公式、变量、数据和可编辑性要求 | 原生公式标记、图表/表格 payload 及原生导出 |
| 逐页讲稿 | 页号、标题、解释和承接结构 | 将 `notes/total.md` 拆分并随页面导出到备注 |
| 渲染检查 | 只读结构检查、Windows PowerPoint 导图及视觉核对 | 使用其当前导出校验；SVG 预览之后仍检查最终 PPTX 渲染 |

不自动加入动画、转场、语音、视频、模型服务、品牌库或云端发布，也不需要这些功能才能完成四类基础制作。

## 接入步骤

1. 检查当前环境是否已安装完整的 PPT Master、Python 及其所需依赖；不能只根据 skill 名称推断其脚本存在。没有时照样使用本 skill 的风格规则、检查脚本及环境原有制作工具。确实需要上游引擎时，按其 [安装说明](https://github.com/hugohe3/ppt-master#readme) 安装，尊重用户当前的安装授权。
2. 读取已安装版本的相关工具帮助和能力文档。仅按任务加载材料转换、原生公式/图表、备注、导出检查部分；保留实际选用转换器要求的技术契约。
3. 将用户模板约束、主体区、页序、每页问题与证据、图表数据和精确 LaTeX 交给制作后端。后端完成可编辑对象与封装，不能自行换掉已经确定的主体风格。
4. 导出后按 [production.md](production.md) 检查备注对应、原生对象及最终渲染。保存后端版本和实际命令，便于复现。

上游也提供 Skills CLI 安装入口：

```bash
npx skills add hugohe3/ppt-master
```

安装器和运行依赖以该版本上游说明为准；本仓库的安装命令不会连带执行它。

## 已核对的接口示例

以下针对 `78759bf62e9a1ef43e926ff9e50afa4cfe9a63cb` 的源代码，调用前运行本机版本的 `--help`。`<ppt-master-scripts>` 表示上游完整安装中的 scripts 目录，`<project>` 是满足其项目结构的工作目录，不能指向任意 PPTX 文件。

```bash
python "<ppt-master-scripts>/source_to_md.py" paper.pdf -o paper.md
python "<ppt-master-scripts>/source_to_md.py" input.pptx --json
python "<ppt-master-scripts>/total_md_split.py" "<project>"
python "<ppt-master-scripts>/svg_to_pptx.py" --help
```

- 原生公式：读取上游 [native-formula.md](https://github.com/hugohe3/ppt-master/blob/78759bf62e9a1ef43e926ff9e50afa4cfe9a63cb/skills/ppt-master/references/native-formula.md)。复杂数学通过受支持的 LaTeX 编译为 Office Math；SVG 预览不等于可编辑数学已导出。
- 图表与表格：读取 [native-data-interface.md](https://github.com/hugohe3/ppt-master/blob/78759bf62e9a1ef43e926ff9e50afa4cfe9a63cb/skills/ppt-master/references/native-data-interface.md)。该版本需要同步可见预览与 JSON 数据，且原生图表/表格导出有专门激活开关；不能仅画出 SVG 图就声称原生可编辑。
- 备注拆分：`total_md_split.py` 按 SVG 页名匹配，拆分后检查缺失与多余标题。用户只提供 PPTX 时先用合适的原生编辑工具，不为了讲稿强制重建整个 SVG 工程。
- 兼容性：上游原生数学以 PowerPoint 为目标；其他客户端可能显示预览回退。应以用户实际使用的软件验证。

这些是源代码核对的接入接口，不构成对所有上游版本、转换器及运行环境的端到端认证。若接口变动，读取当前帮助后调整；不要猜测参数或跳过导出错误。

## 归属与许可

参考项目：[hugohe3/ppt-master](https://github.com/hugohe3/ppt-master)，作者 Hugo He，[MIT License](https://github.com/hugohe3/ppt-master/blob/78759bf62e9a1ef43e926ff9e50afa4cfe9a63cb/LICENSE)，Copyright (c) 2025–2026 Hugo He。

本包的说明、示意、`inspect_pptx.py` 和 `render_pptx.ps1` 为独立实现；未分发上游源码或素材。安装和使用上游时遵循其许可；后续若复制或修改其代码分发，须一并保留原版权和 MIT 许可，不把上游代码重新标成仅由本仓库创作。
