#!/usr/bin/env node
const fs = require('fs');
const os = require('os');
const path = require('path');
const { spawnSync } = require('child_process');
const pkg = require('../package.json');

const repoRoot = path.resolve(__dirname, '..');
const skillsRoot = path.join(repoRoot, 'skills');
const packagesRoot = path.join(repoRoot, 'packages');

function usage() {
  console.log(`Glassroom CLI v${pkg.version}

Structured intelligence analysis workflow core and OpenClaw integration surface.

Current commands:
  glassroom --help
  glassroom --version
  glassroom version
  glassroom list-skills [--json]
  glassroom install openclaw [--mode auto|copy|symlink] [--skills a,b,c] [--target <dir>] [--force]
  glassroom install project  [--mode auto|copy|symlink] [--skills a,b,c] [--target <dir>] [--force]
  glassroom assemble case --out-json <file> [--out-md <file>] [--base-case <file>] [--source-card <file>] [--bias-analysis <file>] [--mitigation-pack <file>] [--structured-analysis <file>]

Planned analysis commands:
  glassroom init
  glassroom ingest source
  glassroom analyze bias
  glassroom analyze structured
  glassroom render html

Defaults:
  install openclaw -> ~/.openclaw/workspace/skills
  install project  -> <current working directory>/skills
  mode auto        -> symlink on Unix, copy on Windows
`);
}

function listSkillNames() {
  if (!fs.existsSync(skillsRoot)) return [];
  return fs.readdirSync(skillsRoot, { withFileTypes: true })
    .filter((d) => d.isDirectory())
    .map((d) => d.name)
    .filter((name) => fs.existsSync(path.join(skillsRoot, name, 'SKILL.md')))
    .sort();
}

function parseArgs(argv) {
  const args = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const token = argv[i];
    if (token === '-h') {
      args.help = true;
      continue;
    }
    if (!token.startsWith('--')) {
      args._.push(token);
      continue;
    }
    const key = token.slice(2);
    if (key === 'force' || key === 'json' || key === 'help' || key === 'version') {
      args[key] = true;
      continue;
    }
    const value = argv[i + 1];
    if (value == null || value.startsWith('--')) {
      throw new Error(`Missing value for --${key}`);
    }
    args[key] = value;
    i += 1;
  }
  return args;
}

function resolveMode(mode) {
  if (!mode || mode === 'auto') {
    return process.platform === 'win32' ? 'copy' : 'symlink';
  }
  if (!['copy', 'symlink'].includes(mode)) {
    throw new Error(`Unsupported mode: ${mode}`);
  }
  return mode;
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function realish(p) {
  try {
    return fs.realpathSync.native(p);
  } catch {
    return path.resolve(p);
  }
}

function installSkill(src, dest, mode, force) {
  const srcReal = realish(src);
  const destParent = path.dirname(dest);
  ensureDir(destParent);

  if (realish(dest) === srcReal) {
    return { status: 'skipped', reason: 'source-and-destination-are-identical' };
  }

  if (fs.existsSync(dest)) {
    if (!force) {
      return { status: 'skipped', reason: 'destination-exists' };
    }
    fs.rmSync(dest, { recursive: true, force: true });
  }

  if (mode === 'copy') {
    fs.cpSync(src, dest, { recursive: true });
    return { status: 'installed', mode: 'copy' };
  }

  fs.symlinkSync(srcReal, dest, 'junction');
  return { status: 'installed', mode: 'symlink' };
}

function doList(args) {
  const names = listSkillNames();
  if (args.json) {
    console.log(JSON.stringify({ count: names.length, skills: names }, null, 2));
    return;
  }
  console.log('Available Glassroom skills:');
  for (const name of names) console.log(`- ${name}`);
}

function doInstall(targetKind, args) {
  const allSkills = listSkillNames();
  const requested = args.skills ? args.skills.split(',').map((x) => x.trim()).filter(Boolean) : allSkills;
  const invalid = requested.filter((name) => !allSkills.includes(name));
  if (invalid.length) {
    throw new Error(`Unknown skills: ${invalid.join(', ')}`);
  }

  const targetRoot = args.target
    ? path.resolve(args.target)
    : targetKind === 'openclaw'
      ? path.join(os.homedir(), '.openclaw', 'workspace', 'skills')
      : path.join(process.cwd(), 'skills');

  ensureDir(targetRoot);
  const mode = resolveMode(args.mode);
  const results = [];

  for (const name of requested) {
    const src = path.join(skillsRoot, name);
    const dest = path.join(targetRoot, name);
    const result = installSkill(src, dest, mode, !!args.force);
    results.push({ skill: name, target: dest, ...result });
  }

  const installed = results.filter((r) => r.status === 'installed');
  const skipped = results.filter((r) => r.status === 'skipped');

  console.log(`Installed ${installed.length} skill(s) to ${targetRoot}`);
  for (const row of installed) console.log(`+ ${row.skill} (${row.mode})`);
  for (const row of skipped) console.log(`- ${row.skill} (${row.reason})`);
}

function runPythonScript(scriptPath, forwardedArgs) {
  const candidates = process.platform === 'win32' ? ['python', 'py'] : ['python3', 'python'];
  let lastError = null;

  for (const bin of candidates) {
    const result = spawnSync(bin, [scriptPath, ...forwardedArgs], { stdio: 'inherit' });
    if (result.error) {
      lastError = result.error;
      continue;
    }
    process.exit(result.status ?? 0);
  }

  throw new Error(`Unable to run Python script (${scriptPath}). Last error: ${lastError ? lastError.message : 'python not found'}`);
}

function doAssemble(sub, args) {
  if (sub !== 'case') {
    throw new Error('Usage: glassroom assemble case --out-json <file> [--out-md <file>] [--base-case <file>] [--source-card <file>] [--bias-analysis <file>] [--mitigation-pack <file>] [--structured-analysis <file>]');
  }

  if (!args['out-json']) {
    throw new Error('Missing required --out-json for glassroom assemble case');
  }

  const scriptPath = path.join(packagesRoot, 'case-assembler', 'assemble_case.py');
  const forwardedArgs = [];
  const mappings = [
    ['base-case', '--base-case'],
    ['source-card', '--source-card'],
    ['bias-analysis', '--bias-analysis'],
    ['mitigation-pack', '--mitigation-pack'],
    ['structured-analysis', '--structured-analysis'],
    ['out-json', '--out-json'],
    ['out-md', '--out-md'],
  ];

  for (const [key, flag] of mappings) {
    if (args[key]) {
      forwardedArgs.push(flag, args[key]);
    }
  }

  runPythonScript(scriptPath, forwardedArgs);
}

function main() {
  try {
    const args = parseArgs(process.argv.slice(2));
    const [cmd, sub] = args._;

    if (args.version || cmd === 'version' || cmd === '--version') {
      console.log(pkg.version);
      return;
    }

    if (args.help || !cmd || cmd === 'help' || cmd === '--help' || cmd === '-h') {
      usage();
      return;
    }

    if (cmd === 'list-skills') {
      doList(args);
      return;
    }

    if (cmd === 'install') {
      if (!sub || !['openclaw', 'project'].includes(sub)) {
        throw new Error('Usage: glassroom install <openclaw|project>');
      }
      doInstall(sub, args);
      return;
    }

    if (cmd === 'assemble') {
      doAssemble(sub, args);
      return;
    }

    throw new Error(`Unknown command: ${cmd}`);
  } catch (err) {
    console.error(`glassroom: ${err.message}`);
    process.exit(1);
  }
}

main();
