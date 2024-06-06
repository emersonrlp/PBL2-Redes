from flask import Flask, jsonify, request
import threading
import requests

app = Flask(__name__)

# Estrutura de dados para armazenar clientes e suas contas
clientes = []
lock = threading.Lock()

# Função auxiliar para encontrar um cliente por ID
def find_cliente(cliente_id):
    return next((cliente for cliente in clientes if cliente['id'] == cliente_id), None)

# Função auxiliar para encontrar uma conta por ID dentro de um cliente
def find_conta(cliente, conta_id):
    return next((conta for conta in cliente['contas'] if conta['id'] == conta_id), None)

# Rotas para clientes
@app.route('/clientes', methods=['GET'])
def get_clientes():
    with lock:
        clientes_sem_senha = [cliente.copy() for cliente in clientes]
        for cliente in clientes_sem_senha:
            del cliente['senha']
        return jsonify(clientes_sem_senha)

@app.route('/clientes/<int:cliente_id>', methods=['GET'])
def get_cliente(cliente_id):
    with lock:
        cliente = find_cliente(cliente_id)
        if cliente:
            cliente_sem_senha = cliente.copy()
            del cliente_sem_senha['senha']
            return jsonify(cliente_sem_senha)
        return jsonify({'message': 'Cliente não encontrado'}), 404

@app.route('/clientes', methods=['POST'])
def criar_cliente():
    novo_cliente = request.json
    required_fields = ['id', 'nome', 'idade', 'senha']
    
    for field in required_fields:
        if field not in novo_cliente:
            return jsonify({'message': f'Campo obrigatório {field} está faltando'}), 400

    with lock:
        if find_cliente(novo_cliente['id']):
            return jsonify({'message': 'Cliente com este ID já existe'}), 400
        novo_cliente['contas'] = []
        clientes.append(novo_cliente)
        cliente_sem_senha = novo_cliente.copy()
        del cliente_sem_senha['senha']
        return jsonify(cliente_sem_senha), 201

@app.route('/clientes/<int:cliente_id>', methods=['DELETE'])
def excluir_cliente(cliente_id):
    with lock:
        cliente = find_cliente(cliente_id)
        if cliente:
            clientes.remove(cliente)
            return jsonify({'message': 'Cliente excluído com sucesso'})
        return jsonify({'message': 'Cliente não encontrado'}), 404

# Rotas para contas dentro de um cliente específico
@app.route('/clientes/<int:cliente_id>/contas', methods=['GET'])
def get_contas(cliente_id):
    with lock:
        cliente = find_cliente(cliente_id)
        if cliente:
            return jsonify(cliente['contas'])
        return jsonify({'message': 'Cliente não encontrado'}), 404

@app.route('/clientes/<int:cliente_id>/contas/<int:conta_id>', methods=['GET'])
def get_conta(cliente_id, conta_id):
    with lock:
        cliente = find_cliente(cliente_id)
        if cliente:
            conta = find_conta(cliente, conta_id)
            if conta:
                return jsonify(conta)
            return jsonify({'message': 'Conta não encontrada'}), 404
        return jsonify({'message': 'Cliente não encontrado'}), 404

@app.route('/clientes/<int:cliente_id>/contas', methods=['POST'])
def criar_conta(cliente_id):
    nova_conta = request.json
    required_fields = ['id', 'saldo']
    
    for field in required_fields:
        if field not in nova_conta:
            return jsonify({'message': f'Campo obrigatório {field} está faltando'}), 400

    with lock:
        cliente = find_cliente(cliente_id)
        if cliente:
            if find_conta(cliente, nova_conta['id']):
                return jsonify({'message': 'Conta com este ID já existe para o cliente'}), 400
            cliente['contas'].append(nova_conta)
            return jsonify(nova_conta), 201
        return jsonify({'message': 'Cliente não encontrado'}), 404

@app.route('/clientes/<int:cliente_id>/contas/<int:conta_id>', methods=['PUT'])
def atualizar_conta(cliente_id, conta_id):
    dados_atualizados = request.json
    with lock:
        cliente = find_cliente(cliente_id)
        if cliente:
            conta = find_conta(cliente, conta_id)
            if conta:
                conta.update(dados_atualizados)
                return jsonify(conta)
            return jsonify({'message': 'Conta não encontrada'}), 404
        return jsonify({'message': 'Cliente não encontrado'}), 404

@app.route('/clientes/<int:cliente_id>/contas/<int:conta_id>', methods=['DELETE'])
def excluir_conta(cliente_id, conta_id):
    with lock:
        cliente = find_cliente(cliente_id)
        if cliente:
            cliente['contas'] = [conta for conta in cliente['contas'] if conta['id'] != conta_id]
            return jsonify({'message': 'Conta excluída com sucesso'})
        return jsonify({'message': 'Cliente não encontrado'}), 404

