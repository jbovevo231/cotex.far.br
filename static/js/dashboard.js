console.log("dashboard.js carregado");

const medicamentos = [];

const btnAdicionar = document.getElementById("btnAdicionar");

btnAdicionar.addEventListener("click", function () {

    let medicamento = document.getElementById("medicamento").value.trim();
    let laboratorio = document.getElementById("laboratorio").value.trim();
    let quantidade = document.getElementById("quantidade").value.trim();

    // Somente o medicamento é obrigatório
    if (!medicamento) {
        alert("Informe o nome do medicamento.");
        return;
    }

    // Campos opcionais
    if (laboratorio === "") {
        laboratorio = "-";
    }

    if (quantidade === "") {
        quantidade = "-";
    }

    medicamentos.push({
        medicamento,
        laboratorio,
        quantidade
    });

    atualizarLista();

    document.getElementById("medicamento").value = "";
    document.getElementById("laboratorio").value = "";
    document.getElementById("quantidade").value = "";

    document.getElementById("medicamento").focus();

});

function atualizarLista() {

    const lista = document.getElementById("listaMedicamentos");

    lista.innerHTML = "";

    medicamentos.forEach((item, index) => {

        lista.innerHTML += `
            <div class="table-row">
                <div>${item.medicamento}</div>
                <div>${item.laboratorio}</div>
                <div>${item.quantidade}</div>

                <button
                    type="button"
                    onclick="removerMedicamento(${index})">

                    <i class="bi bi-trash"></i>

                </button>

                <input type="hidden" name="medicamento[]" value="${item.medicamento}">
                <input type="hidden" name="laboratorio[]" value="${item.laboratorio}">
                <input type="hidden" name="quantidade[]" value="${item.quantidade}">
            </div>
        `;

    });

}

function removerMedicamento(indice) {

    medicamentos.splice(indice, 1);

    atualizarLista();

}