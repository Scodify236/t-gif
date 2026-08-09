"""
Toolbar injected into every page the window shows (both the real app and
the local offline screen), via `window.evaluate_js(...)` after each
`loaded` event. It never touches or reveals the underlying page address —
it only overlays a fixed bar with three buttons (Refresh, Update, About)
and wires them to the Python-side API.
"""

# Disables right-click / "Inspect" / "View source" so the underlying
# address can't be discovered through the context menu, and prevents text
# selection artifacts on the toolbar itself.
HARDENING_JS = """
(function(){
  document.addEventListener('contextmenu', function(e){ e.preventDefault(); });
})();
"""

# Clears client-side storage before a hard "Update" reload. Wrapped
# defensively since not every API is available in every environment.
CLEAR_STORAGE_JS = """
(function(){
  try {
    if (window.caches && caches.keys) {
      caches.keys().then(function(keys){
        keys.forEach(function(k){ caches.delete(k); });
      });
    }
  } catch (e) {}
  try { localStorage.clear(); } catch (e) {}
  try { sessionStorage.clear(); } catch (e) {}
  try {
    if (window.indexedDB && indexedDB.databases) {
      indexedDB.databases().then(function(dbs){
        dbs.forEach(function(db){
          if (db && db.name) { indexedDB.deleteDatabase(db.name); }
        });
      });
    }
  } catch (e) {}
})();
"""

# Builds and injects the fixed top toolbar + About modal. Guards against
# double-injection; re-run safely on every page load.
TOOLBAR_JS = r"""
(function(){
  if (document.getElementById('gcvx-toolbar-root')) { return; }

  var TOOLBAR_H = 46;

  var style = document.createElement('style');
  style.id = 'gcvx-toolbar-style';
  style.textContent =
    '#gcvx-toolbar-root{position:fixed;top:0;left:0;right:0;height:' + TOOLBAR_H + 'px;' +
    'background:rgba(15,23,42,0.94);backdrop-filter:blur(6px);border-bottom:1px solid #334155;' +
    'display:flex;align-items:center;justify-content:space-between;padding:0 14px;' +
    'z-index:2147483647;font-family:"Segoe UI",Arial,sans-serif;-webkit-user-select:none;user-select:none;}' +
    '#gcvx-toolbar-root .gcvx-brand{color:#f1f5f9;font-weight:700;font-size:14px;letter-spacing:.4px;' +
    'display:flex;align-items:center;gap:8px;}' +
    '#gcvx-toolbar-root .gcvx-brand-badge{width:22px;height:22px;border-radius:6px;' +
    'background:linear-gradient(135deg,#38bdf8,#0ea5e9);color:#06202e;font-weight:800;font-size:12px;' +
    'display:flex;align-items:center;justify-content:center;}' +
    '#gcvx-toolbar-root .gcvx-btns{display:flex;gap:8px;}' +
    '#gcvx-toolbar-root button{background:#1e293b;color:#e2e8f0;border:1px solid #334155;border-radius:8px;' +
    'padding:6px 12px;font-size:12.5px;font-weight:600;cursor:pointer;display:flex;align-items:center;gap:6px;' +
    'transition:background .15s ease,transform .1s ease;}' +
    '#gcvx-toolbar-root button:hover{background:#273549;}' +
    '#gcvx-toolbar-root button:active{transform:translateY(1px);}' +
    '#gcvx-toolbar-root button:disabled{opacity:.5;cursor:default;}' +
    '#gcvx-about-overlay{position:fixed;inset:0;background:rgba(2,6,23,0.72);z-index:2147483647;' +
    'display:none;align-items:center;justify-content:center;font-family:"Segoe UI",Arial,sans-serif;}' +
    '#gcvx-about-overlay.gcvx-show{display:flex;}' +
    '#gcvx-about-card{width:340px;max-width:88vw;background:#111827;border:1px solid #334155;' +
    'border-radius:14px;padding:28px 26px;text-align:center;color:#f1f5f9;box-shadow:0 20px 60px rgba(0,0,0,.5);}' +
    '#gcvx-about-card .gcvx-badge-lg{width:46px;height:46px;border-radius:12px;margin:0 auto 14px auto;' +
    'background:linear-gradient(135deg,#38bdf8,#0ea5e9);color:#06202e;font-weight:800;font-size:20px;' +
    'display:flex;align-items:center;justify-content:center;}' +
    '#gcvx-about-card h2{margin:0 0 14px 0;font-size:17px;}' +
    '#gcvx-about-card p{margin:0 0 6px 0;font-size:13.5px;color:#cbd5e1;line-height:1.5;}' +
    '#gcvx-about-card .gcvx-site{color:#38bdf8;font-weight:600;}' +
    '#gcvx-about-card button{margin-top:18px;background:linear-gradient(135deg,#38bdf8,#0ea5e9);' +
    'color:#06202e;border:none;padding:9px 26px;border-radius:999px;font-weight:700;font-size:13px;cursor:pointer;}' +
    'html{scroll-behavior:smooth;}';
  document.head.appendChild(style);

  var bar = document.createElement('div');
  bar.id = 'gcvx-toolbar-root';
  bar.innerHTML =
    '<div class="gcvx-brand"><div class="gcvx-brand-badge">G</div><span>GCVX_IMS</span></div>' +
    '<div class="gcvx-btns">' +
    '<button id="gcvx-btn-refresh" title="Refresh">&#8635; Refresh</button>' +
    '<button id="gcvx-btn-update" title="Update">&#8593; Update</button>' +
    '<button id="gcvx-btn-about" title="About">&#9432; About</button>' +
    '</div>';
  document.documentElement.appendChild(bar);

  var overlay = document.createElement('div');
  overlay.id = 'gcvx-about-overlay';
  overlay.innerHTML =
    '<div id="gcvx-about-card">' +
    '<div class="gcvx-badge-lg">G</div>' +
    '<h2>GCVX_IMS</h2>' +
    '<p>Developed and designed by <strong>Kouzu</strong></p>' +
    '<p class="gcvx-site">kouzu.in</p>' +
    '<button id="gcvx-about-close">Close</button>' +
    '</div>';
  document.documentElement.appendChild(overlay);

  document.getElementById('gcvx-about-close').addEventListener('click', function(){
    overlay.classList.remove('gcvx-show');
  });
  overlay.addEventListener('click', function(e){
    if (e.target === overlay) { overlay.classList.remove('gcvx-show'); }
  });

  function callApi(name, btn){
    if (btn) { btn.disabled = true; }
    var restore = function(){ if (btn) { btn.disabled = false; } };
    try {
      if (window.pywebview && window.pywebview.api && window.pywebview.api[name]) {
        var p = window.pywebview.api[name]();
        if (p && p.then) { p.then(restore).catch(restore); } else { restore(); }
      } else {
        restore();
      }
    } catch (e) { restore(); }
  }

  document.getElementById('gcvx-btn-refresh').addEventListener('click', function(){
    callApi('refresh_app', this);
  });
  document.getElementById('gcvx-btn-update').addEventListener('click', function(){
    callApi('update_app', this);
  });
  document.getElementById('gcvx-btn-about').addEventListener('click', function(){
    document.getElementById('gcvx-about-overlay').classList.add('gcvx-show');
  });
})();
"""
