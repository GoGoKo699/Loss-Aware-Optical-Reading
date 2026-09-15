/* Documentation QA; use an isolated scratch runtime:
 * npm install --prefix <scratch-runtime> --no-save --ignore-scripts \
 *   markdown-it@14.1.0 mathjax-full@3.2.2
 * NODE_PATH=<scratch-runtime>/node_modules node \
 *   integrations/table-cleanup-04/verify_gfm_tables.cjs <fresh-output-directory>
 * The output must be outside the repository; prior evidence is never overwritten.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const cp = require('child_process');
const crypto = require('crypto');
const assert = require('assert/strict');
const MarkdownIt = require('markdown-it');
const {mathjax} = require('mathjax-full/js/mathjax.js');
const {TeX} = require('mathjax-full/js/input/tex.js');
require('mathjax-full/js/input/tex/ams/AmsConfiguration.js');
const {SVG} = require('mathjax-full/js/output/svg.js');
const {liteAdaptor} = require('mathjax-full/js/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler} = require('mathjax-full/js/handlers/html.js');
const root = path.resolve(__dirname, '../..');
const baseline = '55a90a3162326e924b460977d4c19714f39ae606';
const output = process.argv[2] && path.resolve(process.argv[2]);
if (!output) throw Error('Provide a fresh output directory.');
if (output === root || output.startsWith(root + path.sep)) {
  throw Error('Output must be outside the repository.');
}
if (fs.existsSync(output)) throw Error('Refusing to overwrite existing output.');
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
const md = new MarkdownIt('commonmark').enable('table');
const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const engine = mathjax.document('', {InputJax: new TeX({packages: ['base', 'ams']}),
  OutputJax: new SVG({fontCache: 'none'})});
function math(tex) {
  const html = adaptor.outerHTML(engine.convert(tex, {display: true}));
  assert(!/data-mml-node="merror"|data-mjx-error/.test(html), 'MathJax parse error');
  return html;
}
const originalFence = md.renderer.rules.fence;
md.renderer.rules.fence = (tokens, index, options, env, renderer) =>
  tokens[index].info.trim() === 'math' ? '<div class="math-display">' +
    math(tokens[index].content) + '</div>\n' :
    originalFence(tokens, index, options, env, renderer);
function tables(text) {
  const tables = [];
  let table = null, row = null;
  for (const token of md.parse(text, {})) {
    if (token.type === 'table_open') table = {source_lines: token.map, rows: []};
    if (!table) continue;
    if (token.type === 'tr_open') row = [];
    if (token.type === 'inline') row.push(token.children.map(child => child.content).join(''));
    if (token.type === 'tr_close') table.rows.push(row);
    if (token.type === 'table_close') { tables.push(table); table = null; }
  }
  return tables;
}
function displays(text) {
  return md.parse(text, {}).filter(t => t.type === 'fence' && t.info === 'math')
    .map(t => t.content.trim());
}
const source = file => fs.readFileSync(path.join(root, file), 'utf8');
const prior = file => cp.execFileSync('git', ['show', baseline + ':' + file],
  {cwd: root, encoding: 'utf8'});
function markdownFiles(directory) {
  return fs.readdirSync(path.join(root, directory), {withFileTypes: true}).flatMap(entry =>
    entry.isDirectory() ? markdownFiles(directory + '/' + entry.name) :
      entry.name.endsWith('.md') ? [directory + '/' + entry.name] : []);
}
const pages = ['README.md', 'CLAIM_STATUS.md', 'work_orders/CURRENT.md',
  ...markdownFiles('docs'), ...markdownFiles('experiment')].sort();
assert.equal(pages.length, 24);
const allTables = pages.flatMap(file => tables(source(file)).map(table => ({file, ...table})));
assert.equal(allTables.length, 28);
assert.equal(allTables.reduce((sum, table) => sum + table.rows.length - 1, 0), 169);
const commission = 'experiment/COMMISSIONING.md', su4 = 'experiment/SU4.md';
const oldCommission = tables(prior(commission))[0], newCommission = tables(source(commission))[0];
const oldSu4 = tables(prior(su4))[0], newSu4 = tables(source(su4))[0];
// The original defect is reproduced by the GFM table parser: extra cells are dropped.
assert.deepEqual(oldCommission.rows[1], ['SU4', 'A(1,1,1,1)/2 on 0–3', '`O_j=I4-2', 'j><j']);
assert.equal(oldCommission.rows[3][3], '`A sqrt(t)');
assert.deepEqual(oldSu4.rows[2], ['Hidden operation', '`O_j = I4 - 2', 'j><j']);
assert.deepEqual(newCommission.rows, [
  ['Route', 'Prepared paths', 'Hidden labels', 'Expected bright output'],
  ['SU4', 'Equal amplitudes on 0–3', '0–3', 'Port j'],
  ['SU8 four active', 'Equal amplitudes on 0–3; vacuum on 4–7', '0–3', 'Port j; outputs 4–7 stay dark'],
  ['SU8 native', 'Equal amplitudes on 0–7', '0–7', 'Port j'],
]);
assert.deepEqual(newSu4.rows[2], ['Hidden operation',
  'Pi phase flip on path j; uniformly selected j = 0,1,2,3',
  'An independently controlled phase section, hidden from the reader']);
// No procedure, command or acquisition wording changed below the target explanation.
const suffix = '## Reference calculation before touching controls';
assert.equal(source(commission).slice(source(commission).indexOf(suffix)),
  prior(commission).slice(prior(commission).indexOf(suffix)));
const newDisplays = displays(source(commission));
assert.deepEqual(newDisplays, [
  String.raw`a_4=\frac{1}{2}(1,1,1,1)^T.`,
  String.raw`O_{4,j}=I_4-2|j\rangle\langle j|,\qquad D_4=\frac{J_4}{2}-I_4,
\qquad j=0,1,2,3.`,
  String.raw`a_{\rm emb}=\frac{1}{2}(1,1,1,1,0,0,0,0)^T.`,
  String.raw`O_{{\rm emb},j}=O_{4,j}\oplus I_4,\qquad
D_{\rm emb}=D_4\oplus I_4,\qquad j=0,1,2,3.`,
  String.raw`a_8=\frac{1}{\sqrt{8}}(1,1,1,1,1,1,1,1)^T.`,
  String.raw`O_{8,j}=\mathrm{diag}(Z_8[:,j]),\qquad
D_8=\frac{Z_8^\dagger}{\sqrt{8}},\qquad j=0,1,\ldots,7.`,
  String.raw`b_j=A\sqrt{t}\,|j\rangle.`,
]);
const su4Math = displays(source(su4));
assert.equal(su4Math[0], String.raw`O_j=I_4-2|j\rangle\langle j|,\qquad j=0,1,2,3.`);
assert.deepEqual(su4Math.slice(1), displays(prior(su4)), 'Existing SU4 mathematics changed');
const displayResults = [commission, su4].flatMap(file => displays(source(file))
  .map((tex, index) => ({file, display: index + 1, tex, rendered_sha256: hash(math(tex))})));
const style = 'body{margin:32px auto;padding:0 24px;max-width:1012px;color:#1f2328;background:white;'
  + 'font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif}'
  + 'h1,h2{line-height:1.25;border-bottom:1px solid #d1d9e0;padding-bottom:.3em;margin-top:24px}'
  + 'h1{font-size:30px}h2{font-size:24px}p{margin:0 0 16px}table{border-collapse:collapse;'
  + 'margin:0 0 16px;width:100%;font-size:16px}th,td{border:1px solid #d1d9e0;padding:6px 13px;'
  + 'vertical-align:top}th{font-weight:600}tr:nth-child(2n){background:#f6f8fa}'
  + 'code{background:#eff1f3;padding:.15em .3em;border-radius:4px;font-size:85%;'
  + 'font-family:ui-monospace,monospace}a{color:#0969da;text-decoration:underline}'
  + '.math-display{overflow:auto;text-align:center;margin:16px 0}svg{max-width:100%;height:auto}'
  + 'pre{overflow:auto;background:#f6f8fa;padding:16px}';
const previews = [];
for (const [file, end] of [[commission, suffix], [su4, '## Preparation and compiler conventions']]) {
  let text = source(file).slice(0, source(file).indexOf(end));
  let html = md.render(text).replace(/href="[^"]*"/g, 'href="#"');
  const name = path.basename(file, '.md').toLowerCase() + '.html';
  html = '<!doctype html><html lang="en"><head><meta charset="utf-8">'
    + '<meta name="viewport" content="width=device-width,initial-scale=1">'
    + '<title>' + path.basename(file) + ' — local GFM preview</title><style>'
    + style + '</style></head><body>' + html + '</body></html>\n';
  previews.push({name, html});
}
const report = {status: 'PASS', baseline, node_version: process.version,
  markdown_it_version: require('markdown-it/package.json').version,
  mathjax_full_version: require('mathjax-full/package.json').version,
  markdown_parser_mode: 'CommonMark with GFM table rule enabled',
  documents_checked: pages.length, tables_parsed: allTables.length,
  table_body_rows: 169, old_defective_rows_reproduced: 3,
  corrected_expected_rows_preserved: 4,
  math_displays_parsed: displayResults.length,
  live_github_rendering_checked: false, visual_inspection_by_script: false,
  previews: previews.map(({name, html}) => ({name, sha256: hash(html)})),
  page_sha256: Object.fromEntries(pages.map(file => [file, hash(source(file))])),
  old_defect: {commissioning: oldCommission, su4: oldSu4},
  corrected: {commissioning: newCommission, su4: newSu4},
  tables: allTables, math_displays: displayResults,
  limitations: 'Local GFM parsing and MathJax rendering; simplified CSS, not an authenticated GitHub preview.'};
fs.mkdirSync(output, {recursive: true});
for (const {name, html} of previews) fs.writeFileSync(path.join(output, name), html);
fs.writeFileSync(path.join(output, 'GFM_TABLES.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify({status: 'PASS', output, documents: pages.length,
  tables: allTables.length, rows: 169, old_defects: 3, math_displays: displayResults.length}, null, 2));
