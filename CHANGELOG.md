# Changelog - Melhorias Aplicadas

## Versão 2.1 - Melhorias de UX

### Entrada Robusta com Loops de Validação (Melhoria Adicional)

**Problema anterior:**
Quando uma validação falhava (CPF inválido, data errada, valor negativo), o usuário perdia todos os dados e precisava reentrar tudo novamente.

**Solução implementada:**
Cada campo agora usa `while True` com loops de validação específicos. Se um campo falhar, apenas aquele campo é solicitado novamente.

**Campos afetados:**
- `criar_usuario()`: CPF e data em loops independentes
- `criar_conta()`: CPF do titular em loop
- `selecionar_conta()`: número da conta em loop
- `depositar()`: valor em loop
- `sacar()`: valor em loop com tratamento de limites
- `transferir()`: valor em loop

**Exemplo de experiência melhorada:**
```
Antes (perderia dados):
Informe o CPF: 12345678901
CPF inválido! Operação falhou.
[retorna ao menu, precisa começar tudo novamente]

Depois (continua de onde parou):
Informe o CPF: 12345678901
CPF inválido! Tente novamente.
Informe o CPF: 11144477735
[aceita e continua com a data]
```

**Benefícios:**
- Experiência de usuário melhorada
- Menos frustração
- Entrada corrigida sem perder contexto
- Código mais intuitivo

---

## Versão 2.0 - 5 Melhorias Principais

### 1. Persistência em JSON (Melhoria #1)

**Arquivos modificados:** `sistema_bancario.py`

**Adições:**
- Importação de `json`, `re`, `datetime` e `pathlib`
- Constante `ARQUIVO_DADOS = Path("dados_bancarios.json")`
- Função `salvar_dados()` - salva usuários, contas e próximo número de conta em JSON
- Função `carregar_dados()` - carrega dados persistidos ao iniciar o programa
- Chamada `carregar_dados()` no início do loop principal

**Benefícios:**
- Dados persistem entre sessões
- Arquivo JSON legível e editável manualmente se necessário
- Carregamento automático ao iniciar

---

### 2. Validações de CPF e Data (Melhoria #2)

**Arquivos modificados:** `sistema_bancario.py`

**Adições:**
- Função `validar_cpf(cpf)` - valida CPF com algoritmo verificador (MOD 11)
  - Verifica se tem exatamente 11 dígitos
  - Rejeita CPFs com todos os dígitos iguais
  - Calcula dígitos verificadores corretamente
- Função `validar_data(data_str)` - valida data no formato dd-mm-aaaa
- Integração das validações em `criar_usuario()`

**Benefícios:**
- CPFs inválidos são rejeitados antes do cadastro
- Datas de nascimento são validadas quanto ao formato e validade
- Segurança e integridade dos dados

---

### 3. Testes Unitários com Pytest (Melhoria #3)

**Arquivo criado:** `test_sistema_bancario.py`

**Conteúdo:**
- Classe `TestValidacoes` - 8 testes para validações de CPF e data
- Classe `TestUsuarios` - 2 testes para operações com usuários
- Classe `TestContas` - 8 testes para operações de contas e saques
- Classe `TestTransferencia` - 3 testes para validações de transferência

**Total:** 21 testes cobrindo:
- Validação de CPF (válido, inválido, dígitos iguais)
- Validação de data (válida, inválida)
- Criação de usuários e busca
- Operações de depósito, saque e limites
- Transferência entre contas

**Como executar:**
```bash
pytest test_sistema_bancario.py -v
```

---

### 4. Logs com Timestamps (Melhoria #6)

**Arquivos modificados:** `sistema_bancario.py`

**Adições:**
- Campo `"data_criacao"` em usuários (formato ISO)
- Campo `"data_criacao"` em contas (formato ISO)
- Timestamp em cada movimentação no extrato
- Formato: `[dd/mm/aaaa HH:MM:SS] Operação`

**Exemplos de registros com timestamp:**
```
[21/11/2025 14:30:15] Depósito: R$ 1000.00
[21/11/2025 14:31:22] Saque: R$ 200.00
[21/11/2025 14:32:45] Transferência enviada: R$ 500.00 para Agência 0001 Conta 2
[21/11/2025 14:33:10] Transferência recebida: R$ 500.00 de Agência 0001 Conta 1
```

**Benefícios:**
- Rastreabilidade completa de operações
- Data e hora exatas de cada transação
- Auditoria facilitada

---

### 5. Transferência entre Contas (Melhoria #5)

**Arquivos modificados:** `sistema_bancario.py`

**Adições:**
- Função `transferir(contas)` - realiza transferência entre contas
- Nova opção `[t]` no menu interativo
- Validações:
  - Contas diferentes
  - Valor positivo
  - Saldo suficiente
  - Registro com timestamp em ambas as contas

**Fluxo da transferência:**
1. Seleciona conta de origem
2. Seleciona conta de destino
3. Valida se são contas diferentes
4. Solicita valor
5. Valida valor e saldo
6. Debita de origem, credita em destino
7. Registra em ambos os extratos com timestamp
8. Salva dados

**Benefícios:**
- Novas funcionalidades operacionais
- Rastreamento em ambas as contas
- Segurança com validações

---

## Compatibilidade

- ✅ Python 3.8+
- ✅ Sem mudanças quebradoras na API
- ✅ Código original mantido funcional
- ✅ Todas as operações anteriores continuam funcionando

---

## Arquivos Modificados

1. `sistema_bancario.py` - código principal (+200 linhas com melhorias)
2. `README.md` - documentação atualizada
3. `test_sistema_bancario.py` - novo arquivo com testes
4. `dados_bancarios.json` - criado automaticamente na primeira execução

---

## Próximas Melhorias Possíveis

- Autenticação com senha/PIN
- Interface gráfica (Tkinter/Web)
- Suporte a múltiplos usuários simultâneos
- Banco de dados real (SQLite/PostgreSQL)
- API REST com Flask/FastAPI
- Relatórios e analytics
