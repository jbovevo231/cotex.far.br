console.log("conecta.js carregado");

const foto = document.getElementById("foto");
const preview = document.getElementById("previewImagem");
const imagem = document.getElementById("imagemPreview");

if (foto) {

    foto.addEventListener("change", function () {

        console.log("Imagem selecionada");

        if (this.files.length === 0) return;

        const reader = new FileReader();

        reader.onload = function (e) {

            imagem.src = e.target.result;
            preview.style.display = "block";

        };

        reader.readAsDataURL(this.files[0]);

    });

}

function removerImagem() {

    foto.value = "";
    imagem.src = "";
    preview.style.display = "none";

}