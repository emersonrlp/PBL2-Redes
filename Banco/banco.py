from cliente import Cliente
import requests
from api import app
import threading
import time

url_clientes = "http://127.0.0.1:8081/clientes"
usuarios = []

def obter_lista_clientes():
    global url_clientes
    response = requests.get(url_clientes)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao obter a lista de clientes:", response.status_code)
        return None

def obter_lista_requisicoes():
    url_requisicoes = "http://127.0.0.1:8081/requisicoes"
    response = requests.get(url_requisicoes)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao obter a lista de requisicoes:", response.status_code)
        return None
def remover_requisição(requisicoes_id):
    url = f"http://127.0.0.1:8081/requisicoes/{requisicoes_id}"
    response = requests.delete(url)
    if response.status_code == 200:
        print("Requisição removida com sucesso.")
    else:
        print("Erro ao remover requisição:", response.status_code)

def receber_requisicoes():
    global url_clientes
    global usuarios

    try:
        while True:   
            time.sleep(1)
            requisicoes = obter_lista_requisicoes()
            if len(requisicoes) > 0:
                requisicao = requisicoes[0]
                if requisicao["Tipo"] == "novo":
                    cliente = Cliente(requisicao["Nome"], int(requisicao["Idade"]), requisicao["Tipo de conta"], int(requisicao["Numero da conta"]), requisicao["Senha"])
                    usuarios.append(cliente)
                    print("{}".format(cliente.get_id_da_conta()))
                    # Enviar uma solicitação POST para a API Flask para criar o novo cliente
                    response = requests.post(url_clientes, json=cliente.to_dict())
                    remover_requisição(1)
                elif requisicao["Tipo"] == "extrato":
                    continue
                elif requisicao["Tipo"] == "depositar" or requisicao["Tipo"] == "transferir":
                    for item in usuarios:
                        if item.get_id_da_conta() == int(requisicao["Numero da conta"]):
                            item.depositar(requisicao["valor"])
                            url_cliente = 'http://127.0.0.1:8081/clientes/'+ requisicao["Numero da conta"]
                            response = requests.put(url_cliente, json=item.to_dict())
                            remover_requisição(1)
                elif requisicao["Tipo"] == "sacar":
                    for item in usuarios:
                        if item.get_id_da_conta() == int(requisicao["Numero da conta"]):
                            item.depositar(-requisicao["valor"])
                            url_cliente = 'http://127.0.0.1:8081/clientes/'+ requisicao["Numero da conta"]
                            response = requests.put(url_cliente, json=item.to_dict())
                            remover_requisição(1)
    except Exception as e:
        print("", e)

def main():
    try:
        # Inicia os servidores TCP e UDP em threads separadas
        tcp_thread = threading.Thread(target=receber_requisicoes)
        tcp_thread.start()

        # Inicia a aplicação Flask
        app.run(host='0.0.0.0', port=8081, debug=True)

    except Exception as e:
        print('Erro:', e)

if __name__ == "__main__":
    main()
