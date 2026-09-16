// From the repository root:
// NODE_PATH=<isolated math-approval-runtime>/node_modules node audits/final-handover-01/DOCUMENT_RENDER.cjs
// Local parser check only: not a reproduction of GitHub's full rendering pipeline.
'use strict';
const fs=require('fs'),path=require('path'),cp=require('child_process'),crypto=require('crypto');
const MarkdownIt=require('markdown-it'),parse5=require('parse5');
const {mathjax}=require('mathjax-full/js/mathjax.js'),{TeX}=require('mathjax-full/js/input/tex.js');
const {SVG}=require('mathjax-full/js/output/svg.js'),{liteAdaptor}=require('mathjax-full/js/adaptors/liteAdaptor.js');
const {RegisterHTMLHandler}=require('mathjax-full/js/handlers/html.js');
require('mathjax-full/js/input/tex/ams/AmsConfiguration.js');
const root=path.resolve(__dirname,'../..');process.chdir(root);
const md=new MarkdownIt('commonmark').enable('table'),adaptor=liteAdaptor();RegisterHTMLHandler(adaptor);
const engine=mathjax.document('',{InputJax:new TeX({packages:['base','ams']}),OutputJax:new SVG({fontCache:'none'})});
const tracked=cp.execFileSync('git',['ls-files'],{encoding:'utf8'}).trim().split('\n');
const core=[...new Set([...tracked.filter(f=>f==='README.md'||f==='REPORT.md'||f==='CLAIM_STATUS.md'||f==='work_orders/CURRENT.md'||/^docs\/.*\.md$/.test(f)||/^experiment\/.*\.md$/.test(f)), 'docs/ROBUSTNESS_REPORT.md','docs/ROBUSTNESS_PROOFS.md','docs/NUMERICAL_PROOF.md'])];
const support=['SOURCE_AUDIT.md','CONTRIBUTING.md','THIRD_PARTY_NOTICES.md','proofs/THEORY.md','studies/robustness-01/PROOFS.md','studies/robustness-01/REPORT.md','studies/robustness-01/CALIBRATION_WORKSHEET.md','studies/robustness-01/SOURCES.md','studies/robustness-01/README.md','examples/lab/README.md','repairs/theory-01/NUMERICAL_PROOF.md'];
const hash=s=>crypto.createHash('sha256').update(s).digest('hex');
const textNode=n=>(n.nodeName==='#text'?n.value:'')+(n.childNodes||[]).map(textNode).join('');
const findings=[],pages=[];let mathCount=0,tableCount=0,bodyRows=0,linkCount=0,expressionErrors=0;
function headingIDs(txt){
  const counts={},ids=[],tokens=md.parse(txt,{});
  for(let i=0;i<tokens.length;i++)if(tokens[i].type==='heading_open'){
    const h=tokens[i+1].content.replace(/<[^>]*>/g,'').toLowerCase().replace(/[^\p{L}\p{N}_\-\s]/gu,'').replace(/ /g,'-');
    const c=counts[h]||0;counts[h]=c+1;ids.push(h+(c?'-'+c:''));
  }
  for(const m of txt.matchAll(/<a\s+(?:id|name)=["']([^"']+)["']/g))ids.push(m[1]);return ids;
}
function cells(line){return line.trim().replace(/^\|/,'').replace(/\|$/,'').split(/(?<!\\)\|/);}
for(const f of [...core,...support]){
  const src=fs.readFileSync(f,'utf8'),tokens=md.parse(src,{}),lines=src.split('\n'),expressions=[];
  const fenced=lines.slice();
  for(const t of tokens)if(t.type==='fence'||t.type==='code_block'){
    if(t.info.trim()==='math')expressions.push({kind:'fenced',line:t.map[0]+1,tex:t.content.trim()});
    for(let i=t.map[0];i<t.map[1];i++)fenced[i]='';
  }
  const outside=fenced.join('\n');
  for(const m of outside.matchAll(/(?<!\\)\$\$([\s\S]*?)(?<!\\)\$\$|(?<!\\)\$([^\n$]+?)(?<!\\)\$/g))
    expressions.push({kind:m[1]!==undefined?'dollar-display':'inline',line:outside.slice(0,m.index).split('\n').length,tex:(m[1]??m[2]).trim()});
  let nTables=0,nRows=0,nLinks=0;const mResult=[];
  for(const exp of expressions){
    const codeWrapped=exp.kind==='inline'&&exp.tex.startsWith('`')&&exp.tex.endsWith('`');
    if(codeWrapped)exp.tex=exp.tex.slice(1,-1);
    mathCount++;let svg,error=null;
    try{svg=adaptor.outerHTML(engine.convert(exp.tex,{display:exp.kind!=='inline'}));if(/data-mml-node="merror"|data-mjx-error/.test(svg))error='MathJax error node';}catch(e){error=String(e);}
    if(error){expressionErrors++;findings.push({file:f,line:exp.line,category:'mathjax',error});}
    const transported=textNode(parse5.parseFragment('<div>'+exp.tex+'</div>'));
    const transportChanged=transported!==exp.tex;
    if(/[<>]/.test(exp.tex))findings.push({file:f,line:exp.line,category:'raw-html-sensitive-math',transport_changed:transportChanged});
    let mdChanged=false,mdError=null;
    if(exp.kind!=='fenced'){
      const marker=exp.kind==='inline'?'$':'$$';
      const source=codeWrapped?'$`'+exp.tex+'`$':marker+'\n'+exp.tex+'\n'+marker;
      const parsed=textNode(parse5.parseFragment(md.render(source))).trim();
      const payload=parsed.slice(marker.length,-marker.length).trim();
      mdChanged=payload!==exp.tex;
      if(mdChanged){
        try{const out=adaptor.outerHTML(engine.convert(payload,{display:exp.kind!=='inline'}));if(/data-mml-node="merror"|data-mjx-error/.test(out))mdError='MathJax error after Markdown transport';}catch(e){mdError=String(e);}
        findings.push({file:f,line:exp.line,category:'markdown-before-math-change',transported_payload:payload,error:mdError});
      }
    }
    mResult.push({kind:exp.kind,line:exp.line,tex_sha256:hash(exp.tex),svg_sha256:svg?hash(svg):null,parse_error:error,html_transport_changed:transportChanged,markdown_transport_changed:mdChanged,markdown_transport_error:mdError});
  }
  let table=null;
  for(const t of tokens){
    if(t.type==='table_open'){
      nTables++;table={map:t.map};const sep=cells(lines[t.map[0]+1]);
      for(let i=t.map[0];i<t.map[1];i++){
        if(cells(lines[i]).length!==sep.length)findings.push({file:f,line:i+1,category:'table-width'});
        for(const code of lines[i].matchAll(/(`+)(.*?)\1/g))if(/(?<!\\)\|/.test(code[2]))findings.push({file:f,line:i+1,category:'code-pipe-table'});
      }
    }
    if(table&&t.type==='tr_open'&&t.map&&t.map[0]>table.map[0]+1)nRows++;
    if(t.type==='table_close')table=null;
    for(const child of t.children||[])if(child.type==='link_open'||child.type==='image'){
      const href=child.attrGet(child.type==='image'?'src':'href');
      if(!href||/^[a-z][a-z0-9+.-]*:|^\/\//i.test(href))continue;
      nLinks++;const [rel,frag]=href.split('#');let local=path.resolve(path.dirname(f),decodeURIComponent(rel||path.basename(f)));if(!rel)local=path.resolve(f);
      if(!fs.existsSync(local)){findings.push({file:f,category:'missing-local-link',target:href});continue;}
      if(frag&&local.endsWith('.md')&&!headingIDs(fs.readFileSync(local,'utf8')).includes(decodeURIComponent(frag)))findings.push({file:f,category:'missing-local-anchor',target:href});
    }
  }
  tableCount+=nTables;bodyRows+=nRows;linkCount+=nLinks;
  pages.push({file:f,scope:core.includes(f)?'primary':'linked-support',sha256:hash(src),tables:nTables,table_body_rows:nRows,local_links:nLinks,math:mResult});
}
const parseVersion=JSON.parse(fs.readFileSync(path.join(path.dirname(require.resolve('parse5')),'../../package.json'),'utf8')).version;
const result={commit:cp.execFileSync('git',['rev-parse','HEAD'],{encoding:'utf8'}).trim(),runtime:{node:process.version,markdown_it:require('markdown-it/package.json').version,mathjax:require('mathjax-full/package.json').version,parse5:parseVersion},primary_documents:core.length,linked_support_documents:support.length,math_expressions:mathCount,mathjax_errors:expressionErrors,tables:tableCount,table_body_rows:bodyRows,local_links:linkCount,findings,pages,scope_note:'CommonMark with GFM table rule; base+ams MathJax; raw-HTML transport is controlled risk reproduction, not the live GitHub pipeline.'};
const output=path.join(__dirname,process.argv[2]||'DOCUMENT_RENDER_AFTER.json');
if(fs.existsSync(output))throw Error('Refusing to overwrite previous evidence');
fs.writeFileSync(output,JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({...result,pages:undefined},null,2));
