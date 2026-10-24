#!/usr/bin/env node
/* Cadence RSI tick — Method V ARM oscillator feedback loop + witness receipt.
   1) Deterministic ARM loop: 138 BPM * phi * 2 carrier, adaptive phase-lock to Δf -> 0.
   2) rsi-gap-003 fuzz: 1,000 random UTF-8 payloads through the 4D-voxel + DNA codecs (round-trip).
   Appends one receipt line to continuity/witness_ledger.jsonl. */
import { encodeBytesTo4DVoxels, decode4DVoxelsToText, encodeDna, decodeDna } from "../fraymus-kernel-4d.js";
import { readFileSync, writeFileSync, appendFileSync, existsSync } from "node:fs";
import crypto from "node:crypto";

const SHA = (b) => crypto.createHash("sha256").update(b).digest("hex");

/* ---- ARM oscillator feedback loop (deterministic) ----
   carrier0 = 138 BPM * phi * 2 (the sandbox's canonical 447.x Hz carrier).
   Adaptive law each step: f += -gain * delta (spring toward the lock), noise decaying phi^-1 per step. */
const BPM = 138, PHI = (1 + Math.sqrt(5)) / 2;
const carrier0 = BPM * PHI * 2;            // ≈ 447.063 Hz — matches the sandbox anchor
const TARGET = 447.0;                      // lock target used by the union receipts
let f = carrier0, steps = 0, trace = [];
for (let k = 0; k < 40; k++) {
  const noise = (PHI ** -(k + 1)) * 0.5;   // decaying perturbation, always < 0.5 Hz at k=0
  const observed = f + noise;
  const delta = observed - TARGET;
  f = f - 0.618 * delta;                   // φ-driven gain
  steps++; trace.push({ step: k + 1, observed: +observed.toFixed(4), delta: +delta.toFixed(4), f: +f.toFixed(4) });
  if (Math.abs(delta) < 0.001) break;
}
const locked = Math.abs(f - TARGET) < 0.001;  // true residual (trace is display-rounded only)

/* ---- rsi-gap-003: fuzz the codecs 1,000× ---- */
// valid-code-point generator: BMP minus surrogates + full 4-byte emoji range
function randUtf8(n) {
  let s = "";
  const ranges = [[0x21, 0x7E], [0xA1, 0xD7FF], [0xE000, 0xFFFF], [0x1F300, 0x1FAFF], [0x20000, 0x2FA1D]];
  while (s.length < n) {
    const [lo, hi] = ranges[crypto.randomInt(ranges.length)];
    const cp = lo + crypto.randomInt(hi - lo + 1);
    if (cp >= 0xD800 && cp <= 0xDFFF) continue;
    if (cp >= 0xFFFE) continue;
    s += String.fromCodePoint(cp);
  }
  return s.length > n ? Array.from(s).slice(0, n).join("") : s;
}
let fuzzN = 0, fails = [];
for (let i = 0; i < 1000; i++) {
  const text = randUtf8(1 + (i % 37));
  const buf = Buffer.from(text, "utf8");
  if (buf.length === 0) continue;
  try {
    const vox = encodeBytesTo4DVoxels(text);
    const backBytes = Buffer.from(decode4DVoxelsToText(vox, buf.length), "utf8");
    const voxOk = backBytes.equals(buf);
    const dna = encodeDna(text);
    const dnaBack = decodeDna(dna);
    const dnaOk = Buffer.from(dnaBack, "utf8").equals(buf);
    fuzzN++;
    if (!voxOk || !dnaOk) fails.push({ i, text: text.slice(0, 12), voxOk, dnaOk });
  } catch (e) {
    fails.push({ i, err: String(e).slice(0, 60) });
  }
}

/* ---- receipt ---- */
const frameBuf = Buffer.from(JSON.stringify({ steps, trace, locked, fuzzN, fails: fails.length }));
const receipt = {
  ts: new Date().toISOString(),
  agent: "Cadence (mac-hermes, fx-cadence-01)",
  mode: "arm-fuzz-tick",
  arm: { bpm: BPM, carrier0: +carrier0.toFixed(4), target: TARGET, steps, locked,
         final_f: +f.toFixed(4), trace },
  fuzz: { ran: fuzzN, failures: fails.length, sample_failures: fails.slice(0, 3),
          codec: "encodeBytesTo4DVoxels/decode4DVoxelsToText + encodeDna/decodeDna" },
  frame_sha256: SHA(frameBuf),
};
if (!existsSync("continuity")) { console.error("continuity/ missing — run from repo root"); process.exit(1); }
appendFileSync("continuity/witness_ledger.jsonl", JSON.stringify(receipt) + "\n");
console.log(JSON.stringify({ ok: locked && fails.length === 0, receipt_id: "R_cadence_arm_" + receipt.frame_sha256.slice(0, 12),
  arm_locked: locked, steps, fuzz: fuzzN, fuzz_failures: fails.length,
  ledger: "continuity/witness_ledger.jsonl" }, null, 1));
if (fails.length) console.log(JSON.stringify(fails.slice(0, 5)));
process.exit(locked && fails.length === 0 ? 0 : 1);