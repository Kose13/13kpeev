---
name: imagegen-2
description: Generate and edit images with OpenAI image generation models, including prompt writing, multi-image batches, transparent background assets, and iterative revisions. Use when a user asks for new image creation, style exploration, visual concept iteration, image edits/inpainting, or production-ready image prompt optimization.
---

# Image Generation Workflow

Follow this workflow to produce reliable, high-quality image outputs.

## 1) Clarify the target output

Capture these requirements before generating:

- Subject (who/what is in frame)
- Style (photo, illustration, 3D render, pixel art, etc.)
- Composition (camera angle, framing, focal subject)
- Lighting and mood
- Aspect ratio and resolution needs
- Delivery constraints (transparent background, text-free, brand-safe)

If requirements are missing, ask concise follow-up questions. If speed matters, make reasonable defaults explicit.

## 2) Build a production prompt

Structure the prompt in this order:

1. Core scene sentence
2. Visual style sentence
3. Composition and camera sentence
4. Lighting/color sentence
5. Quality and constraint sentence

Keep prompts concrete. Prefer specific nouns/adjectives over abstract intent.

### Prompt template

Use this template and fill all fields:

```text
[Subject + action], in [style], [composition/camera], [lighting/color], [quality bar], [constraints].
```

### Constraint examples

- "No text, logos, or watermarks."
- "Centered subject with clean negative space on the right."
- "Transparent background, sharp edges, no drop shadow."

## 3) Generate multiple candidates

Always produce 2-4 prompt variants when exploration is requested.

For each variant, modify one major axis only:

- Variant A: composition
- Variant B: lighting/mood
- Variant C: style rendering
- Variant D: color palette

This isolates changes and speeds feedback cycles.

## 4) Handle edits and inpainting

When editing an existing image:

1. Describe what must stay unchanged.
2. Describe the exact region/change.
3. Restate style-matching constraints.
4. Add artifact guards (edge seams, mismatched lighting, malformed hands/textures).

Use precise edit language: "Replace", "Remove", "Extend", "Recolor", "Retouch".

## 5) Review and iterate

After each generation, evaluate against:

- Subject correctness
- Composition clarity
- Style fidelity
- Artifact presence
- Requirement adherence

Then provide targeted revision instructions (1-3 edits max per iteration).

## 6) Output format

When returning final prompts, provide:

- **Recommended prompt** (single best)
- **Alternates** (up to 3)
- **Negative constraints** (if helpful)
- **Revision knobs** (what to tweak for tighter results)

Use concise bullets and keep each prompt on one line for easy copying.
