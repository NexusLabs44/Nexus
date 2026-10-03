/* =========================================================
   ECONEXUS — SCRIPT.JS
   Frontend: Vercel
   Backend: Django / Render
   ========================================================= */


/* =========================================================
   CONFIGURAÇÃO GLOBAL
   ========================================================= */

const ECONEXUS_API_URL = "https://nexus-ykvd.onrender.com";

window.ECONEXUS_API_URL = ECONEXUS_API_URL;


/* =========================================================
   TEMA
   ========================================================= */

(function initTheme() {

    const root = document.documentElement;

    const savedTheme =
        localStorage.getItem("econexos-theme") || "light";

    root.setAttribute(
        "data-theme",
        savedTheme
    );


    window.toggleTheme = function () {

        const currentTheme =
            root.getAttribute("data-theme") === "dark"
                ? "light"
                : "dark";


        root.setAttribute(
            "data-theme",
            currentTheme
        );


        localStorage.setItem(
            "econexos-theme",
            currentTheme
        );


        document
            .querySelectorAll(".theme-icon")
            .forEach(icon => {

                icon.textContent =
                    currentTheme === "dark"
                        ? "☀️"
                        : "🌙";

            });

    };


    document
        .querySelectorAll(".theme-icon")
        .forEach(icon => {

            icon.textContent =
                savedTheme === "dark"
                    ? "☀️"
                    : "🌙";

        });

})();


/* =========================================================
   HEADER / SCROLL
   ========================================================= */

(function initHeader() {

    const header =
        document.querySelector(".header");


    if (!header) {
        return;
    }


    window.addEventListener(
        "scroll",
        () => {

            header.classList.toggle(
                "scrolled",
                window.scrollY > 20
            );

        }
    );

})();


/* =========================================================
   MENU MOBILE
   ========================================================= */

window.toggleMenu = function () {

    const nav =
        document.querySelector(".nav-links");


    if (!nav) {
        return;
    }


    nav.classList.toggle("open");

};


/* =========================================================
   REVEAL ON SCROLL
   ========================================================= */

(function initReveal() {

    const elements =
        document.querySelectorAll(".reveal");


    if (!elements.length) {
        return;
    }


    if (!("IntersectionObserver" in window)) {

        elements.forEach(element => {

            element.classList.add("in");

        });

        return;
    }


    const observer =
        new IntersectionObserver(
            entries => {

                entries.forEach(entry => {

                    if (entry.isIntersecting) {

                        entry.target.classList.add("in");

                    }

                });

            },
            {
                threshold: 0.12
            }
        );


    elements.forEach(element => {

        observer.observe(element);

    });

})();


/* =========================================================
   FAQ
   ========================================================= */

(function initFAQ() {

    document
        .querySelectorAll(".faq-item")
        .forEach(item => {

            const question =
                item.querySelector(".faq-q");


            if (!question) {
                return;
            }


            question.addEventListener(
                "click",
                () => {

                    item.classList.toggle("open");

                }
            );

        });

})();


/* =========================================================
   CONTADORES ANIMADOS
   ========================================================= */

(function initCounters() {

    const counters =
        document.querySelectorAll("[data-count]");


    if (!counters.length) {
        return;
    }


    counters.forEach(element => {

        const target =
            Number(element.dataset.count) || 0;


        let current = 0;


        const step =
            target / 60;


        const animate = () => {

            current += step;


            if (current >= target) {

                element.textContent =
                    target.toLocaleString("pt-BR");

                return;
            }


            element.textContent =
                Math.floor(current)
                    .toLocaleString("pt-BR");


            requestAnimationFrame(animate);

        };


        if (!("IntersectionObserver" in window)) {

            animate();

            return;
        }


        const observer =
            new IntersectionObserver(
                (entries, observerInstance) => {

                    entries.forEach(entry => {

                        if (entry.isIntersecting) {

                            animate();

                            observerInstance.disconnect();

                        }

                    });

                },
                {
                    threshold: 0.5
                }
            );


        observer.observe(element);

    });

})();


/* =========================================================
   BARRAS ANIMADAS
   ========================================================= */

