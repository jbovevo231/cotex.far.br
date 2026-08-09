document.addEventListener("DOMContentLoaded", function () {

    console.log("Conecta JS carregado!");


    /* =================================================
       ELEMENTOS
    ================================================= */

    const botaoOportunidade =
        document.getElementById("btn-oportunidade");

    const botaoReceita =
        document.getElementById("btn-receita");

    const botaoEnquete =
        document.getElementById("btn-enquete");

    const tipoPublicacao =
        document.getElementById("tipo-publicacao");

    const enqueteBox =
        document.getElementById("enquete-box");


    /* =================================================
       FOTO
    ================================================= */

    const inputFoto =
        document.getElementById("input-foto");

    const previewFoto =
        document.getElementById("preview-foto");

    const previewFotoImg =
        document.getElementById("preview-foto-img");

    const removerFoto =
        document.getElementById("remover-foto");

    console.log("INPUT FOTO:", inputFoto);
console.log("PREVIEW:", previewFoto);
console.log("IMAGEM PREVIEW:", previewFotoImg);
console.log("BOTÃO REMOVER:", removerFoto);


    /* =================================================
       PRÉ-VISUALIZAÇÃO DA FOTO
    ================================================= */

    if (
        inputFoto &&
        previewFoto &&
        previewFotoImg
    ) {

        inputFoto.addEventListener(
            "change",
            function () {

                const arquivo =
                    this.files[0];


                console.log(
                    "ARQUIVO SELECIONADO:",
                    arquivo
                );


                if (!arquivo) {

                    previewFoto.style.display =
                        "none";

                    previewFotoImg.src = "";

                    return;
                }


                if (
                    !arquivo.type.startsWith(
                        "image/"
                    )
                ) {

                    alert(
                        "Selecione uma imagem válida."
                    );

                    this.value = "";

                    previewFoto.style.display =
                        "none";

                    return;
                }


                const leitor =
                    new FileReader();


                leitor.onload =
                    function (evento) {

                        previewFotoImg.src =
                            evento.target.result;

                        previewFoto.style.display =
                            "block";

                    };


                leitor.readAsDataURL(
                    arquivo
                );

            }
        );

    }


    /* =================================================
       REMOVER FOTO
    ================================================= */

    if (removerFoto) {

        removerFoto.addEventListener(
            "click",
            function () {

                if (inputFoto) {

                    inputFoto.value = "";

                }


                if (previewFotoImg) {

                    previewFotoImg.src = "";

                }


                if (previewFoto) {

                    previewFoto.style.display =
                        "none";

                }

            }
        );

    }

    /* =================================================
   PRÉ-VISUALIZAÇÃO DA FOTO
================================================= */

if (inputFoto) {

    inputFoto.addEventListener("change", function () {

        const arquivo = inputFoto.files[0];

        console.log("FOTO:", arquivo);


        if (!arquivo) {

            if (previewFoto) {
                previewFoto.style.display = "none";
            }

            if (previewFotoImg) {
                previewFotoImg.removeAttribute("src");
            }

            return;
        }


        if (!arquivo.type.startsWith("image/")) {

            alert("Selecione uma imagem válida.");

            inputFoto.value = "";

            return;
        }


        const url =
            URL.createObjectURL(arquivo);


        if (previewFotoImg) {

            previewFotoImg.src = url;

        }


        if (previewFoto) {

            previewFoto.style.display = "block";

        }

    });

}

    /* =================================================
       VERIFICA TIPO
    ================================================= */

    if (!tipoPublicacao) {

        console.error(
            "Campo tipo-publicacao não encontrado."
        );

        return;
    }


    /* =================================================
       LIMPAR SELEÇÕES
    ================================================= */

    function limparSelecoes() {

        if (botaoOportunidade) {

            botaoOportunidade.classList.remove(
                "selecionado"
            );

        }


        if (botaoReceita) {

            botaoReceita.classList.remove(
                "selecionado"
            );

        }


        if (botaoEnquete) {

            botaoEnquete.classList.remove(
                "selecionado"
            );

        }


        if (enqueteBox) {

            enqueteBox.style.display =
                "none";

        }

    }


    /* =================================================
       OPORTUNIDADE
    ================================================= */

    if (botaoOportunidade) {

        botaoOportunidade.addEventListener(
            "click",
            function () {

                if (
                    tipoPublicacao.value ===
                    "oportunidade"
                ) {

                    tipoPublicacao.value =
                        "normal";

                    botaoOportunidade.classList.remove(
                        "selecionado"
                    );

                } else {

                    limparSelecoes();

                    tipoPublicacao.value =
                        "oportunidade";

                    botaoOportunidade.classList.add(
                        "selecionado"
                    );

                }


                console.log(
                    "TIPO:",
                    tipoPublicacao.value
                );

            }
        );

    }


    /* =================================================
       DÚVIDA DE RECEITA
    ================================================= */

    if (botaoReceita) {

        botaoReceita.addEventListener(
            "click",
            function () {

                if (
                    tipoPublicacao.value ===
                    "duvida_receita"
                ) {

                    tipoPublicacao.value =
                        "normal";

                    botaoReceita.classList.remove(
                        "selecionado"
                    );

                } else {

                    limparSelecoes();

                    tipoPublicacao.value =
                        "duvida_receita";

                    botaoReceita.classList.add(
                        "selecionado"
                    );

                }


                console.log(
                    "TIPO:",
                    tipoPublicacao.value
                );

            }
        );

    }


    /* =================================================
       ENQUETE
    ================================================= */

    if (botaoEnquete) {

        botaoEnquete.addEventListener(
            "click",
            function () {

                if (
                    tipoPublicacao.value ===
                    "enquete"
                ) {

                    tipoPublicacao.value =
                        "normal";

                    botaoEnquete.classList.remove(
                        "selecionado"
                    );


                    if (enqueteBox) {

                        enqueteBox.style.display =
                            "none";

                    }

                } else {

                    limparSelecoes();

                    tipoPublicacao.value =
                        "enquete";

                    botaoEnquete.classList.add(
                        "selecionado"
                    );


                    if (enqueteBox) {

                        enqueteBox.style.display =
                            "block";

                    }

                }


                console.log(
                    "TIPO:",
                    tipoPublicacao.value
                );

            }
        );

    }


});

