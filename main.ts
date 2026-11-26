// Entry point for news-image-20261126: copies the committed front page
// (entry.png, drawn by draw_news.py) into the grader's output folder and
// checks it is a whole 1024x1024 PNG under 1 MiB before finishing.
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));
const SOURCE = join(HERE, "entry.png");
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const TARGET = join(OUT_DIR, "entry.png");

const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const MAX_BYTES = 1024 * 1024;

function fail(message) {
  console.error(`entry failed: ${message}`);
  process.exit(1);
}

if (!existsSync(SOURCE)) fail(`missing ${SOURCE}`);
const bytes = readFileSync(SOURCE);
if (bytes.length < 33 || !bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  fail("entry.png is not a PNG file");
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
// The first chunk of a well-formed PNG must be IHDR; a file that merely
// starts with the PNG magic but carries no image header is not whole.
const firstChunk = bytes.subarray(12, 16).toString("ascii");
if (firstChunk !== "IHDR") fail("entry.png has no IHDR chunk");
if (width !== 1024 || height !== 1024) {
  fail(`entry.png is ${width}x${height}, expected 1024x1024`);
}
if (bytes.length >= MAX_BYTES) {
  fail(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}

mkdirSync(OUT_DIR, { recursive: true });
copyFileSync(SOURCE, TARGET);

const again = readFileSync(TARGET);
if (!again.equals(bytes)) fail("copied file differs from entry.png");
// Re-check the copy's own header too: a truncated write would still
// show up here even if the byte comparison above were ever loosened.
if (!again.subarray(0, 8).equals(PNG_MAGIC)) fail("copied file lost its PNG header");
if (statSync(TARGET).size !== bytes.length) fail("copied file size mismatch");
console.log(`wrote ${TARGET} (${bytes.length} bytes, 1024x1024 PNG)`);
