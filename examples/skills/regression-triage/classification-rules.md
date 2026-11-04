# Failure classification rules

Apply top to bottom; first strong match wins, but always sanity-check against the screenshot.

## Environment / infra
- Login failures, `SessionNotCreatedException`, `WebDriverException: unknown error: net::ERR_*`, DNS/timeouts on every scenario of a module.
- Many unrelated modules failing at the same time with the same signature.
- Jenkins console shows agent/Chrome/Nexus problems (`jenkins.sh console <build>`).
- Test-data prerequisites missing in the account (segment, SSP/ESP/WSP integration, catalog not present) — note *which* prerequisite.

## Automation issue (fix in this repo)
- `NoSuchElementException`, `TimeoutException` waiting for a locator, `StaleElementReferenceException`, `ElementClickInterceptedException` — **and** the screenshot shows the feature working (element just moved/renamed/loads slower), or a positional locator opened the wrong one of several same-placeholder dropdowns.
- Toast/notification text read too early or too late (see `NotificationToastMessages`).
- Assertion on data the test itself created wrongly (wrong template, name collision from a previous run, missing cleanup).
- Hard sleeps racing the UI; order-dependent scenarios; static runtime IDs leaking between scenarios.
- Failure started right after a commit touching that page/step (`git log`).

## Product bug (report to manual QA)
- Assertion with a clear business expected vs actual mismatch (counts, stats, labels, saved values not retained) and the test's input is correct.
- UI shows an error message/toast, blank page, or 4xx/5xx in an API step.
- Behaviour contradicts the scenario's intent across retries and environments.
- Already linked to `@issue:<PROJECT>-*` on the scenario → product bug, reference that ticket.

## Both
- Intentional UI change (new label/flow) that breaks locators **and** may need product confirmation — automation must adapt, manual QA confirms it is intended.
- Product bug that also exposed a weak test (e.g. test passed wrongly before).

## Needs human review
- Confidence low, no screenshot, or evidence conflicts. Say what evidence would settle it.
