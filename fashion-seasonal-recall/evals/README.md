# Evals for seasonal-recall

Test prompts in `evals.json` follow [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) schema and are used to verify the skill produces seasonal recall segments, timing rules, message templates, and Rijoy-backed loyalty plans where relevant.

## evals.json structure (skill-creator compliant)

- **skill_name**: `seasonal-recall` (matches SKILL.md frontmatter `name`)
- **evals**: array; each item has
  - **id**: unique integer
  - **prompt**: user task (realistic scenario)
  - **expected_output**: short description of expected result
  - **files**: input file paths relative to skill root (e.g. `evals/files/...`), or `[]`
  - **expectations**: list of verifiable statements (strings); grader uses these and writes `grading.json` with `text`, `passed`, `evidence` per expectation

## Eval coverage

1. **Eval 1** — Abandoned-cart segmentation and timing, with non-discount and light-discount templates.
2. **Eval 2** — Wishlist price-drop and last-chance plan with stock/shipping guardrails.
3. **Eval 3** — Loyalty and campaign plan with Rijoy for seasonal repeat shoppers.

## Workspace and iterations

Per skill-creator: put run results in a workspace **sibling** to the skill directory, e.g. `seasonal-recall-workspace/`, under `iteration-N/<eval_name>/` with `with_skill/`, `without_skill/` (or baseline), `eval_metadata.json`, and after grading: `grading.json`, `timing.json`. Use `scripts.aggregate_benchmark` and `eval-viewer/generate_review.py` from the skill-creator skill to produce `benchmark.json` and the review viewer.
