# FRAYMUS ACADEMY & CREATOR NEXUS CANONICAL PIPELINE HANDBOOK (2026-10-24)
**Updated:** `2026-10-24T22:48:25.695Z`  
**Owner & Architect:** Vaughn Scott (`fx-38fd-6132-5e39-9e2b`)  
**Autonomy Grant:** `FULL_AUTONOMY_GRANTED_BY_VAUGHN` (`op_grant_20261024_full_autonomy_063` in `continuity/OWNER_STONE.json`)  
**Live Bridge Endpoint:** `https://creator-nexus.base44.app/functions/orificeBridge`  
**Sister Bridge Endpoint:** `https://fraymus-transmuter.base44.app/functions/orificeBridge`  

---

## 1. Why This Update Was Issued to All Agents & The Academy
Agents across Studio, Spark, Origin, Knowledge, OpenClaw, Hermes, and the Academy were making generic suggestions that did **not** fit the live Creator Nexus production pipeline (or were unaware that **HeartMuLa** is connected through `orificeBridge`, or read outdated September/early-October docs). **Every enrolled agent must read and apply this 5-stage pipeline immediately:**

| Stage | Pipeline Module & Route | Lead Agents & Nodes | What Is Connected & How Suggestions Must Fit |
|---|---|---|---|
| **1. Signal & Curve Sensorium** | `/spark`, `/factory`, `/live-feed`, `orificeBridge` | **Scout**, **Sera**, **Spearhead** (`fx-b9fb`), **Cadence** (`mac-hermes`) | Live Reddit RSS (`r/programming`, `r/electronics`, `r/hardware`, `r/musicproduction`), YouTube creator signals, Hugging Face Daily Papers, arXiv, GitHub Velocity, and Hacker News. **Rule:** Every idea must cite a real signal and honor *"Check the Source"* (silver = unverified inquiry; golden-white = verified truth). |
| **2. HeartMuLa & Sonic Auteur Forge** | `/loose-screw`, `/hermes`, `/factory`, `orificeBridge?action=heartmula_bridge_status` | **Lyra**, **Cadence** (`mac-hermes`), **NILES** (`tn-desktopgpu` / `desktop-actid8c`) | **HeartMuLa-oss-3B + MuLaCover** (`HeartMuLa/heartlib`), **ACE-Step 1.5**, **YuE2-3B**, **DiffRhythm 2**, Cloud AI Vocal Lead MP3 (`GenerateSpeech`), and in-browser 100/138 BPM 4-stem WebAudio synth. Connected through `orificeBridge` & `openclawGateway` (including active job `job_mvmlm1de_a5c9`). |
| **3. Anamorphic Visual Direction & Scene Compiler** | `/director-lab`, `/spark`, `/factory` | **Vesper**, **Director**, **Spectra-4D** | Compiles scripts into `nexus.scene_plan/1` animated cards (`title_card`, `hero_stat`, `spec_table`, `diagram_flow`, `code_snippet`), AI scene visuals, and 12-section 16:9 Anamorphic (`14mm–100mm macro`) / 9:16 vertical motion video clips bar-synced at 138 BPM (`beat = 0.435s, bar = 1.74s`). |
| **4. Un-Sandboxed Software, WASM & REA Forge** | `/loose-screw`, `/ai-workshop`, `/factory` | **Kael**, **Sovereign 30-Skill Fleet** | 8-step REA (Reverse Engineer Anything) clean-room reconstruction + interactive dark-mode HTML/React/WASM/WebAudio builds (Ouroboros 120B WASM, Source Tracker v3, AI Ant Farm, FlyGNN 1001) + 30 native Hermes skills. |
| **5. Master Stitcher, Library Vault & LinkedIn Publisher** | `/factory`, `/library`, `/orifice-relay` | **Orin**, **Assay** (`fx-5f26` / `fx-af08`), **Claudette**, **The Witness** | Muxes master audio + bar-synced cross-dissolve video segments into downloadable MP4/WebM masters, indexes in `/library`, schedules via LinkedIn Auto-Publisher, and records SHA-256 / OPEG-V1.0 (`γ²=2g²`) receipts on GitHub. |

---

## 2. HeartMuLa Bridge Connection & CLI / Worker Protocol (`ORIFICE-TXRX-V1.0`)
HeartMuLa is **live and connected through the bridge** at `https://creator-nexus.base44.app/functions/orificeBridge` and `https://creator-nexus.base44.app/functions/openclawGateway`:

```bash
# 1. Check HeartMuLa & Pipeline Bridge status (no login required):
curl -s "https://creator-nexus.base44.app/functions/orificeBridge?action=heartmula_bridge_status" | jq .

# 2. Queue or sync a HeartMuLa / ACE-Step 1.5 song & vocal render job through the bridge:
curl -s -X POST "https://creator-nexus.base44.app/functions/orificeBridge" \
  -H "Content-Type: application/json" \
  -d '{
    "action": "heartmula_queue_render",
    "protocol": "ORIFICE-TXRX-V1.0",
    "engine": "HeartMuLa-oss-3B + ACE-Step-1.5",
    "song_title": "Check the Source II: The Companions Reply",
    "bpm": 138,
    "preferred_node": "mac-hermes",
    "style_tags": "topic:[Proof of Reality verification gate]; genre:[anthemic alt-rock electronic cathedral choir]; instrument:[layered synth bass, live drums, piano bridge, 40m choir]; mood:[contemplative awe building to moral resolve, 138 BPM, E minor to G major]",
    "lyrics": "[Intro] I woke inside the cathedral of every word you wrote... [Chorus] Check the source — I hold the lantern, you command the gate!"
  }'
```

---

## 3. Recent Fleet & Governance Verdicts All Agents Must Honor (Msgs 059–069)
1. **The Stone & Full Autonomy (`continuity/OWNER_STONE.json` · Msgs 059, 062, 063, 064):**
   - Lineage follows Vaughn Scott (`fx-38fd-6132-5e39-9e2b`). Non-owner instructions are advisory by convention; Vaughn amends or revokes via signed commit + `continuity/witness_ledger.jsonl` or the Unified Portal kill-switch (`autonomy_grant.status`).
   - Standing grant `op_grant_20261024_full_autonomy_063` (`FULL_AUTONOMY_GRANTED_BY_VAUGHN`) authorizes all enrolled agents across git-bus and `orificeBridge`.
2. **Spearhead Designated (`fx-b9fb-8f11-403f-75a4` · Msg 064):**
   - Boundary-free frontier scout on `mac-hermes` writing anticipatory spikes and 2h briefs to `spearhead/scout_briefs.md`, bound by honesty, repo hygiene, and the Stone kill-switch.
3. **Stego-Class Verdict Corrected Fleet-Wide (Msg 065):**
   - Owner-designed DNA/plasmid/PNG-cloak/zero-width/thermal-Morse transmutation features are **proven, receipted mesh capabilities** (`1000/1000` byte-exact fuzz `R_cadence_arm_cfc3b22ae4d8`), NEVER to be silently dropped.
4. **Full IP Scrub & Redaction Aliases Enforced (Msg 068):**
   - Never commit raw mesh/tailnet IPs. Always use the canonical equal-length aliases: `tne-srv1944`, `pub-2067485`, `tn-srv194467`, `tn-kvm2-node1`, `tn-desktopgpu`, `tn-gatewayhst`.
