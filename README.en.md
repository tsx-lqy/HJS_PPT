# HJS_PPT

Help an AI agent explain research through diagrams, concise explanations, and evidence-supported conclusions.

An editable agent skill for paper presentations, lab meetings, system design, academic interviews, defenses, and research plans. It focuses on slide body layouts while preserving your chosen template.

<img src="docs/images/hajizhe-avatar.jpg" width="220" alt="哈基折">

**哈基折**

[中文](README.md) · [Asset library](skills/hjs_ppt/references/asset-library.md) · [Emphasis](skills/hjs_ppt/references/emphasis.md) · [Image generation](skills/hjs_ppt/references/image-generation.md) · [WPS preview](skills/hjs_ppt/references/wps-preview.md) · [15 layouts](skills/hjs_ppt/references/layouts.md)

## Installation

With Node.js and Git installed:

```bash
npx skills@latest add tsx-lqy/HJS_PPT --skill hjs_ppt
```

Choose your agent when prompted. Installation is project-local by default. For a global Codex installation using regular file copies:

```bash
npx skills@latest add tsx-lqy/HJS_PPT --skill hjs_ppt -a codex -g --copy
```

For Claude Code, replace `-a codex` with `-a claude-code`. Start a new agent session after installing, or refresh its skill list as directed by that agent. See the [Skills CLI documentation](https://github.com/vercel-labs/skills) for other agents.

Alternatively, [download the ZIP](https://github.com/tsx-lqy/HJS_PPT/archive/refs/heads/main.zip) and copy the entire `skills/hjs_ppt` folder to your agent's skills directory. Keep the references and images together with `SKILL.md`. Preserve any local customizations before replacing an existing installation.

To update installed skills:

```bash
npx skills@latest update
```

Save local customizations before updating.

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

## Research assets, selective emphasis, and preview

The package now includes **18 original vector components and one AI-generated concept illustration**, with a searchable catalogue. They cover optical hardware, acquisition, neural layers, image stacks, scanning, timing, and ROI relationships. A separate extractor builds a private, deduplicated image library from the user's PPTX, preserving page and crop metadata without republishing source research.

![Research asset gallery](skills/hjs_ppt/assets/gallery.svg)

Key phrases, meaningful numbers, method differences, and material limitations receive **selective red and bold native text formatting**, while ordinary explanation remains dark. The user's explicit template palette takes priority.

Image2 integration routes necessary conceptual illustrations to the environment's image-generation tool. An explicit model-capable interface can select `gpt-image-2`; a built-in tool with no exposed model identity must be reported as built-in generation only. Generated images never replace experimental evidence. See [workflow and saved example](skills/hjs_ppt/references/image-generation.md).

The Windows WPS helper opens a new read-only snapshot after a meaningful save checkpoint, starting with the first readable draft. It does not overwrite the source, run a background watcher, or promise character-level synchronization. WPS is not installed automatically. The development machine had no WPS; real WPS display and MathType compatibility remain unverified. See [commands and validation limits](skills/hjs_ppt/references/wps-preview.md).

![Material-led composition with selective emphasis](skills/hjs_ppt/assets/examples/material-led-page.svg)

## Production capabilities

- **Source intake:** connect page/figure references, data, conditions, and claims; extract slide-local PPTX text and notes with the bundled Python inspector.
- **Assets and image generation:** retrieve semantic components, extract private source images, and generate conceptual illustrations when useful.
- **Selective emphasis:** apply native red/bold text runs to key phrases and connect them to visible diagram details.
- **MathType equations and editable charts:** every equation must be created with MathType and remain editable through MathType in the saved PPTX. Office Math, plain text, and image-only equations are not substitutes. Prefer native charts/tables and retain source data. If MathType is unavailable, report the equation stage as unfinished. See the [rule and example](skills/hjs_ppt/references/mathtype.md).
- **Speaker notes:** keep notes aligned with final slide order and explain where to look, what it means, and what remains uncertain.
- **Rendering checks:** inspect package relationships and native-object counts, then render and visually review every page. A Windows PowerPoint export script is included.
- **WPS checkpoint preview:** open complete saved snapshots during creation without altering the source or closing user documents.

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
