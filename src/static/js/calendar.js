document.addEventListener("DOMContentLoaded", function () {
  var calendarEl = document.getElementById("calendar");
  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: "dayGridMonth",
    events: "/events",
  });
  calendar.render();
});

function updateTime() {
  const timeElement = document.getElementById("digital-clock");
  const now = new Date();
  const day = now.getDate().toString().padStart(2, "0");
  const month = (now.getMonth() + 1).toString().padStart(2, "0");
  const year = now.getFullYear().toString();
  const hours = now.getHours().toString().padStart(2, "0");
  const minutes = now.getMinutes().toString().padStart(2, "0");
  const seconds = now.getSeconds().toString().padStart(2, "0");

  const dateString = `${day}/${month}/${year}`;
  const timeString = `${hours}:${minutes}:${seconds}`;

  // Criar linhas separadas para data e hora
  const dateLine = `<div>${dateString}</div>`;
  const timeLine = `<div>${timeString}</div>`;

  // Atualizar o conteúdo do elemento HTML com as duas linhas
  timeElement.innerHTML = `${dateLine}${timeLine}`;
}

// Atualiza a cada segundo
setInterval(updateTime, 1000);

// Chama a função para exibir o tempo atual imediatamente
updateTime();

document.getElementById("add-service").addEventListener("click", function () {
  document.getElementById("formulario").style.display = "block";
});

document
  .getElementById("formulario-servico")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Para prevenir o envio do formulário

    // Aqui você pode adicionar código para processar os dados do formulário
    // Por exemplo, você pode enviar os dados para o servidor ou adicionar a um array localmente

    // Resetar o formulário e esconder o formulário
    document.getElementById("formulario-servico").reset();
    document.getElementById("formulario").style.display = "none";
  });
