// Validação do Formulário
const form = document.getElementById("service-form");
const servico = document.getElementById("service");
const preco = document.getElementById("price");
const tempo = document.getElementById("time");
const descricao = document.getElementById("description");

servico.addEventListener("blur", () => {
  checkInputServico();
});

preco.addEventListener("blur", () => {
  checkInputPreco();
});

tempo.addEventListener("blur", () => {
  checkInputTempo();
});

descricao.addEventListener("blur", () => {
  checkInputDescricao();
});

//funçao para verificar o campo serviço
function checkInputServico() {
  const servicoValue = servico.value.trim();

  if (servicoValue === "") {
    errorInput(servico, "Preencha um serviço");
    return false;
  } else {
    clearError(servico);
    return true;
  }
}

function checkInputPreco() {
  const precoValue = preco.value.trim();

  if (precoValue === "") {
    errorInput(preco, "Insira um preço!");
    return false;
  } else if (isNaN(precoValue) || Number(precoValue) <= 0) {
    errorInput(preco, "Insira um preço válido!");
    return false;
  } else {
    clearError(preco);
    return true;
  }
}

function checkInputTempo() {
  const tempoValue = tempo.value.trim();

  if (tempoValue === "") {
    errorInput(tempo, "Insira um tempo estimado!");
    return false;
  } else {
    clearError(tempo);
    return true;
  }
}

function checkInputDescricao() {
  const descricaoValue = descricao.value.trim();

  if (descricaoValue === "") {
    errorInput(descricao, "Insira uma descrição!");
    return false;
  } else {
    clearError(descricao);
    return true;
  }
}

function checkForm() {
  const isServiçoValid = checkInputServico();
  const isPrecoValid = checkInputPreco();
  const isTempoValid = checkInputTempo();
  const isDescricaoValid = checkInputDescricao();

  return isServiçoValid && isPrecoValid && isTempoValid && isDescricaoValid;
}

function errorInput(input, message) {
  const formItem = input.parentElement;
  const textMessage = formItem.querySelector(".error-msg");

  textMessage.innerText = message;
  textMessage.style.display = "block";
}

function clearError(input) {
  const formItem = input.parentElement;
  formItem.querySelector(".error-msg").style.display = "none";
}

//Lista de Serviços

document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("service-form");
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    if (checkForm()) {
      const formData = new FormData(form);
      fetch("/services", {
        method: "POST",
        body: formData,
      })
        .then((response) => response.json())
        .then((data) => {
          if (!data.error) {
            fetchServices();
            form.reset();
          } else {
            alert(data.error);
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    }
  });

  function fetchServices() {
    fetch("/services")
      .then((response) => response.text())
      .then((html) => {
        const parser = new DOMParser();
        const doc = parser.parseFromString(html, "text/html");
        const newServicesList = doc.getElementById("services-list").innerHTML;
        document.getElementById("services-list").innerHTML = newServicesList;
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  }
});
