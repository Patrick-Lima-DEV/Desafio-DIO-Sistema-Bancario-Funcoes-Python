# Desafio-DIO-Sistema-Bancario-Funcoes-Python

[![GitHub code size](https://img.shields.io/github/languages/code-size/Patrick-Lima-DEV/Desafio-DIO-Sistema-Bancario-Funcoes-Python?style=for-the-badge)](https://github.com/Patrick-Lima-DEV/Desafio-DIO-Sistema-Bancario-Funcoes-Python)
[![Status](https://img.shields.io/badge/status-completo-success?style=for-the-badge)](https://github.com/Patrick-Lima-DEV/Desafio-DIO-Sistema-Bancario-Funcoes-Python)

> Sistema bancario em Python criado para o desafio da DIO. O script roda no terminal, permite cadastrar usuarios e executar depositos, saques com regras especificas e emitir extratos usando funcoes claras e reutilizaveis.

## Sumario
1. [Visao geral](#visao-geral)
2. [Funcionalidades](#funcionalidades)
3. [Pre-requisitos](#pre-requisitos)
4. [Execucao](#execucao)
5. [Menu interativo](#menu-interativo)
6. [Estrutura do projeto](#estrutura-do-projeto)
7. [Proximos passos](#proximos-passos)
8. [Contribuicao](#contribuicao)
9. [Licenca](#licenca)

## Visao geral
Este projeto demonstra controle de fluxo, modularizacao e persistencia em Python, simulando um fluxo basico de conta bancaria com dados salvos em arquivo JSON entre sessoes.

## Funcionalidades
- Criar usuario: cadastro com nome, CPF validado por algoritmo verificador (unico na sessao), data de nascimento (formato dd-mm-aaaa) e endereco completo.
- Criar conta: vincula um usuario existente a uma conta (agencia fixa "0001", numero sequencial iniciando em 1) antes de operar.
- Listar contas: mostra todas as contas cadastradas (agencia, conta, titular e saldo atual) para facilitar selecao.
- Deposito: registra valores positivos no extrato com timestamp e ajusta o saldo.
- Saque: aplica validacoes de limite por operacao (R$ 500,00), numero maximo de saques por sessao (3) e saldo disponivel. Registra timestamp.
- Transferencia: permite transferir valores entre contas com validacoes de saldo e contas diferentes. Registra timestamp em ambas.
- Extrato: exibe movimentacoes anteriores com timestamp e o saldo atual formatado como moeda.
- Persistencia: usuarios e contas sao salvos automaticamente em arquivo JSON (dados_bancarios.json) e carregados na proxima sessao.
- Testes: suite completa com pytest para validar funcoes principais.
- Entrada robusta: quando uma validacao falha (CPF, data, valor), o programa pede a entrada do campo especifico novamente, sem perder os dados anteriores.

## Contas
As contas ficam armazenadas em uma lista `contas` e cada registro armazena `agencia` (valor fixo "0001"), `numero_conta` sequencial iniciando em 1, `usuario` (dicionario do titular), `saldo`, `extrato` e contador de saques do dia.
Um usuario pode ter mais de uma conta, mas cada conta pertence a somente um usuario.

## Pre-requisitos
- Python 3.8 ou superior.
- Terminal que aceite a funcao `input()` (PowerShell, Prompt, terminal integrado etc.).
- pytest (opcional, para rodar testes).

## Execucao
```
git clone https://github.com/Patrick-Lima-DEV/Desafio-DIO-Sistema-Bancario-Funcoes-Python.git
cd Desafio-DIO-Sistema-Bancario-Funcoes-Python
python sistema_bancario.py
```

## Menu interativo
Durante a execucao, responda as opcoes exibidas:
- `u` criar novo usuario (CPF validado por algoritmo verificador, unico por sessao).
- `c` criar conta para um usuario existente.
- `l` listar todas as contas cadastradas (agencia, conta, titular e saldo atual).
- `d` depositar valor positivo e registrar no extrato com timestamp.
- `s` sacar respeitando saldo, limite de saque e limite diario. Registra com timestamp.
- `t` transferir entre contas com timestamp em ambas.
- `e` exibir o extrato completo com timestamp de cada operacao e o saldo atual.
- `q` sair do sistema.

Ao selecionar uma conta para operar (opcoes `d`, `s`, `t` ou `e`), o programa pergunta se deseja filtrar contas por CPF; ao aceitar, apenas as contas daquele titular sao exibidas antes de solicitar o numero da conta.

## Estrutura do projeto
- `sistema_bancario.py`: concentra as funcoes principais e loop do menu ativo. Salva/carrega dados automaticamente em `dados_bancarios.json`.
- `test_sistema_bancario.py`: testes unitarios com pytest para validar validacoes, operacoes de usuario/conta e transferencias.
- `dados_bancarios.json`: arquivo gerado automaticamente com persistencia de dados entre sessoes.

## Testes
```
pytest test_sistema_bancario.py -v
```

## Proximos passos
- Associar movimentacoes a contas especificas (multiusuario).
- Adicionar autenticacao com senha/PIN.
- Criar interface grafica (Tkinter ou Web) ou CLI mais elaborada para melhorar a usabilidade.

## Contribuicao
1. Faca um fork do repositorio.
2. Crie uma branch com o novo recurso (`git checkout -b feature/nome-da-feature`).
3. Faca suas alteracoes e adicione testes sempre que necessario.
4. Abra um pull request descrevendo as mudancas implementadas.

## Licenca
Este projeto esta licenciado sob a [MIT License](https://opensource.org/licenses/MIT).
