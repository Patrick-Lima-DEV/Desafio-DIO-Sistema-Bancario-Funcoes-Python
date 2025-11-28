#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script de teste para demonstrar sistema de logging."""

import json
from pathlib import Path
from datetime import datetime
from utils import (
    validar_cpf, carregar_dados, registrar_consulta_extrato,
    ARQUIVO_DADOS, ARQUIVO_LOG
)

# Limpar arquivos anteriores se existirem
if ARQUIVO_DADOS.exists():
    ARQUIVO_DADOS.unlink()
if ARQUIVO_LOG.exists():
    ARQUIVO_LOG.unlink()

# Criar dados de teste
usuarios = [
    {
        "nome": "João Silva",
        "cpf": "12345678900",
        "data_nascimento": "15-06-1990",
        "endereco": "Rua das Flores, 123",
        "data_criacao": datetime.now().isoformat(),
    },
    {
        "nome": "Maria Santos",
        "cpf": "98765432100",
        "data_nascimento": "20-03-1985",
        "endereco": "Avenida Principal, 456",
        "data_criacao": datetime.now().isoformat(),
    }
]

contas = [
    {
        "agencia": "0001",
        "numero_conta": 1,
        "usuario": usuarios[0],
        "saldo": 1500.00,
        "extrato": "[28/11/2025 10:30:00] Depósito: R$ 1000.00\n[28/11/2025 14:15:00] Saque: R$ 500.00\n",
        "saques_realizados": 1,
        "data_criacao": datetime.now().isoformat(),
    },
    {
        "agencia": "0001",
        "numero_conta": 2,
        "usuario": usuarios[1],
        "saldo": 2500.00,
        "extrato": "[28/11/2025 09:00:00] Depósito: R$ 2500.00\n",
        "saques_realizados": 0,
        "data_criacao": datetime.now().isoformat(),
    }
]

# Salvar dados
dados = {
    "usuarios": usuarios,
    "contas": contas,
    "proximo_numero_conta": 3
}
with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=2)

print("✓ Dados de teste criados")

# Registrar consultas de extrato
registrar_consulta_extrato(1, "João Silva")
registrar_consulta_extrato(2, "Maria Santos")
registrar_consulta_extrato(1, "João Silva")

print("✓ Consultas de extrato registradas")

# Exibir conteúdo do log
print("\n" + "="*80)
print("CONTEÚDO DO LOG.TXT:")
print("="*80)

if ARQUIVO_LOG.exists():
    with open(ARQUIVO_LOG, "r", encoding="utf-8") as f:
        conteudo = f.read()
        print(conteudo)
else:
    print("Arquivo log.txt não encontrado")

print("="*80)
print("\n✓ Teste concluído!\n")
print("Observações:")
print("  • Cada consulta de extrato é registrada com timestamp, número da conta e titular")
print("  • O CPF é mascarado (formato: 123.***.***-**)")
print("  • O nome do titular é exibido completamente para auditoria")
print("  • Os dados sensíveis são mascarados para segurança")
