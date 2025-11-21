@echo off
chcp 65001 > nul
cd /d "c:\Users\usuar\Área de Trabalho\DIO\desafio_bancario"

echo [*] Configurando git...
git config user.email "usuario@email.com" 2>nul
git config user.name "Usuario" 2>nul

echo [*] Status atual do repositório:
git status --short

echo.
echo [*] Adicionando arquivos...
git add -A

echo.
echo [*] Fazendo commit...
git commit -m "v2.1: Melhorias de UX com loops de validação e 5 funcionalidades principais

- v2.0: Persistência JSON, validações (CPF/data), logs com timestamps, transferência, testes
- v2.1: Loops de validação em todos os pontos de entrada (criar_usuario, criar_conta, depositar, sacar, transferir)

Benefícios:
- Dados não são perdidos quando validação falha
- Comportamento intuitivo para usuário
- Mensagens específicas para cada erro
- 100%% compatível com versão anterior" 2>&1

echo.
echo [*] Push para repositório remoto...
git push 2>&1

echo.
echo [*] Verificando resultado...
git log --oneline -5

echo.
echo [✓] Concluído!
pause
