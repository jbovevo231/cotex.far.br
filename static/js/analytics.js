console.log("analytics.js carregou");


// =========================================================
// COTAÇÕES REALIZADAS
// =========================================================

async function carregarGraficoCotacoes(){

    try {

        const response =
            await fetch("/analytics/cotacoes-realizadas");

        const dados =
            await response.json();

        const labels =
            dados.map(item => item.dia);

        const valores =
            dados.map(item => item.total);

        const canvas =
            document.getElementById("graficoCotacoes");

        if(!canvas){
            console.error(
                "Canvas graficoCotacoes não encontrado."
            );
            return;
        }

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
            await fetch("/analytics/economia-gerada");

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

        if(!canvas){
            console.error(
                "Canvas graficoEconomia não encontrado."
            );
            return;
        }

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
            await fetch("/analytics/taxa-resposta");

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

        if(!canvas){
            console.error(
                "Canvas graficoResposta não encontrado."
            );
            return;
        }

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
                "/analytics/medicamentos-mais-cotados"
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


        if(!canvas){

            console.error(
                "Canvas graficoMedicamentos não encontrado."
            );

            return;

        }


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
// INICIALIZAÇÃO
// =========================================================

carregarGraficoCotacoes();

carregarGraficoEconomia();

carregarGraficoResposta();

carregarGraficoMedicamentos();