<# 
Resolution AI / Sovereign Reality Engine - ONE FOLDER BUILDER

Creates one working local folder:

  D:\Sovereign-Reality-Engine

If D:\ does not exist, fallback:

  %USERPROFILE%\Desktop\Sovereign-Reality-Engine

Creates:
  package.json
  server.mjs
  public\index.html
  START_RESOLUTION_AI.cmd
  CREATE_DESKTOP_ICON.cmd
  README_START_HERE.txt

Also creates desktop shortcut:
  %USERPROFILE%\Desktop\Resolution AI.lnk

This script is local-only. It does not upload data.
#>

$ErrorActionPreference = "Stop"

$Root = "D:\Sovereign-Reality-Engine"
if (-not (Test-Path "D:\")) {
  $Root = Join-Path $env:USERPROFILE "Desktop\Sovereign-Reality-Engine"
}

$Public = Join-Path $Root "public"
$Data = Join-Path $Root "data"
$Logs = Join-Path $Root "logs"

New-Item -ItemType Directory -Force -Path $Root, $Public, $Data, $Logs | Out-Null

function Write-Utf8 {
  param([string]$Path,[string]$Content)
  $Dir = Split-Path -Parent $Path
  if ($Dir) { New-Item -ItemType Directory -Force -Path $Dir | Out-Null }
  [System.IO.File]::WriteAllText($Path, $Content, [System.Text.UTF8Encoding]::new($false))
}

function Write-Ascii {
  param([string]$Path,[string]$Content)
  $Dir = Split-Path -Parent $Path
  if ($Dir) { New-Item -ItemType Directory -Force -Path $Dir | Out-Null }
  [System.IO.File]::WriteAllText($Path, $Content, [System.Text.ASCIIEncoding]::new())
}

$PackageJson = @'
{
  "name": "sovereign-reality-engine",
  "version": "1.0.0",
  "type": "module",
  "description": "Resolution AI - local Verified AI Operations dashboard",
  "scripts": {
    "start": "node server.mjs",
    "check": "node --check server.mjs"
  },
  "dependencies": {
    "express": "latest"
  },
  "engines": {
    "node": ">=18"
  }
}
'@

$Server = @'
import express from "express";
import fs from "fs";
import path from "path";
import crypto from "crypto";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const app = express();

const PORT = process.env.PORT || 3030;
const DATA_ROOT = process.env.RA_DATA_ROOT || (fs.existsSync("D:/") ? "D:/SovereignRA" : path.join(__dirname, "data"));
const PRIVATE_DIR = path.join(DATA_ROOT, "data", "private");
const LOG_DIR = path.join(DATA_ROOT, "logs");
const uploadsDir = path.join(PRIVATE_DIR, "uploads");

fs.mkdirSync(PRIVATE_DIR, { recursive: true });
fs.mkdirSync(LOG_DIR, { recursive: true });
fs.mkdirSync(uploadsDir, { recursive: true });

app.use((req, res, next) => {
  res.setHeader("Cache-Control", "no-store, no-cache, must-revalidate, proxy-revalidate");
  res.setHeader("Pragma", "no-cache");
  res.setHeader("Expires", "0");
  next();
});

app.use(express.json({ limit: "30mb" }));
app.use(express.static(path.join(__dirname, "public"), { etag: false, maxAge: 0, lastModified: false }));

const graphFile = path.join(PRIVATE_DIR, "graph.json");
const auditFile = path.join(LOG_DIR, "sovereign_audit.jsonl");
const settingsFile = path.join(PRIVATE_DIR, "settings.json");

function sha256(x) {
  return crypto.createHash("sha256").update(String(x)).digest("hex");
}

function readJson(file, fallback) {
  try { return JSON.parse(fs.readFileSync(file, "utf8")); } catch { return fallback; }
}

function writeJson(file, data) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, JSON.stringify(data, null, 2));
}

function safeText(x) {
  return String(x || "").replace(/[\u0000-\u001f\u007f]/g, " ").slice(0, 200000);
}

