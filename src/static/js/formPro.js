const form = document.getElementById("form");
const nome = document.getElementById("name");
const categoria = document.getElementById("category");
const email = document.getElementById("email");
const senha = document.getElementById("password");
const confirmacaoSenha = document.getElementById("confirmPassword");

form.addEventListener("submit", (event) => {
  //Verifica se os campos do formulario são validos
  if (!checkForm()) {
    //Se os campos não forem válidos, previne o envio padrão do formulário
    event.preventDefault();
  }
});

nome.addEventListener("blur", () => {
  checkInputName();
});
categoria.addEventListener("blur", () => {
  checkInputCategory();
});

email.addEventListener("blur", () => {
  checkInputEmail();
});
senha.addEventListener("blur", () => {
  checkInputPassword();
});
confirmacaoSenha.addEventListener("blur", () => {
  checkInputConfirmPassword();
});

// função para verificar se o campo nome foi preenchido
function checkInputName() {
  const NomeValue = nome.value.trim();

  if (NomeValue === "") {
    errorInput(nome, "Preencha um username!");
    return false;
  } else {
    clearError(nome);
    return true;
  }
}

// Função para verificar categoria
function checkInputCategory() {
  const categoriaValue = categoria.value.trim();

  if (categoriaValue === "") {
    errorInput(categoria, "Preencha uma categoria!");
    return false;
  } else {
    clearError(categoria);
    return true;
  }
}

// Função para validar um endereço de e-mail
function isValidEmail(emailValue) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(emailValue);
}

// Função para verificar se o campo de e-mail foi preenchido corretamente
function checkInputEmail() {
  const emailValue = email.value.trim();

  if (!isValidEmail(emailValue)) {
    errorInput(email, "Preencha um e-mail válido!");
    return false;
  } else {
    clearError(email);
    return true;
  }
}

// Função para verificar se o campo de senha foi preenchido
function checkInputPassword() {
  const senhaValue = senha.value.trim();

  if (senhaValue === "") {
    errorInput(senha, "Preencha uma senha!");
    return false;
  } else {
    clearError(senha);
    return true;
  }
}

// Função para verificar se o campo de confirmação de senha coincide com a senha
function checkInputConfirmPassword() {
  const confirmacaoSenhaValue = confirmacaoSenha.value.trim();
  const senhaValue = senha.value.trim();

  if (confirmacaoSenhaValue === "") {
    errorInput(confirmacaoSenha, "Confirme sua senha!");
  } else if (confirmacaoSenhaValue !== senhaValue) {
    errorInput(confirmacaoSenha, "As senhas não coincidem!");
    return false;
  } else {
    clearError(confirmacaoSenha);
    return true;
  }
}

// Função para verificar todo o formulário
function checkForm() {
  //verificar individualmente cada campo do formulário
  const isNameValid = checkInputName();
  const isCategoryValid = checkInputCategory();
  const isEmailValid = checkInputEmail();
  const isPasswordValid = checkInputPassword();
  const isConfirmPasswordValid = checkInputConfirmPassword();

  // Retorna true se todos os campos forem válidos, caso contrário, retorna false
  return (
    isNameValid &&
    isCategoryValid &&
    isEmailValid &&
    isPasswordValid &&
    isConfirmPasswordValid
  );
}

// Função para exibir uma mensagem de erro em um campo de entrada
function errorInput(input, message) {
  const formItem = input.parentElement;
  const textMessage = formItem.querySelector(".error-msg");

  textMessage.innerText = message;
  textMessage.style.display = "block";
}

// Função para limpar uma mensagem de erro em um campo de entrada
function clearError(input) {
  const formItem = input.parentElement;
  formItem.querySelector(".error-msg").style.display = "none";
}
