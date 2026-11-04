---
name: test-case-generation
description: Generate or reorder test cases for a product feature in the standard flow (Positive → Edge/Boundary → Negative → State/Integration → Non-functional) from a spec page alone, or from manual cases plus a spec, then optionally automate them as Cucumber scenarios. Use when given a PRD/Confluence page and/or a test-case sheet.
argument-hint: "<spec content | exported file> [test cases file] [module]"
---

# Test case generation

| Mode | Input | Output |
|---|---|---|
| A — Review & reorder | manual cases + spec | cases checked against the spec, gaps added, duplicates merged, reordered |
| B — Generate | spec only | full case set derived from the spec |

## 1. Read inputs
Spec (pasted or exported), cases (xlsx/CSV/pasted), and the module's existing feature, page, locator and step files.

## 2. Requirement model (show it first)
Entities & screens · fields (type, mandatory, limits, formats, unique) · actions & state transitions ·
rules & messages · integrations · non-functional notes · **open questions** (ask, never assume).

## 3. Cases in standard order
| # | Section | ID prefix |
|---|---|---|
| 1 | Positive (happy path first, CRUD order) | P |
| 2 | Edge / Boundary (min/max ±1, unicode, empty optional, pagination) | E |
| 3 | Negative (missing mandatory, invalid format, duplicate, unauthorised, invalid state) | N |
| 4 | State / Integration (lifecycle, cross-module, UI ↔ API, persistence) | S |
| 5 | Non-functional (UX, performance, accessibility, security, compatibility) | NF |

IDs `TC_<MODULE>_<prefix>_<NN>`. Columns: ID · Section · Title · Req ref · Preconditions · Steps ·
Expected result (observable) · Priority · Automatable (Y/N + reason) · Source ID · Status.

## 4. Deliver
Requirement model → open questions → review findings → case table → counts. Write an xlsx grouped by section.
Ask before automating.

## 5. Automate (on approval)
- Merge cases with shared setup; same flow + different inputs → Scenario Outline.
- Reuse steps (`step-catalog.py`) before adding any; zero duplicate step patterns.
- Prerequisite data → hand off to `test-data-creation`.
- Section comments in the feature file in the same order; case IDs above each scenario.
- Compile, duplicate-step check, tagged local run; then remove the temporary tag.
