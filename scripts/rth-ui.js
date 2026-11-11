/* Four-language UI (ar/en/ur/id) for Umrah pages without the tool app: header dropdown + switching. */
(function(){
'use strict';
var NAMES={ar:'العربية',en:'English',ur:'اردو',id:'Indonesia'};
function UI(){ var h=document.documentElement; return h.getAttribute('data-ui')||(h.getAttribute('data-lang')==='ar'?'ar':'en'); }
function urFont(){ if(document.getElementById('ur-font')) return; var l=document.createElement('link'); l.id='ur-font'; l.rel='stylesheet'; l.href='https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;700&display=swap'; document.head.appendChild(l); }
function setUI(u){
  var h=document.documentElement;
  try{ if(u==='ur'||u==='id'){ localStorage.setItem('rth-ui',u); localStorage.setItem('dfl-lang',u==='ur'?'ar':'en'); } else { localStorage.removeItem('rth-ui'); localStorage.setItem('dfl-lang',u); } }catch(e){}
  if(u==='ur') urFont();
  if(u==='ur'||u==='id'){ h.setAttribute('data-ui',u); h.setAttribute('data-lang',u==='ur'?'ar':'en'); h.setAttribute('dir',u==='ur'?'rtl':'ltr'); }
  else { h.removeAttribute('data-ui'); h.setAttribute('data-lang',u); h.setAttribute('dir',u==='ar'?'rtl':'ltr'); }
  h.setAttribute('lang',u);
  document.dispatchEvent(new CustomEvent('dfl:langchange',{detail:{lang:h.getAttribute('data-lang'),src:'rth'}}));
  if(window.dflTrack) try{ dflTrack('ui_language',{ui:u}); }catch(e){}
}
function render(){ var u=UI();
  document.querySelectorAll('.rh-langmenu [data-ui]').forEach(function(b){ b.setAttribute('aria-checked',b.getAttribute('data-ui')===u?'true':'false'); });
  document.querySelectorAll('[data-langcur]').forEach(function(el){ el.textContent=NAMES[u]; });
}
function closeAll(except){ document.querySelectorAll('[data-langsel]').forEach(function(w){ if(w===except) return; var m=w.querySelector('.rh-langmenu'), b=w.querySelector('.rh-langsel-btn'); if(m) m.hidden=true; if(b) b.setAttribute('aria-expanded','false'); }); }
document.addEventListener('DOMContentLoaded',function(){
  if(UI()==='ur') urFont();
  document.querySelectorAll('[data-langsel]').forEach(function(w){
    var b=w.querySelector('.rh-langsel-btn'), m=w.querySelector('.rh-langmenu');
    b.addEventListener('click',function(e){ e.stopPropagation(); var open=m.hidden; closeAll(w); m.hidden=!open; b.setAttribute('aria-expanded',open?'true':'false'); if(open){ (m.querySelector('[aria-checked="true"]')||m.querySelector('button')).focus(); } });
    m.addEventListener('keydown',function(e){ var it=[].slice.call(m.querySelectorAll('button')), i=it.indexOf(document.activeElement);
      if(e.key==='ArrowDown'){ e.preventDefault(); it[(i+1)%it.length].focus(); } else if(e.key==='ArrowUp'){ e.preventDefault(); it[(i-1+it.length)%it.length].focus(); } else if(e.key==='Escape'){ closeAll(); b.focus(); } });
    m.querySelectorAll('[data-ui]').forEach(function(x){ x.addEventListener('click',function(e){ e.stopPropagation(); closeAll(); setUI(x.getAttribute('data-ui')); b.focus({preventScroll:true}); }); });
  });
  document.addEventListener('click',function(){ closeAll(); });
  render();
});
document.addEventListener('dfl:langchange',function(e){
  if(!(e.detail&&e.detail.src==='rth')&&document.documentElement.hasAttribute('data-ui')){ document.documentElement.removeAttribute('data-ui'); try{localStorage.removeItem('rth-ui');}catch(_){} }
  render();
});
})();

/* Localized links: <a data-href-en="..." data-href-ur="..." data-href-id="..."> follow the chosen UI language. */
(function(){
function ui(){ var h=document.documentElement; return h.getAttribute('data-ui')||(h.getAttribute('data-lang')==='ar'?'ar':'en'); }
function loc(){ var u=ui(); document.querySelectorAll('a[data-href-en]').forEach(function(a){ if(!a.hasAttribute('data-href-ar')) a.setAttribute('data-href-ar',a.getAttribute('href')); a.setAttribute('href',a.getAttribute('data-href-'+u)||a.getAttribute('data-href-ar')); }); }
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',loc); else loc();
document.addEventListener('dfl:langchange',function(){ setTimeout(loc,0); });
})();