function defaultGraph() {
  return [
    { id: "NODE-RA-001", claim: "Verified AI Operations routes AI output through verification before operational trust.", tags: ["verified-ai-operations","method","ra"], status: "rooted" },
    { id: "NODE-RA-002", claim: "Completion language must be blocked unless completion proof exists.", tags: ["completion-proof","false-completion"], status: "rooted" },
    { id: "NODE-RA-003", claim: "User-owned local storage is the default privacy posture.", tags: ["privacy","local-storage","D-drive"], status: "rooted" },
    { id: "NODE-RA-004", claim: "Unverified answers should still be returned with a clear Not Verified badge when safe.", tags: ["verification","ux"], status: "rooted" },
    { id: "NODE-RA-005", claim: "Hosted models are candidate generators, not final truth authorities.", tags: ["hosted-ai","ra-refinery"], status: "rooted" },
    { id: "NODE-RA-006", claim: "Robots require task state, authority, sensor evidence, safety envelope, abort path, completion proof, and audit record before physical action.", tags: ["robotics","safety","baseline"], status: "rooted" }
  ];
}

function getGraph() {
  const g = readJson(graphFile, null);
  if (Array.isArray(g) && g.length) return g;
  const seed = defaultGraph();
  writeJson(graphFile, seed);
  return seed;
}

function getSettings() {
  const defaults = {
    theme: "resolution_assurance_blue",
    provider: "anthropic",
    providerLabel: "Claude",
    fallbackProvider: "local",
    retrievalBudgetMs: 1800,
    modelTimeoutMs: 8000,
    stream: true,
    localStorageRoot: DATA_ROOT,
    allowUnverifiedAnswer: true,
    blockFalseCompletion: true,
    fastMode: true
  };
  return { ...defaults, ...readJson(settingsFile, {}) };
}

function audit(event) {
  let prevHash = "GENESIS";
  try {
    const lines = fs.readFileSync(auditFile, "utf8").trim().split(/\r?\n/).filter(Boolean);
    if (lines.length) prevHash = JSON.parse(lines[lines.length - 1]).hash || prevHash;
  } catch {}
  const record = { ts: new Date().toISOString(), prevHash, ...event };
  record.hash = sha256(JSON.stringify(record));
  fs.appendFileSync(auditFile, JSON.stringify(record) + "\n");
  return record;
}

function searchGraph(query, limit = 8) {
  const q = String(query || "").toLowerCase().split(/\W+/).filter(Boolean);
  if (!q.length) return getGraph().slice(0, limit);
  return getGraph()
    .map(n => {
      const hay = `${n.id} ${n.claim} ${(n.tags || []).join(" ")}`.toLowerCase();
      const score = q.reduce((a, t) => a + (hay.includes(t) ? 1 : 0), 0);
      return { ...n, score };
    })
    .filter(n => n.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit);
}

function refine(question, draft, evidence) {
  const text = `${question} ${draft}`;
  const highImpact = /value|valuation|breach|legal|refund|compensation|robot|dose|cut|heat|lift|transport|completed|done|fixed|sealed|wired|located|tested/i.test(text);
  const completionClaim = /\b(done|completed|fixed|sealed|wired|located|tested|fully operational)\b/i.test(draft);

  let status = "Not Verified";
  let grade = "F";

  if (evidence.length >= 3 && !completionClaim) {
    status = "Verified";
    grade = "A";
  } else if (evidence.length >= 1 && !completionClaim) {
    status = "Partially Verified";
    grade = "C";
  }

  if (completionClaim && !evidence.some(e => /completion|audit|proof/i.test((e.tags || []).join(" ") + e.claim))) {
    status = "Action Not Completed";
    grade = "F";
  }

  if (highImpact && evidence.length < 2) {
    status = completionClaim ? "Action Not Completed" : "Not Verified";
    grade = "F";
  }

  return { status, grade, evidenceIds: evidence.map(e => e.id), unverified: status !== "Verified" };
}