# Endpoint para depositar em uma conta
@app.route('/clientes/<int:cliente_id>/contas/<int:conta_id>/depositar', methods=['POST'])
def depositar(cliente_id, conta_id):
    valor_deposito = request.json.get('valor')
    
    if valor_deposito is None:
        return jsonify({'message': 'Campo obrigatório valor está faltando'}), 400

    if valor_deposito <= 0:
        return jsonify({'message': 'Valor de depósito deve ser maior que zero'}), 400

    with lock:
        cliente = find_cliente(cliente_id)
        if cliente:
            conta = find_conta(cliente, conta_id)
            if conta:
                conta['saldo'] += valor_deposito
                return jsonify(conta)
            return jsonify({'message': 'Conta não encontrada'}), 404
        return jsonify({'message': 'Cliente não encontrado'}), 404

# Endpoint para depositar em uma conta
@app.route('/clientes/<int:cliente_id>/contas/<int:conta_id>/sacar', methods=['POST'])
def sacar(cliente_id, conta_id):
    valor_saque = request.json.get('valor')
    
    if valor_saque is None:
        return jsonify({'message': 'Campo obrigatório valor está faltando'}), 400

    with lock:
        cliente = find_cliente(cliente_id)
        if cliente:
            conta = find_conta(cliente, conta_id)
            if conta:
                if conta['saldo'] >= valor_saque:
                    conta['saldo'] -= valor_saque
                    return jsonify(conta)
                else:
                    return jsonify({'message': 'Saldo insuficiente'}), 404
            return jsonify({'message': 'Conta não encontrada'}), 404
        return jsonify({'message': 'Cliente não encontrado'}), 404
    
# Endpoint para login
@app.route('/login', methods=['POST'])
def login():
    dados_login = request.json
    cliente_id = dados_login.get('id')
    senha = dados_login.get('senha')

    if not cliente_id or not senha:
        return jsonify({'message': 'ID e senha são obrigatórios'}), 400

    with lock:
        cliente = find_cliente(cliente_id)
        if cliente and cliente['senha'] == senha:
            cliente_sem_senha = cliente.copy()
            del cliente_sem_senha['senha']
            return jsonify({'message': 'Login bem-sucedido', 'cliente': cliente_sem_senha})
        return jsonify({'message': 'ID ou senha incorretos'}), 401

@app.route('/receber', methods=['POST'])
def receber_transferencia():
    with lock:
        transferencia = request.get_json()
        for item in clientes:
            if item["id"] == transferencia["id"]:
                item['contas'][0]["saldo"] += transferencia['valor']
                return jsonify(transferencia), 201
        return jsonify({'message': 'Conta não encontrada'}), 404

@app.route('/transferir', methods=['POST'])
def fazer_transferencia():
        nova_transferencia = request.get_json()
        url_destino = f"http://192.168.1.10{str(nova_transferencia["id_destino"])[5]}:8081/receber"

        with lock:
            for item in clientes:
                if item["id"] == nova_transferencia["id_origem"]:
                    if item["contas"][0]["saldo"] < nova_transferencia["valor"]:
                        return jsonify({'message': 'Saldo insuficiente na conta de origem'}), 400
                
        try:
            with lock:
                # Deduz o saldo do remetente localmente
                for item in clientes:
                    if item["id"] == int(nova_transferencia["id_origem"]):
                        item["contas"][0]["saldo"] -= nova_transferencia["valor"]
            
            # Enviar solicitação para adicionar saldo ao destinatário
            transferencia = {
                "id": nova_transferencia['id_destino'],
                "valor": nova_transferencia['valor']
            }

            response = requests.post(url_destino, json=transferencia, timeout=1)

            if response.status_code != 201:
                with lock:
                    # Reverter dedução em caso de exceção
                    for item in clientes:
                        if item["id"] == int(nova_transferencia["id_origem"]):
                            item['Saldo'][0]["saldo"] += nova_transferencia['valor']
                    return jsonify({'message': 'Erro ao realizar transferência'}), 500
            elif response.status_code == 201:
                return "", 201
                    
        except Exception as e:
            with lock:
                # Reverter dedução em caso de exceção
                for item in clientes:
                    if item["id"] == int(nova_transferencia["id_origem"]):
                        item['contas'][0]["saldo"] += nova_transferencia['valor']
                return jsonify({'message': 'Erro ao realizar transferência'}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8081, debug=True)
