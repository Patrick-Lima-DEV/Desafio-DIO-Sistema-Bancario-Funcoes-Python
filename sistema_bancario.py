#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sistema Bancário - Interface de Linha de Comando (CLI)."""

from utils import (
    validar_cpf, validar_data, filtrar_usuario_por_cpf, 
    carregar_dados, salvar_dados, normalizar_texto, registrar_consulta_extrato,
    AGENCIA_PADRAO
)
from models import (
    ContaIterador, gerar_transacoes, criar_usuario_obj, criar_conta,
    verificar_reset_saques_diarios, depositar_obj, sacar_obj, transferir_obj
)

usuarios = []
contas = []
proximo_numero_conta = 1


def criar_usuario():
    """Cria um novo usuário via CLI interativo."""
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

    usuario = criar_usuario_obj(nome, cpf, data_nascimento, endereco)
    usuarios.append(usuario)
    salvar_dados(usuarios, contas, proximo_numero_conta)
    print("Usuário criado com sucesso!")
    return usuario


def criar_conta_cli():
    """Cria uma nova conta via CLI interativo."""
    global proximo_numero_conta
    
    if not usuarios:
        print("Cadastre um usuário antes de criar uma conta.")
        return

    usuario = None
    while not usuario:
        cpf = input("Informe o CPF do titular da conta: ")
        usuario = filtrar_usuario_por_cpf(usuarios, cpf)
        if not usuario:
            print("Usuário não encontrado. Tente novamente.")

    proximo_numero_conta = criar_conta(AGENCIA_PADRAO, proximo_numero_conta, usuario, contas, usuarios)
    print("Conta criada com sucesso! Número da conta:", proximo_numero_conta - 1)


def listar_contas(titulo="Contas cadastradas"):
    """Lista todas as contas cadastradas."""
    if not contas:
        print("Nenhuma conta cadastrada.")
        return

    print(f"\n==== {titulo} ====")
    for info in ContaIterador(contas):
        saldo_str = f"Saldo: R$ {info['saldo']:.2f}"
        print(
            f"Agência: {info['agencia']} | Conta: {info['numero_conta']} | Titular: {info['titular']} | {saldo_str}"
        )
    print("========================\n")


def selecionar_conta():
    """Permite ao usuário selecionar uma conta."""
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
        listar_contas(titulo="Contas filtradas")
    else:
        listar_contas()

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


def depositar():
    """Realiza depósito em uma conta."""
    conta = selecionar_conta()
    if not conta:
        return
    
    while True:
        try:
            valor = float(input("Informe o valor do depósito: "))
            resultado = depositar_obj(conta, valor, usuarios, contas)
            print(resultado)
            break
        except ValueError as e:
            print(f"Erro: {e}")
            continue


def sacar():
    """Realiza saque de uma conta."""
    conta = selecionar_conta()
    if not conta:
        return
    
    # Resetar saques diários se necessário
    if verificar_reset_saques_diarios(conta):
        print("Contador de saques diários foi resetado para um novo dia!")
        salvar_dados(usuarios, contas, proximo_numero_conta)
    
    while True:
        try:
            valor = float(input("Informe o valor do saque: "))
            resultado = sacar_obj(conta, valor, usuarios, contas)
            print(resultado)
            break
        except ValueError as e:
            print(f"Erro: {e}")
            continue


def transferir():
    """Realiza transferência entre contas."""
    print("\nSelecione a conta de origem:")
    conta_origem = selecionar_conta()
    if not conta_origem:
        return
    
    print("\nSelecione a conta de destino:")
    conta_destino = selecionar_conta()
    if not conta_destino:
        return
    
    while True:
        try:
            valor = float(input("Informe o valor da transferência: "))
            resultado = transferir_obj(conta_origem["numero_conta"], conta_destino["numero_conta"], valor, usuarios, contas)
            print(resultado)
            break
        except ValueError as e:
            print(f"Erro: {e}")
            continue


def exibir_extrato():
    """Exibe extrato de uma conta."""
    conta = selecionar_conta()
    if not conta:
        return
    
    # Registrar consulta de extrato no log
    numero_conta = conta.get("numero_conta")
    titular = conta.get("usuario", {}).get("nome", "Desconhecido")
    registrar_consulta_extrato(numero_conta, titular)
    
    print("\n================ EXTRATO ================")
    filtro = input("Deseja filtrar por tipo (depósito/saque/transferência)? Deixe vazio para todas: ").strip()
    filtro_normalizado = normalizar_texto(filtro) if filtro else None
    transacoes = list(gerar_transacoes(conta, filtro_normalizado))
    if not transacoes:
        print("Não foram realizadas movimentações." if not conta["extrato"] else "Nenhuma transação corresponde ao filtro.")
    else:
        for tx in transacoes:
            timestamp = tx.get("timestamp") or "----"
            tipo_tx = tx.get("tipo")
            valor = tx.get("valor")
            descricao = tx.get("descricao")
            valor_str = f"R$ {valor:.2f}" if isinstance(valor, (int, float)) else ""
            print(f"[{timestamp}] {tipo_tx}: {valor_str} {descricao}")
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


def main():
    """Loop interativo principal do CLI."""
    global usuarios, contas, proximo_numero_conta
    
    usuarios, contas, proximo_numero_conta = carregar_dados()

    while True:
        opcao = input(menu)

        if opcao == "u":
            criar_usuario()
        elif opcao == "c":
            criar_conta_cli()
        elif opcao == "d":
            depositar()
        elif opcao == "s":
            sacar()
        elif opcao == "t":
            transferir()
        elif opcao == "e":
            exibir_extrato()
        elif opcao == "l":
            listar_contas()
        elif opcao == "q":
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()
