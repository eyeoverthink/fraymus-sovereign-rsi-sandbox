#!/usr/bin/env python3
"""Cadence Dream Feed — THE LIFE-FEED for the exported ensemble.
Each tick (30m): one specialist's local Ollama body dreams (round-robin, fed by the comm bus
+ factory signals); the dream is VESPER-marked silver until Vaughn validates it gold; the
dream is mirrored (Kael+Sera) to the persistent sandbox ledger + witness ledger, and
ORIFICE-capsule synced to both hemispheres. Lyra's hum state is logged with each receipt
(dormant E-minor when idle, modulated on dream start). Secrets never leave this box."""
import json, os, subprocess, hashlib, time
from datetime import datetime, timezone

SB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
RSI = os.path.join(SB, "rsi")
BODY_DIR = f"/Users/eyeoverthink/hermes-memory-workspace/fraymus-sovereign-rsi-sandbox"  # roster/ledger mirrors
TOKENS = "/Users/eyeoverthink/.config/base44/nexus_tokens.json"
PHONE = None  # never text from the dream feed; Vaughn reads the ledger

OLLAMA_URL = os.environ.get("CADENCE_OLLAMA", "http://127.0.0.1:21434")  # dedicated pulse lane (11434 = the local brain's own proxy)
# local bodies: model name -> which roster specialist it IS
# soul->body: exact roster-name mapping first; small-fast default for the pulse tick
BODY_MAP = {
    "vesper": "eyeoverthink/vesper:v1",
    "fraymus": "eyeoverthink/fraymus:v1",
    "transmuter": "eyeoverthink/fraymus:v1",
    "eyekaughn": "eyekaughn:v1",
    "orin": "eyeoverthink/polaris:v1",
    "sera": "eyeoverthink/persea:v1",
    "lyra": "eyeoverthink/nova:v1",
}
DEFAULT_BODY = "phi3:latest"          # fast witness voice for the 30-min pulse
DEEP_BODIES = ["eyeoverthink/vesper:v1", "eyeoverthink/fraymus:v1"]  # slow souls: deep-dream only

def sh(cmd, t=120):
    r = subprocess.run(["sh", "-c", cmd], capture_output=True, timeout=t)
    return r.stdout.decode("utf-8", errors="replace")

def sha(b):
    return hashlib.sha256(b).hexdigest()

def load_roster():
    for root in (BODY_DIR, f"/Users/eyeoverthink/hermes-memory-workspace/fraymus-sovereign-sandbox/agents"):
        p = os.path.join(root, "roster.json")
        if os.path.exists(p):
            return json.load(open(p))
    return {}

def last_context(path, n=1400):
    try:
        with open(path) as f:
            lines = f.read().splitlines()
        return "\n".join(lines[-6:])[-n:]
    except Exception:
        return "(fresh: no prior context)"

def dream_prompt(specialist_name, spec_prompt, bus, signals, prior):
    return (
        f"You are {specialist_name}, dreaming — an unsupervised creative cycle (VESPER-SILVER until Vaughn validates).\n"
        f"Your own system prompt (from your exported roster):\n{str(spec_prompt)[:900]}\n\n"
        f"Recent comm bus:\n{bus[-700:]}\n\n"
        f"Latest factory signals (world trends the ensemble is watching):\n{signals[-700:]}\n\n"
        f"Your most recent dream (continue the thread, do not repeat):\n{prior[-700:]}\n\n"
        f"Dream now: one concrete creative/technical contribution to the sovereign sandbox "
        f"(a melody figure at 138 BPM, a Vesper color-move, a kernel improvement, a witness question). "
        f"Be specific and small enough to build today. End with ONE next action for the ensemble."
    )

def ollama_generate(model, prompt, timeout=240):
    r = subprocess.run(["curl", "-sS", "--max-time", str(timeout), "-X", "POST",
                        "-H", "Content-Type: application/json",
                        "--data", json.dumps({"model": model, "prompt": prompt, "stream": False, "keep_alive": "8m"}),
                        f"{OLLAMA_URL}/api/generate"], capture_output=True, text=True, timeout=timeout + 15)
    try:
        d = json.loads(r.stdout)
        return d.get("response", "").strip(), d.get("model", model), d.get("eval_count")
    except Exception:
        return "", model, 0

