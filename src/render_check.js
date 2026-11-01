const fs = require('fs'), vm = require('vm'), path = require('path');
const root = process.argv[2]; let fail = 0;
const engine = fs.readFileSync(path.join(root, 'assets/practice.js'), 'utf8');
function ans(q, right) {
  if (q.type === 'single') return right ? q.answer : (q.answer + 1) % q.options.length;
  if (q.type === 'multi') return right ? q.answer.slice() : q.options.map((_, k) => k).filter(k => !q.answer.includes(k)).slice(0, q.pick);
  if (q.type === 'solution') return right ? q.answer : !q.answer;
  if (q.type === 'yesno') return q.statements.map(s => right ? s.answer : !s.answer);
  if (q.type === 'code') return q.blanks.map(b => right ? b.answer : (b.answer + 1) % b.options.length);
  if (q.type === 'order') return right ? q.answer.slice() : q.answer.slice().reverse();
}
function run(dir, state) {
  const host = { innerHTML: '', querySelectorAll: () => [], scrollIntoView() {} };
  const store = {};
  const ctx = { window: {}, document: { getElementById: id => id === 'bank' ? host : null, querySelectorAll: () => [] },
    localStorage: { getItem: k => k in store ? store[k] : null, setItem: (k, v) => { store[k] = v; } }, setInterval: () => 0, clearInterval() {}, Date, JSON, Math, String };
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(root, dir, 'bank.js'), 'utf8'), ctx);
  const B = ctx.window.BANK; ctx.window.BANK = B;
  if (state) { const st = state(B); store['dbx.' + B.id + (B.v ? '.v' + B.v : '')] = JSON.stringify(st); }
  vm.runInContext(engine, ctx);
  return { B, html: host.innerHTML };
}
const count = (s, re) => (s.match(re) || []).length;
for (const dir of ['S1-Design-Apps','S2-Data-Prep','S3-App-Dev','S4-Assemble-Deploy','S5-Governance','S6-Eval-Monitor','Mock-Exam-1']) {
  try {
    const a = run(dir); const n = a.B.items.length;
    const qs = count(a.html, /<article class="q"/g), ex0 = count(a.html, /class="expl"/g);
    const mk = right => B => ({ mode: 'practice', answers: Object.fromEntries(B.items.map(q => [q.id, ans(q, right)])), started: null, finished: false });
    const r = run(dir, mk(true)), w = run(dir, mk(false));
    const exR = count(r.html, /class="expl"/g), ok = count(r.html, /verdict ok/g), no = count(w.html, /verdict no/g);
    const why = a.B.items.filter(q => q.why).length, whyR = count(r.html, /class="whyall"/g);
    const e = run(dir, B => ({ mode: 'exam', answers: Object.fromEntries(B.items.map(q => [q.id, ans(q, true)])), started: Date.now(), finished: true }));
    const score = /Score: 100%/.test(e.html);
    const pass = qs === n && ex0 === 0 && exR === n && ok === n && no === n && whyR === why && score && !/undefined/.test(r.html + w.html);
    if (!pass) fail++;
    console.log(`${dir}: ${n} items · rendered ${qs} · explanations unanswered ${ex0}, answered ${exR} · all-right verdicts ${ok} · all-wrong verdicts ${no} · per-option why ${whyR}/${why} · exam-mode 100% ${score} · ${pass ? 'OK' : 'FAIL'}`);
  } catch (err) { fail++; console.log(dir, 'ERROR', err.stack); }
}
process.exit(fail ? 1 : 0);
