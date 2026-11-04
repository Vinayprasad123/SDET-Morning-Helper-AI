---
name: test-data-creation
description: Create the prerequisite data a scenario needs (JSON templates, upload CSVs, sheet rows, account entities) in the exact shape the framework loads, add it to the idempotent Test Data Creation suite, and store it in the right place (DB / SFTP / repo). Triggered by test-case-generation, by regression-triage (verdict = test data), or on request.
argument-hint: "<what data is needed> [scenario name] [env]"
---

# Test data creation

## 1. Understand the need
Which scenario consumes it, which environment(s), and what must already exist in the account
(integrations, events, attributes, catalogs). List prerequisites explicitly.

## 2. Copy a real shape
Find an existing sample of the same kind (DB template, SFTP file, repo fixture) and copy its keys, nesting
and types. Never invent a structure.

## 3. Name it
Follow the naming convention (type prefix + real-world name, unique suffix if the scenario creates entities).
Synthetic identities only: `test-user-<n>@example.com`, `automation-<module>-<n>`.

## 4. Choose the store
| Store | Use when |
|---|---|
| MySQL template DB (keyed by scenario name) | structured JSON, per-scenario/per-env, changes often, large |
| SFTP shared `TestData/` | files every agent reads, binaries, bulk uploads, pipeline-refreshed data |
| Repo `src/test/resources/testData/` | small, static, should be reviewed with the code |
Lookup order at runtime: DB → repo → SFTP. Say where it went and why.

## 5. Make creation repeatable
Add/extend a scenario in the Test Data Creation suite that **checks first and creates only what is missing**,
so it can run daily on every environment. Every scenario that creates throw-away data ends with a cleanup step.

## 6. Guardrails
`SELECT` freely; any DB write or SFTP upload is shown to a person and approved first. No secrets or real
personal data in any file. Record new prerequisites in the knowledge base.
