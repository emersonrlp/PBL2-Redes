from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista de sensores e solicitações
clientes = []
solicitacoes = []

# Rotas para sensores
@app.route('/clientes', methods=['GET'])
def get_clientes():
    return jsonify(clientes)

@app.route('/clientes/<int:cliente_id>', methods=['GET'])
def get_cliente(cliente_id):
    cliente = next((cliente for cliente in clientes if cliente['id'] == cliente_id), None)
    if cliente:
        return jsonify(cliente)
    return jsonify({'message': 'Cliente não encontrado'}), 404

@app.route('/clientes', methods=['POST'])
def criar_cliente():
    novo_cliente = request.json
    novo_cliente['id'] = len(clientes) + 1
    clientes.append(novo_cliente)
    return jsonify(novo_cliente), 201

@app.route('/clientes/<int:cliente_id>', methods=['PUT'])
def atualizar_cliente(cliente_id):
    cliente = next((cliente for cliente in clientes if cliente['id'] == cliente_id), None)
    if not cliente:
        return jsonify({'message': 'Cliente não encontrado'}), 404
    dados_atualizados = request.json
    cliente.update(dados_atualizados)
    return jsonify(cliente)

@app.route('/clientes/<int:cliente_id>', methods=['DELETE'])
def excluir_cliente(cliente_id):
    global clientes
    clientes = [cliente for cliente in clientes if cliente['id'] != cliente_id]
    return jsonify({'message': 'Cliente excluído com sucesso'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)

