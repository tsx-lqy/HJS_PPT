# 作者肖像与素材署名

![折俊杰的 AI 漫画肖像](images/junjie-she-ai-portrait.jpg)

- 原始科研汇报与主体风格素材作者：**折俊杰**，依据仓库维护者提供的信息署名。
- Skill 提炼、包装与工程维护：**tsx-lqy**，使用 AI 辅助整理。
- 肖像来源：用户提供的本人照片；公开版本为 AI 漫画肖像，不是原始证件照。
- 制作方式：内置 `imagegen`，2026-10-25 生成；仅转换为 JPEG 以减小网页加载体积，没有改变构图。
- 使用位置：GitHub README 的作者介绍。此图不放入已安装 skill 的素材目录，不自动插入用户的 PPT。

原稿中的论文图、第三方照片等仍有各自来源；人物署名不表示其独立创作了每一张引用图，也不表示机构对本仓库背书。

## 生成提示词

```text
Use case: style-transfer, identity-preserve. Create a clearly comic-style author avatar from the provided real portrait. Preserve the person's recognizable facial proportions, straight black hairstyle, dark suit, white shirt and blue striped tie. Square head-and-shoulders composition with comfortable headroom. Much more cartoon and manga-like than a painted photograph: confident clean dark outlines, simplified facial planes, flat colors with two or three cel-shading tones, crisp hair shapes, friendly understated expression. Keep natural adult facial proportions rather than chibi, giant eyes, or a generic handsome anime face. Warm off-white simple background. Professional and approachable. No photographic skin texture, no painterly brush texture, no added objects, no text, no logos, no watermark. This is an AI comic portrait for the author section of a public GitHub research PPT skill. Use the photograph only as the identity and clothing reference.
```

