from flask import Flask, jsonify, request
import requests
import threading

app = Flask(__name__)

# Lista de sensores e solicitações
contas = []

lock = threading.Lock()

# Rotas para sensores
@app.route('/contas', methods=['GET'])
def get_contas():
    with lock:
        return jsonify(contas)

@app.route('/contas/<int:conta_id>', methods=['GET'])
def get_conta(conta_id):
    with lock:
        conta = next((conta for conta in contas if conta['id'] == conta_id), None)
        if conta:
            return jsonify(conta)
        return jsonify({'message': 'Conta não encontrada'}), 404

@app.route('/contas', methods=['POST'])
def criar_conta():
    with lock:
        nova_conta = request.json
        contas.append(nova_conta)
        return jsonify(nova_conta), 201

@app.route('/contas/<int:conta_id>', methods=['PUT'])
def atualizar_conta(conta_id):
    with lock:
        conta = next((conta for conta in contas if conta['id'] == conta_id), None)
        if not conta:
            return jsonify({'message': 'Conta não encontrada'}), 404
        dados_atualizados = request.json
        conta.update(dados_atualizados)
        return jsonify(conta)

@app.route('/contas/<int:conta_id>', methods=['DELETE'])
def excluir_conta(conta_id):
    with lock:
        global contas
        contas = [conta for conta in contas if conta['id'] != conta_id]
        return jsonify({'message': 'Conta excluída com sucesso'})

@app.route('/saques', methods=['POST'])
def criar_saque():
    with lock:
        novo_saque = request.get_json()
        for item in contas:
            if item["id"] == novo_saque["id"]:
                if item["Saldo"] >= novo_saque["Valor"]:
                    item["Saldo"] = item["Saldo"] - novo_saque["Valor"]
                else:
                    print("Saldo insuficiente! ")
        return jsonify(novo_saque), 201

@app.route('/depositos', methods=['POST'])
def criar_depositos():
    with lock:
        novo_deposito = request.get_json()
        for item in contas:
            if item["id"] == novo_deposito["id"]:
                item["Saldo"] = item["Saldo"] + novo_deposito["Valor"]
        return jsonify(novo_deposito), 201

@app.route('/receber', methods=['POST'])
def receber_transferencia():
    with lock:
        transferencia = request.get_json()
        for item in contas:
            if item["id"] == transferencia["id"]:
                item['Saldo'] += transferencia['Valor']
                return jsonify(transferencia), 201
        return jsonify({'message': 'Conta não encontrada'}), 404

@app.route('/transferir', methods=['POST'])
def fazer_transferencia():
        nova_transferencia = request.get_json()
        url_destino = f"http://192.168.1.10{str(nova_transferencia["id_destino"])[5]}:8081/receber"
        print(url_destino)
        with lock:
            for item in contas:
                if item["id"] == nova_transferencia["id_origem"]:
                    if item["Saldo"] < nova_transferencia["Valor"]:
                        return jsonify({'message': 'Saldo insuficiente na conta de origem'}), 400
                
        try:
            with lock:
                # Deduz o saldo do remetente localmente
                for item in contas:
                    if item["id"] == int(nova_transferencia["id_origem"]):
                        item["Saldo"] -= nova_transferencia["Valor"]
            
            # Enviar solicitação para adicionar saldo ao destinatário
            transferencia = {
                "id": nova_transferencia['id_destino'],
                "Valor": nova_transferencia['Valor']
            }

            response = requests.post(url_destino, json=transferencia, timeout=1)

            if response.status_code != 201:
                with lock:
                    # Reverter dedução em caso de exceção
                    for item in contas:
                        if item["id"] == int(nova_transferencia["id_origem"]):
                            item['Saldo'] += nova_transferencia['Valor']
                    return jsonify({'message': 'Erro ao realizar transferência'}), 500
            elif response.status_code == 201:
                return "", 201
                    
        except Exception as e:
            with lock:
                # Reverter dedução em caso de exceção
                for item in contas:
                    if item["id"] == int(nova_transferencia["id_origem"]):
                        item['Saldo'] += nova_transferencia['Valor']
                return jsonify({'message': 'Erro ao realizar transferência'}), 500
            
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)

