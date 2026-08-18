console.log("analytics.js carregou");

// =========================================================
// FILTRO GLOBAL DE PERÍODO
// =========================================================

let periodoAnalytics = {

    inicio: null,

    fim: null

};

// =========================================================
// INSTÂNCIAS DOS GRÁFICOS
// =========================================================

let graficoCotacoes = null;

let graficoEconomia = null;

let graficoResposta = null;

let graficoMedicamentos = null;

let graficoStatus = null;




// =========================================================
// DESTRUIR GRÁFICO ANTERIOR
// =========================================================

function destruirGrafico(canvas) {

    if (!canvas) {
        return;
    }

    const graficoExistente =
        Chart.getChart(canvas);

    if (graficoExistente) {

        graficoExistente.destroy();

    }

}


// =========================================================
// DATA LOCAL YYYY-MM-DD
// =========================================================

function formatarDataLocal(data) {

    const ano =
        data.getFullYear();

    const mes =
        String(
            data.getMonth() + 1
        ).padStart(2, "0");

    const dia =
        String(
            data.getDate()
        ).padStart(2, "0");

    return `${ano}-${mes}-${dia}`;

}


// =========================================================
// CALCULAR PERÍODO
// =========================================================

function calcularPeriodo(tipo) {

    const hoje = new Date();

    let inicio =
        new Date(hoje);

    let fim =
        new Date(hoje);


    // -----------------------------------------------------
    // ÚLTIMOS 7 DIAS
    // -----------------------------------------------------

    if (tipo === "7") {

        inicio.setDate(
            hoje.getDate() - 6
        );

    }


    // -----------------------------------------------------
    // ÚLTIMOS 30 DIAS
    // -----------------------------------------------------

    else if (tipo === "30") {

        inicio.setDate(
            hoje.getDate() - 29
        );

    }


    // -----------------------------------------------------
    // ÚLTIMOS 90 DIAS
    // -----------------------------------------------------

    else if (tipo === "90") {

        inicio.setDate(
            hoje.getDate() - 89
        );

    }


    // -----------------------------------------------------
    // ESTE MÊS
    // -----------------------------------------------------

    else if (tipo === "mes") {

        inicio =
            new Date(
                hoje.getFullYear(),
                hoje.getMonth(),
                1
            );

    }


    // -----------------------------------------------------
    // MÊS PASSADO
    // -----------------------------------------------------

    else if (tipo === "mes_passado") {

        inicio =
            new Date(
                hoje.getFullYear(),
                hoje.getMonth() - 1,
                1
            );

        fim =
            new Date(
                hoje.getFullYear(),
                hoje.getMonth(),
                0
            );

    }


    return {

        inicio:
            formatarDataLocal(inicio),

        fim:
            formatarDataLocal(fim)

    };

}


// =========================================================
// ATUALIZAR DESCRIÇÃO
// =========================================================

function atualizarDescricaoPeriodo(
    texto
) {

    const elemento =
        document.getElementById(
            "periodoDescricao"
        );

    if (elemento) {

        elemento.textContent =
            texto;

    }

}


// =========================================================
// CONSTRUIR URL COM PERÍODO
// =========================================================

function urlComPeriodo(url) {

    const params =
        new URLSearchParams();


    if (periodoAnalytics.inicio) {

        params.append(
            "data_inicio",
            periodoAnalytics.inicio
        );

    }


    if (periodoAnalytics.fim) {

        params.append(
            "data_fim",
            periodoAnalytics.fim
        );

    }


    const query =
        params.toString();


    if (!query) {

        return url;

    }


    return `${url}?${query}`;

}


// =========================================================
// APLICAR PERÍODO
// =========================================================

function aplicarPeriodoAnalytics(
    inicio,
    fim,
    descricao
) {

    periodoAnalytics.inicio =
        inicio;

    periodoAnalytics.fim =
        fim;


    atualizarDescricaoPeriodo(
        descricao
    );


    carregarGraficoCotacoes();

    carregarGraficoEconomia();

    carregarGraficoResposta();

    carregarGraficoMedicamentos();

    carregarDistribuicaoStatus();

}


