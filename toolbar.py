"""
Toolbar injected into every page the window shows (both the real app and
the local offline screen), via `window.evaluate_js(...)` after each
`loaded` event. Corporate boxy monochrome theme.
"""

HARDENING_JS = """
(function(){
  document.addEventListener('contextmenu', function(e){ e.preventDefault(); });
})();
"""

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

TOOLBAR_JS = r"""
(function(){
  if (document.getElementById('gcvx-toolbar-root')) { return; }

  var TOOLBAR_H = 44;

  var style = document.createElement('style');
  style.id = 'gcvx-toolbar-style';
  style.textContent =
    '#gcvx-toolbar-root{position:fixed;top:0;left:0;right:0;height:' + TOOLBAR_H + 'px;' +
    'background:#0a0a0a;border-bottom:1px solid #262626;' +
    'display:flex;align-items:center;justify-content:space-between;padding:0 16px;' +
    'z-index:2147483647;font-family:ui-monospace,SFMono-Regular,Consolas,"Segoe UI",sans-serif;-webkit-user-select:none;user-select:none;}' +
    '#gcvx-toolbar-root .gcvx-brand{color:#ffffff;font-weight:700;font-size:12px;letter-spacing:1px;' +
    'text-transform:uppercase;display:flex;align-items:center;gap:8px;}' +
    '#gcvx-toolbar-root .gcvx-brand-tag{background:#171717;border:1px solid #333333;padding:2px 6px;color:#a3a3a3;font-size:10px;}' +
    '#gcvx-toolbar-root .gcvx-btns{display:flex;gap:6px;}' +
    '#gcvx-toolbar-root button{background:#171717;color:#e5e5e5;border:1px solid #333333;border-radius:0px;' +
    'padding:5px 14px;font-size:11px;font-weight:600;letter-spacing:0.5px;text-transform:uppercase;cursor:pointer;display:flex;align-items:center;gap:6px;' +
    'transition:background .1s linear,border-color .1s linear;}' +
    '#gcvx-toolbar-root button:hover{background:#262626;border-color:#525252;color:#ffffff;}' +
    '#gcvx-toolbar-root button:active{background:#000000;}' +
    '#gcvx-toolbar-root button:disabled{opacity:.4;cursor:default;}' +
    '#gcvx-about-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.85);z-index:2147483647;' +
    'display:none;align-items:center;justify-content:center;font-family:ui-monospace,SFMono-Regular,Consolas,"Segoe UI",sans-serif;backdrop-filter:blur(4px);}' +
    '#gcvx-about-overlay.gcvx-show{display:flex;}' +
    '#gcvx-about-card{width:380px;max-width:92vw;background:#121212;border:1px solid #333333;' +
    'border-radius:0px;padding:0;color:#ffffff;box-shadow:0 0 0 1px #000000, 0 24px 60px rgba(0,0,0,0.95);}' +
    '#gcvx-about-card .gcvx-modal-header{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:#181818;border-bottom:1px solid #262626;font-size:11px;font-weight:700;letter-spacing:1px;color:#a3a3a3;text-transform:uppercase;}' +
    '#gcvx-about-card #gcvx-about-x{background:transparent;border:none;color:#737373;font-size:13px;cursor:pointer;padding:2px 6px;}' +
    '#gcvx-about-card #gcvx-about-x:hover{color:#ffffff;background:#262626;}' +
    '#gcvx-about-card .gcvx-modal-body{padding:22px 18px 18px 18px;text-align:center;}' +
    '#gcvx-about-card .gcvx-badge-square{width:46px;height:46px;border-radius:0px;margin:0 auto 12px auto;' +
    'background:#1c1c1c;border:1px solid #333333;color:#ffffff;font-weight:700;font-size:14px;' +
    'display:flex;align-items:center;justify-content:center;letter-spacing:1px;}' +
    '#gcvx-about-card h2{margin:0 0 16px 0;font-size:15px;letter-spacing:1.5px;text-transform:uppercase;font-weight:700;color:#ffffff;}' +
    '#gcvx-about-card .gcvx-info-table{border:1px solid #262626;background:#171717;margin-bottom:4px;text-align:left;}' +
    '#gcvx-about-card .gcvx-info-row{display:flex;justify-content:space-between;align-items:center;padding:8px 12px;border-bottom:1px solid #262626;font-size:11px;}' +
    '#gcvx-about-card .gcvx-info-row:last-child{border-bottom:none;}' +
    '#gcvx-about-card .gcvx-info-row .lbl{color:#737373;font-weight:600;letter-spacing:0.5px;}' +
    '#gcvx-about-card .gcvx-info-row .val{color:#ffffff;font-weight:600;letter-spacing:0.5px;}' +
    '#gcvx-about-card .gcvx-modal-footer{padding:12px 18px;background:#181818;border-top:1px solid #262626;}' +
    '#gcvx-about-card #gcvx-about-close{background:#ffffff;color:#000000;border:1px solid #ffffff;' +
    'padding:8px 24px;border-radius:0px;font-weight:700;font-size:11px;letter-spacing:1px;text-transform:uppercase;cursor:pointer;width:100%;}' +
    '#gcvx-about-card #gcvx-about-close:hover{background:#e5e5e5;}' +
    '@keyframes gcvx-spin{0%{transform:rotate(0deg);}100%{transform:rotate(360deg);}}' +
    '.gcvx-spinner{width:11px;height:11px;border:2px solid #ffffff;border-top-color:transparent;border-radius:50%;display:inline-block;animation:gcvx-spin .75s linear infinite;}' +
    '.gcvx-loading-bar{position:absolute;bottom:0;left:0;right:0;height:2px;background:#171717;overflow:hidden;display:none;}' +
    '.gcvx-loading-bar::after{content:"";position:absolute;top:0;left:-40%;width:40%;height:100%;background:#ffffff;animation:gcvx-bar-move 1.1s cubic-bezier(0.4,0,0.2,1) infinite;}' +
    '#gcvx-toolbar-root.gcvx-is-updating .gcvx-loading-bar{display:block;}' +
    '@keyframes gcvx-bar-move{0%{left:-40%;width:30%;}50%{width:60%;}100%{left:100%;width:30%;}}' +
    'html{scroll-behavior:smooth;} body{padding-top:' + TOOLBAR_H + 'px !important;}';
  document.head.appendChild(style);

  var bar = document.createElement('div');
  bar.id = 'gcvx-toolbar-root';
  bar.innerHTML =
    '<div class="gcvx-brand"><span>GCVX_IMS</span><span class="gcvx-brand-tag">SYS</span></div>' +
    '<div class="gcvx-btns">' +
    '<button id="gcvx-btn-refresh" title="Refresh">REFRESH</button>' +
    '<button id="gcvx-btn-update" title="Update">UPDATE</button>' +
    '<button id="gcvx-btn-about" title="About">ABOUT</button>' +
    '</div>' +
    '<div class="gcvx-loading-bar"></div>';
  document.documentElement.appendChild(bar);

  var overlay = document.createElement('div');
  overlay.id = 'gcvx-about-overlay';
  overlay.innerHTML =
    '<div id="gcvx-about-card">' +
    '<div class="gcvx-modal-header">' +
    '<span>SYSTEM INFORMATION</span>' +
    '<button id="gcvx-about-x" title="Close">✕</button>' +
    '</div>' +
    '<div class="gcvx-modal-body">' +
    '<div class="gcvx-badge-square">GCVX</div>' +
    '<h2>GCVX_IMS</h2>' +
    '<div class="gcvx-info-table">' +
    '<div class="gcvx-info-row"><span class="lbl">ENVIRONMENT</span><span class="val">PYTHON (SANDBOXED)</span></div>' +
    '<div class="gcvx-info-row"><span class="lbl">SECURITY</span><span class="val">ENCRYPTED / ISOLATED</span></div>' +
    '<div class="gcvx-info-row"><span class="lbl">DEVELOPER</span><span class="val">KOUZU</span></div>' +
    '<div class="gcvx-info-row"><span class="lbl">WEBSITE</span><span class="val">kouzu.in</span></div>' +
    '</div>' +
    '</div>' +
    '<div class="gcvx-modal-footer">' +
    '<button id="gcvx-about-close">CLOSE</button>' +
    '</div>' +
    '</div>';
  document.documentElement.appendChild(overlay);

  var hideModal = function(){ overlay.classList.remove('gcvx-show'); };
  document.getElementById('gcvx-about-close').addEventListener('click', hideModal);
  document.getElementById('gcvx-about-x').addEventListener('click', hideModal);
  overlay.addEventListener('click', function(e){
    if (e.target === overlay) { hideModal(); }
  });
  overlay.addEventListener('click', function(e){
    if (e.target === overlay) { overlay.classList.remove('gcvx-show'); }
  });

  function callApi(name, btn, loadingLabel){
    var originalHTML = btn ? btn.innerHTML : '';
    if (btn) {
      btn.disabled = true;
      btn.innerHTML = '<span class="gcvx-spinner"></span> ' + (loadingLabel || 'LOADING...');
    }
    bar.classList.add('gcvx-is-updating');
    var restore = function(){
      if (btn) {
        btn.disabled = false;
        btn.innerHTML = originalHTML;
      }
      bar.classList.remove('gcvx-is-updating');
    };
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
    callApi('refresh_app', this, 'REFRESHING...');
  });
  document.getElementById('gcvx-btn-update').addEventListener('click', function(){
    callApi('update_app', this, 'UPDATING...');
  });
  document.getElementById('gcvx-btn-about').addEventListener('click', function(){
    document.getElementById('gcvx-about-overlay').classList.add('gcvx-show');
  });
})();
"""
