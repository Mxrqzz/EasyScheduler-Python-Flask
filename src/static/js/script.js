// Função para rolar a página até o elemento com o ID definido
function scrollToDiv(id) {
  var element = document.getElementById(id);
  if (element) {
    element.scrollIntoView({ behavior: "smooth", block: "start" });
  }
}

// Função para verificar se o tipo de conta foi selecionado e redirecionar para a página de registro apropriada
function verificarRadio() {
  var clientChecked = document.getElementById("typeClient").checked;
  var proChecked = document.getElementById("typePro").checked;

  if (!clientChecked && !proChecked) {
    document.querySelector(".error-msg").style.display = "block";
    return true;
  } else {
    document.querySelector(".error-msg").style.display = "none";
    if (clientChecked) {
      //Redireciona para a pagina de registro do cliente
      window.location.href = "/formClient";
    } else if (proChecked) {
      //Redireciona para a pagina de registro do profissional
      window.location.href = "/formPro";
    }
    return true;
  }
}

// PAGINA PERFIL

//alterar dados do usuario
var edit = document.getElementById("edit-button");
var save = document.getElementById("save-button");
var cancel = document.getElementById("cancel-button");
var nomeInput = document.getElementById("name");
var sobrenomeInput = document.getElementById("lastname");
var upload = document.getElementById("upload-button");
var form = document.getElementById("update-form");

edit.addEventListener("click", function (event) {
  event.preventDefault();
  console.log("Botão Editar clicado");
  edit.style.display = "none";
  save.style.display = "inline";
  cancel.style.display = "inline";
  upload.style.display = "inline";
  nomeInput.removeAttribute("readonly");
  sobrenomeInput.removeAttribute("readonly");
});

save.addEventListener("click", function () {
  form.submit();
});

cancel.addEventListener("click", function (event) {
  event.preventDefault();
  save.style.display = "none";
  cancel.style.display = "none";
  edit.style.display = "inline";
  upload.style.display = "none";
  nomeInput.setAttribute("readonly", true);
  sobrenomeInput.setAttribute("readonly", true);
});

//alterar email e senha do usuario

// Edit Login Email
var editLogin = document.getElementById("login-edit-button");
var saveLogin = document.getElementById("login-save-button");
var cancelLogin = document.getElementById("login-cancel-button");
var phoneInput = document.getElementById("phone");
var emailInput = document.getElementById("email")
var formEmail = document.getElementById("login-edit-form");

editLogin.addEventListener("click", function (event) {
  event.preventDefault();
  editLogin.style.display = "none";
  saveLogin.style.display = "inline";
  cancelLogin.style.display = "inline";
  phoneInput.removeAttribute("readonly");
  emailInput.removeAttribute("readonly");
});

saveLogin.addEventListener("click", function () {
  formEmail.submit();
});

cancelLogin.addEventListener("click", function (event) {
  event.preventDefault();
  saveLogin.style.display = "none";
  cancelLogin.style.display = "none";
  editLogin.style.display = "inline";
  emailInput.setAttribute("readonly", true);
});

//tela horarios

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

function redirectToAgenda(type, id) {
  if (type === 'service') {
    window.location.href = `/agendamento?profissional_id=${id}`;
  } else if (type === 'professional') {
    window.location.href = `/agendamento?profissional_id=${id}`;
  }
}

document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("service-select").addEventListener("change", function () {
    var selectedOption = this.options[this.selectedIndex];
    var preco = selectedOption.getAttribute("data-preco");
    var tempo = selectedOption.getAttribute("data-tempo");

    document.getElementById("price-service").innerText = preco
      ? "R$ " + preco
      : "Selecione um serviço";
    document.getElementById("time-service").innerText = tempo
      ? tempo + " minutos"
      : "Selecione um serviço";
  });
});
