(function(root){
'use strict';
const collections=['codes','memos','comparisons','categories','sampling','relations'];
const fields={codes:['source','fragment','code','reason'],memos:['title','text','refs','date'],comparisons:['left','right','finding'],categories:['name','properties','dimensions','refs'],sampling:['category','gap','next','result'],relations:['claim','refs','counter','limit']};
function empty(){return {version:1,project:{title:'',question:'',tradition:'strauss',position:''},completed:[],aiReviews:[],...Object.fromEntries(collections.map(k=>[k,[]]))};}
function validate(input){
 if(!input||input.version!==1||!input.project||!Array.isArray(input.completed))throw Error('El archivo no corresponde a un cuaderno de esta ruta (versión 1).');
 const out=empty();
 for(const k of Object.keys(out.project)){if(typeof input.project[k]!=='string'||input.project[k].length>20000)throw Error('Ficha de proyecto no válida.');out.project[k]=input.project[k];}
 if(!['strauss','clasica','constructivista'].includes(out.project.tradition))throw Error('Vertiente no reconocida.');
 if(input.completed.some(n=>!Number.isInteger(n)||n<0||n>8))throw Error('Registro de avance no válido.');
 out.completed=[...new Set(input.completed)];const ids=new Set();
 for(const k of collections){if(!Array.isArray(input[k])||input[k].length>3000)throw Error('Colección no válida: '+k);out[k]=input[k].map(row=>{if(!row||typeof row.id!=='string'||! /^[A-Za-z0-9_-]{1,70}$/.test(row.id)||ids.has(row.id))throw Error('Identificador ausente, duplicado o inválido.');ids.add(row.id);const clean={id:row.id};for(const f of fields[k]){if(typeof row[f]!=='string'||row[f].length>20000)throw Error('Campo no válido: '+f);clean[f]=row[f];}return clean;});}
 if(input.aiReviews!==undefined){if(!Array.isArray(input.aiReviews)||input.aiReviews.length>5000)throw Error('Bitácora de revisión no válida.');out.aiReviews=input.aiReviews.map(r=>{const clean={};for(const k of ['id','model','revision','mode','kind','source','fragment','quote','code','modelReason','reviewerNote','decision','time','codeId']){if(typeof r?.[k]!=='string'||r[k].length>20000)throw Error('Registro de revisión no válido: '+k);clean[k]=r[k];}for(const k of ['categories','device','dtype','originalProposal']){if(r[k]!==undefined&&(typeof r[k]!=='string'||r[k].length>20000))throw Error('Metadato de revisión no válido.');clean[k]=r[k]||'';}if(!['accepted','rejected'].includes(clean.decision))throw Error('Decisión de revisión no válida.');return clean;});}
 return out;
}
function refs(s){return s.split(/[,;\s]+/).filter(Boolean);}
function nextId(state,prefix){const used=new Set(collections.flatMap(k=>state[k].map(r=>r.id)));let n=1;while(used.has(prefix+n))n++;return prefix+n;}
function issues(s){let out=[];const all=new Set(collections.flatMap(k=>s[k].map(r=>r.id))),codes=new Set(s.codes.map(r=>r.id)),cats=new Set(s.categories.map(r=>r.id));
 for(const k of collections)for(const r of s[k]){
  const links=k==='comparisons'?[r.left,r.right]:k==='sampling'?[r.category]:r.refs?refs(r.refs):[];
  for(const id of links)if(!all.has(id))out.push(r.id+': falta la referencia '+id+'.');
  if(k==='comparisons'&&(!codes.has(r.left)||!codes.has(r.right)))out.push(r.id+': compara identificadores de códigos existentes.');
  if(k==='sampling'&&!cats.has(r.category))out.push(r.id+': vincula una categoría existente.');
  if(['memos','categories','relations'].includes(k)&&!r.refs.trim())out.push(r.id+': sin referencias a otros registros.');
 }
 return [...new Set(out)];
}
function csv(rows,keys){const escape=v=>{let s=String(v??'');if(/^[\s]*[=+@-]/.test(s))s="'"+s;return '"'+s.replaceAll('"','""')+'"';};return '\uFEFF'+[keys,...rows.map(r=>keys.map(k=>r[k]))].map(r=>r.map(escape).join(',')).join('\r\n');}
const api={empty,validate,collections,fields,refs,nextId,issues,csv};if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.TF_CORE=api;
})(typeof window==='undefined'?globalThis:window);