function localAnswer(question, evidence, reason = "") {
  const evidenceText = evidence.map(e => `- ${e.id}: ${e.claim}`).join("\n") || "- No matching local evidence nodes.";
  return `${reason ? reason + "\n\n" : ""}I can answer from the local Resolution Assurance layer.\n\n${evidenceText}\n\nAnswer:\n${question}\n\nStatus note: this response is labelled by RA Refinery based on available local evidence.`;
}

async function claudeAnswer(question, evidence) {
  const key = process.env.ANTHROPIC_API_KEY || process.env.CLAUDE_API_KEY;
  if (!key) return null;

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), Number(getSettings().modelTimeoutMs || 8000));
  const evidenceText = evidence.map(e => `- ${e.id}: ${e.claim}`).join("\n") || "No matching local evidence nodes.";

  try {
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      signal: controller.signal,
      headers: {
        "content-type": "application/json",
        "x-api-key": key,
        "anthropic-version": "2023-06-01"
      },
      body: JSON.stringify({
        model: process.env.RA_MODEL || "claude-3-5-sonnet-latest",
        max_tokens: 900,
        system: "You are Resolution AI. Answer like a normal helpful chatbot. Do not claim done/fixed/completed unless evidence proves it. If evidence is weak, answer but acknowledge uncertainty.",
        messages: [{ role: "user", content: `Question:\n${question}\n\nLocal evidence:\n${evidenceText}` }]
      })
    });

    const j = await r.json().catch(() => ({}));
    if (!r.ok) return localAnswer(question, evidence, `Claude provider returned ${r.status}. Falling back locally.`);
    return (j.content || []).map(c => c.text || "").join("\n").trim() || localAnswer(question, evidence, "Claude returned empty output. Falling back locally.");
  } catch (err) {
    return localAnswer(question, evidence, `Claude timed out or failed (${err.name || "error"}). Falling back locally.`);
  } finally {
    clearTimeout(timeout);
  }
}

async function draftAnswer(question, evidence) {
  return await claudeAnswer(question, evidence) || localAnswer(question, evidence);
}

app.get("/api/status", (req, res) => {
  res.json({
    ok: true,
    app: "Resolution AI / Sovereign Reality Engine",
    version: "1.0.0-one-folder-blue",
    port: PORT,
    provider: (process.env.ANTHROPIC_API_KEY || process.env.CLAUDE_API_KEY) ? "Claude / Anthropic" : "Local evidence fallback",
    dataRoot: DATA_ROOT,
    settings: getSettings()
  });
});

app.get("/api/settings", (req, res) => res.json(getSettings()));

app.post("/api/settings", (req, res) => {
  const next = { ...getSettings(), ...(req.body || {}) };
  writeJson(settingsFile, next);
  const aud = audit({ type: "settings_update", settingsHash: sha256(JSON.stringify(next)) });
  res.json({ ok: true, settings: next, audit: aud.hash });
});

app.post("/api/chat", async (req, res) => {
  const question = safeText(req.body?.message || req.body?.question).trim();
  if (!question) return res.status(400).json({ error: "message required" });

  const trace = [{ step: "classify", status: "ok" }];
  const evidence = searchGraph(question, getSettings().maxGraphNodes || 8);
  trace.push({ step: "graph", status: "ok", count: evidence.length });

  const draft = await draftAnswer(question, evidence);
  trace.push({ step: "model", status: (process.env.ANTHROPIC_API_KEY || process.env.CLAUDE_API_KEY) ? "claude_or_fallback" : "local_fallback" });

  const verification = refine(question, draft, evidence);
  trace.push({ step: "ra_refinery", status: verification.status, grade: verification.grade });

  const aud = audit({ type: "chat", questionHash: sha256(question), verification, evidenceIds: verification.evidenceIds });
  res.json({ answer: draft, verification, trace, audit: { id: aud.hash, prevHash: aud.prevHash }, evidence });
});

