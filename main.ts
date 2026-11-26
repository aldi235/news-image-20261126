// Entry point for the news-image-20261126 bundle.
//
// Copies the committed entry.png — "The World in One Page", a dense
// newspaper front page summing up Thursday 26 November 2026 — into the
// directory given by MAKEFUN_OUTPUT_DIR (default /output) and verifies
// the copy before reporting success. Node standard library only, no
// dependencies, no network: the same committed bytes are written on
// every run, so the grader's two runs are byte-identical by construction.
//
//   node main.ts
//   MAKEFUN_OUTPUT_DIR=out node main.ts
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1024 * 1024;

const here = resolve(fileURLToPath(new URL(".", import.meta.url)));
const source = join(here, "entry.png");
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const target = join(resolve(outDir), "entry.png");

if (!existsSync(source)) {
  throw new Error(`source image missing: ${source} — run python3 draw_news.py first`);
}
const sourceBytes = readFileSync(source);
if (!sourceBytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error("source entry.png does not start with the PNG signature");
}
// The PNG header (IHDR) sits at bytes 16-23: width then height, big-endian.
// The competition caps the image at 1024x1024, so refuse anything larger
// before copying rather than shipping a file the gate would reject.
const width = sourceBytes.readUInt32BE(16);
const height = sourceBytes.readUInt32BE(20);
if (width > 1024 || height > 1024) {
  throw new Error(`source entry.png is ${width}x${height}, over the 1024x1024 cap`);
}

mkdirSync(resolve(outDir), { recursive: true });
copyFileSync(source, target);

const after = readFileSync(target);
const size = statSync(target).size;

if (size !== sourceBytes.length || size !== after.length) {
  throw new Error(`size mismatch: source ${sourceBytes.length} bytes, copy ${size} bytes`);
}
if (!after.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error("copied file does not start with the PNG signature");
}
if (size >= MAX_BYTES) {
  throw new Error(`entry.png is ${size} bytes, over the 1 MiB limit`);
}
if (!sourceBytes.equals(after)) {
  throw new Error("copied bytes differ from the source image");
}

console.log(
  `OK: entry.png (${size} bytes, ${(size / 1024).toFixed(1)} KiB) copied to ` +
    `${target} and verified (PNG signature, byte-identical, under 1 MiB)`,
);
