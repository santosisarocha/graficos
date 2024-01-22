
function renderiza_depesas_mensal() {
  const labels = ['moda da casa', 'de bem com a vida', 'grill', 'receita do chefe'];
  const data = {
    labels: labels,
    datasets: [{
      label: 'fila do restaurante',
      data: [20, 10, 30, 10],
      fill: false,
      backgroundColor: [
        'rgba(255, 149, 89)',
        'rgba(255, 248, 89)',
        'rgba(255, 87, 87)',
        'rgba(255, 248, 89)',
      ],
      borderColor: [
        'rgb(255, 189, 89)',
        'rgb(255, 248, 89)',
        'rgb(255, 87, 87)',
        'rgb(255, 248, 89)',
      ],
      borderWidth: 1
    }]
  };

  const ctxDespesasMensal = document.getElementById('despesas_mensal').getContext('2d');
  
  // Define as dimensões do canvas (opcional, dependendo do seu layout)
  ctxDespesasMensal.canvas.width = 30;
  ctxDespesasMensal.canvas.height = 10;

  

  // Cria um novo gráfico
  window.myChartDespesasMensal = new Chart(ctxDespesasMensal, {
    type: 'bar',
    data: data
  });
}


function renderiza_quantidade_de_pessoas() {
  const labels = ['moda da casa', 'de bem com a vida', 'grill', 'receita do chefe'];
  const data = {
    labels: labels,
    datasets: [{
      label: 'queridos da semana ',
      data: [20, 10, 25, 10],
      fill: false,
      backgroundColor: [
        'rgba(248, 149, 105)',
        'rgba(242, 101, 110)',
        'rgba(255, 87, 87)',
        'rgba(255, 189, 89)',
      ],
      borderColor: [
        'rgb(248, 149, 105)',
        'rgb(242, 101, 110)',
        'rgb(255, 87, 87)',
        'rgb(255, 189, 89)',
      ],
      hoverOffset: 4
    }]
  };

  const ctxQuantidade = document.getElementById('quantidade_de_pessoas').getContext('2d');
  
  // Define as dimensões do canvas
  ctxQuantidade.canvas.width = 400;
  ctxQuantidade.canvas.height = 409;

  
  
  // Cria um novo gráfico desativando a responsividade
  window.myChartQuantidade = new Chart(ctxQuantidade, {
    type: 'pie',
    data: data,
    options: {
      responsive: false, // Desativa a responsividade
      maintainAspectRatio: false,
    }
  });
}




function renderiza_movimentacao_pessoas() {
  const labels = ["11:10", "11:20", "11:30", "11:40", "11:50", "12:00"];
  const data = {
    labels: labels,
    datasets: [{
      label: 'Quantidade de pessoas a cada 10 minutos:',
      data: [2, 10, 8, 6, 12, 4],
      fill: false,
      backgroundColor: [
        'rgba(255, 189, 89)',
        'rgba(255, 87, 87)',
        'rgba(248, 149, 105)',
        'rgba(248, 149, 105)',
        'rgba(255, 87, 87)',
        'rgba(255, 189, 89)',
      ],
      borderColor: [
        'rgb(255, 189, 89)',
        'rgb(255, 248, 89)',
        'rgb(255, 87, 87)',
        'rgb(255, 248, 89)',
        'rgb(255, 248, 89)',
        'rgb(255, 248, 89)',
      ],
      borderWidth: 1
    }]
  };

  const ctxMovimentacaoPessoas = document.getElementById('movimentacao_pessoas').getContext('2d');
  const myChartMovimentacaoPessoas = new Chart(ctxMovimentacaoPessoas, {
    type: 'bar',
    data: data,
    options: {
      responsive: true,
      maintainAspectRatio: false,
      aspectRatio: 1
    }
  });
}

// Adiciona lógica do botão de envio
$("#btnEnvia").click(function () {
  var option = $("input[type=radio][name=opt]:checked").val();
  console.log("Opção escolhida: " + option);

  // Enviar dados para o servidor Django
  $.ajax({
    type: 'POST',
    url: '/enquete/salvar_resultado_enquete/',
    contentType: 'application/json',
    data: JSON.stringify({ option: option }),
    success: function (response) {
      console.log('Dados da enquete enviados com sucesso!');

      // Atualiza o gráfico da quantidade de pessoas
      atualizarGraficoEnquete(response);
    },
    error: function (error) {
      console.error('Erro ao enviar dados da enquete:', error);
    }
  });
});
window.onload = function (event) {
  renderiza_depesas_mensal();
  renderiza_quantidade_de_pessoas();  
  renderiza_movimentacao_pessoas();
};
// Função para atualizar o gráfico da quantidade de pessoas com dados da enquete
function atualizarGraficoEnquete(response) {
  var total = response.total;
  var per_modaCasa = (response.modaCasa * 100) / total;
  var per_bemVida = (response.bemVida * 100) / total;
  var per_grill = (response.grill * 100) / total;
  var per_receitaChefe = (response.receitaChefe * 100) / total;

  // Atualiza a porcentagem do gráfico localmente
  window.myChartQuantidade.data.datasets[0].data = [per_modaCasa, per_bemVida, per_grill, per_receitaChefe];
  window.myChartQuantidade.update();
}



