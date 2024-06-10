function showHours(day) {
  var checkbox = document.getElementById(day);
  var hoursBox = document.getElementById(day + "-hours");
  var status = document.getElementById("status-" + day);
  if (checkbox.checked) {
    hoursBox.style.display = "flex";
    status.style.display = "none";
  } else {
    hoursBox.style.display = "none";
    status.style.display = "block";
  }
}

function addTime(day) {
  var hoursBox = document.getElementById(day + "-hours");
  var horasDiv = hoursBox.getElementsByClassName("horas")[0]; // Obtém a primeira div com a classe "horas"

  var newTimeRow = document.createElement("div"); // Criar a nova div interna para o conjunto de inputs e botão
  newTimeRow.classList.add("hours-box");
  newTimeRow.innerHTML = `
      <h4>De</h4>
      <input type="time" />
      <h4>Até</h4>
      <input type="time" />
      <button type="button" class="button" onclick="removeTime(this)">Remover</button>
    `;

  horasDiv.appendChild(newTimeRow); // Adicionar a nova div dentro da div "horas"
}

function removeTime(button) {
  var timeRow = button.parentNode;
  timeRow.parentNode.removeChild(timeRow);
}
