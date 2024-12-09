from flask import Flask, request, jsonify, render_template
import json
import os

app = Flask(__name__)  # Cria uma instância da aplicação Flask

# Caminho para o arquivo JSON de clientes
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Obtém o diretório base do arquivo atual
CLIENTES_JSON_PATH = os.path.join(BASE_DIR, "data", "clientes.json")  # Define o caminho completo para o arquivo JSON

# Carrega os dados do JSON
def load_clientes():
    """Lê e retorna os dados do arquivo JSON de clientes."""
    with open(CLIENTES_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Salva os dados no JSON
def save_clientes(clientes):
    """Salva os dados fornecidos no arquivo JSON."""
    with open(CLIENTES_JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(clientes, f, ensure_ascii=False, indent=4)  # Salva com indentação e suporte a UTF-8

# Rota para exibir a página HTML principal
@app.route("/")
def index():
    
    """Renderiza a página inicial (HTML)."""
    return render_template("index.html")

# Rota GET para consulta de cliente por CPF
@app.route("/consulta", methods=["GET"])
def consulta_cliente():
    """
    Busca informações de um cliente pelo CPF.
    Exemplo de uso: /consulta?cpf=12345678900
    """
    cpf = request.args.get("cpf")  # Obtém o CPF da query string
    clientes = load_clientes()  # Carrega os clientes do arquivo JSON

    # Busca o cliente com o CPF correspondente
    cliente = next((c for c in clientes if c["cpf"] == cpf), None)
    if cliente:
        return jsonify(cliente)  # Retorna os dados do cliente em formato JSON
    else:
        return jsonify({"error": "Cliente não encontrado"}), 404  # Retorna erro caso o cliente não exista

# Rota POST para cadastro de novos clientes
@app.route("/cadastro", methods=["POST"])
def cadastro_cliente():
    """
    Cadastra um novo cliente.
    Requer JSON com os campos: nome, cpf, e outros dados.
    """
    novo_cliente = request.json  # Obtém os dados do cliente enviados no corpo da requisição
    clientes = load_clientes()  # Carrega os clientes existentes

    # Verifica se o CPF já está cadastrado
    if any(c["cpf"] == novo_cliente["cpf"] for c in clientes):
        return jsonify({"error": "CPF já cadastrado"}), 409

    # Adiciona o novo cliente à lista e ordena por nome
    clientes.append(novo_cliente)
    clientes.sort(key=lambda c: c["nome"])  # Ordena a lista pelo campo "nome"
    save_clientes(clientes)  # Salva os dados atualizados no arquivo JSON

    return jsonify({"message": "Cliente cadastrado com sucesso"}), 201  # Retorna mensagem de sucesso

if __name__ == "__main__":
    app.run(debug=True)  # Executa o servidor Flask no modo de depuração
