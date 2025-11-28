# -*- coding: utf-8 -*-
"""Modelos de negócio - Lógica principal do sistema bancário."""

import re
from datetime import datetime
from utils import (
    log_transacao, filtrar_usuario_por_cpf, validar_cpf, validar_data,
    salvar_dados, normalizar_texto, AGENCIA_PADRAO, LIMITE_SAQUE, LIMITE_SAQUES_DIARIOS
)


class ContaIterador:
    """Iterador personalizado para percorrer as contas cadastradas."""
    def __init__(self, lista_contas):
        self._contas = list(lista_contas)
        self._indice = 0

    def __iter__(self):
        self._indice = 0
        return self

    def __next__(self):
        if self._indice >= len(self._contas):
            raise StopIteration
        conta = self._contas[self._indice]
        self._indice += 1
        usuario = conta.get("usuario", {})
        return {
            "numero_conta": conta.get("numero_conta"),
            "agencia": conta.get("agencia"),
            "titular": usuario.get("nome"),
            "cpf": usuario.get("cpf"),
            "saldo": conta.get("saldo", 0.0),
            "data_criacao": conta.get("data_criacao"),
        }


def gerar_transacoes(conta, tipo=None):
    """Gerador que percorre o extrato e opcionalmente filtra por tipo."""
    extrato = conta.get("extrato", "")
    if not extrato:
        return
    for linha in extrato.strip().splitlines():
        if not linha.strip():
            continue
        match = re.match(r"^\[(?P<timestamp>[^\]]+)\]\s*(?P<tipo>[^:]+):\s*(?P<rest>.+)$", linha)
        timestamp = match.group("timestamp") if match else None
        tipo_tx = match.group("tipo").strip() if match else "Transação"
        descricao = match.group("rest") if match else linha
        valor = None
        valor_match = re.search(r"R\$\s*([\d.,]+)", descricao)
        if valor_match:
            valor_texto = valor_match.group(1)
            if "." in valor_texto and "," in valor_texto:
                valor_texto = valor_texto.replace(".", "").replace(",", ".")
            else:
                valor_texto = valor_texto.replace(",", ".")
            try:
                valor = float(valor_texto)
                # Remove o valor da descrição para evitar duplicação
                descricao = re.sub(r"R\$\s*[\d.,]+", "", descricao).strip()
            except ValueError:
                valor = None
        transacao = {
            "timestamp": timestamp,
            "tipo": tipo_tx,
            "valor": valor,
            "descricao": descricao.strip(),
        }
        tipo_normalizado = normalizar_texto(tipo_tx)
        filtro_normalizado = normalizar_texto(tipo) if tipo else None
        if filtro_normalizado is None or tipo_normalizado.startswith(filtro_normalizado):
            yield transacao


def criar_usuario_obj(nome, cpf, data_nascimento, endereco):
    """Cria um novo objeto de usuário."""
    return {
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "endereco": endereco,
        "data_criacao": datetime.now().isoformat(),
    }


@log_transacao("Criação de Conta")
def criar_conta(agencia, numero_conta, usuario, contas, usuarios_ref):
    """Cria uma nova conta bancária para um usuário."""
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
    salvar_dados(usuarios_ref, contas, numero_conta + 1)
    return numero_conta + 1


def verificar_reset_saques_diarios(conta):
    """Verifica se deve resetar o contador de saques diários baseado na data."""
    hoje = datetime.now().date().isoformat()
    ultimo_reset = conta.get("ultimo_reset_saques", "")
    
    if ultimo_reset != hoje:
        conta["saques_realizados"] = 0
        conta["ultimo_reset_saques"] = hoje
        return True  # Foi resetado
    return False  # Não foi resetado


@log_transacao("Depósito")
def depositar_obj(conta, valor, usuarios, contas):
    """Realiza depósito em uma conta."""
    if valor <= 0:
        raise ValueError("Valor deve ser maior que zero.")
    
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    conta["saldo"] += valor
    conta["extrato"] += f"[{timestamp}] Depósito: R$ {valor:.2f}\n"
    salvar_dados(usuarios, contas, len(contas) + 1)
    return f"Depósito de R$ {valor:.2f} realizado com sucesso!"


@log_transacao("Saque")
def sacar_obj(conta, valor, usuarios, contas):
    """Realiza saque de uma conta."""
    if valor <= 0:
        raise ValueError("Valor deve ser maior que zero.")
    
    # Verificar se deve resetar saques diários
    verificar_reset_saques_diarios(conta)
    
    if valor > conta["saldo"]:
        raise ValueError("Saldo insuficiente.")
    
    if valor > LIMITE_SAQUE:
        raise ValueError(f"Limite de saque é R$ {LIMITE_SAQUE:.2f}")
    
    if conta["saques_realizados"] >= LIMITE_SAQUES_DIARIOS:
        raise ValueError("Limite de saques diários atingido.")
    
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    conta["saldo"] -= valor
    conta["extrato"] += f"[{timestamp}] Saque: R$ {valor:.2f}\n"
    conta["saques_realizados"] += 1
    salvar_dados(usuarios, contas, len(contas) + 1)
    return f"Saque de R$ {valor:.2f} realizado com sucesso!"


@log_transacao("Transferência")
def transferir_obj(numero_origem, numero_destino, valor, usuarios, contas):
    """Realiza transferência entre contas."""
    if valor <= 0:
        raise ValueError("Valor deve ser maior que zero.")
    
    if numero_origem == numero_destino:
        raise ValueError("Não é possível transferir para a mesma conta.")
    
    conta_origem = None
    conta_destino = None
    
    for conta in contas:
        if conta["numero_conta"] == numero_origem:
            conta_origem = conta
        if conta["numero_conta"] == numero_destino:
            conta_destino = conta
    
    if not conta_origem:
        raise ValueError("Conta de origem não encontrada.")
    
    if not conta_destino:
        raise ValueError("Conta de destino não encontrada.")
    
    if valor > conta_origem["saldo"]:
        raise ValueError("Saldo insuficiente.")
    
    timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    conta_origem["saldo"] -= valor
    conta_origem["extrato"] += f"[{timestamp}] Transferência enviada: R$ {valor:.2f} para Agência {conta_destino['agencia']} Conta {conta_destino['numero_conta']}\n"
    
    conta_destino["saldo"] += valor
    conta_destino["extrato"] += f"[{timestamp}] Transferência recebida: R$ {valor:.2f} de Agência {conta_origem['agencia']} Conta {conta_origem['numero_conta']}\n"
    
    salvar_dados(usuarios, contas, len(contas) + 1)
    return "Transferência realizada com sucesso!"
