import re
import os
import requests
import random

ip_local = "192.168.1.106" #Pegar da variavel de ambiente

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
        idade_int = int(id)
    except ValueError:
        # Se ocorrer um erro de conversão, a entrada não é um número válido
        return False   

    if len(str(id)) != 7:
        return False
    else:
        return True
         
def gerar_timestamp_id():
    numeros = str(random.randint(10000, 99999))
    ip_aleatorio = numeros + ip_local[11] + ip_local[12]
    return int(ip_aleatorio)

def criar_conta(id_usuario):
    print("---------------------------------------")
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
    
def adicionar_conta(id_usuario, id_conta, conta):
    print("---------------------------------------")
    tipo_de_conta = input("Conta Pessoal ou Conjunta: (P)/(C): ")
    while validar_conta(tipo_de_conta) == False:
        print("---------------------------------------")
        tipo_de_conta = input("Conta Pessoal ou Conjunta: (P)/(C): ")
    print("---------------------------------------")

    id = gerar_timestamp_id()
    conta = {"id": id, "tipo": tipo_de_conta, "saldo": 0.0}
    url_contas = f"http://{ip_local}:8081/clientes/{id_usuario}/contas"

    response = requests.post(url_contas, json=conta, timeout=1)
    if response.status_code == 201:
        print("Conta criada com sucesso!")
        print("---------------------------------------")
    else:
        print("Erro ao criar conta!")

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
    
    id = gerar_timestamp_id()
    cliente = {"nome": nome, "idade": idade, "senha": senha, "id": id}
    url_clientes = f"http://{ip_local}:8081/clientes"

    response = requests.post(url_clientes, json=cliente, timeout=1)
    if response.status_code == 201:
        print("Usuário cadastrado, adicione uma conta!")
    else:
        print("Erro ao criar usuário!")

    criar_conta(id)

def obter_conta(id):
    url_conta = f"http://127.0.0.1:8081/clientes/{id}"
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

def tabela_opcoes():
    print("#######################################")
    print("#######################################")
    print("#Consultar Saldo:            (1)      #")
    print("#Consultar Extrato:          (2)      #")
    print("#Depositar:                  (3)      #")
    print("#Sacar:                      (4)      #")
    print("#Transferir:                 (5)      #")
    print("#######################################") 

def main():
    while True:
        num = menu()
        if num == 1:
            criar_usuario()
        else:
            sucesso, id = login()
            while sucesso:
                tabela_opcoes()
                num = input("-> ")
                while num != "1" and num != "2" and num != "3" and num != "4" and num != "5":
                    num = input("-> ")
                
                if num == "3":
                    url = f"http://127.0.0.1:8081/clientes/{id}/contas/{id}/depositar"
                    
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
                elif num == "4":
                    url = f"http://127.0.0.1:8081/clientes/{id}/contas/{id}/sacar"

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
            else:
                pass
if __name__ == "__main__":
    main()
