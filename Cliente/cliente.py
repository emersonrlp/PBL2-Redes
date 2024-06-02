import re
import os
import requests
import random

url_depositos = "http://127.0.0.1:8081/depositos"
url_saques = "http://127.0.0.1:8081/saques"
url_contas = "http://127.0.0.1:8081/contas"
ip_local = "192.168.1.106" #Pegar da variavel de ambiente

def menu():
    print("##################################")
    print("#Criar conta: (1)                #")
    print("#Fazer login: (2)                #")
    print("##################################")

def criar_conta():
    global url_contas

    print("----------------------------------")
    tipo_de_conta = input("Pessoal ou Conjunta: (P)/(C): ")
    while validar_conta(tipo_de_conta) == False:
        limpar_terminal()
        print("----------------------------------")
        tipo_de_conta = input("Pessoal ou Conjunta: (P)/(C): ")
    print("----------------------------------")

    senha = input("senha: ")
    while validar_senha(senha) == False:
        limpar_terminal()
        print("----------------------------------")
        senha = input("senha: ")
    print("----------------------------------")

    num = 1
    clientes = []
    while num != 2:
        limpar_terminal()
        print("----------------------------------")
        nome = input("nome: ")
        while validar_nome(nome) == False:
            limpar_terminal()
            print("----------------------------------")
            nome = input("nome: ")
        print("----------------------------------")

        idade = input("idade: ")
        while validar_idade(idade) == False:
            limpar_terminal()
            print("----------------------------------")
            idade = input("idade: ")
        print("----------------------------------")
        
        
        clientes.append((nome, idade))
        limpar_terminal()
        print("----------------------------------")
        num = int(input("Adicionar dono (1): \nCriar conta: (2):\n----------------------------------\n"))
        while num != 2 and num != 1:
            limpar_terminal()
            print("----------------------------------")
            num = int(input("Adicionar dono (1): \nCriar conta: (2):\n----------------------------------\n"))

    id = gerar_timestamp_id()
    cliente = {"Clientes":f"{clientes}", "Tipo de conta":f"{tipo_de_conta}", "id": int(id), "Senha": f"{senha}", "Tipo": "novo", "Saldo": 0.0}
    try:
        # Enviar uma solicitação POST para a API Flask para criar o novo sensor
        response = requests.post(url_contas, json=cliente, timeout=1)
        input("\nDigite enter para voltar ao menu! ")
    except Exception as e:
        print("", e)

def gerar_timestamp_id():
    numeros = [str(random.randint(0, 9)) for _ in range(5)]
    ip_aleatorio = ''.join(numeros) + ip_local[12]
    return ip_aleatorio

def validar_nome(nome):
    # Define o padrão regex para um nome válido
    # O padrão permite letras (maiúsculas e minúsculas), espaços, apóstrofos e hífens
    padrao = re.compile(r"^[A-Za-zÀ-ÿ' -]+$")
    
    # Verifica se o nome corresponde ao padrão
    if padrao.match(nome):
        return True
    else:
        return False

def validar_senha(senha):
    # Verifica se a senha corresponde ao padrão
    if len(senha) >= 5 and len(senha) <= 15:
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

def limpar_terminal():
    if os.name == 'nt':  # Verifica se o sistema operacional é Windows
        os.system('cls')
    else:
        os.system('clear')

def login():
    print("##################################")
    id = int(input("Número da conta: "))
    cliente = obter_conta(id)

    senha = input("Senha: ")
    if senha == cliente["Senha"]:
        print("##################################")
        print("Logando..")
        return True, id
    else:
        print("##################################")
        return False

def valida_num(num):
    if num != 1 and num != 2 and num != 3 and num != 4 and num != 5:
        True
    else:
        False

def obter_conta(id):
    url_conta = f"http://127.0.0.1:8081/contas/{id}"
    response = requests.get(url_conta)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao obter conta:", response.status_code)
        return None
 
def tabela_opcoes():
    print("##################################")
    print("#Consultar Saldo:   (1)          #")
    print("#Consultar Extrato: (2)          #")
    print("#Depositar:         (3)          #")
    print("#Sacar:             (4)          #")
    print("#Transferir:        (5)          #")
    print("##################################")  

def opcoes(id):
    global url_depositos 
    global url_saques

    tabela_opcoes()
    num =  int(input("-> "))
    while valida_num(num):
        limpar_terminal()
        tabela_opcoes()
        num =  input("-> ")
    if num == 1:
        conta = obter_conta(id)
        print("--------------------------")
        print("Saldo: {}".format(conta["Saldo"]))
        print("--------------------------")
        input("Precione enter para continuar! ")
        limpar_terminal()
    elif num == 2:
        pass
    elif num == 3:
        valor = int(input("valor: "))
        deposito = {"id": id, "Valor": valor}
        try:
            # Enviar uma solicitação POST para a API Flask para criar depositar
            response = requests.post(url_depositos, json=deposito, timeout=1)
        except Exception as e:
            print("", e)
    elif num == 4:
        valor = int(input("valor: "))
        saque = {"id": id, "Valor": valor}
        try:
            # Enviar uma solicitação POST para a API Flask para criar depositar
            response = requests.post(url_saques, json=saque, timeout=1)
        except Exception as e:
            print("", e)
    else:
        chave = input("Chave pix: ")
        while chave.isdigit() == False or len(chave) != 6:
            chave = input("Chave pix: ")
        url_transferencias = f"http://192.168.1.10{chave[5]}:8081/transferencias"

        valor = input("valor: ")
        while valor.isdigit() == False:
            valor = input("valor: ")
        valor = int(valor)

        transferencia = {"id": id, "Valor": valor}
        try:
            response = requests.post(url_transferencias, json=transferencia, timeout=1)
            if response.status_code == 201:
                saque = {"id": id, "Valor": valor}
                try:
                    # Enviar uma solicitação POST para a API Flask para criar depositar
                    response = requests.post(url_saques, json=saque, timeout=1)
                except Exception as e:
                    print("", e)
            else:
                print("Erro ao fazer PIX! ")
        except Exception as e:
            print("", e)

def main():
    while True:
        menu()
        num = int(input(""))
        while num != 1 and num != 2:
            limpar_terminal()
            menu()
            num = int(input(""))
        limpar_terminal()

        if num == 1:
            criar_conta()
        else:
            sucesso, id = login()
            limpar_terminal()
            if sucesso:
                while True:
                    opcoes(id)
                    limpar_terminal()
            else:
                continue   

        limpar_terminal()

if __name__ == "__main__":
    main()