(function initBars() {

    const bars =
        document.querySelectorAll(".bar");


    if (!bars.length) {
        return;
    }


    bars.forEach(bar => {

        const height =
            Number(bar.dataset.h) || 0;


        if (!("IntersectionObserver" in window)) {

            bar.style.height =
                `${height}%`;

            return;
        }


        const observer =
            new IntersectionObserver(
                (entries, observerInstance) => {

                    entries.forEach(entry => {

                        if (entry.isIntersecting) {

                            bar.style.height =
                                `${height}%`;

                            observerInstance.disconnect();

                        }

                    });

                },
                {
                    threshold: 0.3
                }
            );


        observer.observe(bar);

    });

})();


/* =========================================================
   CALCULADORA
   ========================================================= */

let selectedProfile = "fisica";


/* =========================================================
   SELECIONAR PESSOA FÍSICA / JURÍDICA
   ========================================================= */

function selectProfile(type) {

    selectedProfile =
        type === "juridica"
            ? "juridica"
            : "fisica";


    const typeInput =
        document.getElementById("tipoCalculo");


    if (typeInput) {

        typeInput.value =
            selectedProfile;

    }


    const formFisica =
        document.getElementById("formFisica");


    const formJuridica =
        document.getElementById("formJuridica");


    const btnFisica =
        document.getElementById("btnFisica");


    const btnJuridica =
        document.getElementById("btnJuridica");


    if (
        !formFisica ||
        !formJuridica ||
        !btnFisica ||
        !btnJuridica
    ) {

        console.warn(
            "Elementos da calculadora não encontrados."
        );

        return;
    }


    if (selectedProfile === "fisica") {

        formFisica.style.display =
            "block";


        formJuridica.style.display =
            "none";


        btnFisica.classList.add(
            "active"
        );


        btnJuridica.classList.remove(
            "active"
        );


        setFieldsDisabled(
            formFisica,
            false
        );


        setFieldsDisabled(
            formJuridica,
            true
        );

    } else {

        formFisica.style.display =
            "none";


        formJuridica.style.display =
            "block";


        btnFisica.classList.remove(
            "active"
        );


        btnJuridica.classList.add(
            "active"
        );


        setFieldsDisabled(
            formFisica,
            true
        );


        setFieldsDisabled(
            formJuridica,
            false
        );

    }

}


/* =========================================================
   HABILITAR / DESABILITAR CAMPOS
   ========================================================= */

function setFieldsDisabled(
    container,
    disabled
) {

    if (!container) {
        return;
    }


    container
        .querySelectorAll("input, select, textarea")
        .forEach(field => {

            field.disabled =
                disabled;


            field.required =
                !disabled;

        });

}


/* =========================================================
   CALCULADORA DE CARBONO
   ========================================================= */

