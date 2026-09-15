/* Documentation QA only; install into an isolated scratch runtime:
 * npm install --prefix <scratch-runtime> --no-save --ignore-scripts \
 *   mathjax-full@3.2.2 markdown-it@14.1.0 katex@0.16.22 parse5@7.2.1
 * NODE_PATH=<scratch-runtime>/node_modules node \
 *   integrations/math-approval-03/verify_math_transport.cjs <fresh-output-dir>
 * No instrument control, numerical claim, or prior evidence is modified.
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
const katex = require('katex');
const parse5 = require('parse5');

const root = path.resolve(__dirname, '../..');
const baseline = '01d715a80dbe48c3c20f43337fb524753e3cdb54';
const output = process.argv[2] && path.resolve(process.argv[2]);
if (!output) throw Error('Provide a fresh output directory.');
if (output === root || output.startsWith(root + path.sep)) {
  throw Error('Output must be a fresh directory outside the repository.');
}
if (fs.existsSync(output)) throw Error('Refusing to overwrite an existing output directory.');
const md = new MarkdownIt('commonmark');
const adaptor = liteAdaptor();
RegisterHTMLHandler(adaptor);
const engine = mathjax.document('', {
  InputJax: new TeX({packages: ['base', 'ams']}),
  OutputJax: new SVG({fontCache: 'none'}),
});
const hash = value => crypto.createHash('sha256').update(value).digest('hex');
const pages = ['docs/CONTRIBUTIONS.md', 'docs/THEORY_ROUTE.md'];
function expectedChange(text) {
  return text.replaceAll('j<k', 'j\\lt k').replaceAll('0<\\eta', '0\\lt\\eta');
}
function displays(text) {
  return md.parse(text, {}).filter(t => t.type === 'fence' && t.info === 'math')
    .map(t => t.content.trim());
}
function mathjaxRender(tex) {
  const html = adaptor.outerHTML(engine.convert(tex, {display: true}));
  return {valid: !/data-mml-node="merror"|data-mjx-error/.test(html),
    svg: html.match(/<svg[\s\S]*<\/svg>/)[0]};
}
function katexRender(tex) {
  try {
    return {valid: true, html: katex.renderToString(tex, {
      displayMode: true, throwOnError: true, strict: 'error', output: 'html',
    })};
  } catch (error) {
    return {valid: false, error: error.message};
  }
}
function textContent(node) {
  return node.nodeName === '#text' ? node.value :
    (node.childNodes || []).map(textContent).join('');
}
function htmlRoundTrip(tex) {
  // Deliberately model a vulnerable raw innerHTML step after fence extraction.
  // This is an HTML5 parser experiment, not GitHub's authenticated pipeline.
  return textContent(parse5.parseFragment('<div>' + tex + '</div>'));
}
const results = [];
const transportCases = [];
const artifacts = [];
for (const file of pages) {
  const oldText = cp.execFileSync('git', ['show', baseline + ':' + file],
    {cwd: root, encoding: 'utf8'});
  const current = fs.readFileSync(path.join(root, file), 'utf8');
  if (expectedChange(oldText) !== current) throw Error(file + ': unexpected document change');
  const oldMath = displays(oldText);
  const newMath = displays(current);
  if (oldMath.length !== newMath.length) throw Error(file + ': changed display count');
  for (let index = 0; index < oldMath.length; index++) {
    const oldTex = oldMath[index], tex = newMath[index];
    if (expectedChange(oldTex) !== tex) throw Error(file + ': changed mathematical payload');
    if (/[<>]/.test(tex)) throw Error(file + ': remaining HTML-sensitive comparison');
    const oldM = mathjaxRender(oldTex), newM = mathjaxRender(tex);
    const oldK = katexRender(oldTex), newK = katexRender(tex);
    if (!oldM.valid || !newM.valid || !oldK.valid || !newK.valid) {
      throw Error(file + ': direct TeX parse failed at display ' + (index + 1));
    }
    if (oldM.svg !== newM.svg || oldK.html !== newK.html) {
      throw Error(file + ': old/new mathematical render differs at display ' + (index + 1));
    }
    const stem = file.replace(/\.md$/, '').replaceAll('/', '-') + '-' + (index + 1);
    artifacts.push([stem + '.svg', newM.svg]);
    results.push({file, display: index + 1, exact_permitted_text_change: true,
      mathjax_svg_identical: true, katex_html_identical: true,
      svg: stem + '.svg', svg_sha256: hash(newM.svg)});
    if (oldTex !== tex) {
      const oldTransported = htmlRoundTrip(oldTex);
      const newTransported = htmlRoundTrip(tex);
      const oldParseM = mathjaxRender(oldTransported), oldParseK = katexRender(oldTransported);
      const newParseM = mathjaxRender(newTransported), newParseK = katexRender(newTransported);
      if (newTransported !== tex || !newParseM.valid || !newParseK.valid) {
        throw Error(file + ': corrected HTML transport failed');
      }
      const sumCase = oldTex.includes('j<k');
      if (sumCase && (oldTransported === oldTex || oldParseM.valid || oldParseK.valid)) {
        throw Error(file + ': expected missing-brace reproduction failed');
      }
      transportCases.push({file, display: index + 1,
        kind: sumCase ? 'pair-sum subscript' : 'positive transmission condition',
        original_tex: oldTex, original_after_html5: oldTransported,
        old_transport_preserved: oldTransported === oldTex,
        old_after_html5_mathjax_parses: oldParseM.valid,
        old_after_html5_katex_parses: oldParseK.valid,
        old_katex_error: oldParseK.error || null,
        corrected_tex: tex, corrected_transport_preserved: true,
        corrected_after_html5_mathjax_parses: true,
        corrected_after_html5_katex_parses: true});
    }
  }
}
if (results.length !== 18 || transportCases.length !== 3) throw Error('Unexpected coverage');
const report = {
  status: 'PASS', baseline, node_version: process.version,
  mathjax_full_version: require('mathjax-full/package.json').version,
  markdown_it_version: require('markdown-it/package.json').version,
  katex_version: katex.version,
  parse5_version: JSON.parse(fs.readFileSync(path.resolve(
    path.dirname(require.resolve('parse5')), '../../package.json'), 'utf8')).version,
  documents_checked: pages.length, displays_checked: results.length,
  changed_displays: transportCases.length,
  scope: 'Exact relation-macro substitution; identical direct mathematical renders; controlled HTML5-before-TeX transport.',
  live_github_rendering_checked: false, visual_inspection_by_this_script: false,
  user_renderer_implementation_identified: false,
  transport_cases: transportCases, results,
};
fs.mkdirSync(output, {recursive: true});
for (const [name, content] of artifacts) fs.writeFileSync(path.join(output, name), content);
fs.writeFileSync(path.join(output, 'MATH_TRANSPORT.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify({status: report.status, output, documents: pages.length,
  displays: results.length, transport_cases: transportCases}, null, 2));
