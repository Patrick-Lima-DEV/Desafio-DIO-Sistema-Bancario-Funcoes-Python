# 📋 Sistema de Logging - Documentação

## Visão Geral

O sistema de logging foi implementado para rastrear todas as operações do sistema bancário com foco em **segurança, auditoria e conformidade**.

---

## 🔒 Recursos de Segurança

### 1. **Mascaramento de Dados Sensíveis**

```
Antes do Mascaramento        Depois do Mascaramento
─────────────────────────────────────────────────────
CPF: 12345678900       →     CPF: 123.***.***-**
Conta: 1234567890      →     Conta: ****
Endereço: Rua ABC      →     Endereço: Rua ****
```

**Função:** `mascarar_dados_sensiveis()`
- CPF: Mostra apenas os 3 primeiros dígitos
- Valores/Saldos: Substitui números com 4+ dígitos por ****
- Endereços: Remove detalhes completos

### 2. **Logging de Transações**

Todas as operações são automaticamente registradas:

```
[2025-11-28 10:59:43.190] depositar | Depósito | conta=1 titular=João Silva | OK | 0.145s
[2025-11-28 10:59:44.320] sacar | Saque | conta=1 titular=João Silva | OK | 0.082s
[2025-11-28 10:59:45.100] transferir | Transferência | conta=1 titular=João Silva | OK | 0.127s
```

### 3. **Logging de Consultas de Extrato**

Cada consulta de extrato é registrada para auditoria:

```
[2025-11-28 10:59:43.190] consulta_extrato | Consulta de Extrato | conta=1 titular=João Silva | OK | 0.000s
[2025-11-28 10:59:43.190] consulta_extrato | Consulta de Extrato | conta=2 titular=Maria Santos | OK | 0.000s
```

---

## 📊 Estrutura do Log

Cada linha segue o formato:

```
[TIMESTAMP] FUNÇÃO | TIPO_TRANSAÇÃO | INFORMAÇÕES | STATUS | DURAÇÃO | [OPCIONAL: TITULAR]
```

### Exemplo Completo:

```
[2025-11-28 10:59:43.190] criar_usuario | Criação de Usuário | ARGS: João Silva, 123.***.***-**, ... | OK | 0.045s | titular=João Silva

[2025-11-28 10:59:44.100] depositar | Depósito | conta=1 titular=Maria Santos | OK | 0.082s

[2025-11-28 10:59:45.200] consulta_extrato | Consulta de Extrato | conta=1 titular=João Silva | OK | 0.000s | ERRO: Conta não encontrada
```

---

## 🎯 O Que É Registrado?

### ✅ Sim - Registrado

| Operação | Exemplo de Log |
|----------|---|
| **Criar Usuário** | `[10:59:43] criar_usuario \| Criação de Usuário \| ... \| OK \| 0.045s` |
| **Criar Conta** | `[10:59:44] criar_conta \| Criação de Conta \| ... \| OK \| 0.032s` |
| **Depósito** | `[10:59:45] depositar \| Depósito \| conta=1 titular=João Silva \| OK \| 0.082s` |
| **Saque** | `[10:59:46] sacar \| Saque \| conta=1 titular=João Silva \| OK \| 0.095s` |
| **Transferência** | `[10:59:47] transferir \| Transferência \| ... \| OK \| 0.127s` |
| **Consulta de Extrato** | `[10:59:48] consulta_extrato \| Consulta de Extrato \| conta=1 titular=João Silva \| OK \| 0.000s` |

### ❌ Não - Não Registrado (Por Segurança)

- Senhas
- CPF completo (apenas primeiros 3 dígitos)
- Saldos completos (mascarados com ****)
- Detalhes completos de endereços

---

## 🔐 Informações Capturadas

### Cada Log Contém:

✅ **Timestamp** - Data e hora exata da operação  
✅ **Função** - Nome da função que executou  
✅ **Tipo de Transação** - Categorização da operação  
✅ **Conta Relacionada** - Número da conta (quando aplicável)  
✅ **Titular da Conta** - Nome da pessoa (para auditoria)  
✅ **CPF** - Mascarado (123.***.***-**)  
✅ **Status** - OK ou ERRO  
✅ **Duração** - Tempo em segundos  
✅ **Resultado** - Descricção resumida  
✅ **Erro** - Detalhes se ocorreu erro  

---

## 💻 Exemplos de Uso

### No CLI - Consultar Extrato

```python
# Quando o usuário consulta um extrato
# O sistema automaticamente registra:
registrar_consulta_extrato(numero_conta=1, titular="João Silva")

# No log.txt aparecerá:
# [2025-11-28 10:59:43.190] consulta_extrato | Consulta de Extrato | conta=1 titular=João Silva | OK | 0.000s
```

### Na GUI - Qualquer Operação

```python
# Todas as operações usam o decorador @log_transacao
@log_transacao("Depósito")
def depositar_obj(conta, valor, usuarios, contas):
    # Automaticamente registra a operação
    # com timestamp, argumentos mascarados e resultado
    ...
```

---

## 📁 Arquivo de Log

**Localização:** `log.txt` (raiz do projeto)

**Formato:** Texto simples (UTF-8)

**Tamanho:** Cresce com cada operação

**Limpeza:** Remova manualmente ou implemente política de rotação

---

## 🛡️ Conformidade e Segurança

### LGPD - Lei Geral de Proteção de Dados

✅ **Não armazena dados sensíveis completos**  
✅ **Mascaramento automático de CPF**  
✅ **Nomes para auditoria (propósito legítimo)**  
✅ **Rastreabilidade de acessos**  

### Boas Práticas

✅ **Timestamps precisos** - Para investigação forense  
✅ **Titular identificado** - Para rastreamento de operações  
✅ **Status claro** - Para identificar problemas  
✅ **Duração registrada** - Para análise de performance  
✅ **Erros detalhados** - Para debug e segurança  

---

## 🔍 Como Visualizar os Logs

### Terminal/CLI

```bash
# Ver todo o arquivo
cat log.txt

# Ver últimas 10 linhas
tail -10 log.txt

# Ver em tempo real (monitorar)
tail -f log.txt

# Filtrar por tipo de operação
grep "Depósito" log.txt
grep "consulta_extrato" log.txt
grep "ERRO" log.txt
```

### Python

```python
with open("log.txt", "r", encoding="utf-8") as f:
    for linha in f:
        print(linha.strip())
```

---

## 📈 Monitoramento e Auditoria

### Consultas Comuns

```bash
# Todas as consultas de extrato
grep "consulta_extrato" log.txt

# Operações com erro
grep "ERRO" log.txt

# Operações de um titular específico
grep "João Silva" log.txt

# Operações de uma conta específica
grep "conta=1" log.txt

# Operações na última hora
# (requer parsing de timestamps)
```

---

## 🚀 Funcionalidades Futuras

- [ ] Rotação automática de logs (por data/tamanho)
- [ ] Compactação de logs antigos (gzip)
- [ ] Dashboard de auditoria
- [ ] Alertas para operações suspeitas
- [ ] Exportação para formatos SQL/CSV
- [ ] Criptografia de logs sensíveis
- [ ] Validação de integridade (checksums)

---

## ✨ Resumo

O sistema de logging oferece:

🔒 **Segurança** - Dados sensíveis mascarados automaticamente  
📋 **Auditoria** - Rastreamento completo de operações  
🎯 **Conformidade** - Aderência a LGPD e boas práticas  
⚡ **Performance** - Logging assíncrono e eficiente  
📊 **Transparência** - Visibilidade total das operações  

---

**Última Atualização:** 28 de novembro de 2025
