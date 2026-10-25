# Skills for Research Presentations

Help an AI agent explain research through diagrams, concise explanations, and evidence-supported conclusions.

Small, editable agent skills for paper presentations, lab meetings, and system design reviews. The first skill focuses on slide body layouts while preserving your chosen template. Instructions are written primarily in Chinese; the skill can produce content in the language you request.

[中文](README.md) · [12 layout recipes](skills/scu-ppt-body-style/references/layouts.md) · [Purpose and examples](skills/scu-ppt-body-style/references/usage-examples.md) · [Production workflow](skills/scu-ppt-body-style/references/production.md)

## Installation

With Node.js and Git installed:

```bash
npx skills@latest add tsx-lqy/skill --skill scu-ppt-body-style
```

Choose your agent when prompted. Installation is project-local by default. For a global Codex installation using regular file copies:

```bash
npx skills@latest add tsx-lqy/skill --skill scu-ppt-body-style -a codex -g --copy
```

For Claude Code, replace `-a codex` with `-a claude-code`. Start a new agent session after installing, or refresh its skill list as directed by that agent. See the [Skills CLI documentation](https://github.com/vercel-labs/skills) for other agents.

Alternatively, [download the ZIP](https://github.com/tsx-lqy/skill/archive/refs/heads/main.zip) and copy the entire `skills/scu-ppt-body-style` folder to your agent's skills directory. Keep the references and images together with `SKILL.md`. Preserve any local customizations before replacing an existing installation.

To update installed skills:

```bash
npx skills@latest update
```

Save local customizations before updating.

## Usage

```text
Use $scu-ppt-body-style to turn this paper into an eight-slide research presentation.
Write in English, preserve my blue template, and focus on methods, comparisons, and limitations.
```

Supply the research material, figures, and any template you want preserved. The skill guides organization and design. Your agent still needs tools to create, edit, and render presentation files; installing this skill alone does not install PowerPoint or produce a deck.

## What it helps with

| Content problem | Layout | Benefit |
|---|---|---|
| Equations feel disconnected from their meaning | Small example → process → formula | Connect variables with visible operations |
| A paper summary lists claims without evidence | Source + mechanism + experiment + limitation | Make the evidence behind a conclusion visible |
| Several technical routes look plausible | Benefits / constraints matrix | Explain a conditional choice using shared criteria |
| A history or research sequence feels fragmented | Persistent timeline + active node | Maintain context across slides |

The [worked examples](skills/scu-ppt-body-style/references/usage-examples.md) include sample standard deviation using explicitly illustrative values 2, 3, and 4; a paper evidence page; and a conditional technology choice. The examples include invocation prompts and speaker-note guidance. They contain no source research data.

## Four production capabilities

- **Source intake:** connect page/figure references, data, conditions, and claims; extract slide-local PPTX text and notes with the bundled Python inspector.
- **Editable equations and charts:** prefer Office Math and native charts/tables, retain exact expressions and data, and disclose image fallbacks.
- **Speaker notes:** keep notes aligned with final slide order and explain where to look, what it means, and what remains uncertain.
- **Rendering checks:** inspect package relationships and native-object counts, then render and visually review every page. A Windows PowerPoint export script is included.

[PPT Master](https://github.com/hugohe3/ppt-master) can optionally supply source converters and native export. This skill owns body design while the user's template remains authoritative. The [integration guide](skills/scu-ppt-body-style/references/ppt-master-integration.md) documents checked interfaces and dependencies. Its engine is not bundled or installed automatically. Animation, narration, and video are outside this update.

## Skills

| Skill | Purpose |
|---|---|
| [scu-ppt-body-style](skills/scu-ppt-body-style/SKILL.md) | Research slide body design and production: 12 layouts, original diagrams, worked examples, source intake, math/charts, speaker notes, and rendering checks |

The twelve recipes cover system overviews, diagrams with equations, progressive system explanations, results with metrics, comparison matrices, paired evidence, feedback loops, parallel mechanisms, paper evidence, worked examples, tradeoffs, and continuous timelines.

![Diagram with equations layout](skills/scu-ppt-body-style/references/images/06-concept-and-equation.svg)

## Provenance

The design guidance was distilled from five distinct research presentations containing 110 pages including covers and appendices. The three newly reviewed inputs contain 58 pages; the 19-page COME deck duplicates a previous input and is counted once. This public edition includes independently written guidance, scripts, and original schematic diagrams. It does not redistribute source decks, research screenshots, experimental images, institutional logos, or machine-specific paths. The `scu` identifier does not imply university endorsement.

Repository presentation and installation-first navigation were inspired by [mattpocock/skills](https://github.com/mattpocock/skills). The research presentation guidance is independently developed.

## Contributing

Open an issue with your agent, input type, expected result, and observed result. Only submit material that is appropriate to publish.

Run the package checks after changes:

```bash
python scripts/validate_skills.py
python -B -m unittest discover -s tests
```

These checks cover structure, metadata, relative links, SVG validity, and the public package file set. They do not replace visual inspection of generated presentations.

## License

[MIT](LICENSE), covering the guidance, documentation, validation script, and original SVG diagrams distributed here. It grants no rights to source decks, research figures, fonts, or trademarks that are not distributed in this repository.
