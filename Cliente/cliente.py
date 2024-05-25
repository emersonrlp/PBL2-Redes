import re
import os
import time

def menu():
    print("##################################")
    print("#Criar conta: (1)                #")
    print("#Fazer login: (2)                #")
    print("##################################")

def criar_cliente():
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
    
    print(gerar_timestamp_id())

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
    print("Número da conta: ")
    print("Senha: ")
    print("##################################")
    
def main():
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
        login()
if __name__ == "__main__":
    main()