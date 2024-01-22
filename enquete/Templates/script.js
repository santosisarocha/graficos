$(document).ready(function () {
    $("#btnEnvia").click(function () {
        var option = $("input[type=radio][name=opt]:checked").val();
        console.log("Opção escolhida: " + option);

        // Recuperar os resultados salvos no armazenamento local
        var savedResults = JSON.parse(localStorage.getItem('enqueteResults')) || {
            bemVida: 0,
            grill: 0,
            modaCasa: 0,
            receitaChefe: 0,
            total: 0
        };

        // Atualizar os resultados
        savedResults[option]++;
        savedResults.total++;

        // Salvar os resultados de volta no armazenamento local
        localStorage.setItem('enqueteResults', JSON.stringify(savedResults));

        // Restante do seu código...

        // Calcular as porcentagens locais (exemplo)
        var total = savedResults.total;
        var per_bemVida = (savedResults.bemVida * 100) / total;
        var per_grill = (savedResults.grill * 100) / total;
        var per_modaCasa = (savedResults.modaCasa * 100) / total;
        var per_receitaChefe = (savedResults.receitaChefe * 100) / total;

        // Atualizar a barra de progresso localmente (exemplo)
        $("#bemVida_bar").css("width", per_bemVida + "%");
        $("#grill_bar").css("width", per_grill + "%");
        $("#modaCasa_bar").css("width", per_modaCasa + "%");
        $("#receitaChefe_bar").css("width", per_receitaChefe + "%");
    });
});
