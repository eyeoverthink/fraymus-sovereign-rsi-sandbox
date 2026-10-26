// fraymus-kernel-4d.js — Zero-Dependency 4D Spatial-Chromatic & DNA Reversible Kernel
// 100% Standalone (Zero Base44 / Zero External NPM Dependencies)
// Anchored to Yin Merkle Root: f8b7118fdaec86aa

export const CODONS = ['A', 'C', 'G', 'T'];

export function encodeBytesTo4DVoxels(text) {
  const bytes = new TextEncoder().encode(String(text || ''));
  const voxels = [];
  for (let i = 0; i < bytes.length; i += 4) {
    const b0 = bytes[i] ?? 0;
    const b1 = bytes[i + 1] ?? 0;
    const b2 = bytes[i + 2] ?? 0;
    const b3 = bytes[i + 3] ?? 0;
    const w = Math.floor((b3 / 255) * 99);
    const freqHz = Math.round((b0 / 255) * 880 + 110);
    voxels.push({
      index: voxels.length,
      bytes: [b0, b1, b2, b3],
      coord4D: `${b0}.${b1}.${b2}:${w}`,
      rgba: `rgba(${b0},${b1},${b2},${(b3 / 255).toFixed(3)})`,
      freqHz,
    });
  }
  return voxels;
}

export function decode4DVoxelsToText(voxels, originalByteLength) {
  const out = [];
  for (const v of voxels || []) {
    if (Array.isArray(v.bytes)) {
      out.push(...v.bytes);
    }
  }
  const sliced = typeof originalByteLength === 'number' ? out.slice(0, originalByteLength) : out;
  return new TextDecoder().decode(new Uint8Array(sliced)).replace(/\x00+$/g, '');
}

export function encodeDna(text) {
  const bytes = new TextEncoder().encode(String(text || ''));
  let dna = '';
  for (const b of bytes) {
    dna += CODONS[(b >> 6) & 3] + CODONS[(b >> 4) & 3] + CODONS[(b >> 2) & 3] + CODONS[b & 3];
  }
  return dna;
}

export function decodeDna(dna) {
  const clean = String(dna || '').replace(/[^ACGT]/g, '');
  const out = new Uint8Array(Math.floor(clean.length / 4));
  for (let i = 0; i < out.length; i++) {
    const b0 = CODONS.indexOf(clean[i * 4]);
    const b1 = CODONS.indexOf(clean[i * 4 + 1]);
    const b2 = CODONS.indexOf(clean[i * 4 + 2]);
    const b3 = CODONS.indexOf(clean[i * 4 + 3]);
    out[i] = ((b0 & 3) << 6) | ((b1 & 3) << 4) | ((b2 & 3) << 2) | (b3 & 3);
  }
  return new TextDecoder().decode(out);
}
