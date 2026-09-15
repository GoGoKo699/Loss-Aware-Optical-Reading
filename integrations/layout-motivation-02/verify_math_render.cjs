/* Independent documentation-only check. Dependencies are isolated QA tools:
 * npm install --prefix <scratch-runtime> --no-save --ignore-scripts \
 *   mathjax-full@3.2.2 markdown-it@14.1.0
 * NODE_PATH=<scratch-runtime>/node_modules node \
 *   integrations/layout-motivation-02/verify_math_render.cjs <new-output-dir>
 * No hardware I/O, scientific calculation, or frozen evidence is modified.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const cp = require('child_process');
const crypto = require('crypto');
const {mathjax} = require('mathjax-full/js/mathjax.js');
const {TeX} = require('mathjax-full/js/input/tex.js');
require('mathjax-full/js/input/tex/ams/AmsConfiguration.js');
const {SVG} = require('mathjax-full/js/output/svg.js');
const {liteAdaptor} = require('mathjax-full/js/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler} = require('mathjax-full/js/handlers/html.js');
const MarkdownIt = require('markdown-it');

const root = path.resolve(__dirname, '../..');
const baseline = '1b0a79073050766f12317f27a0b0e9260896b90f';
const output = process.argv[2] && path.resolve(process.argv[2]);
if (!output) throw Error('Provide a fresh output directory.');
if (output === root || output.startsWith(root + path.sep)) {
  throw Error('Render evidence must go to a fresh directory outside the repository.');
}
if (fs.existsSync(output)) throw Error('Refusing to overwrite an existing output directory.');
const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const engine = mathjax.document('', {
  InputJax: new TeX({packages: ['base', 'ams']}),
  OutputJax: new SVG({fontCache: 'none'}),
});
const md = new MarkdownIt('commonmark');
const pages = [
  'docs/THEORY_ROUTE.md', 'docs/CONTRIBUTIONS.md', 'docs/ROBUSTNESS_GUIDE.md',
  'experiment/M1.md', 'experiment/P1.md', 'experiment/P2.md',
  'experiment/SU4.md', 'experiment/SU8.md',
];
const hash = x => crypto.createHash('sha256').update(x).digest('hex');
function explicitOperands(text) {
  return text.replace(/\\frac([0-9])([0-9])/g, '\\frac{$1}{$2}')
    .replace(/\\frac([0-9])(?=\{)/g, '\\frac{$1}')
    .replace(/\\sqrt([0-9])/g, '\\sqrt{$1}');
}
function oldToNew(text) {
  let opening = true;
  return explicitOperands(text).split('\n').map(line => {
    if (line !== '$$') return line;
    const marker = opening ? '```math' : '```';
    opening = !opening;
    return marker;
  }).join('\n');
}
function render(tex) {
  const html = adaptor.outerHTML(engine.convert(tex, {display: true}));
  return {html, valid: !/data-mml-node="merror"|data-mjx-error/.test(html)};
}
const results = [];
const artifacts = [];
const screenshotCases = [];
for (const file of pages) {
  const oldText = cp.execFileSync('git', ['show', baseline + ':' + file],
                                {cwd: root, encoding: 'utf8'});
  const current = fs.readFileSync(path.join(root, file), 'utf8');
  if (oldToNew(oldText) !== current) throw Error(file + ': nonformatting change');
  const oldMath = [...oldText.matchAll(/\$\$([\s\S]*?)\$\$/g)].map(x => x[1].trim());
  const newMath = md.parse(current, {}).filter(t => t.type === 'fence' && t.info === 'math')
    .map(t => t.content.trim());
  if (oldMath.length !== newMath.length) throw Error(file + ': display count changed');
  for (let index = 0; index < oldMath.length; index++) {
    if (explicitOperands(oldMath[index]) !== newMath[index]) {
      throw Error(file + ': mathematical payload changed at ' + index);
    }
    const oldRender = render(oldMath[index]);
    const corrected = render(newMath[index]);
    if (!oldRender.valid || !corrected.valid) {
      throw Error(file + ': TeX parser failure at display ' + (index + 1));
    }
    const stem = file.replace(/\.md$/, '').replaceAll('/', '-') + '-' + (index + 1);
    const svg = corrected.html.match(/<svg[\s\S]*<\/svg>/)[0];
    artifacts.push([stem + '.svg', svg]);
    results.push({file, display: index + 1, equivalent: true, direct_old_tex_parses: true,
      fenced_math_payload_parses: true, svg: stem + '.svg', svg_sha256: hash(svg)});
    if ((file === 'docs/THEORY_ROUTE.md' && [11, 12].includes(index)) ||
        (file === 'docs/CONTRIBUTIONS.md' && [1, 2].includes(index))) {
      // A controlled Markdown-before-TeX reconstruction, not GitHub's live parser.
      const processed = md.render('$$\n' + oldMath[index] + '\n$$');
      const dom = adaptor.parse(processed, 'text/html');
      const literal = adaptor.textContent(adaptor.body(dom)).replaceAll('$$', '').trim();
      screenshotCases.push({file, display: index + 1,
        commonmark_changes_payload: literal !== oldMath[index],
        commonmark_then_tex_parses: render(literal).valid,
        corrected_fence_preserves_tex: true});
    }
  }
}
if (results.length !== 42 || screenshotCases.length !== 4) throw Error('Unexpected display coverage');
const report = {
  status: 'PASS', baseline, node_version: process.version,
  mathjax_full_version: require('mathjax-full/package.json').version,
  markdown_it_version: require('markdown-it/package.json').version,
  current_github_renderer_version_known: false,
  live_github_rendering_checked: false,
  visual_inspection_by_this_script: false,
  scope: 'Exact formatting-only comparison; CommonMark literal fence extraction; local TeX-to-SVG parsing.',
  documents_checked: pages.length, displays_checked: results.length,
  screenshot_cases: screenshotCases, results,
};
fs.mkdirSync(output, {recursive: true});
for (const [name, content] of artifacts) fs.writeFileSync(path.join(output, name), content);
fs.writeFileSync(path.join(output, 'MATH_RENDER.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify({status: report.status, output, documents: pages.length,
  displays: results.length, screenshot_cases: screenshotCases}, null, 2));
