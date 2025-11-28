#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Teste para verificar carregamento de dados na GUI."""

from utils import carregar_dados

print('Testando carregamento de dados...')
usuarios_test, contas_test, proximo_test = carregar_dados()

print(f'✅ Usuários carregados: {len(usuarios_test)}')
print(f'✅ Contas carregadas: {len(contas_test)}')
print(f'✅ Próximo número de conta: {proximo_test}')

if usuarios_test:
    print('\nUsuários:')
    for u in usuarios_test:
        print(f'  - {u["nome"]} (CPF: {u["cpf"]})')

if contas_test:
    print('\nContas:')
    for c in contas_test:
        print(f'  - Conta {c["numero_conta"]}: {c["usuario"]["nome"]} - Saldo: R$ {c["saldo"]:.2f}')
else:
    print('\n❌ Nenhuma conta carregada!')
