/* Apply before styles paint; explicit preferences override the device setting. */
(()=>{
 'use strict';
 const key='econ-theme',root=document.documentElement,media=window.matchMedia('(prefers-color-scheme: dark)');
 let preference=null;try{const saved=localStorage.getItem(key);if(saved==='light'||saved==='dark')preference=saved}catch{}
 function apply(theme){
  root.dataset.theme=theme;
  const button=document.getElementById('theme-toggle');
  if(button){const dark=theme==='dark';button.textContent=dark?'☀ Light mode':'☾ Dark mode';button.setAttribute('aria-pressed',String(dark));button.title=dark?'Switch to light mode':'Switch to dark mode'}
 }
 apply(preference||(media.matches?'dark':'light'));
 document.addEventListener('DOMContentLoaded',()=>apply(root.dataset.theme));
 document.addEventListener('click',event=>{
  if(!event.target.closest('#theme-toggle'))return;
  preference=root.dataset.theme==='dark'?'light':'dark';apply(preference);
  try{localStorage.setItem(key,preference)}catch{}
 });
 media.addEventListener('change',()=>{if(!preference)apply(media.matches?'dark':'light')});
 window.addEventListener('storage',event=>{if(event.key!==key)return;preference=['light','dark'].includes(event.newValue)?event.newValue:null;apply(preference||(media.matches?'dark':'light'))});
})();
