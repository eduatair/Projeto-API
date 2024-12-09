async function consultarCliente() {
    const cpf = document.getElementById("cpf-consulta").value;
    const response = await fetch(`/consulta?cpf=${cpf}`);
    const result = document.getElementById("resultado-consulta");

    if (response.ok) {
        const cliente = await response.json();
        result.innerHTML = `Nome: ${cliente.nome}<br>Data de Nascimento: ${cliente.data_de_nascimento}<br>E-mail: ${cliente.email}`;
    } else {
        result.innerHTML = "Cliente não encontrado";
    }
}

async function cadastrarCliente() {
    const cpf = document.getElementById("cpf").value;
    const nome = document.getElementById("nome").value;
    const data_de_nascimento = document.getElementById("data_de_nascimento").value;
    const email = document.getElementById("email").value;

    const novoCliente = { cpf, nome, data_de_nascimento, email };
    const response = await fetch("/cadastro", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(novoCliente)
    });

    const result = document.getElementById("resultado-cadastro");
    if (response.ok) {
        result.innerHTML = "Cliente cadastrado com sucesso!";
    } else {
        const error = await response.json();
        result.innerHTML = error.error;
    }
}
