/* ECONEXOS — JS */
(function(){
  // Theme
  const root=document.documentElement;
  const saved=localStorage.getItem('econexos-theme')||'light';
  root.setAttribute('data-theme',saved);
  window.toggleTheme=()=>{
    const cur=root.getAttribute('data-theme')==='dark'?'light':'dark';
    root.setAttribute('data-theme',cur);
    localStorage.setItem('econexos-theme',cur);
    document.querySelectorAll('.theme-icon').forEach(e=>e.textContent=cur==='dark'?'☀️':'🌙');
  };
  document.querySelectorAll('.theme-icon').forEach(e=>e.textContent=saved==='dark'?'☀️':'🌙');

  // Header scroll
  const header=document.querySelector('.header');
  if(header){window.addEventListener('scroll',()=>header.classList.toggle('scrolled',scrollY>20))}

  // Mobile menu
  window.toggleMenu=()=>document.querySelector('.nav-links')?.classList.toggle('open');

  // Reveal on scroll
  const io=new IntersectionObserver(es=>es.forEach(e=>e.isIntersecting&&e.target.classList.add('in')),{threshold:.12});
  document.querySelectorAll('.reveal').forEach(el=>io.observe(el));

  // FAQ
  document.querySelectorAll('.faq-item').forEach(it=>{
    it.querySelector('.faq-q').addEventListener('click',()=>it.classList.toggle('open'));
  });

  // Animated counters
  document.querySelectorAll('[data-count]').forEach(el=>{
    const target=+el.dataset.count;let cur=0;const step=target/60;
    const tick=()=>{cur+=step;if(cur>=target){el.textContent=target.toLocaleString('pt-BR');return}
      el.textContent=Math.floor(cur).toLocaleString('pt-BR');requestAnimationFrame(tick)};
    new IntersectionObserver((es,o)=>es.forEach(e=>{if(e.isIntersecting){tick();o.disconnect()}}),{threshold:.5}).observe(el);
  });

  // Bars
  document.querySelectorAll('.bar').forEach(b=>{
    new IntersectionObserver((es,o)=>es.forEach(e=>{if(e.isIntersecting){b.style.height=b.dataset.h+'%';o.disconnect()}}),{threshold:.3}).observe(b);
  });
})();

/* ===== AUTH ===== */
function showMsg(id,type,text){const m=document.getElementById(id);if(!m)return;m.className='msg '+type;m.textContent=text}
function handleRegister(e){
  e.preventDefault();
  const f=e.target,name=f.name.value.trim(),email=f.email.value.trim(),pwd=f.pwd.value,cpwd=f.cpwd.value,phone=f.phone.value.trim();
  if(name.length<3)return showMsg('msg','error','Nome muito curto.');
  if(!/^[^@]+@[^@]+\.[^@]+$/.test(email))return showMsg('msg','error','E-mail inválido.');
  if(pwd.length<6)return showMsg('msg','error','A senha precisa de pelo menos 6 caracteres.');
  if(pwd!==cpwd)return showMsg('msg','error','As senhas não coincidem.');
  if(phone.length<8)return showMsg('msg','error','Telefone inválido.');
  const user={name,email,phone,createdAt:Date.now()};
  localStorage.setItem('econexos-user',JSON.stringify(user));
  showMsg('msg','ok','Conta criada com sucesso! Redirecionando...');
  setTimeout(()=>location.href='profile.html',1200);
  return false;
}
function handleLogin(e){
  e.preventDefault();
  const f=e.target,email=f.email.value.trim(),pwd=f.pwd.value;
  if(!/^[^@]+@[^@]+\.[^@]+$/.test(email))return showMsg('msg','error','E-mail inválido.');
  if(pwd.length<6)return showMsg('msg','error','Senha muito curta.');
  let u=JSON.parse(localStorage.getItem('econexos-user')||'null');
  if(!u){u={name:email.split('@')[0],email,phone:''};localStorage.setItem('econexos-user',JSON.stringify(u));}
  showMsg('msg','ok','Login realizado! Redirecionando...');
  setTimeout(()=>location.href='profile.html',900);
  return false;
}

/* ===== CALCULATOR ===== */
function calcCarbon(e){
  e.preventDefault();
  const f=e.target;
  const energia=+f.energia.value||0;     // kWh/mês -> 0.0817 kg CO2/kWh (BR)
  const transporte=+f.transporte.value||0; // km/semana carro -> 0.21 kg/km
  const combustivel=+f.combustivel.value||0; // L/mês -> 2.31 kg/L
  const viagens=+f.viagens.value||0;     // h/ano avião -> 90 kg/h
  const agua=+f.agua.value||0;           // L/dia -> 0.000298 kg/L
  const residuos=+f.residuos.value||0;   // kg/semana -> 2.5 kg CO2/kg
  const total=
    energia*0.0817*12 +
    transporte*0.21*52 +
    combustivel*2.31*12 +
    viagens*90 +
    agua*0.000298*365 +
    residuos*2.5*52;
  const breakdown={energia:energia*0.0817*12,transporte:transporte*0.21*52,combustivel:combustivel*2.31*12,viagens:viagens*90,agua:agua*0.000298*365,residuos:residuos*2.5*52};
  const result={total:Math.round(total),breakdown,date:new Date().toISOString()};
  // history
  const hist=JSON.parse(localStorage.getItem('econexos-history')||'[]');
  hist.unshift(result);localStorage.setItem('econexos-history',JSON.stringify(hist.slice(0,20)));
  localStorage.setItem('econexos-last',JSON.stringify(result));
  location.href='resultados.html';
  return false;
}
