import requests
import threading

bank1 = "192.168.1.103"
bank2 = "192.168.1.104"

lista_clientes = [{"nome": "Paulo", "idade": 21, "senha": "123456", "id": 1000103},
                  {"nome": "Nando", "idade": 25, "senha": "123456", "id": 2000103},
                  {"nome": "Julia", "idade": 25, "senha": "123456", "id": 1000104}]

transferencias1 = [{"Usuario": 1000103, "id_origem": 1000103, "id_destino": 2000103, "valor": 100, "status": "default"},
                   {"Usuario": 1000104, "id_origem": 1000104, "id_destino": 2000103, "valor": 100, "status": "default"}] 

transferencias2 = [{"Usuario": 1000103, "id_origem": 1000103, "id_destino": 2000103, "valor": 50, "status": "default"}] 

threads = []

#Criar Usuários
def criar_usuarios():
    global bank1, bank2, lista_clientes

    #Cria dois clientes no primeiro banco
    url_bank1 = f"http://{bank1}:8081/clientes"
    for i in range(2):
        try:
            response = requests.post(url_bank1, json=lista_clientes[i], timeout=1)
            if response.status_code == 201:
                print("Cliente criado com sucesso!")
            else:
                print("Erro ao criar cliente!")
        except Exception as e:
            print(f"Erro: {e}")

    #Cria um cliente no segundo banco
    url_bank2 = f"http://{bank2}:8081/clientes"
    try:
        response = requests.post(url_bank2, json=lista_clientes[2], timeout=1)
        if response.status_code == 201:
            print("Cliente criado com sucesso!")
        else:
            print("Erro ao criar cliente!")
    except Exception as e:
            print(f"Erro: {e}")

    #Cria duas contas no primeiro banco
    for i in range(2):
        try:
            id = lista_clientes[i]["id"]
            url_bank1 = f"http://{bank1}:8081/clientes/{id}/contas"
            conta = {"id": id, "tipo": "P", "saldo": 200}
            response = requests.post(url_bank1, json=conta, timeout=1)
            if response.status_code == 201:
                print("Conta criada com sucesso!")
            else:
                print("Erro ao criar conta!")
        except Exception as e:
            print(f"Erro: {e}")

    #Cria uma conta no segundo banco
    try:
        id = lista_clientes[2]["id"]
        url_bank2 = f"http://{bank2}:8081/clientes/{id}/contas"
        conta = {"id": id, "tipo": "P", "saldo": 200}
        response = requests.post(url_bank2, json=conta, timeout=1)
        if response.status_code == 201:
            print("Conta criada com sucesso!")
        else:
            print("Erro ao criar conta!")
    except Exception as e:
            print(f"Erro: {e}")
          
#Testes
def enviar_transferencia(ip, transferencia):
    url = f"http://{ip}:8081/transferencias"
    pacote = []
    pacote.append(transferencia)
    response = requests.post(url, json=pacote)

    # Verificar a resposta
    if response.status_code == 201:
        print("Transferência publicada com sucesso.")
    else:
        print("Erro ao publicar transferência:", response.json())

#Conta A manda para conta B e conta C manda para B
thread = threading.Thread(target=enviar_transferencia, args=(bank1, transferencias1[0], ))
threads.append(thread)

thread = threading.Thread(target=enviar_transferencia, args=(bank2, transferencias1[1], ))
threads.append(thread)

#Conta C manda para a B duas vezes
thread = threading.Thread(target=enviar_transferencia, args=(bank1, transferencias2[0], ))
threads.append(thread)

thread = threading.Thread(target=enviar_transferencia, args=(bank1, transferencias2[0], ))
threads.append(thread)

def main():
    global threads
    num = input("Criar usuario: (1)\nFazer testes: (2)\n")
    if num == "1":
        criar_usuarios()
    else:
        for t in threads:
            t.start()
        
        for thread in threads:
            thread.join()

if __name__ == "__main__":
    main()

