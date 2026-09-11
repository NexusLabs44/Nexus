/* ECONEXUS — JS */
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

let selectedProfile = 'fisica';


function selectProfile(type) {

  selectedProfile = type;

  const formFisica = document.getElementById('formFisica');
  const formJuridica = document.getElementById('formJuridica');

  const btnFisica = document.getElementById('btnFisica');
  const btnJuridica = document.getElementById('btnJuridica');


  if (type === 'fisica') {

    formFisica.style.display = 'block';
    formJuridica.style.display = 'none';

    btnFisica.classList.add('active');
    btnJuridica.classList.remove('active');

    setFieldsDisabled(formFisica, false);
    setFieldsDisabled(formJuridica, true);

  } else {

    formFisica.style.display = 'none';
    formJuridica.style.display = 'block';

    btnFisica.classList.remove('active');
    btnJuridica.classList.add('active');

    setFieldsDisabled(formFisica, true);
    setFieldsDisabled(formJuridica, false);

  }
}


function setFieldsDisabled(container, disabled) {

  container.querySelectorAll('input').forEach(input => {
    input.disabled = disabled;
    input.required = !disabled;
  });

}


function calcCarbon(e) {

  e.preventDefault();

  const f = e.target;


  /* ==================== */
  /* PESSOA FÍSICA */
  /* ==================== */

  if (selectedProfile === 'fisica') {

    const energia = +f.energia.value || 0;
    const transporte = +f.transporte.value || 0;
    const combustivel = +f.combustivel.value || 0;
    const viagens = +f.viagens.value || 0;
    const agua = +f.agua.value || 0;
    const residuos = +f.residuos.value || 0;


    const total =
      energia * 0.0817 * 12 +
      transporte * 0.21 * 52 +
      combustivel * 2.31 * 12 +
      viagens * 90 +
      agua * 0.000298 * 365 +
      residuos * 2.5 * 52;


    const breakdown = {

      energia: energia * 0.0817 * 12,

      transporte: transporte * 0.21 * 52,

      combustivel: combustivel * 2.31 * 12,

      viagens: viagens * 90,

      agua: agua * 0.000298 * 365,

      residuos: residuos * 2.5 * 52

    };


    const result = {

      tipo: 'fisica',

      total: Math.round(total),

      breakdown,

      date: new Date().toISOString()

    };


    saveCarbonResult(result);

    return false;

  }


  /* ==================== */
  /* PESSOA JURÍDICA */
  /* ==================== */

  if (selectedProfile === 'juridica') {

    const empresa = f.empresa.value.trim();

    const funcionarios = +f.funcionarios.value || 0;

    const energia = +f.energiaPJ.value || 0;

    const gasolina = +f.gasolinaPJ.value || 0;

    const diesel = +f.dieselPJ.value || 0;

    const transporte = +f.transportePJ.value || 0;

    const viagens = +f.viagensPJ.value || 0;

    const residuos = +f.residuosPJ.value || 0;


    /*
      ATENÇÃO:

      Estes fatores são provisórios nesta primeira versão.
      Antes da versão final da Nexus, vamos validar cada fator
      com uma fonte/metodologia adequada ao projeto.
    */


    const energiaCO2 =
      energia * 0.0817 * 12;


    const gasolinaCO2 =
      gasolina * 2.31 * 12;


    const dieselCO2 =
      diesel * 2.68 * 12;


    const transporteCO2 =
      transporte * 0.21 * 12;


    const viagensCO2 =
      viagens * 90;


    const residuosCO2 =
      residuos * 2.5 * 52;


    const total =
      energiaCO2 +
      gasolinaCO2 +
      dieselCO2 +
      transporteCO2 +
      viagensCO2 +
      residuosCO2;


    const breakdown = {

      energia: energiaCO2,

      combustivel: gasolinaCO2 + dieselCO2,

      transporte: transporteCO2,

      viagens: viagensCO2,

      residuos: residuosCO2

    };


    const result = {

      tipo: 'juridica',

      empresa,

      funcionarios,

      total: Math.round(total),

      breakdown,

      date: new Date().toISOString()

    };


    saveCarbonResult(result);

    return false;

  }

}


function saveCarbonResult(result) {

  /* Histórico */

  const hist =
    JSON.parse(
      localStorage.getItem('econexos-history') || '[]'
    );


  hist.unshift(result);


  localStorage.setItem(
    'econexos-history',
    JSON.stringify(hist.slice(0, 20))
  );


  /* Último resultado */

  localStorage.setItem(
    'econexos-last',
    JSON.stringify(result)
  );


  /* Ir para resultados */

  location.href = 'resultados.html';

}