app.get("/api/graph/search", (req, res) => {
  res.json({ results: searchGraph(String(req.query.q || ""), Number(req.query.limit || 20)) });
});

app.post("/api/graph/anchor", (req, res) => {
  const graph = getGraph();
  const node = {
    id: req.body?.id || `NODE-${Date.now()}`,
    claim: safeText(req.body?.claim),
    tags: req.body?.tags || [],
    status: "rooted",
    createdAt: new Date().toISOString()
  };
  graph.push(node);
  writeJson(graphFile, graph);
  const aud = audit({ type: "graph_anchor", nodeId: node.id, claimHash: sha256(node.claim) });
  res.json({ node, audit: aud.hash });
});

app.get("/api/audit", (req, res) => {
  try { res.type("text/plain").send(fs.readFileSync(auditFile, "utf8")); }
  catch { res.type("text/plain").send(""); }
});

app.get("/api/legal", (req, res) => {
  res.json({
    privacy: "Local-first storage. Hosted provider use is optional and outputs are candidate material until verified.",
    terms: "Prototype method documentation for Verified AI Operations. Human review required for high-impact decisions.",
    acceptableUse: "Do not use for unlawful access, unsafe physical action, or unsupported completion claims.",
    verification: "Every answer receives Verified, Partially Verified, Not Verified, Insufficient Evidence, Action Not Completed, or Refused for Safety."
  });
});

