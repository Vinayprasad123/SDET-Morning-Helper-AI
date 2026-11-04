#!/usr/bin/env python3
"""Route AI-classified regression failures to the right Slack channel.

Input: the triage agent's JSON verdict (see sample-verdict.json).
Each failure group has a category and a confidence; this script posts
automation-side groups to the quick-fix channel and product defects to the
manual-QA channel, then replies once in the original build thread.

Webhook URLs / bot token come from environment variables, never from files.

Usage:
    python3 router.py sample-verdict.json            # post
    DRY_RUN=1 python3 router.py sample-verdict.json  # print only
"""
import json
import os
import sys
import urllib.request

ROUTES = {
    "script_fix":   "AUTOMATION_QUICKFIX",
    "test_data":    "AUTOMATION_QUICKFIX",
    "intermittent": "AUTOMATION_QUICKFIX",
    "environment":  "AUTOMATION_QUICKFIX",
    "defect":       "QA_MANUAL",
    "needs_review": "BOTH",
}
ICONS = {
    "script_fix": ":wrench:", "test_data": ":card_file_box:", "intermittent": ":repeat:",
    "environment": ":cloud:", "defect": ":beetle:", "needs_review": ":eyes:",
}
MIN_AUTO_ROUTE_CONFIDENCE = {"high", "medium"}


def route_for(group):
    # Low confidence is never auto-routed as a verdict: a person decides.
    if group["confidence"] not in MIN_AUTO_ROUTE_CONFIDENCE:
        return "BOTH", "needs_review"
    return ROUTES[group["category"]], group["category"]


def format_group(g, category):
    lines = [f"{ICONS[category]} *{category.replace('_', ' ').title()}* — {g['title']} "
             f"({len(g['scenarios'])} scenario(s), confidence: {g['confidence']})"]
    if category == "defect":
        lines += [f"> *Expected:* {g['expected']}", f"> *Actual:* {g['actual']}",
                  f"> *Repro:* {g['repro']}", f"> <{g['evidence_url']}|Screenshot / report>"]
        if g.get("ticket"):
            lines.append(f"> Known issue: {g['ticket']}")
    else:
        lines += [f"> *Root cause:* {g['root_cause']}", f"> *Fix:* `{g['fix_location']}`"]
        if category == "intermittent":
            lines.append(f"> Passed on rerun · flake count: {g.get('flake_count', 1)}")
    return "\n".join(lines)


def post(channel_key, text):
    url = os.environ.get(f"SLACK_WEBHOOK_{channel_key}")
    if os.environ.get("DRY_RUN") or not url:
        print(f"--- [{channel_key}] ---\n{text}\n")
        return
    req = urllib.request.Request(url, data=json.dumps({"text": text}).encode(),
                                 headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=10)


def main(path):
    verdict = json.load(open(path))
    build = verdict["build"]
    buckets = {"AUTOMATION_QUICKFIX": [], "QA_MANUAL": []}
    counts = {}
    for g in verdict["groups"]:
        target, category = route_for(g)
        counts[category] = counts.get(category, 0) + 1
        msg = format_group(g, category)
        for key in (buckets if target == "BOTH" else [target]):
            buckets[key].append(msg)

    header = f"*Build #{build['number']}* · {build['suite']} · {build['env']} · <{build['report_url']}|report>"
    for key, msgs in buckets.items():
        if msgs:
            post(key, header + "\n\n" + "\n\n".join(msgs))

    summary = " · ".join(f"{ICONS[c]} {c.replace('_', ' ')}: {n}" for c, n in counts.items())
    post("BUILD_THREAD", f"AI triage done for #{build['number']} — {summary}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sample-verdict.json")
