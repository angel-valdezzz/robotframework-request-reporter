const {JSDOM,VirtualConsole}=require('jsdom');
const fs=require('fs');const assert=require('node:assert/strict');
const root=require('node:path').resolve(__dirname,'..');
async function check(file,language="en"){
 const errors=[];const vc=new VirtualConsole();vc.on('jsdomError',e=>errors.push(e));
 let copied='';
 const dom=new JSDOM(fs.readFileSync(root+'/results/acceptance/'+(language==='es'?'cases-es/':'cases/')+file,'utf8'),{runScripts:'dangerously',url:'https://example.test/report.html',virtualConsole:vc,beforeParse(w){w.matchMedia=()=>({matches:false});w.HTMLElement.prototype.scrollIntoView=function(){};Object.defineProperty(w.navigator,'clipboard',{value:{writeText:async t=>{copied=t;}}});}});
 const d=dom.window.document;const click=(sel)=>{assert(d.querySelector(sel),sel);d.querySelector(sel).click();};
 const payload=JSON.parse(d.querySelector('#case-data').textContent);
 assert.equal(d.querySelectorAll('#request-overview tbody tr').length,payload.exchanges.length);
 assert(d.querySelector('#info-started').textContent);
 if(file==='Failing_distributor.html'){
  assert.match(d.querySelector('#outcome').textContent,language==='es'?/2 validaciones fallidas en 1/:/2 failed assertions across 1 request/);
  click('[data-overview-request="1"]');assert.equal(d.querySelector('#section-requests').hidden,false);
  const input=d.querySelector('#body-search');input.value='folio';input.dispatchEvent(new dom.window.Event('input',{bubbles:true}));
  assert(d.querySelectorAll('mark').length>0);assert([...d.querySelectorAll('mark')].every(m=>!m.closest('details')||m.closest('details').open));
  click('[data-copy="body"]');await new Promise(r=>setImmediate(r));assert.equal(JSON.parse(copied).registration.folio,'ALT-1042');
  click('[data-body-view="raw"]');assert(d.querySelector('#body-content pre'));assert(d.querySelectorAll('mark').length>0);
  click('[data-tab="assertions"]');click('[data-filter="fail"]');assert.equal(d.querySelectorAll('.validation').length,2);
  click('[data-filter="pass"]');assert.equal(d.querySelectorAll('.validation').length,4);
  click('[data-section="failures"]');click('[data-failure-request="1"]');assert.equal(d.querySelectorAll('.validation').length,6);assert.match(d.activeElement.id,/assertion-/);
  click('#theme-toggle');assert.equal(d.documentElement.dataset.theme,'dark');
 }
 if(file==='Captured_timeout_without_response.html'){assert.equal(d.querySelector('#request-count').textContent,'1');assert.match(d.querySelector('#request-errors').textContent,(language==='es'?/Sin respuesta recibida/:/No response received/));assert(!d.querySelector('#request-errors').textContent.includes('query-secret-SECRET'));}
 if(file==='Non_JSON_error_response.html'){click('[data-overview-request="0"]');assert(d.querySelector('.text-body'));click('[data-copy="body"]');await new Promise(r=>setImmediate(r));assert.equal(copied,'upstream unavailable');}
 if(file==='Passing_distributor.html')assert.equal(d.querySelector('[aria-label="Test case metadata"]'),null);
 if(file==='No_requests.html')assert.match(d.querySelector('#outcome').textContent,(language==='es'?/no se registraron validaciones/:/no assertions recorded/));
 if(file==='Skipped_case.html')assert.match(d.querySelector('#outcome').textContent,(language==='es'?/omitida/:/skipped/));
 if(file==='Binary_response.html'){click('[data-overview-request="0"]');assert.match(d.querySelector('#content').textContent,(language==='es'?/contenido binario no est/:/Binary content is not embedded/));}
 assert.deepEqual(errors.map(e=>e.message),[]);dom.window.close();
}
(async()=>{for(const language of ['en','es'])for(const f of ['Failing_distributor.html','Passing_distributor.html','No_requests.html','Skipped_case.html','Binary_response.html','Untrusted_body_content.html','Captured_timeout_without_response.html','Non_JSON_error_response.html'])await check(f,language);console.log('DOM interaction checks passed: summary, filters, search, copy, raw/tree, failure navigation, themes, optional metadata and states.');})().catch(e=>{console.error(e);process.exit(1)});
