# Desafio-DIO-Sistema-Bancario-Funcoes-Python

Sistema bancário básico em Python com operações de depósito, saque e extrato, refatorado usando funções para modularidade. O projeto foi desenvolvido como desafio da DIO para praticar estruturas de repetição, condicionais e organização em funções.

## Funcionalidades
- **Criar Usuário**: cadastra novo usuário com nome, CPF, data de nascimento e endereço (CPF único).
- **Depósito**: valida valores positivos e registra cada movimento no extrato.
- **Saque**: controla saldo disponível, limite por operação (R$ 500,00) e número máximo de saques diários (3).
- **Extrato**: lista todas as movimentações realizadas na sessão e mostra o saldo atual formatado.
- **Encerramento**: permite finalizar a execução de forma segura.

## Requisitos
- Python 3.12+ (ou qualquer versão 3.8+ que suporte f-strings).
- Console/terminal habilitado para entrada de dados via `input()`.

## Como Executar
1. Clone este repositório ou faça o download dos arquivos.
2. No terminal, navegue até a pasta `desafio_bancario`.
3. Execute o script:

```powershell
python sistema_bancario.py
```

Durante a execução, utilize as opções do menu:
- `u` para criar usuário
- `d` para depositar
- `s` para sacar
- `e` para ver o extrato
- `q` para sair

## Estrutura do Código
- `sistema_bancario.py`: concentra as funções `criar_usuario`, `depositar`, `sacar` e `exibir_extrato`, além do loop principal que interpreta o menu e controla o ciclo de vida da aplicação.

## Possíveis Evoluções
- Persistir dados em arquivo ou banco de dados.
- Implementar múltiplas contas e autenticação simples.
- Criar interface gráfica ou API.
- Adicionar testes automatizados para cada função.

## Licença
Projeto disponível sob a licença MIT. Sinta-se à vontade para usar, estudar e adaptar conforme necessário.
