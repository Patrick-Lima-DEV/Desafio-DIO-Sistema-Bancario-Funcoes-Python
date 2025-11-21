================================================================================
                 MELHORIA DE UX - LOOPS DE VALIDAÇÃO
================================================================================

Data: 21 de novembro de 2025
Versão: 2.1
Status: Implementado

================================================================================
PROBLEMA IDENTIFICADO
================================================================================

Quando um usuário digitava algo inválido durante o cadastro de usuário:
- CPF inválido
- Data de nascimento com formato errado
- Valor negativo em operações

O programa retornava mensagem de erro e saía da função, perdendo todos os 
dados já inseridos. O usuário precisava começar do zero novamente.

EXEMPLO DO PROBLEMA:
┌─────────────────────────────────────────────────────────────────┐
│ Informe o nome completo: Patrick Oliveira                       │
│ Informe o CPF (somente números): [REMOVIDO_POR_PRIVACIDADE] (CPF real inválido)│
│ CPF inválido! Operação falhou.                                  │
│ [retorna ao menu - PERDEU O NOME DIGITADO]                      │
│ [usuário deve digitar tudo novamente]                           │
└─────────────────────────────────────────────────────────────────┘

================================================================================
SOLUÇÃO IMPLEMENTADA
================================================================================

Cada campo agora usa um loop `while True` que:
1. Pede a entrada do usuário
2. Valida o valor
3. Se inválido: exibe mensagem específica e pede novamente
4. Se válido: sai do loop e continua com próximo campo
5. Dados já inseridos são mantidos

EXEMPLO DA MELHORIA:
┌─────────────────────────────────────────────────────────────────┐
│ Informe o nome completo: Patrick Oliveira                       │
│ Informe o CPF (somente números): [REMOVIDO_POR_PRIVACIDADE]                    │
│ CPF inválido! Tente novamente.                                  │
│ Informe o CPF (somente números): 11144477735                    │
│ [aceita e continua]                                             │
│ Informe a data de nascimento (dd-mm-aaaa): 23-11-1990           │
│ [aceita e continua]                                             │
│ [usuário NÃO perdeu nada de oq digitou antes]                   │
└─────────────────────────────────────────────────────────────────┘

================================================================================
CAMPOS AFETADOS
================================================================================

1. criar_usuario():
   ✓ CPF em loop: tenta repetidas vezes até válido e único
   ✓ Data em loop: tenta repetidas vezes até formato válido
   ✓ Nome e endereço: entrada única (sem validação necessária)

2. criar_conta():
   ✓ CPF do titular em loop: tenta até encontrar usuário

3. selecionar_conta():
   ✓ Número da conta em loop: tenta até encontrar ou usuário cancelar

4. depositar():
   ✓ Valor em loop: tenta até valor > 0

5. sacar():
   ✓ Valor em loop: tenta até valor > 0
   ✓ Trata limites: saldo, limite por operação, limite diário
   ✓ Se saldo/limite falhar, pede valor novamente

6. transferir():
   ✓ Valor em loop: trata saldo insuficiente

================================================================================
IMPLEMENTAÇÃO TÉCNICA
================================================================================

PADRÃO GERAL:

def operacao():
    variavel = None
    while not variavel:
        entrada = input("Prompt: ")
        
        # Validação 1
        if nao_valido(entrada):
            print("Erro específico! Tente novamente.")
            continue
        
        # Validação 2
        if outro_erro(entrada):
            print("Outro erro! Tente novamente.")
            continue
        
        variavel = entrada
    
    # Continue com resto da lógica
    # ...

VANTAGEM: continue mantém a posição do loop, permitindo nova tentativa

================================================================================
EXEMPLO PRÁTICO - criar_usuario()
================================================================================

def criar_usuario(usuarios):
    # Entrada única - sem validação necessária
    nome = input("Informe o nome completo: ")
    
    # Loop de validação para CPF
    cpf = None
    while not cpf:
        cpf_input = input("Informe o CPF (somente números): ")
        
        # Validação 1: formato
        if not validar_cpf(cpf_input):
            print("CPF inválido! Tente novamente.")
            continue
        
        # Validação 2: unicidade
        if filtrar_usuario_por_cpf(usuarios, cpf_input):
            print("CPF já cadastrado! Tente novamente.")
            continue
        
        # Passou em todas validações
        cpf = cpf_input

    # Loop de validação para data
    data_nascimento = None
    while not data_nascimento:
        data_input = input("Informe a data de nascimento (dd-mm-aaaa): ")
        
        if not validar_data(data_input):
            print("Data inválida! Use formato dd-mm-aaaa. Tente novamente.")
            continue
        
        data_nascimento = data_input
    
    # Entrada única
    endereco = input("Informe o endereço (...): ")

    # Cria usuário com dados validados
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

================================================================================
BENEFÍCIOS
================================================================================

PARA O USUÁRIO:
✓ Melhor experiência (não perde dados digitados)
✓ Menos frustração
✓ Mais natural (como a maioria dos apps e sites)
✓ Mensagens específicas por tipo de erro

PARA O CÓDIGO:
✓ Reutilizável (padrão pode ser aplicado em outros campos)
✓ Mantém lógica de negócio clara
✓ Facilita testes (cada validação é testável)
✓ Sem estado global perdido

================================================================================
COMPARAÇÃO ANTES E DEPOIS
================================================================================

ANTES:
Entrada de usuário: nome → CPF → data → endereço
Se falhar em CPF: mensagem erro, retorna ao menu
Resultado: dados perdidos

DEPOIS:
Entrada de nome: única
Entrada de CPF: loop até válido e único
Entrada de data: loop até válida
Entrada de endereço: única
Se falhar: mensagem específica, pede campo novamente
Resultado: dados preservados

================================================================================
CONFORMIDADE
================================================================================

✓ Compatível com Python 3.8+
✓ Mantém código anterior funcional
✓ Sem breaking changes
✓ Integrado com persistência JSON
✓ Integrado com validações
✓ Integrado com timestamps

================================================================================
TESTES
================================================================================

Testes inclusos em test_sistema_bancario.py validam:
✓ Validação de CPF (algoritmo verificador)
✓ Validação de data (formato e validade)
✓ Limites de saque
✓ Saldo insuficiente
✓ Valor negativo

Os testes passam mesmo com loops de validação pois testam a lógica
de validação, não a entrada interativa.

================================================================================
