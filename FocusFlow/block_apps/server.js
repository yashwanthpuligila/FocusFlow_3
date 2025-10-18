const express = require('express');
const fs = require('fs');
const path = require('path');
const cors = require('cors');

const app = express();
// Allow CORS from any origin during development so the frontend (which may run on
// 3000, 3002, etc.) can call the API without preflight/CORS failures.
app.use(cors());
app.use(express.json());

const BASE = path.join(__dirname);
const BLOCKLIST_FILE = path.join(BASE, 'blocklist.txt');
const FLAG_FILE = path.join(BASE, 'block_enabled.txt');

function readFlag() {
  try {
    return fs.existsSync(FLAG_FILE) && fs.readFileSync(FLAG_FILE, 'utf8').trim() === '1';
  } catch (e) {
    return false;
  }
}

app.get('/status', (req, res) => {
  res.json({ enabled: readFlag() });
});

app.post('/enable', (req, res) => {
  try {
    fs.writeFileSync(FLAG_FILE, '1', 'utf8');
    res.json({ ok: true, enabled: true });
  } catch (err) {
    res.status(500).json({ ok: false, error: err.message });
  }
});

app.post('/disable', (req, res) => {
  try {
    fs.writeFileSync(FLAG_FILE, '0', 'utf8');
    res.json({ ok: true, enabled: false });
  } catch (err) {
    res.status(500).json({ ok: false, error: err.message });
  }
});

app.get('/blocklist', (req, res) => {
  try {
    const txt = fs.existsSync(BLOCKLIST_FILE) ? fs.readFileSync(BLOCKLIST_FILE, 'utf8') : '';
    const sites = txt.split(/\r?\n/).map(s => s.trim()).filter(Boolean);
    res.json({ sites });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.post('/blocklist', (req, res) => {
  try {
    const sites = Array.isArray(req.body.sites) ? req.body.sites : [];
    const content = sites.map(s => s.trim()).filter(Boolean).join('\n') + (sites.length ? '\n' : '');
    fs.writeFileSync(BLOCKLIST_FILE, content, 'utf8');
    res.json({ ok: true });
  } catch (err) {
    res.status(500).json({ ok: false, error: err.message });
  }
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`[server] API listening on http://localhost:${PORT}`);
  console.log(`[server] Reading/writing: ${BLOCKLIST_FILE}, ${FLAG_FILE}`);
});
