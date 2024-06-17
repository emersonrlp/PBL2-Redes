from flask import Flask, request, jsonify
import requests
import threading
import time
import socket

app = Flask(__name__)

# Configurações da rede - altere estes IPs para os IPs das suas máquinas
ips = ["http://192.168.1.106:5000", "http://192.168.1.105:5000"]
current_ip_index = 0

# Variável global para indicar se a máquina tem o token
has_token = False
token_sequence = 0  # Sequência do token
token_timeout = 30  # Tempo máximo de espera para o token em segundos

@app.route('/token', methods=['POST'])
def receive_token():
    global has_token, token_sequence
    data = request.get_json()
    received_sequence = data.get('sequence', -1)
    
    #if received_sequence > token_sequence: estava assim, mas dava erro
    if received_sequence >= token_sequence:
        token_sequence = received_sequence
        has_token = True
        print(f"Recebi o token com sequência {token_sequence}")
        return jsonify({"status": "ok"})
    else:
        print(f"Token com sequência inválida recebido: {received_sequence}")
        return jsonify({"status": "invalid sequence"}), 400

@app.route('/process', methods=['POST'])
def process_request():
    global has_token
    data = request.get_json()
    if has_token:
        # Processar dados aqui
        print("Processando dados:", data)
        # Simular processamento
        time.sleep(5)
        has_token = False
        pass_token()
        return jsonify({"status": "processed"})
    else:
        return jsonify({"status": "no_token"}), 403

@app.route('/check_token', methods=['GET'])
def check_token():
    global has_token, token_sequence
    return jsonify({"has_token": has_token, "sequence": token_sequence})

def pass_token():
    global current_ip_index, token_sequence
    attempts = 0
    total_ips = len(ips)
    original_index = current_ip_index

    while attempts < total_ips - 1:  # Tentar todos os IPs exceto o atual
        next_ip_index = (current_ip_index + 1) % total_ips
        if next_ip_index == original_index:
            current_ip_index = next_ip_index
            attempts += 1
            continue
        next_ip = ips[next_ip_index]
        print(f"Passando o token para {next_ip}")
        try:
            # Incrementa a sequência do token
            token_sequence += 1
            # Timeout adicionado para evitar espera infinita
            response = requests.post(f"{next_ip}/token", json={"sequence": token_sequence}, timeout=5)
            if response.status_code == 200:
                current_ip_index = next_ip_index
                print(f"Token passado para {next_ip}")
                return
            else:
                print(f"Erro ao passar o token para {next_ip}")
        except requests.exceptions.RequestException as e:
            print(f"Erro ao conectar com {next_ip}: {e}")
        current_ip_index = next_ip_index
        attempts += 1
    
    # Se todas as tentativas falharem, tenta passar o token de volta para a máquina original
    print(f"Tentando passar o token de volta para {ips[original_index]}")
    try:
        token_sequence += 1
        response = requests.post(f"{ips[original_index]}/token", json={"sequence": token_sequence}, timeout=5)
        if response.status_code == 200:
            current_ip_index = original_index
            print(f"Token passado de volta para {ips[original_index]}")
        else:
            print(f"Erro ao passar o token de volta para {ips[original_index]}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar com {ips[original_index]}: {e}")

def start_server(ip, port):
    app.run(host=ip, port=port)

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Não precisa de uma conexão real
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def monitor_token():
    global has_token, token_timeout
    while True:
        if not has_token:
            # Reseta o timer se esta máquina tem o token
            last_token_time = time.time()
            while not has_token:
                time.sleep(1)
                token_passed_time = time.time()
                if (token_passed_time - last_token_time) > token_timeout:
                    print("Timeout do token excedido. Reeleição do token.")
                    reelect_token()
                    break

def reelect_token():
    global current_ip_index, token_sequence
    # Escolhe o IP dele na lista como o novo detentor do token
    next_ip_index = current_ip_index
    next_ip = ips[next_ip_index]
    print(f"Tentando reeleger token para {next_ip} com sequência {token_sequence + 1}")
    try:
        token_sequence += 1
        response = requests.post(f"{next_ip}/token", json={"sequence": token_sequence}, timeout=5)
        if response.status_code == 200:
            current_ip_index = next_ip_index
            print(f"Token reeleito para {next_ip}")
        else:
            print(f"Erro ao reeleger token para {next_ip}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar com {next_ip}: {e}")

def check_network_for_token():
    global token_sequence
    highest_sequence = token_sequence
    for ip in ips:
        try:
            response = requests.get(f"{ip}/check_token", timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get("has_token") and data.get("sequence", -1) > highest_sequence:
                    highest_sequence = data.get("sequence", -1)
                    return True
        except requests.exceptions.RequestException as e:
            print(f"Erro ao conectar com {ip}: {e}")
    return False

def verifica_token():
    global has_token
    while True:
        if has_token:
            # Simular recebimento de uma requisição de processamento
            print("Máquina com token. Pronta para processar.")
            time.sleep(10)  # Tempo de espera para simular processamento
            has_token = False
            pass_token()
        else:
            print("Aguardando token...")
            # Checa se outra máquina tem o token para resolver problemas de reconexão
            '''if not check_network_for_token():
                print("Nenhuma máquina com token detectada. Reeleição do token.")
                reelect_token()'''
            time.sleep(5)

#Funcao para inicializar o token 
def init():
    global token_sequence, has_token
    ip = get_local_ip()

    if f"http://{ip}:5000" == ips[0]:
        has_token = True  # A primeira máquina começa com o token
        token_sequence = 0

def main():
    ip = get_local_ip()
    port = 5000  # Porta fixa

    init()

    server_thread = threading.Thread(target=start_server, args=(ip, port))
    server_thread.start()

    monitor_thread = threading.Thread(target=monitor_token)
    monitor_thread.start()

    verifica_token()

if __name__ == "__main__":
    main()