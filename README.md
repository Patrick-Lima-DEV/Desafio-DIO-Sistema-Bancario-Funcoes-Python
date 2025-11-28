# Desafio-DIO-Sistema-Bancario-Funcoes-Python

[![GitHub code size](https://img.shields.io/github/languages/code-size/Patrick-Lima-DEV/Desafio-DIO-Sistema-Bancario-Funcoes-Python?style=for-the-badge)](https://github.com/Patrick-Lima-DEV/Desafio-DIO-Sistema-Bancario-Funcoes-Python)
[![Status](https://img.shields.io/badge/status-completo-success?style=for-the-badge)](https://github.com/Patrick-Lima-DEV/Desafio-DIO-Sistema-Bancario-Funcoes-Python)

> Sistema bancário em Python criado para o desafio da DIO. O script roda no terminal e em interface gráfica, permite cadastrar usuários e executar depósitos, saques com regras específicas e emitir extratos usando funções claras e reutilizáveis. Inclui sistema robusto de logging com auditoria e conformidade LGPD.

## 📑 Sumário
1. [Visão Geral](#visão-geral)
2. [Funcionalidades](#funcionalidades)
3. [Arquitetura Modular](#arquitetura-modular)
4. [Sistema de Logging](#sistema-de-logging)
5. [Pré-requisitos](#pré-requisitos)
6. [Execução](#execução)
7. [Menu Interativo (CLI)](#menu-interativo-cli)
8. [Interface Gráfica (GUI)](#interface-gráfica-gui)
9. [Testes](#testes)
10. [Próximos Passos](#próximos-passos)

---

## 🎯 Visão Geral

Este projeto demonstra controle de fluxo, modularização e persistência em Python, simulando um fluxo básico de conta bancária com dados salvos em arquivo JSON entre sessões. A arquitetura foi refatorada para eliminar duplicação de código (~250 linhas), melhorando manutenibilidade e testabilidade.

### Arquitetura Modular
```
utils.py (168 linhas)      ← Funções comuns, validações, logging
├── validar_cpf()
├── validar_data()
├── mascarar_dados_sensiveis()
├── registrar_consulta_extrato()
└── log_transacao (decorator)

models.py (171 linhas)     ← Lógica de negócio
├── criar_conta()
├── depositar_obj()
├── sacar_obj()
├── transferir_obj()
├── ContaIterador
└── gerar_transacoes()

sistema_bancario.py        ← CLI (212 linhas)
sistema_bancario_gui.py    ← GUI Tkinter (570 linhas)
test_sistema_bancario.py   ← Testes (20/20 ✅)
```

---

## ✨ Funcionalidades

### Operações Principais
- **Criar usuário**: Cadastro com nome, CPF validado por algoritmo verificador (único na sessão), data de nascimento (formato dd-mm-aaaa) e endereço completo
- **Criar conta**: Vincula um usuário existente a uma conta (agência fixa "0001", número sequencial iniciando em 1) antes de operar
- **Listar contas**: Mostra todas as contas cadastradas (agência, conta, titular e saldo atual)
- **Depósito**: Registra valores positivos no extrato com timestamp e ajusta o saldo
- **Saque**: Aplica validações de limite por operação (R$ 500,00), número máximo de saques por **dia** (3) com **reset automático diário**, e saldo disponível
- **Transferência**: Permite transferir valores entre contas com validações de saldo e contas diferentes
- **Extrato**: Exibe movimentações anteriores com timestamp, filtro por tipo (depósito/saque/transferência) e saldo atual

### Recursos Avançados
- **Decoradores**: Log automático de transações com timestamp e duração
- **Geradores**: Iteração eficiente sobre transações do extrato com filtro por tipo
- **Iteradores personalizados**: Classe `ContaIterador` para percorrer contas cadastradas
- **Persistência**: Usuários e contas salvos automaticamente em arquivo JSON (compartilhado entre CLI e GUI)
- **Testes robustos**: Suite completa com pytest (20/20 testes passando)
- **Validações robustas**: CPF com algoritmo verificador, data em formato correto, valores positivos
- **Interface Gráfica**: Aplicação Tkinter com menu intuitivo, janelas dedicadas, layout responsivo e design moderno

---

## 🔐 Sistema de Logging

### Recursos de Segurança

#### 1. Mascaramento de Dados Sensíveis
```
Dado Original           Mascarado
─────────────────────────────────────
CPF: 12345678900   →   123.***.***-**
Valores: 1234567  →    ****
Endereço: Rua ABC →    Rua ****
```

**Função:** `mascarar_dados_sensiveis()`
- CPF: Mostra apenas os 3 primeiros dígitos
- Valores/Saldos: Substitui números com 4+ dígitos por ****
- Endereços: Remove detalhes completos

#### 2. Logging de Todas as Operações

**Formato de Log:**
```
[TIMESTAMP] FUNÇÃO | TIPO_TRANSAÇÃO | INFORMAÇÕES | STATUS | DURAÇÃO
```

**Exemplos:**
```
[2025-11-28 10:59:43.190] depositar | Depósito | conta=1 titular=João Silva | OK | 0.145s
[2025-11-28 10:59:44.320] sacar | Saque | conta=1 titular=João Silva | OK | 0.082s
[2025-11-28 10:59:45.100] transferir | Transferência | conta=1 titular=João Silva | OK | 0.127s
[2025-11-28 10:59:48.200] consulta_extrato | Consulta de Extrato | conta=1 titular=João Silva | OK | 0.000s
```

#### 3. O Que É Registrado?

| Operação | Registrado | Status |
|----------|-----------|--------|
| Criar Usuário | ✅ | Timestamp, dados mascarados, status |
| Criar Conta | ✅ | Timestamp, conta criada, titular |
| Depósito | ✅ | Conta, titular, valor, duração |
| Saque | ✅ | Conta, titular, valor, motivo erro |
| Transferência | ✅ | Contas origem/destino, valor, titular |
| Consulta Extrato | ✅ | Conta, titular, timestamp |

### Conformidade LGPD
- ✅ Não armazena dados sensíveis completos
- ✅ Mascaramento automático de CPF
- ✅ Nomes para auditoria (propósito legítimo)
- ✅ Rastreabilidade de acessos
- ✅ Timestamps precisos para investigação forense

---

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Terminal que aceite a função `input()`
- pytest (opcional, para rodar testes)

---

## 🚀 Execução

### Terminal (CLI)
```bash
python sistema_bancario.py
```

### Interface Gráfica (GUI com Tkinter)
```bash
python sistema_bancario_gui.py
```

### Testes
```bash
pytest test_sistema_bancario.py -q
# Resultado: 20 passed in 0.04s
```

---

## 📌 Menu Interativo (CLI)

Durante a execução, use as opções:
- `u` - Criar novo usuário (CPF validado e único)
- `c` - Criar conta para usuário existente
- `l` - Listar todas as contas cadastradas
- `d` - Depositar valor e registrar no extrato
- `s` - Sacar com validações de limite e saldo
- `t` - Transferir entre contas
- `e` - Exibir extrato completo com filtros
- `q` - Sair do sistema

### Filtro de Contas
Ao operar (d, s, t, e), o sistema pergunta se deseja filtrar por CPF para exibir apenas as contas do titular antes de solicitar o número da conta.

---

## 🎨 Interface Gráfica (GUI)

A aplicação Tkinter oferece:
- **Menu Principal**: Botões coloridos para acesso direto a todas operações
- **Criar Usuário**: Formulário com validações visuais
- **Criar Conta**: Vinculação simples a usuários existentes
- **Listar Contas**: Visualização em tabela com agência, número, titular e saldo
- **Operações**: Formulários dedicados para depósito, saque e transferência
- **Extrato**: Área de texto scrollável com movimentações e filtros
- **Design Moderno**: Cores, efeitos de hover e feedback visual

Os dados são compartilhados entre CLI e GUI, permitindo alternar entre as duas interfaces.

---

## 🧪 Testes

```bash
pytest test_sistema_bancario.py -q
```

**Cobertura:**
- ✅ Validação de CPF (válidos e inválidos)
- ✅ Validação de Data
- ✅ Criar usuários e contas
- ✅ Operações de depósito, saque e transferência
- ✅ Limites de saque (R$ 500 por operação, 3 por dia)
- ✅ Resets automáticos diários
- ✅ Extratos com filtros

**Resultado:** 20/20 testes passando ✅

---

## 📁 Estrutura do Projeto

```
desafio_bancario/
├── utils.py                 # Funções comuns (validações, logging)
├── models.py                # Lógica de negócio
├── sistema_bancario.py      # Interface CLI
├── sistema_bancario_gui.py  # Interface GUI (Tkinter)
├── test_sistema_bancario.py # Testes unitários
├── README.md                # Este arquivo
└── .gitignore               # Configuração Git
```

---

## 🔄 Refatoração Realizada

### Melhorias Implementadas
- ✅ Extração de 250+ linhas de código duplicado
- ✅ Criação de `utils.py` com funções comuns
- ✅ Consolidação de lógica em `models.py`
- ✅ Simplificação de CLI e GUI
- ✅ Sistema robusto de logging com auditoria
- ✅ Mascaramento automático de dados sensíveis

### Resultados
- **Redução:** ~119 linhas (8.6% do código)
- **Manutenibilidade:** Melhorada com arquitetura modular
- **Testabilidade:** 20/20 testes passando
- **Segurança:** LGPD compliant com mascaramento

---

## 🚀 Próximos Passos

- [ ] Autenticação com senha/PIN
- [ ] Melhorias na GUI (relatórios, gráficos)
- [ ] Versão Web com Flask/Django
- [ ] Rotação automática de logs
- [ ] Dashboard de auditoria
- [ ] Exportação de dados (CSV/PDF)
- [ ] Criptografia de logs sensíveis

---

## 👥 Contribuição

1. Faça um fork do repositório
2. Crie uma branch com o novo recurso (`git checkout -b feature/nome-da-feature`)
3. Faça suas alterações e adicione testes
4. Abra um pull request descrevendo as mudanças

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](https://opensource.org/licenses/MIT).

---

**Última Atualização:** 28 de novembro de 2025
