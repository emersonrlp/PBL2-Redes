import re
import os
import requests
import random
import time

#ip_local= os.getenv('IP_ADDRESS')
ip_local = "192.168.1.103" #Pegar da variavel de ambiente

def menu():
    print("Criar usuário: (1)\nFazer login:   (2)")
    num = input("-> ")
    while valida_menu(num) == False:
        print("Digite uma opção válida!")
        num = input("-> ")
    return int(num)

def valida_menu(num):
    try:
        num = int(num)
    except ValueError:
        return False
    
    if int(num) != 1 and int(num) != 2:
        return False
    else:
        return True
    
def validar_nome(nome):
    # Define o padrão regex para um nome válido
    # O padrão permite letras (maiúsculas e minúsculas), espaços, apóstrofos e hífens
    padrao = re.compile(r"^[A-Za-zÀ-ÿ' -]+$")
    
    # Verifica se o nome corresponde ao padrão
    if padrao.match(nome):
        return True
    else:
        return False

def validar_idade(idade):
    try:
        # Tenta converter a entrada para um número inteiro
        idade_int = int(idade)
    except ValueError:
        # Se ocorrer um erro de conversão, a entrada não é um número válido
        return False

    # Verifica se a idade está no intervalo desejado
    if 0 <= idade_int <= 120:
        return True
    else:
        return False

def validar_conta(tipo_de_conta):
    # Define o padrão regex para uma conta válida
    padrao = re.compile(r"^(p|c|P|C)$")

    # Verifica se o tipo de conta é válido 
    if padrao.match(tipo_de_conta):
        return True
    else:
        return False 

def validar_senha(senha):
    # Verifica se a senha corresponde ao padrão
    if len(senha) >= 5 and len(senha) <= 15:
        return True
    else:
        return False
def validar_id(id):
    try:
        # Tenta converter a entrada para um número inteiro
        id = int(id)
    except ValueError:
        # Se ocorrer um erro de conversão, a entrada não é um número válido
        return False   

    if len(str(id)) > 7 or len(str(id)) < 5:
        return False
    else:
        return True
         
def gerar_timestamp_id(ip_local):
    # Obtém os últimos dígitos depois do último ponto do IP local
    ultimos_digitos_ip = ip_local.split('.')[-1]

    # Gera números aleatórios entre 1000 e 9999
    numeros_aleatorios = str(random.randint(1000, 9999))

    # Concatena os números aleatórios com os últimos dígitos do IP
    id_gerado = int(numeros_aleatorios + ultimos_digitos_ip)

    return id_gerado

def criar_conta(id_usuario):
    tipo_de_conta = input("Conta Pessoal ou Conjunta: (P)/(C): ")
    while validar_conta(tipo_de_conta) == False:
        print("---------------------------------------")
        tipo_de_conta = input("Conta Pessoal ou Conjunta: (P)/(C): ")
    print("---------------------------------------")

    conta = {"id": id_usuario, "tipo": tipo_de_conta, "saldo": 0.0}
    url_contas = f"http://{ip_local}:8081/clientes/{id_usuario}/contas"

    response = requests.post(url_contas, json=conta, timeout=1)
    if response.status_code == 201:
        print("Conta criada com sucesso!")
    else:
        print("Erro ao criar conta!")
    
def adicionar_conta(id_usuario, id_conta):
    conta = obter_cliente(id_conta)
    tipo_de_conta = conta["contas"][0]["tipo"]

    conta = {"id": id_conta, "tipo": tipo_de_conta, "saldo": "***"}
    url_contas = f"http://{ip_local}:8081/clientes/{id_usuario}/contas"

    response = requests.post(url_contas, json=conta, timeout=1)
    if response.status_code == 201:
        print("Conta adicionada com sucesso!")
        print("---------------------------------------")
    else:
        print("Erro ao adicionar conta!")

def criar_usuario():
    global ip_local
    
    print("---------------------------------------")
    nome = input("nome: ")
    while validar_nome(nome) == False:
        print("---------------------------------------")
        nome = input("nome: ")
    print("---------------------------------------")

    idade = input("idade: ")
    while validar_idade(idade) == False:
        print("---------------------------------------")
        idade = input("idade: ")
    print("---------------------------------------")

    senha = input("senha: ")
    while validar_senha(senha) == False:
        print("---------------------------------------")
        senha = input("senha: ")
    print("---------------------------------------")
    
    id = gerar_timestamp_id(ip_local)
    cliente = {"nome": nome, "idade": idade, "senha": senha, "id": id}
    url_clientes = f"http://{ip_local}:8081/clientes"

    response = requests.post(url_clientes, json=cliente, timeout=1)
    if response.status_code == 201:
        pass
        #print("Usuário cadastrado, adicione uma conta!")
    else:
        print("Erro ao criar usuário!")

    criar_conta(id)

def obter_cliente(id):
    global ip_local
    #para ver a ultima parte do ip referente ao id da conta de destino
    if len(str(id)) == 7:
        ip_d = 3
    elif len(str(id)) == 6:
        ip_d = 2
    else:
        ip_d = 1

    url_conta = f"http://{ip_local[:-ip_d] + str(id)[-ip_d:]}:8081/clientes/{id}"
    response = requests.get(url_conta)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao obter cliente:", response.status_code)
        return None
    
