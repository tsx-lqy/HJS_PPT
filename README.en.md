# hjs_ppt

Help an AI agent explain research through diagrams, concise explanations, and evidence-supported conclusions.

An editable agent skill for paper presentations, lab meetings, system design, academic interviews, defenses, and research plans. It focuses on slide body layouts while preserving your chosen template.

<img src="docs/images/junjie-she-ai-portrait.jpg" width="220" alt="AI comic portrait of Junjie She">

**Original research presentations and body-style source material: Junjie She (折俊杰).** Skill distillation, packaging, and maintenance: tsx-lqy. This is an AI comic portrait based on a user-provided photograph, used for author attribution. [Image provenance and prompt](docs/portrait.md). Instructions are written primarily in Chinese; the skill can produce content in the language you request.

[中文](README.md) · [15 layout recipes](skills/hjs_ppt/references/layouts.md) · [Purpose and examples](skills/hjs_ppt/references/usage-examples.md) · [Production workflow](skills/hjs_ppt/references/production.md)

## Installation

With Node.js and Git installed:

```bash
npx skills@latest add tsx-lqy/skill --skill hjs_ppt
```

Choose your agent when prompted. Installation is project-local by default. For a global Codex installation using regular file copies:

```bash
npx skills@latest add tsx-lqy/skill --skill hjs_ppt -a codex -g --copy
```

For Claude Code, replace `-a codex` with `-a claude-code`. Start a new agent session after installing, or refresh its skill list as directed by that agent. See the [Skills CLI documentation](https://github.com/vercel-labs/skills) for other agents.

Alternatively, [download the ZIP](https://github.com/tsx-lqy/skill/archive/refs/heads/main.zip) and copy the entire `skills/hjs_ppt` folder to your agent's skills directory. Keep the references and images together with `SKILL.md`. Preserve any local customizations before replacing an existing installation.

To update installed skills:

```bash
npx skills@latest update
```

Save local customizations before updating.

## Renaming an existing installation

The skill was renamed from `scu-ppt-body-style` to **`hjs_ppt`**. Install using the new command above, preserve your customizations, and move the old installation out of the skills directory. An update alone may not migrate a renamed skill. Invoke `$hjs_ppt`.

The underscore is intentional. Skills CLI discovery and installation have been verified; strict Agent Skills validators that only accept hyphen-case names will reject it. Repository checks do not establish universal client compatibility.

## Usage

```text
Use $hjs_ppt to turn this paper into an eight-slide research presentation.
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

The [worked examples](skills/hjs_ppt/references/usage-examples.md) include sample standard deviation using explicitly illustrative values 2, 3, and 4; a paper evidence page; and a conditional technology choice. The examples include invocation prompts and speaker-note guidance. They contain no source research data.

## Four production capabilities

- **Source intake:** connect page/figure references, data, conditions, and claims; extract slide-local PPTX text and notes with the bundled Python inspector.
- **Editable equations and charts:** prefer Office Math and native charts/tables, retain exact expressions and data, and disclose image fallbacks.
- **Speaker notes:** keep notes aligned with final slide order and explain where to look, what it means, and what remains uncertain.
- **Rendering checks:** inspect package relationships and native-object counts, then render and visually review every page. A Windows PowerPoint export script is included.

[PPT Master](https://github.com/hugohe3/ppt-master) can optionally supply source converters and native export. This skill owns body design while the user's template remains authoritative. The [integration guide](skills/hjs_ppt/references/ppt-master-integration.md) documents checked interfaces and dependencies. Its engine is not bundled or installed automatically. Animation, narration, and video are outside this update.

## Skills

| Skill | Purpose |
|---|---|
| [hjs_ppt](skills/hjs_ppt/SKILL.md) | Research slide body design and production: 15 layouts, original diagrams, worked examples, source intake, math/charts, speaker notes, and rendering checks |

The fifteen recipes cover system overviews, diagrams with equations, progressive system explanations, results with metrics, comparison matrices, paired evidence, feedback loops, parallel mechanisms, paper evidence, worked examples, tradeoffs, continuous timelines, personal contributions with evidence, research maps, and staged research plans.

![Diagram with equations layout](skills/hjs_ppt/references/images/06-concept-and-equation.svg)

## Provenance

The design guidance was distilled from six distinct research presentations containing 133 pages including covers and appendices. The latest input is a 23-page academic interview and research-plan deck; the repeated COME deck is counted once. This public edition includes independently written guidance, scripts, and original schematic diagrams. It does not redistribute source decks, research screenshots, experimental images, institutional logos, or machine-specific paths. The project name does not imply university or institutional endorsement.

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
