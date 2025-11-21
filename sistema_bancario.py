AGENCIA_PADRAO = "0001"
LIMITE_SAQUE = 500
LIMITE_SAQUES_DIARIOS = 3

usuarios = []
contas = []
proximo_numero_conta = 1


def filtrar_usuario_por_cpf(usuarios, cpf):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None


def criar_usuario(usuarios):
    nome = input("Informe o nome completo: ")
    cpf = input("Informe o CPF (somente números): ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    if filtrar_usuario_por_cpf(usuarios, cpf):
        print("CPF já cadastrado! Operação falhou.")
        return None

    usuario = {
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "endereco": endereco,
    }
    usuarios.append(usuario)
    print("Usuário criado com sucesso!")
    return usuario


def criar_conta(agencia, numero_conta, usuarios, contas):
    if not usuarios:
        print("Cadastre um usuário antes de criar uma conta.")
        return numero_conta

    cpf = input("Informe o CPF do titular da conta: ")
    usuario = filtrar_usuario_por_cpf(usuarios, cpf)

    if not usuario:
        print("Usuário não encontrado. Cadastre o CPF primeiro.")
        return numero_conta

    conta = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "usuario": usuario,
        "saldo": 0,
        "extrato": "",
        "saques_realizados": 0,
    }
    contas.append(conta)
    print("Conta criada com sucesso! Número da conta:", numero_conta)
    return numero_conta + 1


def listar_contas(contas, titulo="Contas cadastradas"):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return

    print(f"\n==== {titulo} ====")
    for conta in contas:
        titular = conta["usuario"]["nome"]
        saldo_str = f"Saldo: R$ {conta['saldo']:.2f}"
        print(
            f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Titular: {titular} | {saldo_str}"
        )
    print("========================\n")


def selecionar_conta(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return None

    filtrar = input("Deseja filtrar contas por CPF antes de selecionar? (s/n): ").strip().lower()
    contas_disponiveis = contas

    if filtrar == "s":
        cpf = input("Informe o CPF para filtrar: ")
        contas_filtradas = [conta for conta in contas if conta["usuario"]["cpf"] == cpf]
        if not contas_filtradas:
            print("Nenhuma conta encontrada para o CPF informado.")
            return None
        contas_disponiveis = contas_filtradas
        listar_contas(contas_disponiveis, titulo="Contas filtradas")
    else:
        listar_contas(contas)

    try:
        numero = int(input("Informe o número da conta: "))
    except ValueError:
        print("Número de conta inválido.")
        return None

    for conta in contas_disponiveis:
        if conta["numero_conta"] == numero:
            return conta

    print("Conta não encontrada.")
    return None


def depositar(conta):
    try:
        valor = float(input("Informe o valor do depósito: "))
    except ValueError:
        print("Valor inválido.")
        return

    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
        return

    conta["saldo"] += valor
    conta["extrato"] += f"Depósito: R$ {valor:.2f}\n"
    print("Depósito realizado com sucesso!")


def sacar(conta):
    try:
        valor = float(input("Informe o valor do saque: "))
    except ValueError:
        print("Valor inválido.")
        return

    excedeu_saldo = valor > conta["saldo"]
    excedeu_limite = valor > LIMITE_SAQUE
    excedeu_saques = conta["saques_realizados"] >= LIMITE_SAQUES_DIARIOS

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
    elif valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
    else:
        conta["saldo"] -= valor
        conta["extrato"] += f"Saque: R$ {valor:.2f}\n"
        conta["saques_realizados"] += 1
        print("Saque realizado com sucesso!")


def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not conta["extrato"] else conta["extrato"])
    print(f"\nSaldo: R$ {conta['saldo']:.2f}")
    print("==========================================")


menu = """
[u] Criar Usuário
[c] Criar Conta
[l] Listar Contas
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

def listar_contas(contas):
    if not contas:
        print("Nenhuma conta cadastrada.")
        return

    print("\n==== Contas Criadas ====")
    for conta in contas:
        titular = conta["usuario"]["nome"]
        print(f"Agência: {conta['agencia']} | Conta: {conta['numero_conta']} | Titular: {titular}")
    print("========================\n")

while True:
    opcao = input(menu)

    if opcao == "u":
        criar_usuario(usuarios)
    elif opcao == "c":
        proximo_numero_conta = criar_conta(AGENCIA_PADRAO, proximo_numero_conta, usuarios, contas)
    elif opcao == "d":
        conta = selecionar_conta(contas)
        if conta:
            depositar(conta)
    elif opcao == "s":
        conta = selecionar_conta(contas)
        if conta:
            sacar(conta)
    elif opcao == "e":
        conta = selecionar_conta(contas)
        if conta:
            exibir_extrato(conta)
    elif opcao == "l":
        listar_contas(contas)
    elif opcao == "q":
        break
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