def login():
    global ip_local
    url = f"http://{ip_local}:8081/login"

    print("#######################################")
    id = input("Número da conta: ")
    while validar_id(id) == False:
        id = input("Número da conta: ")

    senha = input("senha: ")
    while validar_senha(senha) == False:
        senha = input("senha")
    print("#######################################")
    # Dados de login
    data = {
        "id": int(id),      # ID do cliente
        "senha": senha  # Senha do cliente
    }

    # Enviar a requisição POST
    response = requests.post(url, json=data)

    # Verificar a resposta
    if response.status_code == 200:
        print("Login bem-sucedido.")
        return True, id
    else:
        print("Erro ao fazer login:", response.json())
        return False

def verificar_conta_cliente(id, id_origem):
    cliente = obter_cliente(id)
    for item in cliente["contas"]:
        if item["id"] == int(id_origem):
            return True
        
    return False

def tabela_opcoes():
    print("#######################################")
    print("#######################################")
    print("#Consultar Saldo:            (1)      #")
    print("#Depositar:                  (2)      #")
    print("#Sacar:                      (3)      #")
    print("#Transferir:                 (4)      #")
    print("#Adicionar conta:            (5)      #")
    print("#Ver contas:                 (6)      #")
    print("#######################################") 

def main():
    global ip_local
    while True:
        num = menu()
        if num == 1:
            criar_usuario()
        else:
            sucesso, id = login()
            while sucesso:
                tabela_opcoes()
                num = input("-> ")
                while num != "1" and num != "2" and num != "3" and num != "4" and num != "5" and num != "6":
                    num = input("-> ")
                if num == "1":
                    cliente = obter_cliente(id)
                    print(cliente["contas"][0]["saldo"])

                elif num == "2":
                    url = f"http://{ip_local}:8081/clientes/{id}/contas/{id}/depositar"
                    
                    valor = input("valor: ")
                    while valor.isdigit() == False:
                        valor = input("valor: ")

                    data = {"valor": int(valor)}

                    response = requests.post(url, json=data)

                    # Verificar a resposta
                    if response.status_code == 200:
                        print("Depósito realizado com sucesso.")
                    else:
                        print("Erro ao realizar depósito:", response.json())
                elif num == "3":
                    url = f"http://{ip_local}:8081/clientes/{id}/contas/{id}/sacar"

                    valor = input("valor: ")
                    while valor.isdigit() == False:
                        valor = input("valor: ")

                    data = {"valor": int(valor)}

                    response = requests.post(url, json=data)

                    # Verificar a resposta
                    if response.status_code == 200:
                        print("Saque realizado com sucesso.")
                    else:
                        print("Erro ao realizar saque:", response.json())
                elif num == "4":
                    pacote_completo = False
                    pacote = []
                    while pacote_completo == False:

                        id_origem = input("Digite de quem vc quer enviar: ")
                        while verificar_conta_cliente(id, id_origem) == False:
                            print("Não pode usar essa conta!")
                            id_origem = input("Digite de quem vc quer enviar: ")
                        
                        id_destino = input("Digite para qum vc quer enviar: ")
                        while validar_id(id_destino) == False:
                            print("Id inválido, escreva um número de conta válido! ")
                            id_destino = input("Digite para qum vc quer enviar: ")

                        valor = input("Digite o valor: ")
                        while valor.isdigit() == False:
                            valor = input("Digite o valor: ")

                        pacote.append({"Usuario": int(id), "id_origem": int(id_origem), "id_destino": int(id_destino), "valor": int(valor), "status": "default"})
                        n = input("Deseja acresentar mais alguma transação? (S)/(N)")
                        while n != "S" and n != "s" and n != "N" and n != "n":
                            n = input("Deseja acresentar mais alguma transação? (S)/(N)")

                        if n == "N" or n == "n":
                            pacote_completo = True
                    
                    url = f"http://{ip_local}:8081/transferencias"
                    response = requests.post(url, json=pacote)

                    # Verificar a resposta
                    if response.status_code == 201:
                        print("Transferência publicada com sucesso.")
                    else:
                        print("Erro ao publicar transferência:", response.json())

                    time.sleep(15)
                    url_conta = f"http://{ip_local}:8081//transferencias_finalizadas/usuario/{id}"
                    print(url_conta)
                    response = requests.get(url_conta)

                    if response.status_code == 201:
                        print("Transferencia realizada!")
                    else:
                        print("Erro ao realizar transferência!")

                elif num == "5":
                    id_conta = input("Digite o id da conta: ")
                    while validar_id(id) == False:
                        id_conta = input("Digite o id da conta: ")
                    id_conta = int(id_conta)
                    adicionar_conta(id, id_conta)
                elif num == "6":
                    cliente = obter_cliente(id)
                    for item in cliente["contas"]:
                        print(item)
if __name__ == "__main__":
    main()