// =========================================================
// INICIALIZAR FILTRO
// =========================================================

function inicializarFiltroPeriodo() {

    const select =
        document.getElementById(
            "filtroPeriodo"
        );

    if (!select) {

        return;

    }


    // padrão = últimos 30 dias

    const periodo =
        calcularPeriodo("30");


    periodoAnalytics.inicio =
        periodo.inicio;

    periodoAnalytics.fim =
        periodo.fim;


    // -----------------------------------------------------
    // TROCA DO SELECT
    // -----------------------------------------------------

    select.addEventListener(
        "change",
        function() {

            const tipo =
                this.value;


            if (
                tipo ===
                "personalizado"
            ) {

                document.getElementById(
                    "periodoPersonalizado"
                ).style.display =
                    "flex";

                atualizarDescricaoPeriodo(
                    "Escolha as datas"
                );

                return;

            }


            document.getElementById(
                "periodoPersonalizado"
            ).style.display =
                "none";


            const periodo =
                calcularPeriodo(
                    tipo
                );


            let descricao =
                "Período selecionado";


            if (tipo === "7") {

                descricao =
                    "Últimos 7 dias";

            }

            else if (tipo === "30") {

                descricao =
                    "Últimos 30 dias";

            }

            else if (tipo === "90") {

                descricao =
                    "Últimos 90 dias";

            }

            else if (tipo === "mes") {

                descricao =
                    "Este mês";

            }

            else if (
                tipo ===
                "mes_passado"
            ) {

                descricao =
                    "Mês passado";

            }


            aplicarPeriodoAnalytics(

                periodo.inicio,

                periodo.fim,

                descricao

            );

        }
    );


    // -----------------------------------------------------
    // PERSONALIZADO
    // -----------------------------------------------------

    const btn =
        document.getElementById(
            "btnAplicarPeriodo"
        );


    if (btn) {

        btn.addEventListener(
            "click",
            function() {

                const inicio =
                    document.getElementById(
                        "dataInicio"
                    ).value;


                const fim =
                    document.getElementById(
                        "dataFim"
                    ).value;


                if (
                    !inicio ||
                    !fim
                ) {

                    alert(
                        "Selecione a data inicial e a data final."
                    );

                    return;

                }


                if (inicio > fim) {

                    alert(
                        "A data inicial não pode ser maior que a data final."
                    );

                    return;

                }


                aplicarPeriodoAnalytics(

                    inicio,

                    fim,

                    `${inicio.split("-").reverse().join("/")} até ${fim.split("-").reverse().join("/")}`

                );

            }
        );

    }

}

// =========================================================
// COTAÇÕES REALIZADAS
// =========================================================

