# 2 · Regression Triage Skill

An AI skill (a `SKILL.md` procedure the agent follows) that turns a Jenkins build number into two actionable reports. It is the engine behind the automated report verification in [01](01-ai-report-verification.md), and can also be run on demand: `/regression-triage 17750`.

## Flow

```mermaid
flowchart TD
    A[Input: build number or local report dir] --> B[jenkins.sh status → suite, module, env]
    B --> C[jenkins.sh fetch-report → Serenity JSON + screenshots]
    C --> D[failures.py → groups by error signature]
    D --> E[Read knowledge base<br/>failure-patterns.md]
    E --> F{> 5 groups?}
    F -->|yes| G[Parallel sub-agents,<br/>one per group]
    F -->|no| H[Analyse in main agent]
    G --> I
    H --> I[Per group: step text → step-catalog → page method → locator]
    I --> J[git log -3 days on touched files]
    J --> K[Classify with classification-rules.md<br/>+ evidence + confidence]
    K --> L[Automation report]
    K --> M[Manual QA report + draft Jira]
    L --> N[Offer /fix-and-rerun]
    K --> O[Append learnings to knowledge base]
```

## What makes it reliable

| Technique | Why |
|---|---|
| **Signature grouping** (`failures.py`) normalises error text (strips IDs, timestamps, line numbers) and groups scenarios that fail the same way | Analyse 6 root causes, not 40 scenarios |
| **Code-path tracing** with a step catalog (`step-catalog.py`) that maps every Gherkin step to its Java definition `file:line` | The agent reads the exact locator that failed instead of guessing |
| **Rule table** with ordered, evidence-based rules (see [`examples/skills/regression-triage/classification-rules.md`](../examples/skills/regression-triage/classification-rules.md)) | Same failure → same verdict, regardless of who runs it |
| **Recent-change signal**: a commit touching the failing page in the last 3 days | Strong indicator of an automation regression |
| **Knowledge base** of flaky scenarios, known bugs ↔ ticket IDs, past misclassifications | Each run starts smarter than the last |
| **Two audiences, two reports** | Engineers get file:line and before/after code; manual QA get business language, repro steps and expected vs actual |

## Hand-off to fixing

```mermaid
flowchart LR
    T[Triage: Script-fix groups] --> F[fix-and-rerun skill]
    F --> B[branch autofix/build-N]
    B --> L{Broken locator?}
    L -->|yes| LF[locator-fixer sub-agent<br/>inspects live page via Playwright]
    L -->|no| W[Fix wait / data / cleanup]
    LF --> R[Tag failed scenarios @rerun_N]
    W --> R
    R --> RR[Rerun only those, locally or on Jenkins]
    RR --> U[Remove temporary tags → MR]
```

Guardrails: a product bug is never "fixed" by weakening an assertion; rerun tags are never committed; a compile hook blocks the agent from finishing with broken Java.