async function calcCarbon(event) {

    event.preventDefault();


    const form =
        event.target;


    if (!form) {

        console.error(
            "Formulário não encontrado."
        );

        return false;
    }


    /* =====================================================
       PESSOA FÍSICA
       ===================================================== */

    if (selectedProfile === "fisica") {

        const energia =
            Number(
                form.energia?.value
            ) || 0;


        const transporte =
            Number(
                form.transporte?.value
            ) || 0;


        const combustivel =
            Number(
                form.combustivel?.value
            ) || 0;


        const viagens =
            Number(
                form.viagens?.value
            ) || 0;


        const agua =
            Number(
                form.agua?.value
            ) || 0;


        const residuos =
            Number(
                form.residuos?.value
            ) || 0;


        /* ---------------------------------------------
           Fatores de cálculo
           --------------------------------------------- */

        const energiaCO2 =
            energia * 0.0817 * 12;


        const transporteCO2 =
            transporte * 0.21 * 52;


        const combustivelCO2 =
            combustivel * 2.31 * 12;


        const viagensCO2 =
            viagens * 90;


        const aguaCO2 =
            agua * 0.000298 * 365;


        const residuosCO2 =
            residuos * 2.5 * 52;


        /* ---------------------------------------------
           Total
           --------------------------------------------- */

        const total =
            energiaCO2 +
            transporteCO2 +
            combustivelCO2 +
            viagensCO2 +
            aguaCO2 +
            residuosCO2;


        /* ---------------------------------------------
           Detalhamento
           --------------------------------------------- */

        const breakdown = {

            energia:
                energiaCO2,

            transporte:
                transporteCO2,

            combustivel:
                combustivelCO2,

            viagens:
                viagensCO2,

            agua:
                aguaCO2,

            residuos:
                residuosCO2

        };


        /* ---------------------------------------------
           Resultado
           --------------------------------------------- */

        const result = {

            tipo: "fisica",

            total:
                Math.round(total),

            breakdown,

            date:
                new Date().toISOString()

        };


        await saveCarbonResult(result);


        return false;
    }


    /* =====================================================
       PESSOA JURÍDICA
       ===================================================== */

    if (selectedProfile === "juridica") {

        const empresa =
            String(
                form.empresa?.value || ""
            ).trim();


        const funcionarios =
            Number(
                form.funcionarios?.value
            ) || 0;


        const energia =
            Number(
                form.energiaPJ?.value
            ) || 0;


        const gasolina =
            Number(
                form.gasolinaPJ?.value
            ) || 0;


        const diesel =
            Number(
                form.dieselPJ?.value
            ) || 0;


        const transporte =
            Number(
                form.transportePJ?.value
            ) || 0;


        const viagens =
            Number(
                form.viagensPJ?.value
            ) || 0;


        const residuos =
            Number(
                form.residuosPJ?.value
            ) || 0;


        /* ---------------------------------------------
           Fatores provisórios
           --------------------------------------------- */

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


        /* ---------------------------------------------
           Total
           --------------------------------------------- */

        const total =
            energiaCO2 +
            gasolinaCO2 +
            dieselCO2 +
            transporteCO2 +
            viagensCO2 +
            residuosCO2;


        /* ---------------------------------------------
           Detalhamento
           --------------------------------------------- */

        const breakdown = {

            energia:
                energiaCO2,

            combustivel:
                gasolinaCO2 +
                dieselCO2,

            transporte:
                transporteCO2,

            viagens:
                viagensCO2,

            residuos:
                residuosCO2

        };


        /* ---------------------------------------------
           Resultado
           --------------------------------------------- */

        const result = {

            tipo: "juridica",

            empresa,

            funcionarios,

            total:
                Math.round(total),

            breakdown,

            date:
                new Date().toISOString()

        };


        await saveCarbonResult(result);


        return false;
    }


    console.error(
        "Tipo de cálculo desconhecido."
    );


    return false;
}


/* =========================================================
   SALVAR RESULTADO
   ========================================================= */

async function saveCarbonResult(result) {

    /* =====================================================
       VALIDAÇÃO
       ===================================================== */

    if (!result) {

        console.error(
            "Resultado inválido."
        );

        return;
    }


    /* =====================================================
       LOCAL STORAGE — BACKUP
       ===================================================== */

    try {

        const history =
            JSON.parse(
                localStorage.getItem(
                    "econexos-history"
                ) || "[]"
            );


        history.unshift(result);


        localStorage.setItem(
            "econexos-history",
            JSON.stringify(
                history.slice(0, 20)
            )
        );


        localStorage.setItem(
            "econexos-last",
            JSON.stringify(result)
        );

    } catch (error) {

        console.error(
            "Erro ao salvar resultado localmente:",
            error
        );

    }


    /* =====================================================
       API DJANGO
       ===================================================== */

    try {

        const response =
            await fetch(
                `${ECONEXUS_API_URL}/api/calculations/`,
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    credentials: "include",

                    body:
                        JSON.stringify(result)
                }
            );


        /* ---------------------------------------------
           Verificar resposta
           --------------------------------------------- */

        if (!response.ok) {

            const errorText =
                await response.text();


            console.error(
                "Erro retornado pela API Django:",
                response.status,
                errorText
            );

        } else {

            let data = null;


            try {

                data =
                    await response.json();

            } catch {

                data = null;

            }


            console.log(
                "Cálculo enviado ao backend:",
                data
            );

        }

    } catch (error) {

        console.error(
            "Erro de conexão com o backend:",
            error
        );

    }


    /* =====================================================
       REDIRECIONAR PARA RESULTADOS
       ===================================================== */

    window.location.href =
        "/resultados/";

}


/* =========================================================
   EXPOR FUNÇÕES PARA O HTML
   ========================================================= */

window.selectProfile =
    selectProfile;


window.setFieldsDisabled =
    setFieldsDisabled;


window.calcCarbon =
    calcCarbon;


window.saveCarbonResult =
    saveCarbonResult;
