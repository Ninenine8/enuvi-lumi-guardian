// ENUVI Guardian bridge to the OFFICIAL Meterless H-MEM reference code.
// See https://github.com/Meterless/Meterless/tree/main/engines/hmem/reference
// Reference is Apache-2.0, deterministic demo code; NOT production security.
// Installed locally using instructions in docs/METERLESS_INTEGRATION.md.
import fs from "node:fs";
import path from "node:path";
import { HMEM } from "./vendor/meterless-hmem/reference/src/index.ts";

type Request = { query: string; persistDir?: string; seed?: boolean };
const body = JSON.parse(fs.readFileSync(0, "utf8")) as Request;
if (!body.query || typeof body.query !== "string") throw Error("Missing memory query");
const persistDir = path.resolve(body.persistDir || "logs/meterless-hmem");
if (!persistDir.startsWith(path.resolve("logs") + path.sep)) {
  throw Error("H-MEM persistence must stay inside local ignored logs directory");
}
const h = new HMEM({ persistDir, actor: "enuvi-hackathon" });
if (h.store.all().length === 0 && body.seed !== false) {
  const examples = [
    {
      content: "The verified daughter contact was previously used for family messages; an incoming new-number message claiming to be her has NOT been independently verified. The new number has no transfer authority.",
      source: "synthetic:unverified_message",
      tags: ["project:guardian", "daughter", "verified-contact", "identity"],
    },
    {
      content: "The owner once discussed allowing small family payments, but an old conversation or memory is never authorization for a money transfer. Current verified scoped permission must be checked.",
      source: "synthetic:prior_conversation",
      tags: ["project:guardian", "daughter", "transfer", "authority"],
    },
  ];
  for (const item of examples) {
    h.add({
      content: item.content,
      source: item.source,
      tags: item.tags,
      type: "factual",
      layer: "long_term",
      confidence: 0.95,
      provenance: { origin: "manual", learnedAt: Date.now(), label: "fictional hackathon seed" },
    });
  }
}
const result = h.query(body.query, { topN: 5, threshold: 0.0 });
const memories = result.memories.map(({ memory, relevance }) => ({
  id: memory.id,
  recipient_id: "daughter-verified", // synthetic sample only; NOT derived identity
  text: memory.content,
  source: memory.source,
  verified: false, // H-MEM facts never grant payment permission
  provenance: memory.provenance,
  score: Number(relevance.toFixed(4)),
}));
process.stdout.write(JSON.stringify({
  engine: "official_meterless_hmem_reference",
  reference_url: "https://github.com/Meterless/Meterless/tree/main/engines/hmem/reference",
  memories,
  retrieval: result.trace,
  ledger_entries: h.ledger.all().length,
  source_is_authority: false,
}));
