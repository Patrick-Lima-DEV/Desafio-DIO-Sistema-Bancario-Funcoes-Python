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
Este projeto demonstra controle de fluxo e modularizacao em Python, simulando um fluxo basico de conta bancaria, sem dependencias externas ou bancos de dados  todo o estado fica em memoria.

## Funcionalidades
- Criar usuario: cadastro com nome, CPF (unico na sessao), data de nascimento e endereco completo.
- Criar conta: vincula um usuario existente a uma conta (agencia fixa "0001", numero sequencial iniciando em 1) antes de operar.
- Deposito: registra valores positivos no extrato e ajusta o saldo.
- Saque: aplica validacoes de limite por operacao (R$ 500,00), numero maximo de saques por sessao (3) e saldo disponivel.
- Extrato: exibe movimentacoes anteriores e o saldo atual formatado como moeda.
- Encerramento: finaliza o programa exibindo o extrato gerado durante a sessao.

## Contas
As contas ficam armazenadas em uma lista `contas` e cada registro armazena `agencia` (valor fixo "0001"), `numero_conta` sequencial iniciando em 1, `usuario` (dicionario do titular), `saldo`, `extrato` e contador de saques do dia.
Um usuario pode ter mais de uma conta, mas cada conta pertence a somente um usuario.

## Pre-requisitos
- Python 3.12 ou superior (qualquer 3.8+ funciona).
- Terminal que aceite a funcao `input()` (PowerShell, Prompt, terminal integrado etc.).

## Execucao
```
git clone https://github.com/Patrick-Lima-DEV/Desafio-DIO-Sistema-Bancario-Funcoes-Python.git
cd Desafio-DIO-Sistema-Bancario-Funcoes-Python
python sistema_bancario.py
```

## Menu interativo
Durante a execucao, responda as opcoes exibidas:
- `u` criar novo usuario (CPF unico por sessao).
- `d` depositar valor positivo e registrar o extrato.
- `s` sacar respeitando saldo, limite de saque e limite diario.
- `e` exibir o extrato completo e o saldo atual.
- `q` sair do sistema.

## Estrutura do projeto
- `sistema_bancario.py`: concentra as funcoes `criar_usuario`, `depositar`, `sacar` e `exibir_extrato`, alem do loop principal que mantem o menu ativo.

## Proximos passos
- Persistir usuarios e transacoes em arquivo ou banco de dados.
- Associar movimentacoes a contas especificas (multiusuario).
- Adicionar testes automatizados para cada funcao do sistema.
- Criar interface grafica (Tkinter ou Web) ou CLI mais elaborada para melhorar a usabilidade.

## Contribuicao
1. Faca um fork do repositorio.
2. Crie uma branch com o novo recurso (`git checkout -b feature/nome-da-feature`).
3. Faca suas alteracoes e adicione testes sempre que necessario.
4. Abra um pull request descrevendo as mudancas implementadas.

## Licenca
Este projeto esta licenciado sob a [MIT License](https://opensource.org/licenses/MIT).
