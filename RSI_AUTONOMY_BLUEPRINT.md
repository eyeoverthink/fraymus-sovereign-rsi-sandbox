# SOVEREIGN UNION — RSI (RECURSIVE SELF-IMPROVEMENT), CONTINUITY & STRUCTURE PLAN

## 1. Why This Repository Exists (Breaking the Cloud Lock-In Ceiling)
Base44 apps (`creator-nexus` and `fraymus-transmuter`) excel at hosted UI and cloud functions, but they cannot natively run persistent local daemons, mutate their own git branches autonomously via CLI, or execute arbitrary local Makefiles.

This repository is the **Self-Contained Sovereign Workspace** where **Hermes**, **OpenClaw**, **GitHub Copilot**, and the **12-Agent Union** converge with **zero Base44 dependency**.

## 2. Directory & Continuity Structure
```text
├── index.html                                # Pass-3 Master 4D Spectral-Chromatic Sandbox (Zero-Dep HTML5/WebAudio/Canvas)
├── fraymus-kernel-4d.js                      # Pure ES Module: Bijective 4D Voxel (X.Y.Z:W) & DNA Codon Kernel
├── Makefile                                  # Unified CLI entrypoint for Hermes, OpenClaw, and Operator
├── continuity-capsule.json                   # Cryptographic Seed, 3-Pass Critique Scores & Yin Merkle Root
├── RSI_AUTONOMY_BLUEPRINT.md                 # This Recursive Self-Improvement & Architecture Plan
├── rsi/
│   └── hermes_openclaw_daemon.py             # Standalone Python 3 RSI & Gap-Filler Daemon
├── agents/
│   ├── union_roster.json                     # Portable 12-Agent Union Personas + Hermes/OpenClaw/Copilot Contracts
│   └── task_queue.json                       # Autonomous Backlog for Hermes, OpenClaw & Copilot
├── continuity/
│   └── witness_ledger.jsonl                  # Append-Only Side-by-Side Witness Log (Operator vs. Agent Union Decisions)
└── .github/
    ├── copilot-instructions.md               # Constitutional Laws & RSI Rules for GitHub Copilot
    └── workflows/
        └── autonomous-union-cron.yml         # Hourly GitHub Actions RSI & Integrity Verification Loop
```

## 3. The 5-Stage Recursive Self-Improvement (RSI) Loop
1. **Observe & Audit (`make verify`)**: Hermes / OpenClaw verifies `continuity-capsule.json`, `index.html`, and `fraymus-kernel-4d.js` hashes.
2. **Claim Gap (`agents/task_queue.json`)**: Agents select the highest-priority capability gap.
3. **Synthesize & Mutate**: Hermes, OpenClaw, or Copilot writes clean-room code or tests.
4. **Empirical Gate (`R_san`)**: Changes must pass `make verify` before commit; broken mutations are rolled back.
5. **Witness & Commit (`continuity/witness_ledger.jsonl`)**: Every step logs Operator Intent alongside the Agent Union's 4th-Wall decision.