async function carregarGraficoCotacoes(){

    try {

        const response =
            await fetch(
    urlComPeriodo(
        "/analytics/cotacoes-realizadas"
    )
);

        const dados =
            await response.json();

        const labels =
            dados.map(item => item.dia);

        const valores =
            dados.map(item => item.total);

        const canvas =
            document.getElementById("graficoCotacoes");

        if (!canvas) {

            console.error(
                "Canvas graficoCotacoes não encontrado."
            );

            return;

        }

        destruirGrafico(canvas);

        graficoCotacoes =
            new Chart(canvas, {
            type: "line",

            data: {

                labels: labels,

                datasets: [{

                    label: "Cotações realizadas",

                    data: valores,

                    borderColor: "#2563eb",

                    backgroundColor:
                        "rgba(37,99,235,0.15)",

                    fill: true,

                    tension: 0.4,

                    borderWidth: 3,

                    pointRadius: 4,

                    pointHoverRadius: 6

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {
                        display: false
                    }

                },

                scales: {

                    x: {

                        grid: {
                            display: false
                        }

                    },

                    y: {

                        beginAtZero: true,

                        ticks: {
                            precision: 0
                        }

                    }

                }

            }

        });

    } catch(error) {

        console.error(
            "Erro no gráfico de cotações:",
            error
        );

    }

}


// =========================================================
// ECONOMIA GERADA
// =========================================================

async function carregarGraficoEconomia(){

    try {

        const response =
            await fetch(
    urlComPeriodo(
        "/analytics/economia-gerada"
    )
);

        const dados =
            await response.json();

        const labels =
            dados.map(i => i.dia);

        const valores =
            dados.map(i => i.total);

        const canvas =
            document.getElementById(
                "graficoEconomia"
            );

        if (!canvas) {

            console.error(
                "Canvas graficoEconomia não encontrado."
            );

            return;

        }

        destruirGrafico(canvas);

        graficoEconomia =
            new Chart(canvas, {

            type: "line",

            data: {

                labels: labels,

                datasets: [{

                    data: valores,

                    borderColor: "#16a34a",

                    backgroundColor:
                        "rgba(22,163,74,.12)",

                    fill: true,

                    tension: .4,

                    borderWidth: 3,

                    pointRadius: 6,

                    pointHoverRadius: 8,

                    pointBackgroundColor:
                        "#16a34a",

                    pointBorderColor:
                        "#16a34a"

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {
                        display: false
                    }

                },

                scales: {

                    x: {

                        grid: {
                            display: false
                        }

                    },

                    y: {

                        beginAtZero: true

                    }

                }

            }

        });

    } catch(error) {

        console.error(
            "Erro no gráfico de economia:",
            error
        );

    }

}


// =========================================================
// TAXA DE RESPOSTA
// =========================================================

async function carregarGraficoResposta(){

    try {

        const response =
            await fetch(
    urlComPeriodo(
        "/analytics/taxa-resposta"
    )
);

        const dados =
            await response.json();

        console.log(
            "Taxa:",
            dados
        );

        const labels =
            dados.map(i => i.dia);

        const valores =
            dados.map(i => i.total);

        const canvas =
            document.getElementById(
                "graficoResposta"
            );

        if (!canvas) {

            console.error(
                "Canvas graficoResposta não encontrado."
            );

            return;

        }

        destruirGrafico(canvas);

        graficoResposta =
            new Chart(canvas, {

            type: "line",

            data: {

                labels: labels,

                datasets: [{

                    data: valores,

                    borderColor: "#8b5cf6",

                    backgroundColor:
                        "rgba(139,92,246,.15)",

                    fill: true,

                    tension: .4,

                    borderWidth: 3,

                    pointRadius: 5,

                    pointHoverRadius: 7

                }]

            },

            options: {

                responsive: true,

                maintainAspectRatio: false,

                plugins: {

                    legend: {
                        display: false
                    }

                },

                scales: {

                    x: {

                        grid: {
                            display: false
                        }

                    },

                    y: {

                        beginAtZero: true,

                        max: 100,

                        ticks: {

                            callback: (v) =>
                                v + "%"

                        }

                    }

                }

            }

        });

    } catch(error) {

        console.error(
            "Erro no gráfico de resposta:",
            error
        );

    }

}


// =========================================================
// MEDICAMENTOS MAIS COTADOS
// =========================================================

async function carregarGraficoMedicamentos(){

    try {

        console.log(
            "Carregando medicamentos mais cotados..."
        );


        const response =
            await fetch(
    urlComPeriodo(
        "/analytics/medicamentos-mais-cotados"
    )
);


        if(!response.ok){

            throw new Error(
                "Erro HTTP: " +
                response.status
            );

        }


        const dados =
            await response.json();


        console.log(
            "Medicamentos mais cotados:",
            dados
        );


        // -------------------------------------------------
        // Nomes dos medicamentos
        // -------------------------------------------------

        const labels =
            dados.map(
                item => item.medicamento
            );


        // -------------------------------------------------
        // QUANTIDADE DE VEZES COTADO
        //
        // IMPORTANTE:
        // O Python retorna "quantidade",
        // não "total".
        // -------------------------------------------------

        const valores =
            dados.map(
                item => item.quantidade
            );


        console.log(
            "Labels:",
            labels
        );

        console.log(
            "Valores:",
            valores
        );


        const canvas =
            document.getElementById(
                "graficoMedicamentos"
            );


if (!canvas) {

    console.error(
        "Canvas graficoMedicamentos não encontrado."
    );

    return;

}

destruirGrafico(canvas);

graficoMedicamentos =
    new Chart(canvas, {

            type: "bar",


            data: {

                labels: labels,


                datasets: [{

                    label:
                        "Quantidade de cotações",

                    data: valores,


                    backgroundColor:
                        "#2563eb",


                    hoverBackgroundColor:
                        "#1d4ed8",


                    borderRadius: 8,


                    borderSkipped: false,


                    barThickness: 16,


                    maxBarThickness: 20

                }]

            },


            options: {

                indexAxis: "y",


                responsive: true,


                maintainAspectRatio: false,


                animation: {

                    duration: 700

                },


                plugins: {

                    legend: {

                        display: false

                    },


                    tooltip: {

                        displayColors: false,


                        callbacks: {

                            title: function(context){

                                return context[0]
                                    .label;

                            },


                            label: function(context){

                                const quantidade =
                                    context.raw;

                                return (
                                    quantidade +
                                    (
                                        quantidade === 1
                                            ? " cotação"
                                            : " cotações"
                                    )
                                );

                            }

                        }

                    }

                },


                scales: {

                    x: {

                        beginAtZero: true,


                        ticks: {

                            precision: 0,


                            color: "#64748b",


                            font: {

                                size: 11

                            }

                        },


                        grid: {

                            color:
                                "#edf1f5"

                        }

                    },


                    y: {

                        grid: {

                            display: false

                        },


                        ticks: {

                            color:
                                "#1e293b",


                            font: {

                                size: 11,

                                weight: "600"

                            }

                        }

                    }

                }

            }

        });


    } catch(error) {

        console.error(
            "Erro no gráfico de medicamentos:",
            error
        );

    }

}



// =========================================================
// CARREGAR DISTRIBUIÇÃO DOS STATUS
// =========================================================

async function carregarDistribuicaoStatus() {

    const canvas =
        document.getElementById(
            "graficoStatus"
        );


    if (!canvas) {

        console.error(
            "Canvas graficoStatus não encontrado."
        );

        return;

    }


    try {

        // -------------------------------------------------
        // BUSCA OS DADOS REAIS
        // -------------------------------------------------

        const response =
    await fetch(
        urlComPeriodo(
            "/analytics/status"
        )
    );

        if (!response.ok) {

            throw new Error(
                "Erro HTTP: " +
                response.status
            );

        }


        const dados =
            await response.json();


        console.log(
            "Distribuição dos status:",
            dados
        );


        // -------------------------------------------------
        // DADOS
        // -------------------------------------------------

        const tenho =
            Number(
                dados.tenho || 0
            );


        const oferta =
            Number(
                dados.oferta || 0
            );


        const naoTenho =
            Number(
                dados.nao_tenho || 0
            );


        const total =
            tenho +
            oferta +
            naoTenho;


        // -------------------------------------------------
        // TOTAL NO CENTRO
        // -------------------------------------------------

        const totalElemento =
            document.getElementById(
                "statusTotal"
            );


        if (totalElemento) {

            totalElemento.textContent =
                total.toLocaleString(
                    "pt-BR"
                );

        }


        // -------------------------------------------------
        // LEGENDA
        // -------------------------------------------------

        atualizarLegendaStatus(
            total,
            tenho,
            oferta,
            naoTenho
        );


        // -------------------------------------------------
        // DESTROI GRÁFICO ANTERIOR
        // -------------------------------------------------

        if (graficoStatus) {

            graficoStatus.destroy();

        }


        // -------------------------------------------------
        // GRÁFICO VAZIO
        // -------------------------------------------------

        if (total === 0) {

            graficoStatus =
                new Chart(
                    canvas,
                    {

                        type: "doughnut",

                        data: {

                            labels: [
                                "Sem respostas"
                            ],

                            datasets: [{

                                data: [1],

                                backgroundColor: [
                                    "#E9EEF5"
                                ],

                                borderWidth: 0

                            }]

                        },


                        options: {

                            responsive: true,

                            maintainAspectRatio: false,

                            cutout: "68%",

                            plugins: {

                                legend: {
                                    display: false
                                },

                                tooltip: {
                                    enabled: false
                                }

                            }

                        }

                    }
                );


            return;

        }


        // -------------------------------------------------
        // GRÁFICO REAL
        // -------------------------------------------------

        graficoStatus =
            new Chart(
                canvas,
                {

                    type: "doughnut",


                    data: {

                        labels: [

                            "Tenho",

                            "Tenho oferta",

                            "Não tenho"

                        ],


                        datasets: [{

                            data: [

                                tenho,

                                oferta,

                                naoTenho

                            ],


                            backgroundColor: [

                                "#16A34A",

                                "#F59E0B",

                                "#EF4444"

                            ],


                            borderColor:
                                "#ffffff",


                            borderWidth: 4,


                            hoverOffset: 7

                        }]

                    },


                    options: {

                        responsive: true,

                        maintainAspectRatio: false,

                        cutout: "68%",


                        animation: {

                            duration: 700

                        },


                        plugins: {

                            legend: {

                                display: false

                            },


                            tooltip: {

                                displayColors: false,


                                callbacks: {

                                    label:
                                        function(context) {

                                        const valor =
                                            Number(
                                                context.raw ||
                                                0
                                            );


                                        const percentual =
                                            total > 0

                                                ? (
                                                    valor /
                                                    total *
                                                    100
                                                ).toFixed(1)

                                                : 0;


                                        return (

                                            context.label +

                                            ": " +

                                            valor.toLocaleString(
                                                "pt-BR"
                                            ) +

                                            " (" +

                                            percentual +

                                            "%)"

                                        );

                                    }

                                }

                            }

                        }

                    }

                }

            );


    } catch (error) {

        console.error(
            "Erro na distribuição dos status:",
            error
        );

    }

}



// =========================================================
// LEGENDA DOS STATUS
// =========================================================

function atualizarLegendaStatus(
    total,
    tenho,
    oferta,
    naoTenho
) {

    const legenda =
        document.getElementById(
            "statusLegenda"
        );


    if (!legenda) {

        return;

    }


    function percentual(
        valor
    ) {

        if (total === 0) {

            return "0%";

        }


        return (

            (
                valor /
                total *
                100
            ).toFixed(1)

            + "%"

        );

    }


    legenda.innerHTML = `

        <div class="status-legenda-item">

            <div class="status-legenda-nome">

                <span
                    class="status-dot status-dot-verde">
                </span>

                <span>
                    Tenho
                </span>

            </div>

            <strong>
                ${percentual(tenho)}
            </strong>

        </div>


        <div class="status-legenda-item">

            <div class="status-legenda-nome">

                <span
                    class="status-dot status-dot-laranja">
                </span>

                <span>
                    Tenho oferta
                </span>

            </div>

            <strong>
                ${percentual(oferta)}
            </strong>

        </div>


        <div class="status-legenda-item">

            <div class="status-legenda-nome">

                <span
                    class="status-dot status-dot-vermelho">
                </span>

                <span>
                    Não tenho
                </span>

            </div>

            <strong>
                ${percentual(naoTenho)}
            </strong>

        </div>

    `;

}



// =========================================================
// INICIALIZAÇÃO DO ANALYTICS
// =========================================================

document.addEventListener(
    "DOMContentLoaded",
    function() {

        inicializarFiltroPeriodo();

        // -------------------------------------------------
        // PRIMEIRA CARGA
        // -------------------------------------------------

        carregarGraficoCotacoes();

        carregarGraficoEconomia();

        carregarGraficoResposta();

        carregarGraficoMedicamentos();

        carregarDistribuicaoStatus();

    }
);