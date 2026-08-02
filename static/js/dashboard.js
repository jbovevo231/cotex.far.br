console.log("dashboard.js carregado");

const medicamentos = [];

const btnAdicionar = document.getElementById("btnAdicionar");



document
.getElementById("btnPendencias")
.addEventListener(

    "click",

    abrirPendencias

);

btnAdicionar.addEventListener("click", function () {

    let medicamento = document.getElementById("medicamento").value.trim();
    let quantidade = document.getElementById("quantidade").value.trim();

    // Somente o medicamento é obrigatório
    if (!medicamento) {
        alert("Informe o nome do medicamento.");
        return;
    }

    // Campos opcionais


    if (quantidade === "") {
        quantidade = "-";
    }

        medicamentos.push({
        medicamento,
        quantidade
    });

        atualizarLista();

        salvarRascunho();

        document.getElementById("medicamento").value = "";
        document.getElementById("quantidade").value = "";

        document.getElementById("medicamento").focus();

        });

function atualizarLista() {

    const lista = document.getElementById("listaMedicamentos");

    lista.innerHTML = "";

    medicamentos.forEach((item, index) => {

        lista.innerHTML += `
            <tr>

    <td>${item.medicamento}</td>

    <td>${item.quantidade}</td>

    <td class="acoes">

        <button
            type="button"
            class="btn-remover-lista"
            onclick="removerMedicamento(${index})">

            <i class="bi bi-trash"></i>

        </button>

        <input
            type="hidden"
            name="medicamento[]"
            value="${item.medicamento}">

        <input
            type="hidden"
            name="laboratorio[]"
            value="">

        <input
            type="hidden"
            name="quantidade[]"
            value="${item.quantidade}">

    </td>

</tr>
        `;

    });

}

function removerMedicamento(indice) {

    medicamentos.splice(indice, 1);

    atualizarLista();

    salvarRascunho();

}

document.getElementById("btnLimparLista").addEventListener("click", function () {

    if (medicamentos.length === 0) {
        return;
    }

    if (!confirm("Deseja limpar toda a lista?")) {
        return;
    }

medicamentos.length = 0;

atualizarLista();

localStorage.removeItem("rascunhoCotacao");

});

/* ===================================
   RASCUNHO AUTOMÁTICO DA COTAÇÃO
=================================== */

function salvarRascunho() {

    localStorage.setItem(

        "rascunhoCotacao",

        JSON.stringify({

            nomeCotacao: document.getElementById("nomeCotacao").value,

            medicamentos: medicamentos

        })

    );

}

function restaurarRascunho() {

    const salvo = localStorage.getItem("rascunhoCotacao");

    if (!salvo) {

        return;

    }

    const dados = JSON.parse(salvo);

    document.getElementById("nomeCotacao").value =
        dados.nomeCotacao || "";

    medicamentos.length = 0;

    dados.medicamentos.forEach(item => {

        medicamentos.push(item);

    });

    atualizarLista();

}

document.addEventListener("DOMContentLoaded", function () {

    restaurarRascunho();

});

/* ==========================================
   REPOR PENDÊNCIAS
========================================== */

async function abrirPendencias(){

    const resposta = await fetch(
        "/dashboard/pendencias"
    );

    const dados = await resposta.json();


`Encontramos <strong>${dados.length}</strong> medicamento(s) sem cotação ou com valor igual a zero na última cotação encerrada. Selecione os itens que deseja adicionar à nova lista.`;

    console.log(JSON.stringify(dados));

    const lista =
        document.getElementById("listaPendencias");

    lista.innerHTML = "";

    if(dados.length===0){

        lista.innerHTML = `
            <p>
                Nenhuma pendência encontrada.
            </p>
        `;

        document
            .getElementById("modalPendencias")
            .style.display="flex";

        return;

    }

    dados.forEach(item => {

    const jaExiste = medicamentos.some(med =>

    med.medicamento.toLowerCase() === item[0].toLowerCase()

);

console.log(item[0], jaExiste);

    lista.innerHTML += `

        <label class="item-pendencia ${jaExiste ? 'ja-adicionado' : ''}">

            <input
                type="checkbox"
                class="chkPendencia"
                ${jaExiste ? 'disabled' : 'checked'}
                data-medicamento="${item[0]}"
                data-laboratorio="${item[1]}"
                data-quantidade="${item[2]}">

            <span>

                <strong>${item[0]}</strong>

                <br>

                ${item[1]}

                • Quantidade: ${item[2]}

                ${
                    jaExiste
                    ? '<span class="badge-adicionado">✓ Já adicionado</span>'
                    : ''
                }

            </span>

        </label>

    `;

});

    document
        .getElementById("modalPendencias")
        .style.display="flex";

}

