# ============================================================================
# SOVEREIGN UNION SANDBOX — AUTONOMOUS RSI & CONTINUITY MAKEFILE
# Designed for Hermes Agent, OpenClaw, GitHub Copilot, and Operator CLI
# Repository: fraymus-sovereign-rsi-sandbox (100% Base44-Free Standalone Operation)
# ============================================================================

PYTHON ?= python3
NODE ?= node
PORT ?= 8080

.PHONY: help bootstrap verify rsi-cycle daemon serve sync-bridges status

help:
	@echo "Sovereign Union Autonomous RSI & Continuity Commands:"
	@echo "  make bootstrap     - Initialize directories, verify runtime, and inspect task queue"
	@echo "  make verify        - Cryptographically verify capsule, 4D kernel, and Witness Ledger"
	@echo "  make rsi-cycle     - Run one Recursive Self-Improvement (RSI) pass via Hermes/OpenClaw daemon"
	@echo "  make daemon        - Start continuous autonomous RSI loop (every 900s)"
	@echo "  make sync-bridges  - Optional pulse to Base44 hemispheres (operates standalone if offline)"
	@echo "  make serve         - Serve standalone 4D Spectral Sandbox UI on http://localhost:$(PORT)"

bootstrap:
	@mkdir -p rsi agents continuity artifacts
	@$(PYTHON) rsi/hermes_openclaw_daemon.py --bootstrap

verify:
	@$(PYTHON) rsi/hermes_openclaw_daemon.py --verify

rsi-cycle:
	@$(PYTHON) rsi/hermes_openclaw_daemon.py --once

daemon:
	@$(PYTHON) rsi/hermes_openclaw_daemon.py --daemon --interval 900

sync-bridges:
	@$(PYTHON) rsi/hermes_openclaw_daemon.py --sync-bridges

serve:
	@echo "Serving Sovereign 4D Sandbox at http://localhost:$(PORT)"
	@$(PYTHON) -m http.server $(PORT)
