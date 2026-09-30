const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('.nav');
function closeMenu(){navigation?.classList.remove('open');menuButton?.setAttribute('aria-expanded','false');}
menuButton?.addEventListener('click',()=>{const open=navigation.classList.toggle('open');menuButton.setAttribute('aria-expanded',String(open));});
navigation?.querySelectorAll('a').forEach(link=>link.addEventListener('click',closeMenu));
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&navigation?.classList.contains('open')){closeMenu();menuButton.focus();}});
const filters=document.querySelectorAll('[data-filter]');
const rows=document.querySelectorAll('[data-report-type]');
filters.forEach(button=>button.addEventListener('click',()=>{
 filters.forEach(other=>other.setAttribute('aria-pressed',String(other===button)));
 let count=0;
 rows.forEach(row=>{row.hidden=button.dataset.filter!=='all'&&row.dataset.reportType!==button.dataset.filter;if(!row.hidden)count++;});
 const status=document.querySelector('.report-count');
 if(status)status.textContent=`${count} ${count===1?'year':'years'} shown`;
}));
document.querySelector('[data-print]')?.addEventListener('click',()=>window.print());

document.querySelectorAll('[data-gallery]').forEach(gallery=>{
 const slides=[...gallery.querySelectorAll('[data-gallery-slide]')];
 const thumbnails=[...gallery.querySelectorAll('[data-gallery-select]')];
 const counter=gallery.querySelector('[data-gallery-counter]');
 const announcement=gallery.querySelector('[data-gallery-announcement]');
 const yearFilter=gallery.querySelector('[data-gallery-year-filter]');
 let selection=slides.map((_,index)=>index);
 let active=0;
 function updateDetails(){
  const item=slides[active].dataset;
  gallery.querySelector('[data-gallery-title]').textContent=item.title;
  gallery.querySelector('[data-gallery-caption]').textContent=item.caption;
  gallery.querySelector('[data-gallery-year]').textContent=item.year;
  gallery.querySelectorAll('[data-gallery-peek]').forEach(peek=>{
   const previous=peek.hasAttribute('data-gallery-prev');
   const index=selection[(selection.indexOf(active)+(previous?-1:1)+selection.length)%selection.length];
   peek.hidden=selection.length<2;
   peek.querySelector('img').src=slides[index].dataset.poster;
   peek.querySelector('.peek-label').textContent=slides[index].dataset.title;
   peek.setAttribute('aria-label',`View ${previous?'previous':'next'}: ${slides[index].dataset.title}`);
  });
 }
 function show(index,force=false){
  const next=index;
  if(next===active&&!force)return;
  slides[active].querySelector('video')?.pause();
  slides[active].hidden=true;
  thumbnails[active].setAttribute('aria-pressed','false');
  active=next;
  slides[active].hidden=false;
  thumbnails[active].setAttribute('aria-pressed','true');
  counter.textContent=`${String(selection.indexOf(active)+1).padStart(2,'0')} / ${String(selection.length).padStart(2,'0')}`;
  announcement.textContent=`${slides[active].dataset.year}. ${slides[active].dataset.title}`;
  updateDetails();
 }
 function step(direction){show(selection[(selection.indexOf(active)+direction+selection.length)%selection.length]);}
 gallery.querySelectorAll('[data-gallery-prev]').forEach(button=>button.addEventListener('click',()=>step(-1)));
 gallery.querySelectorAll('[data-gallery-next]').forEach(button=>button.addEventListener('click',()=>step(1)));
 thumbnails.forEach((button,index)=>button.addEventListener('click',()=>show(index)));
 yearFilter?.addEventListener('change',()=>{
  selection=slides.map((_,index)=>index).filter(index=>yearFilter.value==='all'||slides[index].dataset.yearKey===yearFilter.value);
  thumbnails.forEach((button,index)=>{
   button.hidden=!selection.includes(index);
   if(!button.hidden)button.setAttribute('aria-label',`Show item ${selection.indexOf(index)+1} of ${selection.length}: ${slides[index].dataset.title}`);
  });
  gallery.querySelectorAll('.gallery-arrows button').forEach(button=>{button.disabled=selection.length<2;button.hidden=selection.length<2;});
  slides.forEach((slide,index)=>{if(selection.includes(index))slide.setAttribute('aria-label',`${selection.indexOf(index)+1} of ${selection.length}: ${slide.dataset.title}`);});
  show(selection[0],true);
 });
 gallery.addEventListener('keydown',event=>{
  // Leave the native video player's keyboard shortcuts alone.
  if(!event.target.closest('.gallery-thumb,.gallery-arrows button,.gallery-peek'))return;
  if(event.key==='ArrowRight'||event.key==='ArrowLeft'){
   event.preventDefault();
   step(event.key==='ArrowRight'?1:-1);
   if(event.target.closest('.gallery-thumb'))thumbnails[active].focus();
  }
 });
 const stage=gallery.querySelector('.gallery-slides');
 let gesture=null;
 let suppressClickUntil=0;
 function resetDrag(){
  gesture=null;
  stage.classList.remove('is-dragging');
  stage.style.setProperty('--gallery-drag','0px');
 }
 stage.addEventListener('pointerdown',event=>{
  if(event.target.closest('video,.gallery-arrows')||!event.isPrimary||event.button!==0)return;
  gesture={x:event.clientX,y:event.clientY,id:event.pointerId,dragging:false};
 });
 stage.addEventListener('pointermove',event=>{
  if(!gesture||event.pointerId!==gesture.id)return;
  const dx=event.clientX-gesture.x,dy=event.clientY-gesture.y;
  if(!gesture.dragging){
   if(Math.abs(dy)>10&&Math.abs(dy)>Math.abs(dx)){resetDrag();return;}
   if(Math.abs(dx)<7||Math.abs(dx)<Math.abs(dy)*1.5)return;
   gesture.dragging=true;
   stage.setPointerCapture(event.pointerId);
   stage.classList.add('is-dragging');
  }
  const travel=Math.min(stage.clientWidth*.2,180);
  stage.style.setProperty('--gallery-drag',`${Math.max(-travel,Math.min(travel,dx))}px`);
 });
 stage.addEventListener('pointerup',event=>{
  if(!gesture||event.pointerId!==gesture.id)return;
  const dx=event.clientX-gesture.x,dy=event.clientY-gesture.y;
  const dragged=gesture.dragging;
  if(dragged)suppressClickUntil=performance.now()+350;
  resetDrag();
  if(dragged&&Math.abs(dx)>45&&Math.abs(dx)>Math.abs(dy)*1.5)step(dx<0?1:-1);
 });
 stage.addEventListener('pointercancel',resetDrag);
 stage.addEventListener('lostpointercapture',resetDrag);
 // A drag on a neighboring photo must not also activate that photo's button.
 stage.addEventListener('click',event=>{
  if(event.detail>0&&performance.now()<suppressClickUntil){event.preventDefault();event.stopPropagation();}
 },true);
 updateDetails();
 gallery.querySelectorAll('[data-gallery-controls]').forEach(control=>control.hidden=false);
 gallery.querySelectorAll('[data-gallery-peek]').forEach(control=>control.hidden=false);
});

