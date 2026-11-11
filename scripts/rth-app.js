/* Return to Hotel v2 — app logic. Storage keys kept from v1: dfl_hotels, dfl_hotel, dfl_meet. */
(function(){
'use strict';
var $=function(id){return document.getElementById(id);};
var UI=function(){var h=document.documentElement;return h.getAttribute('data-ui')||(h.getAttribute('data-lang')==='ar'?'ar':'en');};
var isAr=function(){return UI()==='ar';};
var T=function(ar,en,ur,id){var u=UI();return u==='ar'?ar:u==='ur'?(ur||en):u==='id'?(id||en):en;};
var LOC=function(){return {ar:'ar-SA',en:'en-GB',ur:'ur-PK',id:'id-ID'}[UI()];};
var track=function(e,p){ if(window.dflTrack) try{dflTrack(e,p);}catch(_){} };
var FIELDS=['name','address','addressAr','phone','room','area','checkin','checkout','notes','mapslink','lat','lng'];
var pack={active:'makkah',makkah:null,madinah:null};
var hotel=null, deferredInstall=null, pendingGps=null, taxiKey='SA';

/* ---------- storage ---------- */
function load(){
  var raw=null; try{raw=JSON.parse(localStorage.getItem('dfl_hotels')||'null');}catch(e){}
  if(raw&&(raw.makkah||raw.madinah||raw.active)){
    pack.active=raw.active==='madinah'?'madinah':'makkah'; pack.makkah=raw.makkah||null; pack.madinah=raw.madinah||null;
  }else{
    var old=null; try{old=JSON.parse(localStorage.getItem('dfl_hotel')||'null');}catch(e){}
    if(old&&old.name){ var c=guessCity(old); pack.active=c; pack[c]=old; persist(); }
  }
  hotel=pack[pack.active]||null;
}
function persist(){
  try{
    localStorage.setItem('dfl_hotels',JSON.stringify({active:pack.active,makkah:pack.makkah,madinah:pack.madinah}));
    if(hotel) localStorage.setItem('dfl_hotel',JSON.stringify(hotel)); else localStorage.removeItem('dfl_hotel');
  }catch(e){}
}
function guessCity(h){
  var t=((h.addressAr||'')+' '+(h.address||'')+' '+(h.name||'')).toLowerCase();
  return /المدين|madinah|medina/.test(t)?'madinah':'makkah';
}

/* ---------- prefill links (?d= compact or legacy params) ---------- */
function applyPrefill(){
  var p=new URLSearchParams(location.search);
  var clean=function(){ try{history.replaceState(null,'',location.pathname);}catch(e){} };
  if(p.get('d')){
    try{
      var r=p.get('d').replace(/-/g,'+').replace(/_/g,'/'); while(r.length%4) r+='=';
      var o=JSON.parse(decodeURIComponent(escape(atob(r)))); p=new URLSearchParams();
      if(o.h)p.set('h',String(o.h)); if(o.a)p.set('a',String(o.a)); if(o.r)p.set('ar',String(o.r)); if(o.p)p.set('ph',String(o.p));
      if(o.y!=null&&o.x!=null){p.set('lat',String(o.y));p.set('lng',String(o.x));}
      p.set('c',o.c==='m'?'madinah':'makkah'); if(o.s)p.set('src',String(o.s));
    }catch(e){ clean(); return; }
  }
  var n=(p.get('h')||'').trim(); if(!n) return;
  var d={name:n.slice(0,120),address:(p.get('a')||'').trim().slice(0,200),addressAr:(p.get('ar')||'').trim().slice(0,200),phone:(p.get('ph')||'').trim().slice(0,30)};
  var lat=parseFloat(p.get('lat')),lng=parseFloat(p.get('lng'));
  if(isFinite(lat)&&isFinite(lng)&&Math.abs(lat)<=90&&Math.abs(lng)<=180){d.lat=lat.toFixed(6);d.lng=lng.toFixed(6);}
  if(!d.address) d.address=d.addressAr||d.name;
  var c=p.get('c'); c=(c==='madinah'||c==='makkah')?c:guessCity(d);
  var cur=pack[c];
  if(cur&&cur.name&&cur.name!==d.name&&!confirm(T('استبدال بطاقة «'+cur.name+'» ببطاقة «'+d.name+'»؟','Replace "'+cur.name+'" with "'+d.name+'"?','«'+cur.name+'» کی جگہ «'+d.name+'» محفوظ کریں؟','Ganti "'+cur.name+'" dengan "'+d.name+'"?'))){clean();return;}
  pack.active=c; pack[c]=d; hotel=d; persist(); clean();
  track('prefill_saved',{city:c,partner:(p.get('src')||'link').slice(0,40)});
  setTimeout(function(){toast(T('✓ تم حفظ بطاقة '+d.name,'✓ Saved: '+d.name,'✓ محفوظ: '+d.name,'✓ Tersimpan: '+d.name));},500);
}

/* ---------- geolocation ---------- */
function getPos(btn,ok){
  if(!navigator.geolocation){toast(T('المتصفح لا يدعم تحديد الموقع','Location is not supported','براؤزر مقام کی سہولت نہیں دیتا','Lokasi tidak didukung'));return;}
  if(btn) btn.disabled=true;
  navigator.geolocation.getCurrentPosition(function(p){
    if(btn) btn.disabled=false;
    ok({lat:p.coords.latitude.toFixed(6),lng:p.coords.longitude.toFixed(6),acc:Math.round(p.coords.accuracy)});
  },function(e){
    if(btn) btn.disabled=false;
    toast(e.code===1?T('اسمح بالوصول لموقعك من إعدادات المتصفح ثم أعد المحاولة','Allow location access in your browser, then try again','براؤزر کی ترتیبات میں مقام کی اجازت دیں، پھر دوبارہ کوشش کریں','Izinkan akses lokasi di browser, lalu coba lagi'):T('تعذر تحديد الموقع، حاول مرة أخرى','Could not get your location, try again','مقام معلوم نہیں ہو سکا، دوبارہ کوشش کریں','Lokasi tidak didapat, coba lagi'));
  },{enableHighAccuracy:true,timeout:20000,maximumAge:0});
}

/* ---------- views ---------- */
function show(){
  var has=!!(hotel&&hotel.name);
  $('rh-empty').hidden=has; $('rh-mycard').hidden=!has;
  if(has) renderCard();
  renderCities();
}
function renderCities(){
  document.querySelectorAll('[data-city]').forEach(function(b){
    var c=b.getAttribute('data-city'); b.classList.toggle('is-on',c===pack.active);
    b.setAttribute('aria-pressed',c===pack.active?'true':'false');
    var dot=b.querySelector('.dot'); if(dot) dot.hidden=!(pack[c]&&pack[c].name);
  });
}
function ll(h){return (h&&h.lat&&h.lng)?(h.lat+','+h.lng):'';}
function mapsWalk(h){var l=ll(h);return l?('https://www.google.com/maps/dir/?api=1&destination='+l+'&travelmode=walking'):(h.mapslink||('https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(h.name+' '+(h.address||''))));}
function mapsPin(h){var l=ll(h);return l?('https://www.google.com/maps/search/?api=1&query='+l):(h.mapslink||('https://www.google.com/maps/search/?api=1&query='+encodeURIComponent(h.name+' '+(h.address||''))));}
function renderCard(){
  var h=hotel;
  $('c-name').textContent=h.name;
  var addr=isAr()?(h.addressAr||h.address):(h.address||h.addressAr);
  $('c-addr').textContent=addr&&addr!==h.name?addr:'';
  $('c-gps-ok').hidden=!ll(h); $('c-gps-no').hidden=!!ll(h);
  var ph=$('c-phone'); if(h.phone){ph.hidden=false;ph.href='tel:'+h.phone.replace(/\s/g,'');ph.querySelector('b').textContent=h.phone;}else ph.hidden=true;
  var rm=$('c-room'); if(h.room){rm.hidden=false;rm.querySelector('b').textContent=h.room;}else rm.hidden=true;
  $('c-walk').href=mapsWalk(h);
  var l=ll(h), q=encodeURIComponent(h.name+' '+(h.address||''));
  $('c-waze').href=l?('https://waze.com/ul?ll='+l+'&navigate=yes'):('https://waze.com/ul?q='+encodeURIComponent(h.address||h.name));
  $('c-apple').href=l?('https://maps.apple.com/?daddr='+l+'&dirflg=w'):('https://maps.apple.com/?q='+q);
  $('c-uber').href='https://m.uber.com/ul/?action=setPickup&pickup=my_location'+(l?('&dropoff[latitude]='+h.lat+'&dropoff[longitude]='+h.lng):'')+'&dropoff[nickname]='+encodeURIComponent(h.name)+'&dropoff[formatted_address]='+encodeURIComponent(h.address||h.addressAr||h.name);
  renderTaxi(taxiKey);
}

/* ---------- form ---------- */
function openForm(withGps){
  var f=$('rh-form'); f.hidden=false;
  writeForm(hotel);
  $('rh-form-title').textContent=hotel?T('تعديل بطاقة الفندق','Edit hotel card','ہوٹل کارڈ میں ترمیم','Ubah kartu hotel'):T('بطاقة فندقك','Your hotel card','آپ کا ہوٹل کارڈ','Kartu hotel Anda');
  setTimeout(function(){ f.scrollIntoView({behavior:'smooth',block:'start'}); },60);
  if(withGps) captureGps(); else setTimeout(function(){ $('f-name').focus({preventScroll:true}); },400);
}
function closeForm(){ $('rh-form').hidden=true; }
function writeForm(h){
  FIELDS.forEach(function(k){ var el=$('f-'+k); if(el) el.value=(h&&h[k])||''; });
  pendingGps=(h&&h.lat)?{lat:h.lat,lng:h.lng,acc:h.acc||''}:null; renderGpsRow();
}
function renderGpsRow(){
  var row=$('f-gps'); row.classList.toggle('ok',!!pendingGps);
  $('f-gps-t').innerHTML=pendingGps
    ? T('<b>✓ موقع الفندق محفوظ بدقة</b>الملاحة ستعيدك إلى باب الفندق مباشرة.','<b>✓ Exact hotel location saved</b>Navigation will take you to the hotel door.','<b>✓ ہوٹل کا درست مقام محفوظ</b>نقشہ آپ کو سیدھا ہوٹل کے دروازے تک لے جائے گا۔','<b>✓ Lokasi tepat hotel tersimpan</b>Navigasi akan membawa Anda sampai pintu hotel.')
    : T('<b>هل أنت في الفندق الآن؟</b>احفظ موقعه بدقة لتعود إلى بابه مشياً.','<b>Are you at the hotel now?</b>Save its exact spot to walk back to the door.','<b>کیا آپ ابھی ہوٹل میں ہیں؟</b>اس کا درست مقام محفوظ کریں تاکہ پیدل دروازے تک واپس آ سکیں۔','<b>Anda di hotel sekarang?</b>Simpan lokasi tepatnya agar bisa jalan kaki kembali ke pintunya.');
  $('f-gps-b').textContent=pendingGps?T('تحديث الموقع','Update','اپ ڈیٹ','Perbarui'):T('📍 احفظ موقعي','📍 Save my spot','📍 میری جگہ محفوظ کریں','📍 Simpan posisi saya');
}
function captureGps(){
  getPos($('f-gps-b'),function(p){ pendingGps=p; renderGpsRow(); toast(T('✓ تم تحديد الموقع (دقة '+p.acc+' م)، اكتب اسم الفندق واحفظ','✓ Location captured (±'+p.acc+' m). Add the hotel name and save','✓ مقام مل گیا (±'+p.acc+' میٹر)۔ ہوٹل کا نام لکھیں اور محفوظ کریں','✓ Lokasi didapat (±'+p.acc+' m). Tulis nama hotel lalu simpan')); setTimeout(function(){$('f-name').focus();},300); track('hotel_gps_saved'); });
}
function saveForm(e){
  if(e) e.preventDefault();
  var name=$('f-name').value.trim();
  if(!name){ toast(T('اكتب اسم الفندق','Enter the hotel name','ہوٹل کا نام لکھیں','Tulis nama hotel')); $('f-name').focus(); return; }
  var d={}; FIELDS.forEach(function(k){ var el=$('f-'+k); d[k]=el?el.value.trim():''; });
  if(pendingGps){ d.lat=pendingGps.lat; d.lng=pendingGps.lng; }
  if(!d.address) d.address=d.addressAr||name;
  pack[pack.active]=d; hotel=d; persist();
  closeForm(); show(); window.scrollTo({top:0,behavior:'smooth'});
  toast(T('✓ حُفظت بطاقة فندقك. جرّب «ارجع مشياً»','✓ Hotel card saved. Try "Walk back"','✓ ہوٹل کارڈ محفوظ ہو گیا۔ «پیدل واپس جائیں» آزمائیں','✓ Kartu hotel tersimpan. Coba "Jalan kembali"'));
  track('hotel_saved',{city:pack.active,has_gps:d.lat?'yes':'no'});
}
function switchCity(c){
  if(c!==pack.active){ pack.active=c; hotel=pack[c]||null; persist(); show(); if(!$('rh-form').hidden) writeForm(hotel); }
}
function clearCard(){
  if(!hotel) return;
  if(!confirm(T('مسح بطاقة '+hotel.name+'؟','Clear the '+hotel.name+' card?',hotel.name+' کا کارڈ مٹائیں؟','Hapus kartu '+hotel.name+'?'))) return;
  pack[pack.active]=null; hotel=null; persist(); show();
}

/* ---------- actions ---------- */
function shareText(){
  var h=hotel;
  return T('🏨 فندقي: '+h.name+(h.addressAr?('\n'+h.addressAr):'')+(h.address&&h.address!==h.name&&h.address!==h.addressAr?('\n'+h.address):'')+(h.phone?('\n☎ '+h.phone):'')+'\n📍 '+mapsPin(h)+'\n\nاحفظ بطاقة فندقك مجاناً: https://dotforlife.com/hotel',
           '🏨 My hotel: '+h.name+(h.address&&h.address!==h.name&&h.address!==h.addressAr?('\n'+h.address):'')+(h.addressAr?('\n'+h.addressAr):'')+(h.phone?('\n☎ '+h.phone):'')+'\n📍 '+mapsPin(h)+'\n\nSave your hotel card free: https://dotforlife.com/hotel',
           '🏨 میرا ہوٹل: '+h.name+(h.addressAr?('\n'+h.addressAr):'')+(h.phone?('\n☎ '+h.phone):'')+'\n📍 '+mapsPin(h)+'\n\nاپنا ہوٹل کارڈ مفت محفوظ کریں: https://dotforlife.com/hotel',
           '🏨 Hotel saya: '+h.name+(h.address&&h.address!==h.name&&h.address!==h.addressAr?('\n'+h.address):'')+(h.addressAr?('\n'+h.addressAr):'')+(h.phone?('\n☎ '+h.phone):'')+'\n📍 '+mapsPin(h)+'\n\nSimpan kartu hotel Anda gratis: https://dotforlife.com/hotel');
}
function shareFamily(){ window.open('https://wa.me/?text='+encodeURIComponent(shareText()),'_blank'); track('whatsapp_share'); }
function copyAddr(){
  var t=shareText();
  if(navigator.clipboard&&navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(function(){toast(T('✓ تم النسخ','✓ Copied','✓ کاپی ہو گیا','✓ Tersalin'));},function(){prompt('',t);});
  else prompt('',t);
  track('copy_address');
}
function openDriver(){
  var h=hotel; if(!h) return;
  $('d-k').textContent='من فضلك، أوصلني إلى هذا الفندق';
  $('d-k2').textContent='Please take me to this hotel · '+(pack.active==='madinah'?'Madinah':'Makkah');
  $('d-n').textContent=h.name;
  $('d-ar').textContent=h.addressAr||''; $('d-ar').hidden=!h.addressAr;
  $('d-en').textContent=(h.address&&h.address!==h.name&&h.address!==h.addressAr)?h.address:''; $('d-en').hidden=!$('d-en').textContent;
  var p=$('d-p'); if(h.phone){p.hidden=false;p.textContent=h.phone;p.href='tel:'+h.phone.replace(/\s/g,'');}else p.hidden=true;
  var ov=$('rh-driver'); if(ov.parentNode!==document.body) document.body.appendChild(ov);
  ov.classList.add('is-open'); document.body.style.overflow='hidden'; ov.scrollTop=0;
  track('driver_card_open');
}
function closeDriver(){ $('rh-driver').classList.remove('is-open'); document.body.style.overflow=''; }

/* hotel image card */
function wrap(x,text,cx,y,maxW,lh,align){
  var s=String(text||''), rtl=/[֐-ࣿ]/.test(s); x.save(); x.direction=rtl?'rtl':'ltr'; x.textAlign=align||'center';
  var words=s.split(/\s+/), line='';
  for(var i=0;i<words.length;i++){ var t=line?line+' '+words[i]:words[i]; if(x.measureText(t).width>maxW&&line){x.fillText(line,cx,y);y+=lh;line=words[i];} else line=t; }
  if(line){x.fillText(line,cx,y);y+=lh;} x.restore(); return y;
}
function drawCard(){
  var h=hotel, W=1080, H=1350, c=document.createElement('canvas'); c.width=W; c.height=H; var x=c.getContext('2d');
  var g=x.createLinearGradient(0,0,W,H); g.addColorStop(0,'#043a39'); g.addColorStop(1,'#0a5b57'); x.fillStyle=g; x.fillRect(0,0,W,H);
  x.fillStyle='#e3c35a'; x.font='800 34px sans-serif'; x.textAlign='center'; x.fillText(pack.active==='madinah'?'MADINAH · المدينة':'MAKKAH · مكة',W/2,110);
  x.fillStyle='#fff'; x.font='800 46px sans-serif'; wrap(x,'من فضلك، أوصلني إلى هذا الفندق',W/2,190,940,56);
  x.fillStyle='#cfe7e4'; x.font='700 32px sans-serif'; x.fillText('Please take me to this hotel',W/2,250);
  x.fillStyle='#fff'; x.beginPath(); x.roundRect?x.roundRect(70,300,W-140,700,40):x.rect(70,300,W-140,700); x.fill();
  x.fillStyle='#054241'; x.font='900 76px sans-serif'; var y=wrap(x,h.name,W/2,420,860,88);
  x.fillStyle='#1f2937'; x.font='800 44px sans-serif'; if(h.addressAr) y=wrap(x,h.addressAr,W/2,y+30,860,56);
  x.fillStyle='#4b5563'; x.font='700 36px sans-serif'; if(h.address&&h.address!==h.name&&h.address!==h.addressAr) y=wrap(x,h.address,W/2,y+20,860,46);
  if(h.phone){ x.fillStyle='#054241'; x.font='900 56px sans-serif'; x.direction='ltr'; x.fillText(h.phone,W/2,Math.min(y+70,960)); }
  if(ll(h)){ x.fillStyle='#e3c35a'; x.font='700 30px sans-serif'; x.fillText('📍 '+h.lat+', '+h.lng,W/2,1090); }
  x.fillStyle='#9ad3cd'; x.font='700 30px sans-serif'; x.fillText('dotforlife.com/hotel',W/2,H-70);
  return c;
}
function saveImage(){
  var c=drawCard(); c.toBlob(function(b){
    var f=new File([b],'hotel-card.png',{type:'image/png'});
    if(navigator.canShare&&navigator.canShare({files:[f]})){ navigator.share({files:[f],title:hotel.name}).catch(function(){}); }
    else { var a=document.createElement('a'); a.download='hotel-card.png'; a.href=c.toDataURL('image/png'); a.click(); }
  },'image/png');
  track('driver_card_save');
}
function install(){
  track('install_click');
  if(deferredInstall){ deferredInstall.prompt(); deferredInstall.userChoice.then(function(){deferredInstall=null;}); return; }
  toast(T('من قائمة المتصفح أو زر المشاركة اختر «إضافة إلى الشاشة الرئيسية»','From the browser menu or Share, choose "Add to Home Screen"','براؤزر مینو یا شیئر سے «ہوم اسکرین پر شامل کریں» چنیں','Dari menu browser atau Bagikan, pilih "Tambahkan ke Layar Utama"'));
}

/* ---------- taxi phrases ---------- */
var LANGS={
 SA:{l:'العربية',p:'من فضلك، أوصلني إلى هذا الفندق.',e:[['Help!','النجدة!','an-NAJ-dah'],["I'm lost",'أنا تائه','ana TAA-ih'],['Call police','اتصل بالشرطة','ittasil bish-SHUR-ta'],['How much?','بكم؟','bi-KAM?'],['Stop here','قف هنا','qif HU-na'],['Thank you','شكراً','SHUK-ran']]},
 UR:{l:'اردو',p:'براہ کرم مجھے اس ہوٹل لے چلیں۔',e:[['Help!','مدد!','MA-dad!'],["I'm lost",'میں راستہ بھول گیا ہوں','main RAAS-ta bhool ga-ya hoon'],['Call police','پولیس کو بلائیں','police ko bu-LAA-ein'],['How much?','کتنے پیسے؟','KIT-ne PAI-se?'],['Stop here','یہاں روکیں','ya-HAAN RO-kein'],['Thank you','شکریہ','SHUK-ri-ya']]},
 BN:{l:'বাংলা',p:'অনুগ্রহ করে আমাকে এই হোটেলে নিয়ে চলুন।',e:[['Help!','সাহায্য করুন!','sha-HAJ-jo KO-run!'],["I'm lost",'আমি পথ হারিয়ে ফেলেছি','A-mi poth HA-ri-ye fe-le-chi'],['Call police','পুলিশ ডাকুন','PU-lish DA-kun'],['How much?','কত?','KO-to?'],['Stop here','এখানে থামুন','E-kha-ne THA-mun'],['Thank you','ধন্যবাদ','DHON-no-bad']]},
 ID:{l:'Indonesia',p:'Tolong antar saya ke hotel ini.',e:[['Help!','Tolong!','Toh-LONG!'],["I'm lost",'Saya tersesat','SA-ya ter-seh-SAT'],['Call police','Panggil polisi','PANG-gil po-LEE-see'],['How much?','Berapa?','Beh-RAH-pah?'],['Stop here','Berhenti di sini','Ber-HEN-tee dee SEE-nee'],['Thank you','Terima kasih','TEH-ree-mah KAH-sih']]},
 TR:{l:'Türkçe',p:'Lütfen beni bu otele götürün.',e:[['Help!','İmdat!','Im-DAT!'],["I'm lost",'Kayboldum','KAY-bol-doom'],['Call police','Polis çağırın','Poh-LEES cha-EE-run'],['How much?','Ne kadar?','Neh KAH-dar?'],['Stop here','Burada durun','Boo-RAH-dah DOO-roon'],['Thank you','Teşekkürler','Tesh-ek-EUR-ler']]},
 FR:{l:'Français',p:"Veuillez m'emmener à cet hôtel, s'il vous plaît.",e:[['Help!',"À l'aide !",'Ah LED!'],["I'm lost",'Je suis perdu','Zhuh swee pair-DUE'],['Call police','Appelez la police','Ah-pleh la poh-LEES'],['How much?','Combien ?','Kom-BYAN?'],['Stop here','Arrêtez ici','Ah-reh-TAY ee-SEE'],['Thank you','Merci','Mehr-SEE']]}
};
function renderTaxi(k){
  taxiKey=LANGS[k]?k:'SA'; var L=LANGS[taxiKey];
  document.querySelectorAll('[data-taxi]').forEach(function(b){ b.classList.toggle('is-on',b.getAttribute('data-taxi')===taxiKey); });
  $('t-ph').textContent=L.p; $('t-ph').dir=(taxiKey==='SA'||taxiKey==='UR')?'rtl':'ltr';
  $('t-nm').textContent=hotel?hotel.name:T('احفظ فندقك أولاً ليظهر هنا','Save your hotel first to show it here','یہاں دکھانے کے لیے پہلے اپنا ہوٹل محفوظ کریں','Simpan hotel Anda dulu agar tampil di sini');
  $('t-ad').textContent=hotel?(hotel.addressAr||hotel.address||''):'';
  var g=$('t-phr'); g.innerHTML='';
  L.e.forEach(function(r){ var d=document.createElement('div'); var b=document.createElement('b'); b.textContent=r[1]; var s=document.createElement('span'); s.textContent=r[0]; var i=document.createElement('i'); i.textContent=' · '+r[2]; d.appendChild(b); d.appendChild(s); d.appendChild(i); g.appendChild(d); });
}

/* ---------- meeting point ---------- */
function getMeet(){ try{return JSON.parse(localStorage.getItem('dfl_meet')||'null');}catch(e){return null;} }
function renderMeet(){
  var m=getMeet(); $('m-empty').hidden=!!m; $('m-saved').hidden=!m; if(!m) return;
  $('m-label').textContent=m.gate||T('نقطة لقائنا','Our meeting point','ہمارے ملنے کی جگہ','Titik kumpul kami');
  var hh=new Date(m.t).toLocaleTimeString(LOC(),{hour:'2-digit',minute:'2-digit'});
  $('m-time').textContent=T('حُفظت الساعة '+hh+(m.acc?' · دقة '+m.acc+' م':''),'Saved at '+hh+(m.acc?' · ±'+m.acc+' m':''),hh+' بجے محفوظ'+(m.acc?' · ±'+m.acc+' میٹر':''),'Disimpan pukul '+hh+(m.acc?' · ±'+m.acc+' m':''));
  $('m-go').href='https://www.google.com/maps/dir/?api=1&destination='+m.lat+','+m.lng+'&travelmode=walking';
}
function saveMeet(){
  getPos($('m-save'),function(p){
    var m={lat:p.lat,lng:p.lng,acc:p.acc,gate:$('m-gate').value.trim().slice(0,60),t:Date.now()};
    try{localStorage.setItem('dfl_meet',JSON.stringify(m));}catch(e){}
    renderMeet(); toast(T('✓ حُفظت نقطة اللقاء، أرسلها لعائلتك الآن','✓ Meeting point saved. Send it to your family','✓ ملنے کی جگہ محفوظ۔ اب گھر والوں کو بھیجیں','✓ Titik kumpul tersimpan. Kirim ke keluarga Anda'));
    track('meet_saved',{has_gate:m.gate?'yes':'no'});
  });
}
function shareMeet(){
  var m=getMeet(); if(!m) return;
  var hh=new Date(m.t).toLocaleTimeString(LOC(),{hour:'2-digit',minute:'2-digit'});
  var url='https://www.google.com/maps/search/?api=1&query='+m.lat+','+m.lng;
  var msg=T('📍 نقطة لقائنا'+(m.gate?': '+m.gate:'')+'\nإذا تفرقنا، تعالوا هنا (حُفظت الساعة '+hh+'):\n'+url+'\n\nاحفظ فندقك ونقطة لقائك مجاناً: https://dotforlife.com/hotel',
            '📍 Our meeting point'+(m.gate?': '+m.gate:'')+'\nIf we get separated, come here (saved '+hh+'):\n'+url+'\n\nSave your hotel and meeting point free: https://dotforlife.com/hotel',
            '📍 ہمارے ملنے کی جگہ'+(m.gate?': '+m.gate:'')+'\nاگر ہم بچھڑ جائیں تو یہاں آ جائیں ('+hh+' بجے محفوظ):\n'+url+'\n\nاپنا ہوٹل اور ملنے کی جگہ مفت محفوظ کریں: https://dotforlife.com/hotel',
            '📍 Titik kumpul kami'+(m.gate?': '+m.gate:'')+'\nJika terpisah, datang ke sini (disimpan '+hh+'):\n'+url+'\n\nSimpan hotel dan titik kumpul Anda gratis: https://dotforlife.com/hotel');
  window.open('https://wa.me/?text='+encodeURIComponent(msg),'_blank'); track('meet_shared');
}
function clearMeet(){ try{localStorage.removeItem('dfl_meet');}catch(e){} $('m-gate').value=''; renderMeet(); }

/* ---------- child card ---------- */
function kidCard(){
  var nm=$('k-name').value.trim(), p1=$('k-p1').value.trim(), p2=$('k-p2').value.trim();
  if(!p1){ toast(T('اكتب رقم جوال الأب أو الأم','Enter a parent phone number','والدین کا فون نمبر لکھیں','Tulis nomor telepon orang tua')); $('k-p1').focus(); return; }
  var cv=$('k-canvas'), x=cv.getContext('2d'), W=1080, H=1350;
  x.fillStyle='#fff'; x.fillRect(0,0,W,H); x.fillStyle='#C9A227'; x.fillRect(0,0,W,22); x.fillRect(0,H-22,W,22);
  x.textAlign='center';
  x.direction='rtl'; x.fillStyle='#b42318'; x.font='900 66px sans-serif'; x.fillText('إذا وجدتني ضائعاً، اتصل بأهلي',W/2,140);
  x.direction='ltr'; x.font='800 44px sans-serif'; x.fillText('If I am lost, please call my family',W/2,205);
  x.direction='rtl'; x.fillStyle='#4b5563'; x.font='700 34px sans-serif'; x.fillText('میں گم ہو گیا ہوں، میرے گھر والوں کو فون کریں',W/2,264);
  if(nm){ x.fillStyle='#054241'; x.font='900 88px sans-serif'; x.fillText(nm.slice(0,30),W/2,400); }
  var y=nm?540:440, bh=p2?300:170;
  x.fillStyle='#054241'; x.beginPath(); x.roundRect?x.roundRect(80,y-90,W-160,bh,28):x.rect(80,y-90,W-160,bh); x.fill();
  x.direction='ltr'; x.fillStyle='#fff'; x.font='900 92px sans-serif'; x.fillText(p1,W/2,y+20);
  if(p2){ x.font='800 70px sans-serif'; x.fillStyle='#ffd54f'; x.fillText(p2,W/2,y+150); }
  y+=bh;
  var h=hotel||pack.makkah||pack.madinah;
  if(h&&h.name){
    y+=60; x.direction='rtl'; x.fillStyle='#6b7280'; x.font='700 34px sans-serif'; x.fillText('فندقنا · Our hotel',W/2,y);
    y+=70; x.fillStyle='#111827'; x.font='900 56px sans-serif'; x.fillText(String(h.name).slice(0,34),W/2,y);
    var ad=h.addressAr||h.address||''; if(ad&&ad!==h.name){ y+=60; x.font='700 34px sans-serif'; x.fillStyle='#374151'; x.direction=/[؀-ۿ]/.test(ad)?'rtl':'ltr'; x.fillText(String(ad).slice(0,55),W/2,y); }
    if(h.phone){ y+=60; x.direction='ltr'; x.font='800 40px sans-serif'; x.fillStyle='#054241'; x.fillText(h.phone,W/2,y); }
  }
  x.direction='rtl'; x.fillStyle='#6b7280'; x.font='700 30px sans-serif'; x.fillText('أو سلّمني لأقرب رجل أمن · Or take me to the nearest security officer',W/2,H-90);
  x.direction='ltr'; x.fillStyle='#9ca3af'; x.font='600 24px sans-serif'; x.fillText('dotforlife.com/hotel',W/2,H-45);
  $('k-out').hidden=false; track('kid_card_created');
}
function kidDownload(){ var a=document.createElement('a'); a.download='child-card.png'; a.href=$('k-canvas').toDataURL('image/png'); a.click(); track('kid_card_download'); }
function kidPrint(){
  var u=$('k-canvas').toDataURL('image/png'), w=window.open('','_blank'); if(!w){kidDownload();return;}
  w.document.write('<html><head><title>Child card</title><style>@page{margin:10mm}body{margin:0;display:flex;flex-wrap:wrap;gap:6mm}img{width:62mm;height:auto;border:1px dashed #999}</style></head><body>'+'<img src="'+u+'">'.repeat(6)+'<script>onload=function(){print()}<\/script></body></html>');
  w.document.close(); track('kid_card_print');
}

/* ---------- tabs ---------- */
function tab(id){
  document.querySelectorAll('.rh-tab').forEach(function(t){ var on=t.getAttribute('aria-controls')===id; t.setAttribute('aria-selected',on?'true':'false'); t.tabIndex=on?0:-1; });
  document.querySelectorAll('.rh-pane').forEach(function(p){ p.hidden=p.id!==id; });
}

/* ---------- misc ---------- */
var tt=null;
function toast(m){ var t=$('rh-toast'); t.textContent=m; t.classList.add('show'); clearTimeout(tt); tt=setTimeout(function(){t.classList.remove('show');},2800); }
function placeholders(){ var u=UI(); document.querySelectorAll('[data-ph-ar]').forEach(function(el){ el.placeholder=el.getAttribute('data-ph-'+u)||el.getAttribute(u==='ur'?'data-ph-ar':'data-ph-en'); }); }
function setUI(u){
  var h=document.documentElement;
  try{ if(u==='ur'||u==='id'){ localStorage.setItem('rth-ui',u); localStorage.setItem('dfl-lang',u==='ur'?'ar':'en'); } else { localStorage.removeItem('rth-ui'); localStorage.setItem('dfl-lang',u); } }catch(e){}
  if(u==='ur'&&!document.getElementById('ur-font')){ var l=document.createElement('link'); l.id='ur-font'; l.rel='stylesheet'; l.href='https://fonts.googleapis.com/css2?family=Noto+Naskh+Arabic:wght@400;700&display=swap'; document.head.appendChild(l); }
  if(u==='ur'||u==='id'){ h.setAttribute('data-ui',u); h.setAttribute('data-lang',u==='ur'?'ar':'en'); h.setAttribute('dir',u==='ur'?'rtl':'ltr'); }
  else { h.removeAttribute('data-ui'); h.setAttribute('data-lang',u); h.setAttribute('dir',u==='ar'?'rtl':'ltr'); }
  h.setAttribute('lang',u);
  document.dispatchEvent(new CustomEvent('dfl:langchange',{detail:{lang:h.getAttribute('data-lang'),src:'rth'}}));
  track('ui_language',{ui:u});
}
var UINAMES={ar:'العربية',en:'English',ur:'اردو',id:'Indonesia'};
function renderUIButtons(){ var u=UI();
  document.querySelectorAll('.rh-langmenu [data-ui]').forEach(function(b){ b.setAttribute('aria-checked',b.getAttribute('data-ui')===u?'true':'false'); });
  document.querySelectorAll('[data-langcur]').forEach(function(el){ el.textContent=UINAMES[u]; });
}
function closeLangMenus(except){ document.querySelectorAll('[data-langsel]').forEach(function(w){ if(w===except) return; var m=w.querySelector('.rh-langmenu'), b=w.querySelector('.rh-langsel-btn'); if(m) m.hidden=true; if(b) b.setAttribute('aria-expanded','false'); }); }
function initLangMenus(){
  document.querySelectorAll('[data-langsel]').forEach(function(w){
    var b=w.querySelector('.rh-langsel-btn'), m=w.querySelector('.rh-langmenu');
    b.addEventListener('click',function(e){ e.stopPropagation(); var open=m.hidden; closeLangMenus(w); m.hidden=!open; b.setAttribute('aria-expanded',open?'true':'false'); if(open){ var c=m.querySelector('[aria-checked="true"]')||m.querySelector('button'); c.focus(); } });
    m.addEventListener('keydown',function(e){ var items=[].slice.call(m.querySelectorAll('button')), i=items.indexOf(document.activeElement);
      if(e.key==='ArrowDown'){ e.preventDefault(); items[(i+1)%items.length].focus(); }
      else if(e.key==='ArrowUp'){ e.preventDefault(); items[(i-1+items.length)%items.length].focus(); }
      else if(e.key==='Escape'){ closeLangMenus(); b.focus(); } });
    m.querySelectorAll('[data-ui]').forEach(function(it){ it.addEventListener('click',function(e){ e.stopPropagation(); closeLangMenus(); setUI(it.getAttribute('data-ui')); b.focus({preventScroll:true}); }); });
  });
  document.addEventListener('click',function(){ closeLangMenus(); });
}
function relang(){ renderUIButtons(); placeholders(); if(hotel) renderCard(); else renderTaxi(taxiKey); renderMeet(); if(!$('rh-form').hidden) renderGpsRow(); }

/* ---------- wire up ---------- */
function on(id,ev,fn){ var el=$(id); if(el) el.addEventListener(ev,fn); }
document.addEventListener('DOMContentLoaded',function(){
  load(); applyPrefill(); placeholders(); renderUIButtons(); show(); renderTaxi(UI()==='ur'?'UR':UI()==='id'?'ID':'SA'); renderMeet();
  initLangMenus();
  on('b-here','click',function(){ openForm(true); });
  on('b-manual','click',function(){ openForm(false); });
  on('rh-form-x','click',closeForm);
  on('rh-form','submit',saveForm);
  on('f-gps-b','click',captureGps);
  on('c-edit','click',function(){ openForm(false); });
  on('c-gps-no','click',function(){ openForm(true); });
  on('c-clear','click',clearCard);
  on('c-driver','click',openDriver);
  on('c-family','click',shareFamily);
  on('c-copy','click',copyAddr);
  on('c-image','click',saveImage);
  on('c-install','click',install);
  on('c-walk','click',function(){ track('nav_open',{app:'walk'}); });
  ['c-waze','c-apple','c-uber'].forEach(function(id){ on(id,'click',function(){ track('nav_open',{app:id.slice(2)}); }); });
  on('d-close','click',closeDriver);
  on('d-call','click',function(){ if(hotel&&hotel.phone) location.href='tel:'+hotel.phone.replace(/\s/g,''); });
  on('d-img','click',saveImage);
  on('m-save','click',saveMeet); on('m-share','click',shareMeet); on('m-clear','click',clearMeet);
  on('m-go','click',function(){ track('meet_nav'); });
  on('k-make','click',kidCard); on('k-dl','click',kidDownload); on('k-print','click',kidPrint);
  document.querySelectorAll('[data-city]').forEach(function(b){ b.addEventListener('click',function(){ switchCity(b.getAttribute('data-city')); }); });
  document.querySelectorAll('[data-taxi]').forEach(function(b){ b.addEventListener('click',function(){ renderTaxi(b.getAttribute('data-taxi')); }); });
  var tabs=[].slice.call(document.querySelectorAll('.rh-tab'));
  tabs.forEach(function(t,i){
    t.addEventListener('click',function(){ tab(t.getAttribute('aria-controls')); });
    t.addEventListener('keydown',function(e){ var d=e.key==='ArrowLeft'?1:e.key==='ArrowRight'?-1:0; if(document.documentElement.dir==='ltr') d=-d; if(d){ var n=tabs[(i+d+tabs.length)%tabs.length]; n.focus(); n.click(); } });
  });
  if(location.hash&&/^#(meet|kid|sos|taxi)$/.test(location.hash)){ tab('p-'+location.hash.slice(1)); }
  document.addEventListener('keydown',function(e){ if(e.key==='Escape') closeDriver(); });
  document.addEventListener('dfl:langchange',function(e){
    if(!(e.detail&&e.detail.src==='rth')&&document.documentElement.hasAttribute('data-ui')){ document.documentElement.removeAttribute('data-ui'); try{localStorage.removeItem('rth-ui');}catch(_){} }
    relang();
  });
});
window.addEventListener('beforeinstallprompt',function(e){ e.preventDefault(); deferredInstall=e; });
if('serviceWorker' in navigator){ navigator.serviceWorker.register('/sw.js').then(function(){ var n=$('rh-offline'); if(n) n.hidden=false; }).catch(function(){}); }
})();

/* Localized links: <a data-href-en="..." data-href-ur="..." data-href-id="..."> follow the chosen UI language. */
(function(){
function ui(){ var h=document.documentElement; return h.getAttribute('data-ui')||(h.getAttribute('data-lang')==='ar'?'ar':'en'); }
function loc(){ var u=ui(); document.querySelectorAll('a[data-href-en]').forEach(function(a){ if(!a.hasAttribute('data-href-ar')) a.setAttribute('data-href-ar',a.getAttribute('href')); a.setAttribute('href',a.getAttribute('data-href-'+u)||a.getAttribute('data-href-ar')); }); }
if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',loc); else loc();
document.addEventListener('dfl:langchange',function(){ setTimeout(loc,0); });
})();
