from flask import Flask, request, jsonify
import requests
import threading
import time

app = Flask(__name__)

# Configurações de rede - altere esses IPs para os IPs das suas duas máquinas
ips = ["http://192.168.1.106:5000", "http://192.168.1.105:5000"]
indice_ip_atual = 0
ip = "192.168.1.106"

# Variável global para indicar se a máquina possui o token
tem_token = False
sequencia_token = 0  # Sequência do token
timeout_token = 30  # Tempo máximo de espera pelo token em segundos

@app.route('/token', methods=['POST'])
def receber_token():
    global tem_token, sequencia_token
    dados = request.get_json()
    sequencia_recebida = dados.get('sequencia', -1)
    
    if sequencia_recebida > sequencia_token:
        sequencia_token = sequencia_recebida
        tem_token = True
        print(f"Recebeu token com sequência {sequencia_token}")
        return jsonify({"status": "ok"})
    else:
        #print(f"Sequência de token inválida recebida: {sequencia_recebida}")
        return jsonify({"status": "sequência inválida"}), 400

@app.route('/processar', methods=['POST'])
def processar_requisicao():
    global tem_token
    dados = request.get_json()
    if tem_token:
        # Processar dados aqui
        print("Processando dados:", dados)
        # Simular processamento
        time.sleep(5)
        tem_token = False
        passar_token()
        return jsonify({"status": "processado"})
    else:
        return jsonify({"status": "sem_token"}), 403

@app.route('/verificar_token', methods=['GET'])
def verificar_token():
    global tem_token, sequencia_token
    return jsonify({"tem_token": tem_token, "sequencia": sequencia_token})

def passar_token():
    global indice_ip_atual, sequencia_token, ips, tem_token, ip
    conseguiu = False
    for i in range(len(ips)):
        if ips[i] != ips[indice_ip_atual]:
            try:
                resposta = requests.post(f"{ips[i]}/token", json={"sequencia": sequencia_token + 1}, timeout=5)
                if resposta.status_code == 200:
                    conseguiu = True
                    print(f"Token passado para {ips[i]}")
                    break
                else:
                    print(f"Erro ao passar Token para {ips[i]}") 
            except requests.exceptions.RequestException as e:
                print(f"Erro ao conectar a {ips[i]}: {e}")
                pass
    if conseguiu == False:
        tem_token = True
        sequencia_token +=1
        
def iniciar_servidor(ip, porta):
    app.run(host=ip, port=porta)

def monitorar_token():
    global tem_token, timeout_token
    while True:
        if not tem_token:
            ultimo_tempo_token = time.time()
            while not tem_token:
                time.sleep(1)
                tempo_passado_token = time.time()
                if (tempo_passado_token - ultimo_tempo_token) > timeout_token:
                    print("Tempo de espera do token excedido. Reeleição do token.")
                    reeleger_token()
                    break

def reeleger_token():
    global indice_ip_atual, sequencia_token
    proximo_indice_ip = indice_ip_atual
    proximo_ip = ips[proximo_indice_ip]
    print(f"Tentando reeleger token para {proximo_ip} com sequência {sequencia_token + 1}")
    try:
        resposta = requests.post(f"{proximo_ip}/token", json={"sequencia": sequencia_token+1}, timeout=5)
        if resposta.status_code == 200:
            indice_ip_atual = proximo_indice_ip
            print(f"Token reeleito para {proximo_ip}")
        else:
            print(f"Erro ao reeleger token para {proximo_ip}")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao conectar a {proximo_ip}: {e}")

def iniciar():
    global sequencia_token, tem_token, ip, ips

    if f"http://{ip}:5000" == ips[0]:
        tem_token = True  # A primeira máquina começa com o token
        sequencia_token = 0

def main():
    global tem_token, ip
    porta = 5000  # Porta fixa

    iniciar()

    thread_servidor = threading.Thread(target=iniciar_servidor, args=(ip, porta))
    thread_servidor.start()

    thread_monitor = threading.Thread(target=monitorar_token)
    thread_monitor.start()

    while True:
        if tem_token:
            # Simular recebimento de uma solicitação de processamento
            print("Máquina com token. Pronta para processar.")
            time.sleep(1)
            passar_token()

if __name__ == "__main__":
    main()