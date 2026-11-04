# #qa-manual — Suspected product defects · Build #1042 (Prod US)

| # | Module | What broke | Expected vs actual | Evidence | Ticket | Confidence |
|---|---|---|---|---|---|---|
| D1 | Journeys | Exit count on journey stats doesn't update | Exited = 1 → **0** after 15 min (reproduced on rerun) | screenshot `abc123.png` | — (draft below) | High |

### D1 — Repro steps
1. Create a journey: trigger on event `automation_event`, wait 1 min, exit condition at block 2.
2. Fire `automation_event` for user `automation-journeys-1`.
3. Wait until the user passes block 2.
4. Open the journey → Stats.

**Expected:** Exited = 1 **Actual:** Exited = 0 · **Env:** Prod US · **Report:** `<link>`

### Draft ticket
- **Title:** Journey stats: Exited count stays 0 after user exits
- **Steps / Expected / Actual / Environment:** as above
- **Found by:** nightly UI regression, AI-triaged, awaiting manual confirmation
