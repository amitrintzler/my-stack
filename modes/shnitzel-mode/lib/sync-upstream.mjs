import { readFileSync, writeFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import { join } from 'node:path';

const [port, oldDir, newDir, output] = process.argv.slice(2);
const sync = await import(pathToFileURL(join(port, 'tools/sync.mjs')));
const gen = await import(pathToFileURL(join(port, 'tools/generate.mjs')));
const upstream = JSON.parse(readFileSync(join(port, 'tools/upstream.json')));
const spec = upstream.components.pstack;
const { substitutions, denylist } = sync.parseSubstitutions(JSON.parse(readFileSync(join(port, 'tools/substitutions.json'))));
const models = gen.loadModels(port);
const leads = gen.loadLeadLines(port);
const forks = sync.parseForks(JSON.parse(readFileSync(join(port, 'tools/forks.json'))), upstream.components).pstack;
const args = {
  oldDir, newDir, localDir: join(port, spec.localPath),
  rules: substitutions, denylist, exclude: spec.exclude, forks,
  derive: (rel, text) => gen.deriveSkill(join(spec.localPath, rel), text, models, leads)
};
const report = sync.syncComponent({ ...args, dryRun: true });
writeFileSync(output, JSON.stringify(report, (key, value) => value instanceof Map ? Object.fromEntries(value) : value, 2));
if (report.hits.length || report.undeclared.length || report.collisions.length || report.binaryConflicts.length) process.exit(1);
sync.syncComponent(args);
