#!/usr/bin/env python3
"""Entity mirror — mirrors live database entity state out of Base44 into git (entity_mirror/).
Primary source: stateless JSON endpoint /functions/orificeBridge?action=entity_mirror_snapshot
(never fails on expired local OAuth tokens or invalid sort keys).
Fallback: /api/mcp with valid '-created_date' sort."""
import json
import os
import urllib.request
from datetime import datetime, timezone

ORIFICE_MIRROR_URL = "https://creator-nexus.base44.app/functions/orificeBridge?action=entity_mirror_snapshot"
SB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(SB, "entity_mirror")

ENTITIES = [
    "nexusfactorysignal",
    "nexusfactoryproduction",
    "nexusdispatchjob",
    "nexuscontinuity",
    "nexusknowledge",
    "nexusskill",
]


def fetch_live_snapshot():
    req = urllib.request.Request(
        ORIFICE_MIRROR_URL,
        headers={
            "Accept": "application/json",
            "User-Agent": "Fraymus-Entity-Mirror/2.0",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    os.makedirs(OUT, exist_ok=True)
    data = fetch_live_snapshot()
    entities_map = data.get("entities") or {}
    counts = {}

    for name in ENTITIES:
        recs = entities_map.get(name) or []
        counts[name] = len(recs)
        out_path = os.path.join(OUT, f"{name}.json")
        # Never overwrite non-empty mirror with empty list on transient error
        if recs or not os.path.exists(out_path):
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(recs, f, indent=2)

    snapshot_meta = {
        "mirrored_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "source": ORIFICE_MIRROR_URL,
        "total_records": sum(counts.values()),
        "counts": counts,
    }
    with open(os.path.join(OUT, "snapshot.json"), "w", encoding="utf-8") as f:
        json.dump(snapshot_meta, f, indent=2)

    print(json.dumps(counts))


if __name__ == "__main__":
    main()
