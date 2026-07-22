console.log("dashboard.js carregado");

const medicamentos = [];

const btnAdicionar = document.getElementById("btnAdicionar");

btnAdicionar.addEventListener("click", function () {

    const medicamento = document.getElementById("medicamento").value.trim();
    const laboratorio = document.getElementById("laboratorio").value.trim();
    const quantidade = document.getElementById("quantidade").value.trim();

    if (!medicamento || !quantidade) {
        alert("Informe o medicamento e a quantidade.");
        return;
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