// Normal profile links remain usable offline and without JavaScript.
const profileDialog=document.querySelector('[data-profile-dialog]');
if(profileDialog&&typeof profileDialog.showModal==='function'){
 const content=profileDialog.querySelector('[data-profile-content]');
 let profileTrigger=null;
 document.querySelectorAll('[data-profile]').forEach(link=>{
  link.setAttribute('aria-haspopup','dialog');
  link.addEventListener('click',event=>{
   if(event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
   const template=document.getElementById(`profile-${link.dataset.profile}`);
   if(!template)return;
   event.preventDefault();
   profileTrigger=link;
   content.replaceChildren(template.content.cloneNode(true));
   profileDialog.setAttribute('aria-labelledby',`${link.dataset.profile}-name`);
   profileDialog.showModal();
   document.body.classList.add('profile-open');
   profileDialog.querySelector('[data-profile-close]').focus();
  });
 });
 profileDialog.querySelector('[data-profile-close]').addEventListener('click',()=>profileDialog.close());
 profileDialog.addEventListener('click',event=>{
  if(event.target!==profileDialog)return;
  const box=profileDialog.getBoundingClientRect();
  if(event.clientX<box.left||event.clientX>box.right||event.clientY<box.top||event.clientY>box.bottom)profileDialog.close();
 });
 profileDialog.addEventListener('close',()=>{
  document.body.classList.remove('profile-open');
  if(profileTrigger?.isConnected)profileTrigger.focus({preventScroll:true});
  content.replaceChildren();
 });
}

// A short, manually controlled report carousel, with native touch scrolling.
document.querySelectorAll('[data-report-carousel]').forEach(carousel=>{
 const rail=carousel.querySelector('[data-report-rail]');
 const panels=[...rail.querySelectorAll('[data-report-year]')];
 const selectors=[...carousel.querySelectorAll('[data-report-select]')];
 const previous=carousel.querySelector('[data-report-prev]');
 const next=carousel.querySelector('[data-report-next]');
 const status=carousel.querySelector('[data-report-announcement]');
 let active=0,scrollFrame=0,drag=null,suppressClickUntil=0;
 function update(index){
  const changed=index!==active;
  active=index;
  selectors.forEach((button,i)=>button.setAttribute('aria-pressed',String(i===active)));
  previous.disabled=active===0;next.disabled=active===panels.length-1;
  if(changed)status.textContent=panels[active].getAttribute('aria-label');
 }
 function show(index,keyboard=false){
  const destination=Math.max(0,Math.min(panels.length-1,index));
  const left=destination===panels.length-1?rail.scrollWidth-rail.clientWidth:panels[destination].offsetLeft;
  rail.scrollTo({left,behavior:keyboard||matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
  if(keyboard)update(destination);
 }
 selectors.forEach((button,i)=>button.addEventListener('click',event=>show(i,event.detail===0)));
 previous.addEventListener('click',event=>show(active-1,event.detail===0));
 next.addEventListener('click',event=>show(active+1,event.detail===0));
 carousel.querySelector('.report-years').addEventListener('keydown',event=>{
  if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
  event.preventDefault();
  const index=event.key==='Home'?0:event.key==='End'?panels.length-1:Math.max(0,Math.min(panels.length-1,active+(event.key==='ArrowRight'?1:-1)));
  show(index,true);selectors[index].focus();
 });
 rail.addEventListener('scroll',()=>{
  if(scrollFrame)return;
  scrollFrame=requestAnimationFrame(()=>{
   scrollFrame=0;
   const middle=rail.scrollLeft+rail.clientWidth/2;
   let closest=0;
   panels.forEach((panel,i)=>{if(Math.abs(panel.offsetLeft+panel.offsetWidth/2-middle)<Math.abs(panels[closest].offsetLeft+panels[closest].offsetWidth/2-middle))closest=i;});
   update(closest);
  });
 },{passive:true});
 rail.addEventListener('pointerdown',event=>{
  if(event.pointerType!=='mouse'||event.button!==0||!event.isPrimary)return;
  drag={id:event.pointerId,x:event.clientX,y:event.clientY,left:rail.scrollLeft,moving:false};
 });
 rail.addEventListener('pointermove',event=>{
  if(!drag||drag.id!==event.pointerId)return;
  const dx=event.clientX-drag.x,dy=event.clientY-drag.y;
  if(!drag.moving){
   if(Math.abs(dy)>10&&Math.abs(dy)>Math.abs(dx)){drag=null;return;}
   if(Math.abs(dx)<7)return;
   drag.moving=true;rail.setPointerCapture(event.pointerId);rail.classList.add('is-dragging');
  }
  rail.scrollLeft=drag.left-dx;
 });
 function endDrag(){
  if(!drag)return;
  const moved=drag.moving;
  drag=null;rail.classList.remove('is-dragging');
  if(moved){
   suppressClickUntil=performance.now()+350;
   const middle=rail.scrollLeft+rail.clientWidth/2;
   let closest=0;
   panels.forEach((panel,i)=>{if(Math.abs(panel.offsetLeft+panel.offsetWidth/2-middle)<Math.abs(panels[closest].offsetLeft+panels[closest].offsetWidth/2-middle))closest=i;});
   show(closest);
  }
 }
 rail.addEventListener('pointerup',endDrag);
 rail.addEventListener('pointercancel',endDrag);
 rail.addEventListener('lostpointercapture',endDrag);
 rail.addEventListener('dragstart',event=>event.preventDefault());
 rail.addEventListener('click',event=>{if(event.detail>0&&performance.now()<suppressClickUntil){event.preventDefault();event.stopPropagation();}},true);
 carousel.querySelectorAll('[data-report-controls]').forEach(control=>control.hidden=false);
});
