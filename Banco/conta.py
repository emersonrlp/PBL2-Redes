class Conta:
    def __init__(self, clientes, tipo_de_conta, id_da_conta, senha, saldo=0.0):
        self._clientes = clientes
        self._tipo_de_conta = tipo_de_conta
        self._id_da_conta = id_da_conta
        self._senha = senha
        self._saldo = saldo

    # Getter para tipo de conta
    def get_tipo_de_conta(self):
        return self._tipo_de_conta
    
    # Getter para id da conta
    def get_id_da_conta(self):
        return self._id_da_conta
    
    # Getter e Setter para o senha
    def get_senha(self):
        return self._senha

    def set_senha(self, senha):
        self._senha = senha
    
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
        print(f"Clientes: {self._clientes}")
        print(f"Tipo de Conta: {self._tipo_de_conta}")
        print(f"ID da Conta: {self._id_da_conta}")
        print(f"Senha: {self._senha}")
        print(f"Saldo: {self._saldo:.2f}")

    def to_dict(self):
        return {
            "clientes": self._clientes,
            "tipo_de_conta": self._tipo_de_conta,
            "id": self._id_da_conta,
            "Senha": self._senha,
            "saldo": self._saldo
        }