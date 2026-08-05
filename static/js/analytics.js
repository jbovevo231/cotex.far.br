console.log("analytics.js carregou");

async function carregarGraficoCotacoes(){

    const response = await fetch("/analytics/cotacoes-realizadas");

    const dados = await response.json();

    const labels = dados.map(item => item.dia);

    const valores = dados.map(item => item.total);

    const canvas = document.getElementById("graficoCotacoes");

    new Chart(canvas, {

        type: "line",

        data: {

            labels: labels,

            datasets: [

                {

                    label: "Cotações realizadas",

                    data: valores,

                    borderColor: "#2563eb",

                    backgroundColor: "rgba(37,99,235,0.15)",

                    fill: true,

                    tension: 0.4,

                    borderWidth: 3,

                    pointRadius: 4,

                    pointHoverRadius: 6

                }

            ]

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

                y: {

                    beginAtZero: true,

                    ticks: {

                        precision: 0

                    }

                }

            }

        }

    });

}

console.log(document.getElementById("graficoCotacoes"));
console.log(typeof Chart);



async function carregarGraficoEconomia(){

    const response =
        await fetch("/analytics/economia-gerada");

    const dados =
        await response.json();

    const labels =
        dados.map(i=>i.dia);

    const valores =
        dados.map(i=>i.total);

    new Chart(

        document.getElementById("graficoEconomia"),

        {

            type:"line",

            data:{

                labels,

                datasets:[{

                    data:valores,

                    borderColor:"#16a34a",

                    backgroundColor:"rgba(22,163,74,.12)",

                    fill:true,

                    tension:.4,

                    borderWidth:3,

                    pointRadius:6,
pointHoverRadius:8,
pointBackgroundColor:"#16a34a",
pointBorderColor:"#16a34a",

                }]

            },

            options:{

                responsive:true,

                maintainAspectRatio:false,

                plugins:{
                    legend:{
                        display:false
                    }
                },

                scales:{

                    x:{
                        grid:{
                            display:false
                        }
                    },

                    y:{
                        beginAtZero:true
                    }

                }

            }

        }

    );

}

carregarGraficoCotacoes();

carregarGraficoEconomia();

async function carregarGraficoResposta(){

    const response =
        await fetch("/analytics/taxa-resposta");

    const dados =
        await response.json();

    console.log("Taxa:", dados);

    const labels =
        dados.map(i => i.dia);

    const valores =
        dados.map(i => i.total);

    new Chart(

        document.getElementById("graficoResposta"),

        {

            type:"line",

            data:{

                labels,

                datasets:[{

                    data:valores,

                    borderColor:"#8b5cf6",

                    backgroundColor:"rgba(139,92,246,.15)",

                    fill:true,

                    tension:.4,

                    borderWidth:3,

                    pointRadius:5,

                    pointHoverRadius:7

                }]

            },

            options:{

                responsive:true,

                maintainAspectRatio:false,

                plugins:{
                    legend:{
                        display:false
                    }
                },

                scales:{

                    x:{
                        grid:{
                            display:false
                        }
                    },

                    y:{

                        beginAtZero:true,

                        max:100,

                        ticks:{
                            callback:(v)=>v+"%"
                        }

                    }

                }

            }

        }

    );

}

carregarGraficoResposta();