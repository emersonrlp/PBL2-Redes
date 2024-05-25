class Cliente:
    def __init__(self, nome, idade, tipo_de_conta, id_da_conta, saldo=0.0):
        self._nome = nome
        self._idade = idade
        self._tipo_de_conta = tipo_de_conta
        self._id_da_conta = id_da_conta
        self._saldo = saldo

    # Getter e Setter para o nome
    def get_nome(self):
        return self._nome

    def set_nome(self, nome):
        self._nome = nome

    # Getter e Setter para o idade
    def get_idade(self):
        return self._idade

    def set_idade(self, idade):
        self._idade = idade
    
    # Getter para tipo de conta
    def get_tipo_de_conta(self):
        return self._tipo_de_conta
    
    # Getter para id da conta
    def get_id_da_conta(self):
        return self._id_da_conta
    
    def depositar(self, valor):
        self._saldo += valor
        print(f"{valor} depositados. Novo saldo: {self._saldo:.2f}")

    def sacar(self, valor):
        if valor > self._saldo:
            print("Saldo insuficiente!")
        else:
            self._saldo -= valor
            print(f"{valor} sacados. Novo saldo: {self._saldo:.2f}")

    def mostrar_informacoes(self):
        print(f"Nome: {self._nome}")
        print(f"Idade: {self._idade}")
        print(f"Tipo de Conta: {self._tipo_de_conta}")
        print(f"ID da Conta: {self._id_da_conta}")
        print(f"Saldo: {self._saldo:.2f}")
