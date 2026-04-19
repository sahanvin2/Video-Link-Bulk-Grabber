const creatorUrlEl = document.getElementById('creatorUrl');
const platformEl = document.getElementById('platform');
const qualityEl = document.getElementById('quality');
const maxItemsEl = document.getElementById('maxItems');
const grabBtn = document.getElementById('grabBtn');
const copyBtn = document.getElementById('copyBtn');
const txtBtn = document.getElementById('txtBtn');
const csvBtn = document.getElementById('csvBtn');
const resultBox = document.getElementById('resultBox');
const statusEl = document.getElementById('status');
const metaEl = document.getElementById('meta');

let latestLinks = [];

function setBusy(isBusy) {
  grabBtn.disabled = isBusy;
  if (isBusy) {
    statusEl.textContent = 'Fetching links...';
  }
}

function setExportEnabled(enabled) {
  copyBtn.disabled = !enabled;
  txtBtn.disabled = !enabled;
  csvBtn.disabled = !enabled;
}

function toCsv(lines) {
  const rows = ['index,link'];
  lines.forEach((item, idx) => {
    const escaped = '"' + item.replaceAll('"', '""') + '"';
    rows.push(`${idx + 1},${escaped}`);
  });
  return rows.join('\n');
}

function downloadText(content, filename, mime) {
  const blob = new Blob([content], { type: mime });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}

grabBtn.addEventListener('click', async () => {
  const creator_url = creatorUrlEl.value.trim();
  if (!creator_url) {
    statusEl.textContent = 'Enter a creator URL first.';
    return;
  }

  const body = {
    creator_url,
    platform: platformEl.value,
    quality: qualityEl.value,
    max_items: Number(maxItemsEl.value || 5000),
  };

  setBusy(true);
  setExportEnabled(false);
  resultBox.value = '';
  metaEl.textContent = '';

  try {
    const response = await fetch('/api/grab', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.detail || 'Request failed');
    }

    latestLinks = data.links || [];
    resultBox.value = latestLinks.join('\n');
    statusEl.textContent = `Done. ${data.total} links found.`;
    metaEl.textContent = `Platform: ${data.platform} | Source: ${data.source}${data.note ? ` | ${data.note}` : ''}`;
    setExportEnabled(latestLinks.length > 0);
  } catch (err) {
    latestLinks = [];
    resultBox.value = '';
    setExportEnabled(false);
    statusEl.textContent = `Error: ${err.message}`;
    metaEl.textContent = '';
  } finally {
    setBusy(false);
  }
});

copyBtn.addEventListener('click', async () => {
  if (!latestLinks.length) return;
  try {
    await navigator.clipboard.writeText(latestLinks.join('\n'));
    statusEl.textContent = `Copied ${latestLinks.length} links to clipboard.`;
  } catch {
    statusEl.textContent = 'Clipboard copy failed in this browser context.';
  }
});

txtBtn.addEventListener('click', () => {
  if (!latestLinks.length) return;
  downloadText(latestLinks.join('\n') + '\n', 'links.txt', 'text/plain;charset=utf-8');
});

csvBtn.addEventListener('click', () => {
  if (!latestLinks.length) return;
  downloadText(toCsv(latestLinks), 'links.csv', 'text/csv;charset=utf-8');
});
