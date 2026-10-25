# 所有公式必须使用 MathType

这是 HJS_PPT 的成片要求，适用于新建、重排和修改 PPT。**最终 PPTX 中的每个公式都必须由 MathType 制作，并能重新用 MathType 打开编辑。** 可编辑的 Office Math 不等同于 MathType；把图片命名为 MathType 也不算完成。

## 范围与制作

- 覆盖行内与独立公式、简单等式和赋值、分式、矩阵、多行推导、图表或截图中的数学表达式。单独的数字、单位、普通变量标签不必强制转成公式对象；一旦构成数学关系或运算表达式，就使用 MathType。
- 为公式建立清单：`页号 / 位置或对象名 / 精确表达式 / 来源 / 变量与单位 / MathType 制作状态 / 重新打开验证结果`。LaTeX、MathML 可以作为输入或备份，不是最终公式的替代品。
- 先检查当前 MathType 与 PowerPoint 版本、可用授权及自动化能力。在受支持的 MathType 7 桌面环境中使用可编辑嵌入对象；使用 MathType for Microsoft 365 时，通过该加载项插入并重新打开编辑。不同版本的存储形式不同，不把所有合格公式都判定为 OLE，也不因存在 OLE 就认定合格。
- 从论文或旧 PPT 引用公式时，核对上下标、负号、括号、矩阵维度和变量，再用 MathType 重建。对含公式的科学图，保留原始素材与来源，在不遮掉数据、不改变证据的前提下拆分公式区域并重建为 MathType。无法可靠拆分时明确列为未完成，不能把整张公式截图当作合格交付。
- 数学字体、字号和行距在 MathType 内统一设置，符合模板与版面需要。保持纵横比，给根号、分式和上下标留足高度，不用拉伸对象挤进空间。

## 缺少工具时

继续整理材料、图表、讲稿和布局，用清晰标记的公式位置作为工作草稿，并交付精确公式源与待办清单。明确说明“尚未完成 MathType 制作/验证”。不要自动降级为 Office Math、PNG/SVG、普通文本或 LaTeX 渲染图后宣称完成；不要编造 MathType 对象、伪改格式标识，或假称安装本 skill 就安装了 MathType。

## 验收

1. 对照清单逐页检查，包括图中及行内公式，确认无遗漏。
2. 保存并重新打开最终 PPTX，逐个用实际 MathType 客户端打开，核对结构、符号及编辑能力；验证修改可在副本中进行。
3. 渲染所有页面，放大检查公式的基线、清晰度、裁切、遮挡和与图文的对应关系。
4. 报告 MathType/PowerPoint 版本、公式总数、已验证数和未完成项。`inspect_pptx.py` 的 `math_objects` 只统计 Office Math XML，不是 MathType 数量或合规检查；零计数和结构检查通过都不能证明符合本规则。

仓库中的 Markdown 表达式及 SVG 版式示意仅用于解释布局，不能直接当作最终 PPT 的公式对象。

## 示例

样本标准差页：用 MathType 插入 `s=\sqrt{\frac{\sum_{i=1}^{n}(x_i-\bar{x})^2}{n-1}}`；教学结果 `s=1\,\mathrm{a.u.}` 也用 MathType。数据点、箭头和“样本离散程度”等解释仍用普通可编辑对象。保存后分别重新打开两个公式验证，而不是仅检查它们看起来正确。

操作入口与兼容性以当前官方文档为准：[MathType for Microsoft 365 的 PowerPoint 使用指南](https://docs.wiris.com/mathtype-for-microsoft-365/get-started-with-mathtype-in-microsoft-powerpoint)、[MathType 7 的 PowerPoint 支持](https://docs.wiris.com/mathtypes-support-for-microsoft-powerpoint?kb_language=en_US)。
