/* Buildless reader. No code execution or model requests occur in this browser. */
const data = JSON.parse(document.getElementById('chapter-data').textContent);
const skills = JSON.parse(document.getElementById('skill-data').textContent);
const $ = id => document.getElementById(id);
const escapeHtml = text => String(text).replace(/[&<>"']/g, ch => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
function loadState(){try{return JSON.parse(localStorage.getItem('career-forge-v1'))||{};}catch{return {};}}
let state = loadState();
if (!Array.isArray(state.completed)) state.completed=[];
if (!state.answers || typeof state.answers!=='object') state.answers={};
function save(){try{localStorage.setItem('career-forge-v1',JSON.stringify(state));}catch{/* Browser storage may be unavailable. Export remains usable. */}}
function download(name, text){const url=URL.createObjectURL(new Blob([text],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
function markdown(text){
  let html='', inCode=false, code=[], list=false;
  function closeList(){if(list){html+='</ul>';list=false;}}
  for(const line of text.split('\n')){
    if(line.startsWith('```')){closeList();if(inCode){html+='<pre><code>'+escapeHtml(code.join('\n'))+'</code></pre>';code=[];}inCode=!inCode;continue;}
    if(inCode){code.push(line);continue;}
    if(line.startsWith('- ')){if(!list){html+='<ul>';list=true;}html+='<li>'+escapeHtml(line.slice(2))+'</li>';continue;}
    closeList();
    if(line.startsWith('## ')){html+='<h3>'+escapeHtml(line.slice(3))+'</h3>';continue;}
    if(line.trim()) html+='<p>'+escapeHtml(line)+'</p>';
  }
  closeList();return html;
}
const navItems=[...data.lessons.map(l=>({id:l.id,label:l.label})),{id:'completed',label:'Run · Completed project'},{id:'practice',label:'Practice · 12 challenges'},{id:'analyzer',label:'Build · Analyzer demo'},{id:'portfolio',label:'Ship · Portfolio checklist'}];
let current='mission';
let lastLesson='mission';
function renderNav(){
 $('nav').innerHTML=navItems.map((n,i)=>(i===9?'<div class="group">APPLY YOUR KNOWLEDGE</div>':'')+'<button type="button" data-go="'+n.id+'" '+(current===n.id?'aria-current="page" class="active"':'')+'>'+escapeHtml(n.label)+(state.completed.includes(n.id)?' ✓':'')+'</button>').join('');
 $('nav').querySelectorAll('button').forEach(b=>b.onclick=()=>go(b.dataset.go));
 $('progress').value=state.completed.filter(id=>data.lessons.some(l=>l.id===id)).length;
 $('progress-text').textContent=$('progress').value+' / 9 sections marked read';
}
function go(id){
 current=navItems.some(n=>n.id===id)?id:'mission';renderNav();
 const lesson=data.lessons.find(l=>l.id===current);
 if(lesson){lastLesson=current;$('workspace').innerHTML='<div class="eyebrow">'+escapeHtml(lesson.label)+'</div><h2>'+escapeHtml(lesson.title)+'</h2>'+markdown(lesson.body)+'<div class="actions"><button class="btn" id="mark">'+(state.completed.includes(current)?'Marked read ✓':'Mark section read')+'</button><button class="btn secondary" id="next">Next section →</button></div>';
  $('mark').onclick=()=>{if(!state.completed.includes(current))state.completed.push(current);save();go(current);};
  $('next').onclick=()=>{const index=navItems.findIndex(n=>n.id===current);go(navItems[(index+1)%navItems.length].id);};
 }else if(current==='completed') renderAnalyzer(true);
 else if(current==='practice') renderPractice();
 else if(current==='analyzer') renderAnalyzer();
 else renderPortfolio();
 $('workspace').focus({preventScroll:true});
}
function renderPractice(){
 $('workspace').innerHTML='<div class="eyebrow">Practice workspace</div><h2>Prove the small things first.</h2><p>Multiple choice, fill-in-the-blank, fill-in-code, and fix-the-code challenges.</p><div class="note">Short-answer practice only: code is displayed, not executed. Run the Python tests and unseen lab for executable evidence. Answers are included in this open-source draft.</div>'+data.questions.map(q=>'<section class="question" id="card-'+q.id+'"><span class="eyebrow">'+escapeHtml(q.kind)+'</span><h3>'+escapeHtml(q.title)+'</h3><p>'+escapeHtml(q.prompt)+'</p>'+(q.starter?'<pre><code>'+escapeHtml(q.starter)+'</code></pre>':'')+(q.options?q.options.map((o,i)=>'<label><input type="radio" name="'+q.id+'" value="'+i+'">'+escapeHtml(o)+'</label>').join(''):'<label class="sr-only" for="answer-'+q.id+'">Your answer to '+escapeHtml(q.title)+'</label><input id="answer-'+q.id+'" type="text" autocomplete="off" placeholder="Type the missing token or answer">')+'<div class="actions"><button class="btn secondary" data-check="'+q.id+'">Check answer</button></div><div id="feedback-'+q.id+'" role="status"></div></section>').join('');
 document.querySelectorAll('[data-check]').forEach(button=>button.onclick=()=>{
   const q=data.questions.find(x=>x.id===button.dataset.check);
   const selected=document.querySelector('input[name="'+q.id+'"]:checked');
   const answer=q.options?(selected?q.options[Number(selected.value)]:''):$('answer-'+q.id).value;
   const correct=[q.answer,...(q.aliases||[])].some(x=>x.toLowerCase()===answer.trim().toLowerCase());
   state.answers[q.id]=correct;save();
   const feedback=$('feedback-'+q.id);feedback.className='feedback '+(correct?'good':'bad');feedback.textContent=(correct?'Correct. ':'Try again. ')+q.explanation;
 });
}
function baseline(text){
 const requirements=[];
 for(const part of text.split(/\n|(?<=[.!?])\s+/)){
  const evidence=part.trim();
  for(const [skill,pattern] of Object.entries(skills)){
   if(!new RegExp(pattern,'i').test(evidence))continue;
   const priority=/\b(?:not required|optional|nice to have|preferred|bonus)\b/i.test(evidence)?'preferred':/\b(?:required|must|mandatory|minimum)\b/i.test(evidence)?'required':'unspecified';
   if(!requirements.some(r=>r.skill===skill&&r.priority===priority&&r.evidence===evidence))requirements.push({skill,priority,evidence});
  }
 }
 return {mode:'rules-browser',requirements,limitations:['Keyword mentions are not proof of a hiring requirement.','Mixed priorities, heading scope, and negation require human review.','No model request was made. Use the Python project for live AI and hashed reports.']};
}
function renderAnalyzer(completed=false){
 $('workspace').innerHTML=(completed?'<div class="eyebrow">Finished reference application · Chapter 1</div><h2>Job Requirements Analyzer</h2><p>This is the working browser edition students can build toward. A fictional posting has already been analyzed. Edit it and run again to explore.</p><div class="note">Free rules mode runs here without an API key. The Python project adds Pydantic validation, source hashing, and optional live AI. Previewing this example does not complete your exercises.</div>':'<div class="eyebrow">Chapter project · browser demo</div><h2>Inspect the evidence.</h2><p>Paste a posting or try the fictional Plano example.</p><div class="note">Free deterministic baseline. This browser version uses keyword rules, not an LLM. The Python application includes the optional live AI adapter.</div>')+'<label for="posting">Job description</label><textarea id="posting" maxlength="20000"></textarea><div class="actions"><button class="btn" id="analyze">Analyze posting</button><button class="btn secondary" id="load-example">Load chapter example</button><button class="btn secondary" id="challenge">Try a failure case</button></div><p class="fine">Input stays in this browser. No model request is made.</p><div id="results" aria-live="polite"></div>'+(completed?'<div class="actions"><button class="btn secondary" id="return-lesson">← Return to my lesson</button></div>':'');
 $('posting').value=data.sample;
 $('load-example').onclick=()=>{$('posting').value=data.sample;$('analyze').click();};
 $('challenge').onclick=()=>{$('posting').value='Python is required, but Docker is preferred.';$('analyze').click();};
 $('analyze').onclick=()=>{
  const text=$('posting').value.trim();
  if(!text){$('results').textContent='Paste a job description before analyzing.';return;}
  if(text.length>20000){$('results').textContent='Use at most 20,000 characters.';return;}
  const result=baseline(text);
  const counts={required:0,preferred:0,unspecified:0};
  result.requirements.forEach(r=>counts[r.priority]++);
  $('results').innerHTML='<h3>'+result.requirements.length+' skill mentions</h3><p class="result-summary">'+counts.required+' required · '+counts.preferred+' preferred · '+counts.unspecified+' unspecified</p>'+(result.requirements.length?'<table><thead><tr><th>Skill</th><th>Priority</th><th>Source evidence</th></tr></thead><tbody>'+result.requirements.map(r=>'<tr><td>'+escapeHtml(r.skill)+'</td><td>'+escapeHtml(r.priority)+'</td><td>'+escapeHtml(r.evidence)+'</td></tr>').join('')+'</tbody></table>':'<p>No known skills found. The registry may be incomplete.</p>')+'<p class="fine">All displayed quotes occur in the input. This does not prove that each priority is correct. Salary, location, and years are not inferred. Re-run after editing.</p><details><summary>Inspect the JSON report</summary><pre><code>'+escapeHtml(JSON.stringify(result,null,2))+'</code></pre></details><div class="actions"><button id="export-result" class="btn secondary">Export browser report</button></div>';
  $('export-result').onclick=()=>download('browser-job-analysis.json',JSON.stringify(result,null,2));
 };
 if(completed){
   $('return-lesson').onclick=()=>go(lastLesson);
   $('analyze').click();
 }
}
function renderPortfolio(){
 const tasks=['Run Python tests and evaluation','Label an unseen posting before extraction','Document one failure and correction','Deploy the analyzer in rules mode','Publish source and setup instructions','Explain the provider boundary','Record whether live AI was tested','Record a two-minute demonstration'];
 if(!state.portfolio || typeof state.portfolio!=='object')state.portfolio={};
 $('workspace').innerHTML='<div class="eyebrow">Your release checklist</div><h2>Ship something you can defend.</h2><p>Turn chapter completion into inspectable engineering evidence.</p><div class="checklist">'+tasks.map((t,i)=>'<label><input type="checkbox" data-task="'+i+'" '+(state.portfolio[i]?'checked':'')+'> '+escapeHtml(t)+'</label>').join('')+'</div><div class="actions"><button class="btn" id="export-progress">Export progress</button><button class="btn secondary" id="reset-progress">Reset local progress</button></div><p class="fine">Self-reported progress is saved in this browser only. Export it before changing devices. No job matching or employer certification is active in this draft.</p>';
 document.querySelectorAll('[data-task]').forEach(c=>c.onchange=()=>{state.portfolio[c.dataset.task]=c.checked;save();});
 $('export-progress').onclick=()=>download('chapter-1-progress.json',JSON.stringify(state,null,2));
 $('reset-progress').onclick=()=>{if(confirm('Reset this browser’s chapter progress?')){state={completed:[],answers:{},portfolio:{}};save();go('portfolio');}};
}
$('run-completed').onclick=()=>go('completed');
go('mission');
