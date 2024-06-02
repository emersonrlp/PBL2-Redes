from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Lista de sensores e solicitações
contas = []

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

@app.route('/saques', methods=['POST'])
def criar_saque():
    novo_saque = request.get_json()
    for item in contas:
        if item["id"] == novo_saque["id"]:
            item["Saldo"] = item["Saldo"] - novo_saque["Valor"]
    return jsonify(novo_saque), 201

@app.route('/depositos', methods=['POST'])
def criar_depositos():
    novo_deposito = request.get_json()
    for item in contas:
        if item["id"] == novo_deposito["id"]:
            item["Saldo"] = item["Saldo"] + novo_deposito["Valor"]
    return jsonify(novo_deposito), 201

@app.route('/transferencias', methods=['POST'])
def criar_transferencia():
    nova_transferencia = request.get_json()
    for item in contas:
        if item["id"] == nova_transferencia["id"]:
            item["Saldo"] = item["Saldo"] + nova_transferencia["Valor"]
            saque = {"id": int(nova_transferencia["id_remetente"]), "Valor": nova_transferencia["Valor"]}
            try:
                # Enviar uma solicitação POST para a API Flask para criar depositar
                url_saques = f"http://192.168.1.10{nova_transferencia["id_remetente"][5]}:8081/saques"
                response = requests.post(url_saques, json=saque, timeout=1)
            except Exception as e:
                print("", e)
    return jsonify(nova_transferencia), 201

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)

