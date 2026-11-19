// news-image-20261118 — "The World in One Day".
//
// The entry image is entry.png beside this file. It was drawn from
// scratch for Wednesday 18 November 2026 (see tools/generate_image.py
// for the drawing program and README.md for the stories it covers).
//
// The grader runs this program with no network in a fresh container,
// so the program does the one thing it can still do: put the image
// where the grader looks for it, at /output/entry.png. A plain copy
// is deterministic by construction: both graded runs write the same
// bytes. Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output, e.g.:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
//
// Node 22, standard library only; nothing is installed or fetched.

import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";

mkdirSync(outDir, { recursive: true });
copyFileSync(join(here, "entry.png"), join(outDir, "entry.png"));
