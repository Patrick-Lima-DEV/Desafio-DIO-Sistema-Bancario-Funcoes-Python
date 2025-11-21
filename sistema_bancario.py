import json
import re
from datetime import datetime
from pathlib import Path

AGENCIA_PADRAO = "0001"
LIMITE_SAQUE = 500
LIMITE_SAQUES_DIARIOS = 3
ARQUIVO_DADOS = Path("dados_bancarios.json")

usuarios = []
contas = []
proximo_numero_conta = 1


def validar_cpf(cpf):
    """Valida CPF com algoritmo verificador."""
    if not re.match(r"^\d{11}$", cpf):
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Calcula primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = 11 - (soma % 11)
    digito1 = 0 if digito1 > 9 else digito1
    
    # Calcula segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = 11 - (soma % 11)
    digito2 = 0 if digito2 > 9 else digito2
    
    return int(cpf[9]) == digito1 and int(cpf[10]) == digito2


def validar_data(data_str):
    """Valida data no formato dd-mm-aaaa."""
    try:
        datetime.strptime(data_str, "%d-%m-%Y")
        return True
    except ValueError:
        return False


def salvar_dados():
    """Salva usuários e contas em arquivo JSON."""
    dados = {
        "usuarios": usuarios,
        "contas": contas,
        "proximo_numero_conta": proximo_numero_conta
    }
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def carregar_dados():
    """Carrega usuários e contas do arquivo JSON."""
    global usuarios, contas, proximo_numero_conta
    
    if ARQUIVO_DADOS.exists():
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                dados = json.load(f)
                usuarios = dados.get("usuarios", [])
                contas = dados.get("contas", [])
                proximo_numero_conta = dados.get("proximo_numero_conta", 1)
        except (json.JSONDecodeError, KeyError):
            pass


def filtrar_usuario_por_cpf(usuarios, cpf):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None


def criar_usuario(usuarios):
    nome = input("Informe o nome completo: ")
    
    cpf = None
    while not cpf:
        cpf_input = input("Informe o CPF (somente números): ")
        if not validar_cpf(cpf_input):
            print("CPF inválido! Tente novamente.")
            continue
        if filtrar_usuario_por_cpf(usuarios, cpf_input):
            print("CPF já cadastrado! Tente novamente.")
            continue
        cpf = cpf_input

    data_nascimento = None
    while not data_nascimento:
        data_input = input("Informe a data de nascimento (dd-mm-aaaa): ")
        if not validar_data(data_input):
            print("Data inválida! Use formato dd-mm-aaaa. Tente novamente.")
            continue
        data_nascimento = data_input
    
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuario = {
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "endereco": endereco,
        "data_criacao": datetime.now().isoformat(),
    }
    usuarios.append(usuario)
    salvar_dados()
    print("Usuário criado com sucesso!")
    return usuario


def criar_conta(agencia, numero_conta, usuarios, contas):
    if not usuarios:
        print("Cadastre um usuário antes de criar uma conta.")
        return numero_conta

    usuario = None
    while not usuario:
        cpf = input("Informe o CPF do titular da conta: ")
        usuario = filtrar_usuario_por_cpf(usuarios, cpf)
        if not usuario:
            print("Usuário não encontrado. Tente novamente.")

    conta = {
        "agencia": agencia,
        "numero_conta": numero_conta,
        "usuario": usuario,
        "saldo": 0,
        "extrato": "",
        "saques_realizados": 0,
        "data_criacao": datetime.now().isoformat(),
    }
    contas.append(conta)
    salvar_dados()
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

    while True:
        try:
            numero = int(input("Informe o número da conta: "))
        except ValueError:
            print("Número de conta inválido. Tente novamente.")
            continue

        for conta in contas_disponiveis:
            if conta["numero_conta"] == numero:
                return conta

        print("Conta não encontrada. Tente novamente.")


def depositar(conta):
    while True:
        try:
            valor = float(input("Informe o valor do depósito: "))
        except ValueError:
            print("Valor inválido. Tente novamente.")
            continue

        if valor <= 0:
            print("Operação falhou! O valor informado é inválido. Tente novamente.")
            continue

        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        conta["saldo"] += valor
        conta["extrato"] += f"[{timestamp}] Depósito: R$ {valor:.2f}\n"
        salvar_dados()
        print("Depósito realizado com sucesso!")
        break


def sacar(conta):
    while True:
        try:
            valor = float(input("Informe o valor do saque: "))
        except ValueError:
            print("Valor inválido. Tente novamente.")
            continue

        excedeu_saldo = valor > conta["saldo"]
        excedeu_limite = valor > LIMITE_SAQUE
        excedeu_saques = conta["saques_realizados"] >= LIMITE_SAQUES_DIARIOS

        if excedeu_saldo:
            print("Operação falhou! Você não tem saldo suficiente. Tente novamente.")
        elif excedeu_limite:
            print("Operação falhou! O valor do saque excede o limite. Tente novamente.")
        elif excedeu_saques:
            print("Operação falhou! Número máximo de saques excedido.")
            break
        elif valor <= 0:
            print("Operação falhou! O valor informado é inválido. Tente novamente.")
        else:
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            conta["saldo"] -= valor
            conta["extrato"] += f"[{timestamp}] Saque: R$ {valor:.2f}\n"
            conta["saques_realizados"] += 1
            salvar_dados()
            print("Saque realizado com sucesso!")
            break


def transferir(contas):
    """Realiza transferência entre contas."""
    conta_origem = selecionar_conta(contas)
    if not conta_origem:
        return
    
    print("\nSelecione a conta de destino:")
    conta_destino = selecionar_conta(contas)
    if not conta_destino:
        return
    
    if conta_origem["numero_conta"] == conta_destino["numero_conta"]:
        print("Operação falhou! Não é possível transferir para a mesma conta.")
        return
    
    while True:
        try:
            valor = float(input("Informe o valor da transferência: "))
        except ValueError:
            print("Valor inválido. Tente novamente.")
            continue
    
        if valor <= 0:
            print("Operação falhou! O valor informado é inválido. Tente novamente.")
            continue
    
        if valor > conta_origem["saldo"]:
            print("Operação falhou! Saldo insuficiente. Tente novamente.")
            continue
        
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        conta_origem["saldo"] -= valor
        conta_origem["extrato"] += f"[{timestamp}] Transferência enviada: R$ {valor:.2f} para Agência {conta_destino['agencia']} Conta {conta_destino['numero_conta']}\n"
        
        conta_destino["saldo"] += valor
        conta_destino["extrato"] += f"[{timestamp}] Transferência recebida: R$ {valor:.2f} de Agência {conta_origem['agencia']} Conta {conta_origem['numero_conta']}\n"
        
        salvar_dados()
        print("Transferência realizada com sucesso!")
        break


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
[t] Transferir
[e] Extrato
[q] Sair

=> """

carregar_dados()

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
    elif opcao == "t":
        transferir(contas)
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
