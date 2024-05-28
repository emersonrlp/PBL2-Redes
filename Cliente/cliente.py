import re
import os
import time
import requests

url_requisicoes = "http://127.0.0.1:8081/requisicoes"
url_clientes = "http://127.0.0.1:8081/clientes"

bancos = {"BB": "127.0.0.1"}

def menu():
    print("##################################")
    print("#Criar conta: (1)                #")
    print("#Fazer login: (2)                #")
    print("##################################")

def criar_cliente():
    global url_requisicoes

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

    tipo_de_conta = input("PJ/PF/CP/CC: ")
    while validar_conta(tipo_de_conta) == False:
        limpar_terminal()
        print("----------------------------------")
        tipo_de_conta = input("PJ/PF/CP/CC: ")
    print("----------------------------------")

    senha = input("senha: ")
    while validar_senha(senha) == False:
        limpar_terminal()
        print("----------------------------------")
        senha = input("senha: ")
    print("----------------------------------")

    id = gerar_timestamp_id()
    cliente = {"Nome":f"{nome}", "Idade": f"{idade}", "Tipo de conta":f"{tipo_de_conta}", "Numero da conta": f"{id}", "Senha": f"{senha}", "Tipo": "novo"}
    try:
        # Enviar uma solicitação POST para a API Flask para criar o novo sensor
        response = requests.post(url_requisicoes, json=cliente, timeout=1)
        print(gerar_timestamp_id())
    except Exception as e:
        print("", e)

def gerar_timestamp_id():
    return str(int(time.time() * 1000))

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
    padrao = re.compile(r"^(pj|pf|cp|cc|PJ|PF|CP|CC)$")

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
    cliente = obter_cliente(id)

    senha = input("Senha: ")
    if senha == cliente["Senha"]:
        print("##################################")
        print("Logando..")
        return True, id
    else:
        print("##################################")
        return False

def get_cliente(id):
    try:
        url = f"https://127.0.0.1:8081/clientes/{id}"  # Substitua pela URL da sua API
        response = requests.get(url)

        if response.status_code == 200:
            cliente = response.json()  # Converte a resposta em formato JSON
            return cliente
        else:
            print(f"Erro ao pegar o cliente: {response.status_code}")
            return None
    except:
        pass

def valida_num(num):
    if num != 1 and num != 2 and num != 3 and num != 4 and num != 5:
        True
    else:
        False

def obter_cliente(id):
    url_cliente = f"http://127.0.0.1:8081/clientes/{id}"
    response = requests.get(url_cliente)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao obter cliente:", response.status_code)
        return None
 
def tabela_opcoes():
    print("##################################")
    print("#Consultar Saldo:   (1)          #")
    print("#Consultar Extrato: (2)          #")
    print("#Depositar:         (3)          #")
    print("#Sacar:             (4)          #")
    print("#Transferir:        (5)          #")
    print("##################################")  

def verificar_banco(banco):
    global bancos

    for item in bancos:
        if banco in item:
            return True
    return False

def opcoes(id):
    global url_requisicoes
    global bancos 

    tabela_opcoes()
    num =  int(input("-> "))
    while valida_num(num):
        limpar_terminal()
        tabela_opcoes()
        num =  input("-> ")
    if num == 1:
        cliente = obter_cliente(id)
        print("--------------------------")
        print("Saldo: {}".format(cliente["saldo"]))
        print("--------------------------")
        input("Precione enter para continuar! ")
        limpar_terminal()
    elif num == 2:
        pass
    elif num == 3:
        valor = int(input("valor: "))
        deposito = {"Numero da conta": f"{id}", "valor": valor, "Tipo": "depositar"}
        try:
            # Enviar uma solicitação POST para a API Flask para criar depositar
            response = requests.post(url_requisicoes, json=deposito, timeout=1)
        except Exception as e:
            print("", e)
    elif num == 4:
        valor = int(input("valor: "))
        saque = {"Numero da conta": f"{id}", "valor": valor, "Tipo": "sacar"}
        try:
            # Enviar uma solicitação POST para a API Flask para criar depositar
            response = requests.post(url_requisicoes, json=saque, timeout=1)
        except Exception as e:
            print("", e)
    else:
        banco = input("Banco: ")
        while verificar_banco(banco) == False or banco == "":
            banco = input("Banco: ")
        id_banco = bancos[banco]

        valor = input("valor: ")
        while valor.isdigit() == False:
            valor = input("valor: ")
        valor = int(valor)

        transferencia = {"Numero da conta": f"{id}", "valor": valor, "Tipo": "transferir"}
        try:
            url_transferencia = "http://{}:8081/requisicoes".format(id_banco)
            response = requests.post(url_transferencia, json=transferencia, timeout=1)
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
            criar_cliente()
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
