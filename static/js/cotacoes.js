async function enviarCotacao(id){

    try{

        const response = await fetch(`/cotacoes/${id}/gerar-link`,{
            method:"POST"
        });

        const dados = await response.json();
        console.log(dados);

        if(!dados.sucesso){
            alert("Erro ao gerar o link.");
            return;
        }

        const link = `${window.location.origin}/responder/${dados.token}`;

        const mensagem =
`Olá!

Segue o link da cotação para preenchimento:

${link}

Obrigado!`;

        window.location.href =
    `https://api.whatsapp.com/send?text=${encodeURIComponent(mensagem)}`;

    }catch(erro){

        console.error(erro);
        alert("Erro ao gerar o link.");

    }

}

function abrirCotacao(id){

    const div = document.getElementById("itens-" + id);

    const aberto = div.style.display === "block";

    fecharTodosOsPaineis(id);

    if(aberto){

        return;

    }

    fetch("/cotacoes/" + id + "/itens")
        .then(response => response.json())
        .then(itens => {

            let html = `
                <div style="
                    margin-top:15px;
                    background:#f8f9fa;
                    border:1px solid #dcdcdc;
                    border-radius:10px;
                    overflow:hidden;
                ">

                    <div style="
                        padding:12px 18px;
                        background:#198754;
                        color:white;
                        font-weight:600;
                    ">
                        ▼ Medicamentos da Cotação #${id}
                    </div>

                    <table style="
                        width:100%;
                        border-collapse:collapse;
                    ">

                        <thead>

    <tr style="background:#f5f7fb;">

    <th style="
        padding:12px 16px;
        text-align:left;
        color:#1f2937;
        font-weight:700;
    ">
        Medicamento
    </th>

    <th style="
        padding:12px 16px;
        text-align:center;
        color:#1f2937;
        font-weight:700;
    ">
        Quantidade
    </th>

</tr>

                        </thead>

                        <tbody>
            `;

            itens.forEach(item => {

                html += `
                    <tr>

                        <td style="padding:10px;border-top:1px solid #eee;">
                            ${item.medicamento}
                        </td>



                        <td style="padding:10px;border-top:1px solid #eee;text-align:center;">
                            ${item.quantidade}
                        </td>

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

        })
        .catch(error => {

            console.error(error);

            div.innerHTML = `
                <div style="
                    margin-top:15px;
                    padding:15px;
                    background:#ffe5e5;
                    color:#b00020;
                    border-radius:8px;
                ">
                    Erro ao carregar os medicamentos.
                </div>
            `;

            div.style.display = "block";

        });

}

async function abrirComparativo(id){

    const div = document.getElementById("comparativo-" + id);

    const aberto = div.style.display === "block";

    fecharTodosOsPaineis(id);

    if(aberto){

        return;

    }

    div.style.display="block";
    div.innerHTML="<h4>Carregando...</h4>";

    try{

        const response = await fetch("/comparativo/" + id);
        const dados = await response.json();

        let html=`


        `;

        dados.forEach(medicamento=>{

    html+=`

<div class="comparativo-card">

    <!-- COMPARATIVO PRIMEIRO -->
    <div class="comparativo-header">

        <div>

            <h3>
                <i class="bi bi-bar-chart-fill"></i>
                Comparativo de Preços
            </h3>

            <small>
                Ordenado do menor para o maior preço
            </small>

        </div>

    </div>

    <!-- MEDICAMENTO DEPOIS -->
    <div class="comparativo-topo">

        <div class="medicamento-info">

            <div class="medicamento-icone">
                <i class="bi bi-capsule"></i>
            </div>

            <div>

                <h2>${medicamento.nome}</h2>

                <span>Medicamento</span>

            </div>

        </div>

        <div class="resultado-badge">

            ${medicamento.representantes.length} resultados

        </div>

    </div>

    <div class="ranking-lista">

`;

            medicamento.representantes.forEach((rep,index)=>{

        html += `

<div class="ranking-card ${index === 0 ? 'primeiro' : ''}">

    <div class="ranking-posicao">

    <div class="medalha ${index==0?'ouro':index==1?'prata':index==2?'bronze':'normal'}">

        <div class="medalha-circulo">

            ${index+1}

        </div>

        ${
            index < 3
            ?
            `
            <div class="medalha-fitas">

                <span></span>

                <span></span>

            </div>
            `
            :
            ""
        }

    </div>

</div>

    <div class="ranking-info">

    <div class="ranking-nome">

        ${rep.representante}

    </div>

    <div class="ranking-laboratorio">

        ${rep.laboratorio}

    </div>

    ${
    rep.oferta
    ? `
        <div class="oferta-linha">

            <span class="offer-badge">OFERTA</span>

            <span class="offer-texto">

                A partir de ${rep.quantidade} un.

            </span>

        </div>
    `
    : ""
}

</div>

    <div class="ranking-preco">

    <div class="valor">

        ${
            rep.oferta
            ? `R$ ${rep.preco_oferta}`
            : `R$ ${rep.preco}`
        }

    </div>

    <small>

    ${
        rep.oferta
        ? `${rep.quantidade} unidades`
        : "Preço Unitário"
    }

</small>

</div>

</div>

`;

            });

            html+=`

                    </div>

                </div>

            `;

        });

        html+=`

            </div>

        </div>

        `;

        div.innerHTML=html;

    }catch(e){

        div.innerHTML="Erro ao carregar comparativo.";

    }

}

async function abrirResultado(id){

    const div = document.getElementById("resultado-" + id);

        div.dataset.cotacaoId = id;

    const aberto = div.style.display === "block";

    fecharTodosOsPaineis(id);

    if(aberto){

        return;

    }

    div.style.display="block";
    div.innerHTML="<h4>Carregando resultado...</h4>";

    try{

        const response = await fetch("/resultado/" + id);
const dados = await response.json();

resultadoAtual = dados;

console.log(resultadoAtual);

console.log(dados);

        let html = `

<div class="resultado-card">

    <div class="comparativo-header">

        <div>

            <h3>

                <i class="bi bi-file-earmark-text-fill"></i>

                Resultado da Cotação

            </h3>

            <small>

                Vencedores da cotação

            </small>

        </div>

    </div>

`;

dados.forEach(rep=>{

html += `

<div class="resultado-representante">

    <div class="resultado-topo">

        <div class="resultado-usuario">

            <div class="resultado-avatar">

                <i class="bi bi-person-fill"></i>

            </div>

            <div>

                <h2>${rep.representante}</h2>

                <span>${rep.distribuidora}</span>

            </div>

        </div>

    </div>

    <table class="resultado-tabela">

        <thead>

            <tr>

                <th>Medicamento</th>

                <th style="width:190px;">Ação</th>

                <th>Preço</th>

                <th>Quantidade</th>

            </tr>

        </thead>

        <tbody>

`;

rep.itens.forEach(item=>{

    const medicamento = item.medicamento;

    const quantidade = item.quantidade;

    const preco = item.preco;

    const precoOferta = item.preco_oferta;

    const status = item.oferta ? "OFERTA" : "TENHO";

    html+=`

        <tr>


    <td class="col-medicamento">

        <strong>${medicamento}</strong>

        <small class="condicao-mobile">

            ${
                status=="OFERTA"
                ? `Oferta a partir de ${quantidade} un.`
                : "Preço Unitário"
            }

        </small>

    </td>

<td class="col-acoes">

    <select
        class="acao-medicamento"
        data-medicamento="${medicamento}"
    >

        <option value="">
            Selecionar ação
        </option>

        <option value="proximo">
            Próximo melhor preço
        </option>

        <option value="proxima_cotacao">
            Próxima cotação
        </option>

    </select>

</td>

    <td class="col-preco">

        R$ ${status=="OFERTA" ? precoOferta : preco}

    </td>

    <td class="col-qtd">

        <input
            type="number"
            value="${quantidade ?? 1}"
            min="1"
            class="campo-quantidade"
        >

    </td>

</tr>

    `;

});

let totalRepresentante = 0;

rep.itens.forEach(item=>{

    const quantidade = Number(item.quantidade ?? 1);

    const preco = item.oferta
        ? Number(item.preco_oferta ?? 0)
        : Number(item.preco ?? 0);

    totalRepresentante += quantidade * preco;

});

html+=`

        </tbody>

    </table>

    <div class="resultado-rodape">

        <div class="resultado-total">

            <small>TOTAL</small>

            <h2 class="total-representante">

    R$ ${totalRepresentante.toFixed(2)}

</h2>

        </div>

        <button
    class="btn-gerar-pedido"
    onclick="abrirPedido(this, ${id}, '${rep.representante}')">

    <i class="bi bi-cart3"></i>

    GERAR PEDIDO

</button>

    </div>

</div>

`;

});

    html += `

</div>

`;

div.innerHTML = html;

/* =====================================================
   AÇÕES DOS MEDICAMENTOS
===================================================== */

div.addEventListener("change", async function (event) {

    const select = event.target.closest(".acao-medicamento");

    if (!select) {
        return;
    }

const acao = select.value;

const medicamento =
    select.dataset.medicamento;

        console.log(
            "AÇÃO:",
            acao,
            "MEDICAMENTO:",
            medicamento
        );


if (!acao) {

    select.classList.remove(
        "acao-selecionada"
    );

    return;
}


select.classList.add("acao-selecionada");


        /* =============================================
           ENVIAR PARA O PRÓXIMO
        ============================================= */

if (acao === "proximo") {

    const cotacaoId =
        div.dataset.cotacaoId;

    if (!cotacaoId) {

        alert(
            "Não foi possível identificar a cotação."
        );

        select.value = "";

        return;
    }

const linhaAtual =
    select.closest("tr");

const cardAtual =
    select.closest(
        ".resultado-representante"
    );

    if (!linhaAtual || !cardAtual) {

        alert(
            "Não foi possível identificar o medicamento."
        );

        select.value = "";

        return;
    }

    select.disabled = true;

    try {

        /*
         * REPRESENTANTE ATUAL
         */

        const representanteAtual =
            cardAtual.querySelector(
                ".resultado-usuario h2"
            )?.innerText.trim() || "";

        const distribuidoraAtual =
            cardAtual.querySelector(
                ".resultado-usuario span"
            )?.innerText.trim() || "";


        /*
         * BUSCA O PRÓXIMO PREÇO
         */

        const formData =
            new FormData();

        formData.append(
            "medicamento",
            medicamento
        );

        formData.append(
            "representante_atual",
            representanteAtual
        );

        formData.append(
            "distribuidora_atual",
            distribuidoraAtual
        );


        const resposta =
            await fetch(
                `/cotacoes/${cotacaoId}/proximo-melhor-preco`,
                {
                    method: "POST",
                    body: formData
                }
            );


        const resultado =
            await resposta.json();


        console.log(
            "PRÓXIMO MELHOR PREÇO:",
            resultado
        );


        if (!resultado.sucesso) {

            alert(
                resultado.erro ||
                "Não existe outro preço disponível."
            );

            select.value = "";

            return;
        }


        /*
         * =========================================
         * ATUALIZA O ESTADO DO PEDIDO
         * =========================================
         */

        const pedidoAtual =
            resultadoAtual.find(
                r =>
                    r.representante
                    === representanteAtual
            );


        if (pedidoAtual) {

            pedidoAtual.itens =
                pedidoAtual.itens.filter(
                    item =>
                        item.medicamento
                        !== medicamento
                );

        }


        /*
         * Procura o representante de destino
         */

        let pedidoDestino =
            resultadoAtual.find(
                r =>
                    r.representante
                    === resultado.representante
            );


        /*
         * Se ainda não existe,
         * cria o representante.
         */

        if (!pedidoDestino) {

            pedidoDestino = {

                representante:
                    resultado.representante,

                distribuidora:
                    resultado.distribuidora,

                whatsapp:
                    resultado.whatsapp,

                itens: []

            };

            resultadoAtual.push(
                pedidoDestino
            );
        }


        /*
         * Adiciona o medicamento
         * ao novo representante.
         */

        pedidoDestino.itens.push({

            medicamento:
                resultado.medicamento,

            preco:
                resultado.preco,

            preco_oferta:
                resultado.preco_oferta,

            preco_final:
                resultado.preco_final,

            quantidade:
                resultado.quantidade,

            oferta:
                resultado.oferta

        });


        /*
         * =========================================
         * REMOVE DA TELA ATUAL
         * =========================================
         */

        linhaAtual.remove();


        /*
         * =========================================
         * PROCURA O CARD DE DESTINO
         * =========================================
         */

        let cardDestino =
            Array.from(
                div.querySelectorAll(
                    ".resultado-representante"
                )
            ).find(card => {

                const nome =
                    card.querySelector(
                        ".resultado-usuario h2"
                    )?.innerText.trim();

                const distribuidora =
                    card.querySelector(
                        ".resultado-usuario span"
                    )?.innerText.trim();

                return (
                    nome ===
                    resultado.representante

                    &&

                    distribuidora ===
                    resultado.distribuidora
                );

            });


        /*
         * =========================================
         * CRIA CARD SE NÃO EXISTIR
         * =========================================
         */

        if (!cardDestino) {

            const resultadoCard =
                div.querySelector(
                    ".resultado-card"
                );

            cardDestino =
                document.createElement(
                    "div"
                );

            cardDestino.className =
                "resultado-representante";


            cardDestino.innerHTML = `

                <div class="resultado-topo">

                    <div class="resultado-usuario">

                        <div class="resultado-avatar">

                            <i class="bi bi-person-fill"></i>

                        </div>

                        <div>

                            <h2>
                                ${resultado.representante}
                            </h2>

                            <span>
                                ${resultado.distribuidora}
                            </span>

                        </div>

                    </div>

                </div>


                <table class="resultado-tabela">

                    <thead>

                        <tr>

                            <th>
                                Medicamento
                            </th>

                            <th>
                                Ação
                            </th>

                            <th>
                                Preço
                            </th>

                            <th>
                                Quantidade
                            </th>

                        </tr>

                    </thead>


                    <tbody></tbody>

                </table>


                <div class="resultado-rodape">

                    <div class="resultado-total">

                        <small>
                            TOTAL
                        </small>

                        <h2 class="total-representante">
                            R$ 0,00
                        </h2>

                    </div>


                    <button
                        class="btn-gerar-pedido"
                        onclick="abrirPedido(
                            this,
                            '${cotacaoId}',
                            '${resultado.representante}'
                        )"
                    >

                        <i class="bi bi-cart3"></i>

                        GERAR PEDIDO

                    </button>

                </div>

            `;

            resultadoCard.appendChild(
                cardDestino
            );
        }


        /*
         * =========================================
         * ADICIONA A LINHA NO CARD DESTINO
         * =========================================
         */

        const tbody =
            cardDestino.querySelector(
                "tbody"
            );


        const novaLinha =
            document.createElement(
                "tr"
            );


        const precoExibido =
            Number(
                resultado.preco_final
            );


        const quantidade =
            Number(
                resultado.quantidade || 1
            );


        novaLinha.innerHTML = `

            <td class="col-medicamento">

                <strong>
                    ${resultado.medicamento}
                </strong>

                <small class="condicao-mobile">

                    ${
                        resultado.oferta
                        ? `Oferta a partir de ${resultado.quantidade_oferta || resultado.quantidade} un.`
                        : "Preço Unitário"
                    }

                </small>

            </td>


            <td class="col-acoes">

                <select
                    class="acao-medicamento"
                    data-medicamento="${resultado.medicamento}"
                >

                    <option value="">
                        Selecionar ação
                    </option>

                    <option value="proximo">
                        Próximo melhor preço
                    </option>

                    <option value="proxima_cotacao">
                        Próxima cotação
                    </option>

                </select>

            </td>


            <td class="col-preco">

                R$
                ${precoExibido
                    .toFixed(2)
                    .replace(".", ",")}

            </td>


            <td class="col-qtd">

                <input
                    type="number"
                    value="${quantidade}"
                    min="1"
                    class="campo-quantidade"
                >

            </td>

        `;


        tbody.appendChild(
            novaLinha
        );


        /*
         * =========================================
         * ATUALIZA TOTAL
         * =========================================
         */

        const atualizarTotalDestino =
            () => {

                let total = 0;


                cardDestino
                    .querySelectorAll(
                        "tbody tr"
                    )
                    .forEach(linha => {

                        const texto =
                            linha.cells[2]
                                .innerText
                                .replace("R$", "")
                                .replace(/\./g, "")
                                .replace(",", ".")
                                .trim();


                        const precoLinha =
                            Number(texto);


                        const qtd =
                            Number(
                                linha.querySelector(
                                    ".campo-quantidade"
                                ).value
                            );


                        total +=
                            precoLinha * qtd;

                    });


                const totalElemento =
                    cardDestino.querySelector(
                        ".total-representante"
                    );


                if (totalElemento) {

                    totalElemento.innerText =
                        "R$ " +
                        total
                            .toFixed(2)
                            .replace(".", ",");

                }

            };


        const inputQuantidade =
            novaLinha.querySelector(
                ".campo-quantidade"
            );


        inputQuantidade.addEventListener(
            "input",
            atualizarTotalDestino
        );


        inputQuantidade.addEventListener(
            "change",
            atualizarTotalDestino
        );


        atualizarTotalDestino();


        /*
         * =========================================
         * SE O CARD ORIGINAL FICOU VAZIO
         * REMOVE O CARD
         * =========================================
         */

        const tbodyAtual =
            cardAtual.querySelector(
                "tbody"
            );


        if (
            tbodyAtual
            &&
            tbodyAtual.children.length === 0
        ) {

            cardAtual.remove();

        }


        /*
         * IMPORTANTE:
         *
         * NÃO fazemos mais:
         *
         * fetch("/resultado/${cotacaoId}")
         *
         * porque isso reconstruiria o resultado
         * original e desfaria a transferência.
         */

    } catch (erro) {

        console.error(
            "ERRO AO PASSAR PARA O PRÓXIMO:",
            erro
        );

        alert(
            "Erro ao passar para o próximo melhor preço."
        );

    } finally {

select.disabled = false;
select.value = "";

    }

}


/* =============================================
   ENVIAR PARA A PRÓXIMA COTAÇÃO
============================================= */

if (acao === "proxima_cotacao") {

    console.log(
        "Enviar para próxima cotação:",
        medicamento
    );

    const confirmar = confirm(
    "Deseja remover este item e guardá-lo em Recuperar pendências para a próxima cotação?"
);

if (!confirmar) {

    // Volta o select para "Selecionar ação"
select.value = "";

select.classList.remove(
    "acao-selecionada"
);

    return;
}

    const cotacaoId =
        div.dataset.cotacaoId;


    if (!cotacaoId) {

        console.error(
            "ID DA COTAÇÃO NÃO ENCONTRADO"
        );

        alert(
            "Não foi possível identificar a cotação."
        );

        return;

    }


    const formData =
        new FormData();

    formData.append(
        "medicamento",
        medicamento
    );


    try {

        const resposta =
            await fetch(
                `/cotacoes/${cotacaoId}/enviar-proxima-cotacao`,
                {
                    method: "POST",
                    body: formData
                }
            );


        const resultado =
            await resposta.json();


        console.log(
            "RESPOSTA:",
            resultado
        );


        if (!resultado.sucesso) {

            alert(
                resultado.erro ||
                "Erro ao enviar o medicamento."
            );

            return;

        }


        alert(
    "Medicamento enviado para a próxima cotação."
);

/* =========================================
   REMOVE SOMENTE A LINHA DO MEDICAMENTO
   E MANTÉM O RESULTADO ABERTO
========================================= */

const linha = select.closest("tr");

if (linha) {
    linha.remove();
}



    } catch (erro) {

        console.error(
            "ERRO AO ENVIAR MEDICAMENTO:",
            erro
        );

        alert(
            "Erro ao enviar o medicamento para a próxima cotação."
        );

    }

}

    });

div.querySelectorAll(".resultado-representante").forEach(card=>{

    function atualizarTotal(){

        let total = 0;

        const linhas = card.querySelectorAll("tbody tr");

        linhas.forEach(linha=>{

            const precoTexto = linha.cells[2].innerText
                .replace("R$", "")
                .replace(",", ".")
                .trim();

            const preco = Number(precoTexto);

            const quantidade = Number(
                linha.querySelector(".campo-quantidade").value
            );

            total += preco * quantidade;

        });

        card.querySelector(".total-representante").innerText =
            "R$ " + total.toFixed(2);

    }

    card.querySelectorAll(".campo-quantidade").forEach(input=>{

        input.addEventListener("input", atualizarTotal);
        input.addEventListener("change", atualizarTotal);

    });

});

} catch (e) {

    console.error(e);

    div.innerHTML = `
        <pre style="color:red;padding:20px">
${e.stack}
        </pre>
    `;

}
}




function fecharTodosOsPaineis(id){

    const cotacao = document.querySelector(`#itens-${id}`).closest(".cotacao-card");

    cotacao.querySelectorAll(
        ".itens-cotacao, .comparativo-cotacao, .resultado-cotacao"
    ).forEach(painel=>{

        painel.style.display="none";
        painel.innerHTML="";

    });

}

async function encerrarCotacao(id){

    if(!confirm("Deseja realmente encerrar esta cotação?")){
        return;
    }

    try{

        const response = await fetch(`/cotacoes/${id}/encerrar`,{
            method:"POST"
        });

        const dados = await response.json();

        if(dados.sucesso){

            alert("Cotação encerrada com sucesso.");

            location.reload();

        }else{

            alert("Erro ao encerrar a cotação.");

        }

    }catch(e){

    console.error(e);

    alert("Erro ao encerrar a cotação.");

}

}

function cotacaoEncerrada(){

    alert(
        "Esta cotação foi encerrada e não pode mais ser enviada aos representantes."
    );

}

async function excluirCotacao(id){

    if(!confirm("Deseja realmente excluir esta cotação?")){
        return;
    }

    try{

const response = await fetch(`/cotacoes/${id}/excluir`,{
    method:"POST"
});

const dados = await response.json();

console.log(dados);

if(response.ok && dados.sucesso){

    alert("Cotação excluída com sucesso.");

    location.reload();

}else{

    alert(dados.erro || "Erro ao excluir a cotação.");

}

}catch(e){

    console.error(e);

    alert("Erro ao excluir a cotação.");

}

}
let resultadoAtual = [];

let whatsappPedido = "";
let mensagemPedido = "";

function abrirPedido(botao, cotacaoId, representante){

    document.getElementById("pedidoRepresentante").innerText =
        representante;

const pedido = resultadoAtual.find(
    r => r.representante === representante
);

if(!pedido){

    alert("Pedido não encontrado.");

    return;

}

whatsappPedido = pedido.whatsapp;

console.log("Whats:", whatsappPedido);

    // Card do representante na tela
    const card = botao.closest(".resultado-representante");

    

    let html = "";
    let total = 0;

    let mensagem = `🟢 *PEDIDO - COTEX CONECTA*

    👤 *Representante:* ${representante}

    ────────────────────────

`;

const linhas = card.querySelectorAll("tbody tr");

linhas.forEach(linha => {

    const medicamento =
        linha.querySelector(
            ".col-medicamento strong"
        )?.innerText.trim();

    if (!medicamento) {
        return;
    }


    const precoTexto =
        linha.querySelector(
            ".col-preco"
        )?.innerText
            .replace("R$", "")
            .replace(",", ".")
            .trim();

    const preco = Number(precoTexto);


    if (!Number.isFinite(preco)) {
        return;
    }


    const inputQuantidade =
        linha.querySelector(
            ".campo-quantidade"
        );

    const quantidade =
        Number(inputQuantidade?.value || 1);


    const subtotal =
        preco * quantidade;


    total += subtotal;


    mensagem +=
`💊 *${medicamento}*
📦 Quantidade: ${quantidade}
💰 Preço: R$ ${preco.toFixed(2)}
💵 Subtotal: R$ ${subtotal.toFixed(2)}

`;


    html += `
        <tr>
            <td>${medicamento}</td>
            <td>R$ ${preco.toFixed(2)}</td>
            <td style="text-align:center">${quantidade}</td>
            <td>R$ ${subtotal.toFixed(2)}</td>
        </tr>
    `;

});

mensagem +=
`────────────────────────

💲 *TOTAL DO PEDIDO*
R$ ${total.toFixed(2)}

🤝 Pedido gerado automaticamente pelo *Cotex Conecta*.`;

mensagemPedido = mensagem;

document.getElementById("pedidoItens").innerHTML = html;

document.getElementById("pedidoTotal").innerHTML =
    "R$ " + total.toFixed(2);

document.getElementById("modalPedido").style.display = "flex";
}

function enviarWhatsappPedido(){

    if(!whatsappPedido){

        alert("WhatsApp do representante não encontrado.");

        return;

    }

    window.open(

        `https://wa.me/55${whatsappPedido}?text=${encodeURIComponent(mensagemPedido)}`,

        "_blank"

    );

}

function fecharPedido(){

    document.getElementById("modalPedido").style.display = "none";

}