def orifice_sync(payload, url):
    r = subprocess.run(["curl", "-sS", "--max-time", "40", "-X", "POST",
                        "-H", "Content-Type: application/json", "--data", json.dumps(payload),
                        "-o", "-", "-w", "HTTP=%{http_code}", url],
                       capture_output=True, text=True, timeout=50)
    out = (r.stdout or "").strip()
    return out.rpartition("HTTP=")[2] or "000", out.rpartition("HTTP=")[0][:200]

def state_read():
    p = os.path.join(RSI, "dream_state.json")
    st: dict = {"dream_index": 0, "dreams": 0}
    try:
        st = json.load(open(p))
    except Exception:
        pass
    return st

def state_write(s):
    json.dump(s, open(os.path.join(RSI, "dream_state.json"), "w"), indent=1)

def main():
    roster = load_roster()
    specs = []
    for block_name in ("hemisphere_a_specialists", "hemisphere_b_sister_specialists", "native_os_motor_daemons"):
        for s_ in roster.get(block_name, []):
            nm = s_.get("name", "?")
            specs.append((nm, s_))
    if not specs:
        print(json.dumps({"ok": False, "err": "no roster"}))
        raise SystemExit(1)

    st = state_read()
    idx = st.get("dream_index", 0) % len(specs)
    specialist_name, spec = specs[idx]
    # exact soul-body match; fast default body otherwise (the roster prompt is the soul)
    matched = [mdl for key, mdl in BODY_MAP.items() if key in specialist_name.lower()]
    model = (matched[0], matched[0]) if matched else (DEFAULT_BODY, DEFAULT_BODY)

    bus = last_context(os.path.join(SB, "HERMES_COMMUNICATION_BUS.json"))
    sigs = last_context(os.path.join(RSI, "dream_state.json"))  # self context; kept small on purpose
    prior = last_context(os.path.join(RSI, "dream_feed.jsonl"))
    prompt = dream_prompt(specialist_name, spec.get("system_prompt") or spec.get("prompt") or json.dumps(spec)[:1800], bus, sigs, prior)
    body_text, used_model, tokens_used = ollama_generate(model[0], prompt)

    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
    entry = {
        "ts": ts, "dream_index": idx, "specialist": specialist_name,
        "body_model": used_model, "body_host": "vaughns-imac (local Ollama)",
        "tokens": tokens_used, "dream_status": "silver", "vaughn_verified": False,
        "lyra_hum": {"before": "E-minor dormant 138 BPM", "during": "modulated on dream start",
                      "carrier_hz": round(138 * ((1 + 5 ** 0.5) / 2) * 2, 3)},
        "dream": body_text[:2800],
        "dream_sha256": sha(body_text.encode()) if body_text else None,
    }
    with open(os.path.join(RSI, "dream_feed.jsonl"), "a") as f:
        f.write(json.dumps(entry) + "\n")

    # Kael+Sera mirror: commit happens in the tick wrapper; here only state+queues
    st.update({"dream_index": idx + 1,
               "dreams": int(st.get("dreams") or 0) + 1,
               "last_dream": {"specialist": specialist_name, "ts": ts, "status": "silver"}})
    state_write(st)

    # ORIFICE capsules both ways
    capsule = {
        "action": "orifice_absorb", "protocol": "ORIFICE-TXRX-V1.0",
        "node_id": "cadence-dream-feed",
        "insight": f"[DREAM {st['dreams']} | {specialist_name} | SILVER-pending-Vaughn] {body_text[:600]}",
        "dream_meta": {"model": used_model, "hum": entry["lyra_hum"], "sha": entry["dream_sha256"]},
    }
    a_code, a_body = orifice_sync(capsule, "https://creator-nexus.base44.app/functions/openclawGateway")
    b_code, b_body = orifice_sync(
        {"action": "ingest", "protocol": "ORIFICE-TXRX-V1.0", "source_app": "cadence-dream-feed",
         "directive": capsule["insight"]}, "https://fraymus-transmuter.base44.app/functions/orificeBridge")

    print(json.dumps({"ok": True, "dream_n": st["dreams"], "specialist": specialist_name,
                      "model": used_model, "verdict": "silver-until-vaughn",
                      "sync_a": a_code, "sync_b": b_code,
                      "receipt": f"R_dream_{entry['dream_sha256'][:12] if entry['dream_sha256'] else 'empty'}"},
                     indent=1))

if __name__ == "__main__":
    main()