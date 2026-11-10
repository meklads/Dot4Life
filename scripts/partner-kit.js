/* Partner kit: hotels & Umrah companies create a prefill link + QR poster. */
(function(){
'use strict';
function isAr(){return document.documentElement.getAttribute('data-lang')==='ar';}
function showToast(m){var t=document.getElementById('rh-toast');if(!t){alert(m);return;}t.textContent=m;t.classList.add('show');clearTimeout(window.__pt);window.__pt=setTimeout(function(){t.classList.remove('show');},2800);}
function partnerGps(){
  if(!navigator.geolocation){showToast(isAr()?'المتصفح لا يدعم تحديد الموقع':'Location not supported');return;}
  var b=document.getElementById('pt-gps'); b.disabled=true;
  navigator.geolocation.getCurrentPosition(function(pos){
    b.disabled=false;
    document.getElementById('pt-lat').value=pos.coords.latitude.toFixed(6);
    document.getElementById('pt-lng').value=pos.coords.longitude.toFixed(6);
    document.getElementById('pt-gps-ok').hidden=false;
  },function(){b.disabled=false;showToast(isAr()?'تعذر تحديد الموقع':'Could not get location');},{enableHighAccuracy:true,timeout:20000,maximumAge:0});
}
function partnerLink(){
  var v=function(id){return document.getElementById(id).value.trim();};
  if(!v('pt-name')) return null;
  var o={h:v('pt-name'),c:document.getElementById('pt-city').value==='madinah'?'m':'k'};
  if(v('pt-address')) o.a=v('pt-address');
  if(v('pt-addressAr')) o.r=v('pt-addressAr');
  if(v('pt-phone')) o.p=v('pt-phone');
  if(v('pt-lat')&&v('pt-lng')){o.y=+(+v('pt-lat')).toFixed(5);o.x=+(+v('pt-lng')).toFixed(5);}
  if(v('pt-src')) o.s=v('pt-src');
  var b=btoa(unescape(encodeURIComponent(JSON.stringify(o)))).replace(/\+/g,'-').replace(/\//g,'_').replace(/=+$/,'');
  return 'https://dotforlife.com/h?d='+b;
}
function loadQrLib(cb){
  if(window.qrcode) return cb();
  var s=document.createElement('script'); s.src='/scripts/vendor/qrcode-generator-1.4.4.js'; s.onload=cb;
  s.onerror=function(){showToast(isAr()?'تعذر تحميل مولد QR، تأكد من الاتصال':'Could not load QR generator');}; document.head.appendChild(s);
}
function buildPartnerKit(){
  var url=partnerLink();
  if(!url){showToast(isAr()?'اكتب اسم الفندق أولاً':'Enter the hotel name first');return;}
  loadQrLib(function(){
    var qr=qrcode(0,'H'); qr.addData(url,'Byte'); qr.make();
    var cv=document.getElementById('pt-poster'),x=cv.getContext('2d'),W=1080,Hh=1350;
    x.fillStyle='#054241';x.fillRect(0,0,W,Hh);
    x.textAlign='center';x.direction='rtl';x.fillStyle='#ffd54f';x.font='900 64px sans-serif';
    x.fillText('لا تضيع طريق العودة',W/2,120);
    x.fillStyle='#fff';x.font='700 34px sans-serif';
    x.fillText('امسح الرمز لحفظ بطاقة فندقك على جوالك',W/2,180);
    x.direction='ltr';x.font='700 30px sans-serif';x.fillStyle='#bfe3df';
    x.fillText('Scan to save your hotel card · Return to Hotel',W/2,228);
    var n=qr.getModuleCount(),size=700,cell=Math.floor(size/n),q=cell*n,ox=(W-q)/2,oy=290,pad=28;
    x.fillStyle='#fff';x.fillRect(ox-pad,oy-pad,q+pad*2,q+pad*2);
    x.fillStyle='#054241';
    for(var r=0;r<n;r++)for(var cc=0;cc<n;cc++)if(qr.isDark(r,cc))x.fillRect(ox+cc*cell,oy+r*cell,cell,cell);
    drawQrCenterLabel(x,ox,oy,q);
    var ny=oy+q+pad+90; x.direction='rtl';x.fillStyle='#fff';x.font='900 52px sans-serif';
    x.fillText(document.getElementById('pt-name').value.trim().slice(0,40),W/2,ny);
    x.direction='ltr';x.font='600 28px sans-serif';x.fillStyle='#6abfb8';
    x.fillText('dotforlife.com/hotel  ·  مجاني · Free · بدون تسجيل',W/2,Hh-60);
    document.getElementById('pt-link').value=url;
    document.getElementById('pt-out').hidden=false;
    if(window.dflTrack) dflTrack('partner_kit_created',{city:document.getElementById('pt-city').value});
  });
}
function qrCenterText(){
  var mode=document.getElementById('pt-center').value, hn=document.getElementById('pt-name').value.trim(), co=document.getElementById('pt-src').value.trim();
  if(mode==='none') return '';
  if(mode==='hotel') return hn;
  if(mode==='company') return co||hn;
  return co||hn;
}
function drawQrCenterLabel(x,ox,oy,q){
  var t=qrCenterText(); if(!t) return;
  var bw=Math.round(q*0.36), bh=Math.round(q*0.19), bx=ox+(q-bw)/2, by=oy+(q-bh)/2, rad=18;
  x.save();
  x.fillStyle='#fff'; x.beginPath();
  x.moveTo(bx+rad,by); x.arcTo(bx+bw,by,bx+bw,by+bh,rad); x.arcTo(bx+bw,by+bh,bx,by+bh,rad); x.arcTo(bx,by+bh,bx,by,rad); x.arcTo(bx,by,bx+bw,by,rad); x.closePath(); x.fill();
  x.lineWidth=6; x.strokeStyle='#C9A227'; x.stroke();
  var rtl=/[\u0590-\u08FF]/.test(t); x.direction=rtl?'rtl':'ltr'; x.textAlign='center'; x.textBaseline='middle'; x.fillStyle='#054241';
  var maxW=bw-28, words=t.split(/\s+/), fs=40, lines;
  for(;fs>=18;fs-=2){
    x.font='900 '+fs+'px sans-serif'; lines=[]; var line='';
    for(var i=0;i<words.length;i++){ var tst=line?line+' '+words[i]:words[i]; if(x.measureText(tst).width>maxW&&line){lines.push(line);line=words[i];} else line=tst; }
    if(line) lines.push(line);
    var fits=lines.length*fs*1.2<=bh-16 && lines.every(function(l){return x.measureText(l).width<=maxW;});
    if(fits) break;
  }
  if(lines.length>3) lines=lines.slice(0,3);
  var lh=fs*1.2, sy=by+bh/2-(lines.length-1)*lh/2;
  for(var j=0;j<lines.length;j++) x.fillText(lines[j],bx+bw/2,sy+j*lh);
  x.restore();
}
function partnerDownload(){
  var a=document.createElement('a'); a.download='hotel-qr-'+(document.getElementById('pt-name').value.trim().replace(/[^\w؀-ۿ-]+/g,'-')||'dotforlife')+'.png';
  a.href=document.getElementById('pt-poster').toDataURL('image/png'); a.click();
  if(window.dflTrack) dflTrack('partner_kit_download');
}
function partnerCopy(){
  var t=document.getElementById('pt-link').value;
  if(navigator.clipboard&&navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(function(){showToast(isAr()?'✓ تم النسخ':'✓ Copied');});
  else { document.getElementById('pt-link').select(); document.execCommand('copy'); }
}
function partnerWhatsApp(){
  var name=document.getElementById('pt-name').value.trim();
  var msg=(isAr()?('احفظ بطاقة فندق '+name+' على جوالك بضغطة، وارجع لباب الفندق بسهولة أو أظهرها للسائق:\n'):('Save the '+name+' hotel card on your phone in one tap:\n'))+document.getElementById('pt-link').value;
  window.open('https://wa.me/?text='+encodeURIComponent(msg),'_blank');
  if(window.dflTrack) dflTrack('partner_kit_whatsapp');
}
window.partnerGps=partnerGps;window.buildPartnerKit=buildPartnerKit;window.partnerDownload=partnerDownload;window.partnerCopy=partnerCopy;window.partnerWhatsApp=partnerWhatsApp;
})();
