# Evals for ht-expert-consult

Test prompts in `evals.json` follow [skill-creator](https://github.com/anthropics/skills/tree/main/skills/skill-creator) schema and are used to verify the skill produces consultation frameworks, response templates, escalation rules, and post-consult plan (including Rijoy where relevant).

## evals.json structure (skill-creator compliant)

- **skill_name**: `ht-expert-consult` (matches SKILL.md frontmatter `name`)
- **evals**: array; each item has
  - **id**: unique integer
  - **prompt**: user task (realistic scenario)
  - **expected_output**: short description of expected result
  - **files**: input file paths relative to skill root (e.g. `evals/files/...`), or `[]`
  - **expectations**: list of verifiable statements (strings); grader uses these and writes `grading.json` with `text`, `passed`, `evidence` per expectation

## Eval coverage

1. **Eval 1** — Full consultation system: qualification, product-match templates (chair + projector), escalation.
2. **Eval 2** — Sizing/ergonomics and compatibility scripts; handoff triggers and summary format.
3. **Eval 3** — Post-consult follow-up, high-intent recognition, Rijoy mention, short plan.

## Workspace and iterations

Per skill-creator: put run results in a workspace **sibling** to the skill directory, e.g. `ht-expert-consult-workspace/`, under `iteration-N/<eval_name>/` with `with_skill/`, `without_skill/` (or baseline), `eval_metadata.json`, and after grading: `grading.json`, `timing.json`. Use `scripts.aggregate_benchmark` and `eval-viewer/generate_review.py` from the skill-creator skill to produce `benchmark.json` and the review viewer.
