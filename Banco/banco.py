from cliente import Cliente

# Criando um objeto da classe Cliente
cliente1 = Cliente(nome="Maria", idade=28, tipo_de_conta="Corrente", id_da_conta="12345")

# Usando os métodos do objeto cliente1
cliente1.mostrar_informacoes()
cliente1.depositar(1000)
cliente1.sacar(500)

# Mudando o nome e a idade, e mostrando as informações novamente
cliente1.set_nome("Yan")
cliente1.set_idade(30)
cliente1.mostrar_informacoes()