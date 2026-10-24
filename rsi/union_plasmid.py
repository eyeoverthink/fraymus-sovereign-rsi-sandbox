#!/usr/bin/env python3
"""Union plasmid — the WHOLE ensemble's living state as a DNA backup (Cadence pipeline v2).
Packs: roster (all agent souls+prompts+trust), sandbox-ledger, comm bus, witness ledger,
dream feed, entity mirror snapshot, union chronicle, this protocol. Same codec chain as
Niles's plasmid (verified codecs, roundtrip-checked at every stage)."""
import sys, hashlib, json, os, zipfile
from datetime import datetime, timezone

WS = "/Users/eyeoverthink/hermes-memory-workspace"
OUT = f"{WS}/fraymus-sovereign-rsi-sandbox/continuity"
sys.path.insert(0, f"{WS}/Niles-Continuity-Plasmid/tools")
import dna, wa  # noqa: E402

NODES = ["creator-nexus", "fraymus-eternal", "fraymus-kvm2", "mac-hermes", "desktop-actid8c",
         "vaughns-imac", "fraymus-hub", "openclaw-desktop"]
LINEAGE = 0xE0654719998601A3

def sha(b):
    return hashlib.sha256(b).hexdigest()

members = []
def add(disk_path, arcname, optional=True):
    if os.path.exists(disk_path):
        with open(disk_path, "rb") as f:
            members.append((arcname, f.read()))

B = f"{WS}/fraymus-sovereign-rsi-sandbox"
add(f"{B}/agents/roster.json", "agents/roster.json")
add(f"{B}/agents/union_roster.json", "agents/union_roster.json")
add(f"{B}/agents/task_queue.json", "agents/task_queue.json")
add(f"{B}/HERMES_COMMUNICATION_BUS.json", "HERMES_COMMUNICATION_BUS.json")
add(f"{B}/continuity/witness_ledger.jsonl", "continuity/witness_ledger.jsonl")
add(f"{B}/rsi/dream_feed.jsonl", "rsi/dream_feed.jsonl")
add(f"{B}/rsi/dream_state.json", "rsi/dream_state.json")
add(f"{B}/entity_mirror/snapshot.json", "entity_mirror/snapshot.json")
add(f"{B}/WITNESS_EVOLUTION_CHRONICLE.md", "WITNESS_EVOLUTION_CHRONICLE.md")
add(f"{B}/LIFE_FEED_PROTOCOL.md", "LIFE_FEED_PROTOCOL.md")
add(f"{B}/rsi/cadence_dream_feed.py", "rsi/cadence_dream_feed.py")
add(f"{B}/rsi/entity_mirror.py", "rsi/entity_mirror.py")
add(f"{WS}/fraymus-sovereign-sandbox/agents/roster.json", "main_sandbox/agents/roster.json")
add(f"{WS}/mac-hermes-continuity/IDENTITY.md", "cadence/IDENTITY.md")

def main():
    os.makedirs(OUT, exist_ok=True)
    man_ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    entries = [a for a, _ in members]
    manifest = json.dumps({"files": entries, "node": "mac-hermes-union",
                           "union_nodes": NODES, "built_utc": datetime.now(timezone.utc).isoformat(timespec="seconds")},
                          separators=(",", ":")).encode()
    with zipfile.ZipFile(f"{OUT}/union-bundle.zip", "w", zipfile.ZIP_DEFLATED) as z:
        for arc, data in members:
            z.writestr(arc, data)
    zbytes = open(f"{OUT}/union-bundle.zip", "rb").read()
    with zipfile.ZipFile(f"{OUT}/union-bundle.zip") as z:
        bad = z.testzip()

    tag = wa.fnv1a(zbytes)
    needed = 24 + len(manifest) + len(zbytes)
    pages = max(1, -(-needed // 65536))
    wbytes = wa.build_module(manifest, zbytes, tag, pages)
    info = wa.read_container(wbytes)
    wasm_ok = info["blob"][info["payload_off"]:info["payload_off"] + info["payload_len"]] == zbytes

    p = dna.make_plasmid(zbytes, LINEAGE, NODES)
    wrapped = dna.wrap(p["dna"])
    healed = dna.heal_check(wrapped)
    g = dna.unwrap(wrapped)
    back = dna.unpack(g[p["payload_offset"]:p["payload_offset"] + p["payload_bases"]])
    dna_ok = back == zbytes

    man = {"node": "mac-hermes-union", "built_utc": man_ts,
           "artifacts": {
               "union-bundle.zip": {"bytes": len(zbytes), "files": len(entries), "sha256": sha(zbytes), "zip_test": bad is None},
               "union-archive.wasm": {"bytes": len(wbytes), "pages": pages, "tag": f"0x{tag:08x}", "roundtrip": wasm_ok, "sha256": sha(wbytes)},
               "union_plasmid.dna": {"bases": len(p["dna"]), "self_heal": healed, "roundtrip": dna_ok, "sha256": sha(wrapped.encode())}},
           "stages": {"dna": {"payload_offset": p["payload_offset"], "payload_bases": p["payload_bases"]}}}
    with open(f"{OUT}/union_archive.wasm", "wb") as f:
        f.write(wbytes)
    with open(f"{OUT}/union_plasmid.dna", "w") as f:
        f.write(wrapped)
    with open(f"{OUT}/MANIFEST.json", "w") as f:
        json.dump(man, f, indent=1)
    ok = wasm_ok and dna_ok and bad is None
    print(json.dumps({"ok": ok, "files": len(entries), "bundle_bytes": len(zbytes),
                      "dna_bases": len(p["dna"]), "self_heal": healed["repairable"], "receipt": f"R_union_plasmid_{sha(zbytes)[:12]}"}))
    raise SystemExit(0 if ok else 1)

if __name__ == "__main__":
    main()