---
name: regression-triage
description: Triage a UI regression build — fetch Serenity results from Jenkins (or a local report dir), group failures by root cause, classify each as script fix / test data / intermittent / environment / product defect, and write two reports (automation team, manual QA team). Use when given a Jenkins build number, a Slack regression report, or asked why a run failed.
argument-hint: "<jenkins-build-number | local> [slack-thread-link]"
---

# Regression triage

## 1. Collect evidence
1. `bash scripts/jenkins.sh status <build>` → suite, module, environment, result.
2. `bash scripts/jenkins.sh fetch-report <build> <scratch>/build-<build>` → Serenity JSON + screenshots.
3. `python3 scripts/failures.py <dir>` → failure groups by normalised error signature.
4. Read `references/failure-patterns.md` — known flaky scenarios, known bugs ↔ tickets, past corrections.

## 2. Analyse each group (not each scenario)
- Trace: step text → `scripts/step-catalog.py <words>` → step definition → page method → locator.
- More than ~5 groups → one parallel sub-agent per group, each given these rules.
- `git log --since="3 days ago" -- <touched files>` — a recent change is a strong automation signal.
- Suspected intermittent → tag the scenarios `@rerun_<build>` and rerun them; pass = intermittent, fail = reclassify.
- Classify with `classification-rules.md`. Every verdict carries **evidence** (error line, expected vs actual,
  screenshot), **confidence** (high/medium/low) and a **next action**. Low confidence → *Needs human review*.

## 3. Write the reports
- **Automation report** — summary counts, table `group | scenarios | root cause | fix file:line | confidence`,
  before/after code per group, rerun tag.
- **Manual QA report** — business-language description, expected vs actual, repro steps from the Gherkin,
  screenshot link, existing ticket or a draft ticket.
- Emit `verdict.json` (schema: `examples/report-router/sample-verdict.json`) for the router.

## 4. Deliver
- Ask before posting to Slack or creating tickets (unless running in the approved nightly pipeline mode).
- Append new learnings to `references/failure-patterns.md`.
- Offer `/fix-and-rerun <build>` for script-fix groups.