document
.getElementById("btnAdicionarPendencias")
.addEventListener("click", function () {

    document
    .querySelectorAll(".chkPendencia:checked")
    .forEach(function (item) {

        const jaExiste = medicamentos.some(med =>

            med.medicamento.toLowerCase() ===
            item.dataset.medicamento.toLowerCase()

        );

        if (!jaExiste) {

            medicamentos.push({

    medicamento: item.dataset.medicamento,

    quantidade: item.dataset.quantidade

});

        }

    });

    atualizarLista();

    salvarRascunho();

    fecharPendencias();

});

function fecharPendencias(){

    document
        .getElementById("modalPendencias")
        .style.display = "none";

    document
        .getElementById("listaPendencias")
        .innerHTML = "";

}

/* =====================================
   AUTOCOMPLETE DE MEDICAMENTOS
===================================== */

const campoMedicamento = document.getElementById("medicamento");
const listaSugestoes = document.getElementById("listaSugestoes");

campoMedicamento.addEventListener("input", async function () {

    console.log("Digitou:", this.value);
    const termo = this.value.trim();

    if (termo.length < 2) {

        listaSugestoes.innerHTML = "";
        listaSugestoes.style.display = "none";

        return;
    }

        console.log("Buscando...");

    const resposta = await fetch(
        "/dashboard/historico?q=" +
        encodeURIComponent(termo)
    );

    const dados = await resposta.json();

    console.log(dados);

    listaSugestoes.innerHTML = "";

    if (dados.length === 0) {

        listaSugestoes.style.display = "none";
        return;

    }

    dados.forEach(item => {

        const div = document.createElement("div");

        div.className = "item-sugestao";

        div.innerHTML = `
    <strong>${item[0]}</strong>
`;

        div.onclick = function(){

            campoMedicamento.value = item[0];

            listaSugestoes.innerHTML = "";

            listaSugestoes.style.display = "none";

            document
                .getElementById("quantidade")
                .focus();

        };

        listaSugestoes.appendChild(div);

    });

    listaSugestoes.style.display = "block";

});

function abrirImportacao(){


    document.getElementById("modalImportacao").style.display = "flex";

}

function fecharImportacao(){

    document.getElementById("modalImportacao").style.display = "none";

}

window.addEventListener("click", function(e){

    const modal = document.getElementById("modalImportacao");

    if(e.target === modal){

        fecharImportacao();

    }

});

function importarLista(){

    const texto = document
        .getElementById("listaMedicamentosTexto")
        .value
        .trim();

    if(texto === ""){

        alert("Cole uma lista de medicamentos.");

        return;

    }

    const linhas = texto
        .split(/\r?\n/)
        .map(l => l.trim())
        .filter(l => l !== "");

    linhas.forEach(function(linha){

        const existe = medicamentos.some(item =>
            item.medicamento.toLowerCase() === linha.toLowerCase()
        );

        if(!existe){

            medicamentos.push({

    medicamento: linha,

    quantidade: "-"

});

        }

    });

    atualizarLista();

    salvarRascunho();

    document.getElementById("listaMedicamentosTexto").value = "";

    fecharImportacao();

}

function fecharTodosOsPaineisDashboard(id){

    document
        .querySelectorAll("[id^='itens-']")
        .forEach(div => {

            if(div.id !== "itens-" + id){

                div.style.display = "none";

            }

        });

}

function abrirCotacaoDashboard(id){
    
    console.log("Abrindo", id);
    const div = document.getElementById("itens-" + id);
    console.log(div);

    const aberto = div.style.display === "block";

    fecharTodosOsPaineisDashboard(id);

    if(aberto){

        div.style.display = "none";

        return;

    }

    fetch("/cotacoes/" + id + "/itens")
        .then(response => response.json())
        .then(itens => {

            let html = `

                <div class="painel-itens">

                    <div class="painel-itens-header">

                        Medicamentos da Cotação

                    </div>

                    <table class="tabela-produtos">

                        <thead>

                            <tr>

                                <th>Medicamento</th>

                                <th>Quantidade</th>

                            </tr>

                        </thead>

                        <tbody>

            `;

            itens.forEach(item => {

                html += `

                    <tr>

                        <td>${item.medicamento}</td>

                        <td>${item.quantidade}</td>

                    </tr>

                `;

            });

            html += `

                        </tbody>

                    </table>

                </div>

            `;

            div.innerHTML = html;

            div.style.display = "block";

        });

}