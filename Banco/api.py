from flask import Flask, jsonify, request

app = Flask(__name__)

# Lista de sensores e solicitações
contas = []
requisicoes = []

# Rotas para sensores
@app.route('/contas', methods=['GET'])
def get_clientes():
    return jsonify(contas)

@app.route('/contas/<int:conta_id>', methods=['GET'])
def get_conta(conta_id):
    conta = next((conta for conta in contas if conta['id'] == conta_id), None)
    if conta:
        return jsonify(conta)
    return jsonify({'message': 'Conta não encontrada'}), 404

@app.route('/contas', methods=['POST'])
def criar_conta():
    nova_conta = request.json
    contas.append(nova_conta)
    return jsonify(nova_conta), 201

@app.route('/contas/<int:conta_id>', methods=['PUT'])
def atualizar_conta(conta_id):
    conta = next((conta for conta in contas if conta['id'] == conta_id), None)
    if not conta:
        return jsonify({'message': 'Conta não encontrada'}), 404
    dados_atualizados = request.json
    conta.update(dados_atualizados)
    return jsonify(conta)

@app.route('/contas/<int:conta_id>', methods=['DELETE'])
def excluir_conta(conta_id):
    global contas
    contas = [conta for conta in contas if conta['id'] != conta_id]
    return jsonify({'message': 'Conta excluída com sucesso'})

# Rotas para sensores
@app.route('/requisicoes', methods=['GET'])
def get_requisicoes():
    return jsonify(requisicoes)

@app.route('/requisicoes/<int:requisicao_id>', methods=['GET'])
def get_requisicao(requisicao_id):
    requisicao = next((requisicao for requisicao in requisicoes if requisicao['id'] == requisicao_id), None)
    if requisicao:
        return jsonify(requisicao)
    return jsonify({'message': 'Requisição não encontrada'}), 404

@app.route('/requisicoes', methods=['POST'])
def criar_requisicao():
    nova_requisicao = request.json
    nova_requisicao['id'] = len(requisicoes) + 1
    requisicoes.append(nova_requisicao)
    return jsonify(nova_requisicao), 201

@app.route('/requisicoes/<int:requisicao_id>', methods=['PUT'])
def atualizar_requisicao(requisicao_id):
    requisicao = next((requisicao for requisicao in requisicoes if requisicao['id'] == requisicao_id), None)
    if not requisicao:
        return jsonify({'message': 'Requisições não encontrada'}), 404
    dados_atualizados = request.json
    requisicao.update(dados_atualizados)
    return jsonify(requisicao)

@app.route('/requisicoes/<int:requisicao_id>', methods=['DELETE'])
def excluir_requisicao(requisicao_id):
    global requisicoes
    requisicoes = [requisicao for requisicao in requisicoes if requisicao['id'] != requisicao_id]
    return jsonify({'message': 'Requisição excluída com sucesso'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)