app.post("/api/upload", (req, res) => {
  const name = String(req.body?.name || `upload-${Date.now()}.txt`).replace(/[\\/:*?"<>|]/g, "_");
  const content = safeText(req.body?.content || "");
  const file = path.join(uploadsDir, name);
  fs.writeFileSync(file, content);
  const h = sha256(content);
  const node = { id: `UPLOAD-${Date.now()}`, claim: `Uploaded local text file ${name}`, tags: ["upload","local"], status: "rooted", sha256: h, path: file };
  const graph = getGraph();
  graph.push(node);
  writeJson(graphFile, graph);
  const aud = audit({ type: "upload", file: name, sha256: h });
  res.json({ ok: true, file, node, audit: aud.hash });
});

app.get("*", (req, res) => res.sendFile(path.join(__dirname, "public", "index.html")));

app.listen(PORT, () => console.log(`Resolution AI running at http://localhost:${PORT}`));
'@

$Index = @'
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width,initial-scale=1" />
<meta http-equiv="Cache-Control" content="no-store" />
<title>Resolution AI</title>
<style>
:root{--blue950:#061826;--blue900:#082033;--blue850:#0B2D45;--blue700:#155D7A;--teal:#22A6A6;--gold:#C9A227;--paper:#F6F8FA;--card:#fff;--ink:#102030;--muted:#607080;--border:#D8E4EA;--danger:#B42318;--success:#027A48;--warn:#B54708}
*{box-sizing:border-box}
body{margin:0;font-family:Inter,Segoe UI,Arial,sans-serif;background:var(--paper)!important;color:var(--ink);height:100vh;overflow:hidden}
.app{display:grid;grid-template-columns:274px 1fr;height:100vh}
.side{background:linear-gradient(180deg,var(--blue950),var(--blue850))!important;color:#f7fbfc;padding:18px;display:flex;flex-direction:column;gap:12px}
.brand{display:flex;gap:12px;align-items:center;font-weight:850;margin-bottom:4px}
.mark{width:42px;height:42px;border-radius:14px;background:linear-gradient(135deg,#2fc7c7,#e2c15b);display:grid;place-items:center;color:var(--blue950);font-weight:950}
.brand-sub{font-size:12px;color:#b9d6df}
.navbtn{border:1px solid rgba(255,255,255,.18);background:rgba(255,255,255,.08);color:#fff;border-radius:14px;padding:11px 12px;text-align:left;cursor:pointer;font-weight:650}
.navbtn:hover,.navbtn.active{background:rgba(34,166,166,.26);border-color:rgba(47,199,199,.58)}
.side-status{font-size:12px;color:#b9d6df;line-height:1.45;margin-top:auto}
.main{display:flex;flex-direction:column;min-width:0;background:var(--paper)}
.top{height:58px;background:rgba(255,255,255,.92);border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;padding:0 20px}
.provider{font-size:13px;color:var(--muted);max-width:55vw;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.chat{flex:1;overflow:auto;padding:24px 0}
.inner{width:min(920px,calc(100% - 32px));margin:0 auto}
.empty{text-align:center;margin-top:10vh;color:var(--muted)}
.empty h1{color:var(--blue900);margin-bottom:8px}
.msg{display:flex;gap:14px;margin:18px 0}
.avatar{width:34px;height:34px;border-radius:999px;display:grid;place-items:center;font-weight:850;flex:0 0 auto}
.avatar.ai{background:linear-gradient(135deg,var(--blue700),var(--teal));color:#fff}
.avatar.you{background:#EAF5F8;color:var(--blue900)}
.bubble{background:var(--card);border:1px solid var(--border);border-radius:18px;padding:14px 16px;box-shadow:0 8px 24px rgba(8,32,51,.06);white-space:pre-wrap;line-height:1.45;max-width:100%}
.you .bubble{background:#EAF5F8}
.badge{display:inline-flex;align-items:center;gap:6px;border-radius:999px;padding:5px 10px;font-size:12px;font-weight:850;margin-bottom:10px}
.verified{background:#E6F4EA;color:var(--success);border:1px solid #A6D8B5}
.partial{background:#FFF7E6;color:var(--warn);border:1px solid #F2C94C}
.not{background:#FEE4E2;color:var(--danger);border:1px solid #FDA29B}
.trace{font-size:12px;color:var(--muted);margin-top:10px;border-top:1px solid var(--border);padding-top:8px}
.composer{background:rgba(255,255,255,.96);border-top:1px solid var(--border);padding:10px}
.bar{width:min(920px,calc(100% - 32px));margin:0 auto;display:flex;gap:8px;align-items:flex-end;border:1px solid var(--border);border-radius:18px;background:white;box-shadow:0 10px 30px rgba(8,32,51,.1);padding:8px}
.icon{border:0;background:#EEF6F8;color:var(--blue900);border-radius:12px;width:38px;height:38px;cursor:pointer;font-weight:850}
.icon:hover{background:#DFF0F4}
textarea{flex:1;border:0;outline:0;resize:none;max-height:88px;min-height:38px;font:inherit;padding:9px;background:transparent;color:var(--ink)}
.send{border:0;background:linear-gradient(135deg,var(--blue700),var(--teal));color:white;border-radius:12px;height:38px;padding:0 16px;font-weight:850;cursor:pointer}
.panel{display:none}
.panel.active{display:block}
.card{background:white;border:1px solid var(--border);border-radius:18px;padding:16px;box-shadow:0 8px 24px rgba(8,32,51,.06);margin:14px 0}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.field{display:flex;flex-direction:column;gap:6px;font-size:13px}
.field input,.field select{border:1px solid var(--border);border-radius:12px;padding:10px;background:#fff;color:var(--ink)}
pre{white-space:pre-wrap;background:#f7fbfc;border:1px solid var(--border);border-radius:14px;padding:12px;max-height:50vh;overflow:auto}
.fileinput{display:none}
@media(max-width:780px){.app{grid-template-columns:1fr}.side{display:none}.top{padding:0 12px}.inner,.bar{width:calc(100% - 18px)}}
</style>
</head>
<body>
<div class="app">
  <aside class="side">
    <div class="brand"><div class="mark">RA</div><div><div>Resolution AI</div><div class="brand-sub">Verified AI Operations</div></div></div>
    <button class="navbtn active" onclick="showPanel('chat',this)">＋ New / Chat</button>
    <button class="navbtn" onclick="showPanel('graph',this); loadGraph()">Evidence Graph</button>
    <button class="navbtn" onclick="showPanel('audit',this); loadAudit()">Audit Log</button>
    <button class="navbtn" onclick="showPanel('legal',this); loadLegal()">Privacy / Legal</button>
    <button class="navbtn" onclick="showPanel('settings',this); loadSettings()">Settings</button>
    <button class="navbtn" onclick="testProvider()">Test Provider</button>
    <button class="navbtn" onclick="clearCacheReload()">Force Blue Reload</button>
    <div class="side-status" id="sideStatus"><b>Privacy:</b> local-first storage.<br><b>Provider:</b> Claude first, local fallback.<br><b>Rule:</b> answer + badge.</div>
  </aside>
  <main class="main">
    <header class="top"><b id="title">Resolution AI</b><span class="provider" id="status">Checking…</span></header>
    <section class="chat"><div class="inner">
      <div id="chatPanel" class="panel active"><div id="messages"><div class="empty"><h1>How can I help?</h1><p>Ask normally. I’ll answer normally and label the result Verified or Not Verified.</p></div></div></div>
      <div id="graphPanel" class="panel"><h2>Evidence Graph</h2><div class="card"><input id="graphQ" placeholder="Search graph…" onkeydown="if(event.key==='Enter')loadGraph()" style="width:100%;border:1px solid var(--border);border-radius:12px;padding:10px"><pre id="graphOut">Loading…</pre></div></div>
      <div id="auditPanel" class="panel"><h2>Audit Log</h2><div class="card"><pre id="auditOut">Loading…</pre></div></div>
      <div id="legalPanel" class="panel"><h2>Privacy / Legal</h2><div class="card"><pre id="legalOut">Loading…</pre></div></div>
      <div id="settingsPanel" class="panel"><h2>Settings</h2><div class="card grid"><label class="field">Provider<select id="provider"><option value="anthropic">Claude / Anthropic</option><option value="local">Local fallback</option></select></label><label class="field">Retrieval budget ms<input id="budget" type="number" value="1800"></label><label class="field">Theme<input value="resolution_assurance_blue" disabled></label><label class="field">Storage root<input id="storage" disabled></label></div><button class="send" onclick="saveSettings()">Save Settings</button><pre id="settingsOut"></pre></div>
    </div></section>
    <div class="composer"><div class="bar"><input id="file" class="fileinput" type="file" onchange="attachFile(this.files[0])"><button class="icon" onclick="document.getElementById('file').click()" title="Attach">＋</button><button class="icon" onclick="mic()" title="Microphone">🎙</button><textarea id="input" placeholder="Message Resolution AI…" rows="1"></textarea><button class="send" onclick="send()">Send</button></div></div>
  </main>
</div>
<script>
const messages=document.getElementById('messages'), input=document.getElementById('input');let first=true;
function $(id){return document.getElementById(id)}
input.addEventListener('keydown',e=>{if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send();}});
input.addEventListener('input',()=>{input.style.height='auto';input.style.height=Math.min(input.scrollHeight,88)+'px'});
async function api(url,opts){const r=await fetch(url,{cache:'no-store',...opts});if(!r.ok)throw new Error(url+' '+r.status);return await (r.headers.get('content-type')||'').includes('json')?r.json():r.text()}
async function status(){try{const j=await api('/api/status');$('status').textContent=j.provider+' · '+j.dataRoot;$('sideStatus').innerHTML='<b>Provider:</b> '+j.provider+'<br><b>Storage:</b> '+j.dataRoot+'<br><b>Version:</b> '+j.version}catch(e){$('status').textContent='server offline';$('sideStatus').textContent='Server offline'}}status();
function showPanel(name,btn){document.querySelectorAll('.panel').forEach(p=>p.classList.remove('active'));document.querySelectorAll('.navbtn').forEach(b=>b.classList.remove('active'));$(name+'Panel').classList.add('active');if(btn)btn.classList.add('active');$('title').textContent=name==='chat'?'Resolution AI':name[0].toUpperCase()+name.slice(1)}
function clearCacheReload(){location.href='/?v='+Date.now()}
function add(role,text,ver,trace){if(first){messages.innerHTML='';first=false}const wrap=document.createElement('div');wrap.className='msg '+(role==='you'?'you':'ai');const av=document.createElement('div');av.className='avatar '+(role==='you'?'you':'ai');av.textContent=role==='you'?'Y':'RA';const bub=document.createElement('div');bub.className='bubble';if(ver){const b=document.createElement('div');let cls=ver.status==='Verified'?'verified':ver.status==='Partially Verified'?'partial':'not';b.className='badge '+cls;b.textContent=ver.status+' · '+ver.grade;bub.appendChild(b)}const body=document.createElement('div');body.textContent=text;bub.appendChild(body);if(trace){const t=document.createElement('div');t.className='trace';t.textContent='Working: '+trace.map(x=>x.step+': '+x.status).join(' → ');bub.appendChild(t)}wrap.appendChild(av);wrap.appendChild(bub);messages.appendChild(wrap);messages.closest('.chat').scrollTop=messages.closest('.chat').scrollHeight}
async function send(){showPanel('chat',document.querySelector('.navbtn'));const q=input.value.trim();if(!q)return;input.value='';input.style.height='38px';add('you',q);add('ai','Working…',{status:'Partially Verified',grade:'…'},[{step:'starting',status:'ok'}]);const pending=messages.lastChild;try{const j=await api('/api/chat',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({message:q})});pending.remove();add('ai',j.answer||JSON.stringify(j),j.verification,j.trace);status()}catch(e){pending.remove();add('ai','Server error: '+e.message,{status:'Not Verified',grade:'F'},[{step:'error',status:'failed'}])}}
async function loadGraph(){try{const q=encodeURIComponent($('graphQ')?.value||'');const j=await api('/api/graph/search?q='+q+'&limit=50');$('graphOut').textContent=JSON.stringify(j,null,2)}catch(e){$('graphOut').textContent=e.message}}
async function loadAudit(){try{$('auditOut').textContent=await api('/api/audit')}catch(e){$('auditOut').textContent=e.message}}
async function loadLegal(){try{$('legalOut').textContent=JSON.stringify(await api('/api/legal'),null,2)}catch(e){$('legalOut').textContent=e.message}}
async function loadSettings(){try{const j=await api('/api/settings');$('provider').value=j.provider||'anthropic';$('budget').value=j.retrievalBudgetMs||1800;$('storage').value=j.localStorageRoot||'';$('settingsOut').textContent=JSON.stringify(j,null,2)}catch(e){$('settingsOut').textContent=e.message}}
async function saveSettings(){try{const j=await api('/api/settings',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({provider:$('provider').value,retrievalBudgetMs:Number($('budget').value),theme:'resolution_assurance_blue'})});$('settingsOut').textContent=JSON.stringify(j,null,2);status()}catch(e){$('settingsOut').textContent=e.message}}
async function testProvider(){showPanel('chat',document.querySelector('.navbtn'));input.value='Provider test: reply with one sentence and verification badge.';await send()}
async function attachFile(file){if(!file)return;const text=await file.text().catch(()=>null);if(text==null){add('ai','Attachment could not be read as text.',{status:'Not Verified',grade:'F'});return}try{await api('/api/upload',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({name:file.name,content:text})});add('ai','Attached and anchored locally: '+file.name,{status:'Partially Verified',grade:'C'},[{step:'upload',status:'ok'}])}catch(e){add('ai','Upload failed: '+e.message,{status:'Not Verified',grade:'F'})}}
function mic(){if(!('webkitSpeechRecognition'in window||'SpeechRecognition'in window)){alert('Speech recognition not available in this browser.');return}const SR=window.SpeechRecognition||window.webkitSpeechRecognition;const rec=new SR();rec.lang='en-AU';rec.onresult=e=>{input.value=e.results[0][0].transcript;input.dispatchEvent(new Event('input'))};rec.start()}
</script>
</body>
</html>
'@

$StartCmd = @'
@echo off
setlocal
cd /d "%~dp0"
title Resolution AI - Sovereign Reality Engine
set RA_PROVIDER=anthropic
set RA_DEFAULT_PROVIDER=anthropic
set RA_FALLBACK_PROVIDER=local
set RA_THEME=resolution_assurance_blue
set RA_FAST_MODE=1
set RA_PARALLEL_RETRIEVAL=1
set RA_STREAM=1
where node >nul 2>nul
if errorlevel 1 (
  echo Node.js is required. Install Node.js LTS from https://nodejs.org/
  pause
  exit /b 1
)
if not exist node_modules\express (
  echo Installing required modules...
  call npm install
  if errorlevel 1 (
    echo npm install failed.
    pause
    exit /b 1
  )
)
echo Starting Resolution AI on http://localhost:3030
start "" "http://localhost:3030/?v=%RANDOM%%RANDOM%"
node server.mjs
pause
'@

$IconCmd = @'
@echo off
setlocal
set TARGET=%~dp0START_RESOLUTION_AI.cmd
set SHORTCUT=%USERPROFILE%\Desktop\Resolution AI.lnk
powershell -NoProfile -ExecutionPolicy Bypass -Command "$W=New-Object -ComObject WScript.Shell; $S=$W.CreateShortcut('%SHORTCUT%'); $S.TargetPath='%TARGET%'; $S.WorkingDirectory='%~dp0'; $S.IconLocation='%SystemRoot%\System32\shell32.dll,44'; $S.Save()"
echo Created desktop icon: %SHORTCUT%
pause
'@

$Readme = @"
Resolution AI / Sovereign Reality Engine

WORKING FOLDER:
$Root

START FILE:
$Root\START_RESOLUTION_AI.cmd

DESKTOP ICON:
$env:USERPROFILE\Desktop\Resolution AI.lnk

DATA ROOT:
D:\SovereignRA

This one-folder build is blue, Claude-first, local-fallback, and includes working left buttons:
- New / Chat
- Evidence Graph
- Audit Log
- Privacy / Legal
- Settings
- Test Provider
- Force Blue Reload
"@

Write-Utf8 (Join-Path $Root "package.json") $PackageJson
Write-Utf8 (Join-Path $Root "server.mjs") $Server
Write-Utf8 (Join-Path $Public "index.html") $Index
Write-Ascii (Join-Path $Root "START_RESOLUTION_AI.cmd") $StartCmd
Write-Ascii (Join-Path $Root "CREATE_DESKTOP_ICON.cmd") $IconCmd
Write-Utf8 (Join-Path $Root "README_START_HERE.txt") $Readme

try {
  $W = New-Object -ComObject WScript.Shell
  $S = $W.CreateShortcut((Join-Path $env:USERPROFILE "Desktop\Resolution AI.lnk"))
  $S.TargetPath = Join-Path $Root "START_RESOLUTION_AI.cmd"
  $S.WorkingDirectory = $Root
  $S.IconLocation = "$env:SystemRoot\System32\shell32.dll,44"
  $S.Save()
} catch {}

$Manifest = @()
Get-ChildItem $Root -Recurse -File | ForEach-Object {
  try {
    $Manifest += "$((Get-FileHash $_.FullName -Algorithm SHA256).Hash)  $($_.FullName)"
  } catch {}
}
Write-Utf8 (Join-Path $Root "SHA256_MANIFEST.txt") ($Manifest -join "`r`n")

Write-Host ""
Write-Host "BUILT ONE WORKING FOLDER:"
Write-Host "  $Root"
Write-Host ""
Write-Host "START FILE:"
Write-Host "  $(Join-Path $Root 'START_RESOLUTION_AI.cmd')"
Write-Host ""
Write-Host "DESKTOP ICON:"
Write-Host "  $(Join-Path $env:USERPROFILE 'Desktop\Resolution AI.lnk')"
Write-Host ""
Write-Host "Open the desktop icon or START_RESOLUTION_AI.cmd."
Write-Host ""
pause
