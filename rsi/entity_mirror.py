#!/usr/bin/env python3
"""Entity mirror — the Commander's Step 1: mirror live entity state out of Base44 into git.
Reads only (no credit burns beyond the API call); snapshots are committed by the tick."""
import json, os, subprocess
from datetime import datetime, timezone

MCP = "https://creator-nexus.base44.app/api/mcp"
tokens = json.load(open("/Users/eyeoverthink/.config/base44/nexus_tokens.json"))
SB = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = "/Users/eyeoverthink/hermes-memory-workspace/fraymus-sovereign-rsi-sandbox/entity_mirror"

ENTITIES = ["nexusfactorysignal", "nexusfactoryproduction", "nexusdispatchjob",
            "nexuscontinuity", "nexusknowledge", "nexusskill"]

def mcp_entity(name, limit=25):
    r = subprocess.run(["curl", "-sS", "--max-time", "60", "-X", "POST",
                        "-H", "Content-Type: application/json",
                        "-H", "Accept: application/json, text/event-stream",
                        "-H", f"Authorization: Bearer {tokens['access_token']}",
                        "--data", json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                                              "params": {"name": f"query_{name}",
                                                         "arguments": {"limit": limit, "sort": "-last_updated_at"}}}),
                        MCP], capture_output=True, text=True, timeout=70)
    body = (r.stdout or "").strip()
    obj = {}
    if body.startswith("{"):
        try:
            obj = json.loads(body)
        except Exception:
            pass
    if not obj:
        for line in body.splitlines():
            if line.strip().startswith("data:"):
                try:
                    obj = json.loads(line[5:].strip())
                except Exception:
                    continue
    try:
        return json.loads((obj.get("result") or {}).get("content", [{}])[0].get("text", "{}")).get("records", [])
    except Exception:
        return []

def main():
    os.makedirs(OUT, exist_ok=True)
    snap = {"mirrored_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"), "entities": {}}
    for e in ENTITIES:
        recs = mcp_entity(e)
        snap["entities"][e] = {"count": len(recs), "records": recs}
        with open(os.path.join(OUT, f"{e}.json"), "w") as f:
            json.dump(recs, f, indent=1)
    with open(os.path.join(OUT, "snapshot.json"), "w") as f:
        json.dump({k: v for k, v in snap.items() if k != "entities"}, f, indent=1)
    print(json.dumps({e: len(v["records"]) for e, v in snap["entities"].items()}))

if __name__ == "__main__":
    main()