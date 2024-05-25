from cliente import Cliente
import requests

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

def receber_requisicoes():
    global url_clientes
    global usuarios

    requisicoes = obter_lista_requisicoes()
    while len(requisicoes) > 0:
        requisicao = requisicoes[0]
        if requisicao["Tipo"] == "novo":
            cliente = Cliente(requisicao["Nome"], int(requisicao["Idade"]), requisicao["Tipo de conta"], requisicao["id"], requisicao["Senha"])
            usuarios.append(cliente)
        # Enviar uma solicitação POST para a API Flask para criar o novo sensor
        response = requests.post(url_clientes, json=cliente.to_dict(), timeout=1)
def main():  
    receber_requisicoes()

if __name__ == "__main__":
    main()
