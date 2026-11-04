# #automation-quickfix — Build #1042 (UX Regression, Prod US)

**Summary:** 9 failed / 5 groups — 2 script fix · 1 test data · 1 intermittent · 1 needs review

| # | Category | Group | Scenarios | Root cause | Fix | Confidence |
|---|---|---|---|---|---|---|
| G1 | 🔧 Script fix | Catalog event mapping: wrong dropdown | 2 | Positional locator picked the new optional `price as` dropdown | `CatalogsPageElements.EVENT_ROW_ATTRIBUTE_DD` → locate by header label | High |
| G2 | 🗂 Test data | Static segment upload | 1 | Prerequisite list missing on this env | Run Test Data Creation → StaticSegments | High |
| G3 | 🔁 Intermittent | Push save toast | 1 | Toast read before render — **passed on rerun** (flake count 3) | `PushCampaignPage.verifySaveToast` → wait for visibility | Medium |
| G4 | 👀 Needs review | Funnel chart not rendered | 1 | No screenshot; slow API or locator change | Check `FunnelsPage.waitForChart` | Low |

### G1 — before / after
```java
// before
EVENT_ROW_ATTRIBUTE_DD(getXpath("(//span[text()='Select Attribute'])[last()]/.."))
// after — dropdown located by the label beside it
static final String EVENT_ROW_ATTRIBUTE_DD =
    "(//*[normalize-space(translate(.,'*',''))='%s'])[last()]/following::span[text()='Select Attribute'][1]/..";
```
Rerun: `@rerun_1042` → `/fix-and-rerun 1042 G1,G3`