/* =====================================================
   FILTROS DAS ABAS DO CONECTA
===================================================== */

document.addEventListener("DOMContentLoaded", function () {

    const tabs =
        document.querySelectorAll(
            ".conecta-tabs a[data-filtro]"
        );

    const posts =
        document.querySelectorAll(
            ".post-card[data-tipo]"
        );


    console.log(
        "ABAS COM FILTRO:",
        tabs.length
    );

    console.log(
        "POSTS:",
        posts.length
    );


    tabs.forEach(function (tab) {

        tab.addEventListener(
            "click",
            function (evento) {

                evento.preventDefault();


                const filtro =
                    tab.getAttribute(
                        "data-filtro"
                    );


                console.log(
                    "FILTRO CLICADO:",
                    filtro
                );


                /* =====================================
                   ATIVA A ABA
                ===================================== */

                tabs.forEach(function (t) {

                    t.classList.remove(
                        "active"
                    );

                });


                tab.classList.add(
                    "active"
                );


                /* =====================================
                   FILTRA PUBLICAÇÕES
                ===================================== */

                posts.forEach(function (post) {

                    const tipo =
                        post.getAttribute(
                            "data-tipo"
                        ) || "normal";


                    console.log(
                        "POST:",
                        tipo
                    );


                    /* =================================
                       INÍCIO
                    ================================= */

                    if (
                        filtro === "todos"
                    ) {

                        post.style.display = "";

                    }


                    /* =================================
                       DISCUSSÕES

                       MOSTRA:
                       normal
                       duvida_receita

                       ESCONDE:
                       oportunidade
                       enquete
                    ================================= */

                    else if (
                        filtro === "discussoes"
                    ) {

                        if (
                            tipo === "normal" ||
                            tipo === "duvida_receita"
                        ) {

                            post.style.display = "";

                        } else {

                            post.style.display =
                                "none";

                        }

                    }


                    /* =================================
                       OPORTUNIDADES
                    ================================= */

                    else if (
                        filtro === "oportunidade"
                    ) {

                        if (
                            tipo === "oportunidade"
                        ) {

                            post.style.display = "";

                        } else {

                            post.style.display =
                                "none";

                        }

                    }

                });

            }
        );

    });

});