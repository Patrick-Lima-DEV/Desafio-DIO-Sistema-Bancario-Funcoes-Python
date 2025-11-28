# -*- coding: utf-8 -*-
"""Utilitários e funções comuns do sistema bancário."""

import json
import re
import unicodedata
from datetime import datetime
from functools import wraps
from pathlib import Path

# ============= CONFIGURAÇÕES =============
AGENCIA_PADRAO = "0001"
LIMITE_SAQUE = 500
LIMITE_SAQUES_DIARIOS = 3
ARQUIVO_DADOS = Path("dados_bancarios.json")
ARQUIVO_LOG = Path("log.txt")


# ============= UTILIDADES GERAIS =============

def normalizar_texto(texto):
    """Remove acentos e coloca texto em minúsculas para comparações."""
    if not texto:
        return ""
    return unicodedata.normalize("NFKD", texto).encode("ASCII", "ignore").decode("ASCII").lower()


def validar_cpf(cpf):
    """Valida CPF com algoritmo verificador."""
    if not re.match(r"^\d{11}$", cpf):
        return False
    
    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False
    
    # Calcula primeiro dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = 11 - (soma % 11)
    digito1 = 0 if digito1 > 9 else digito1
    
    # Calcula segundo dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = 11 - (soma % 11)
    digito2 = 0 if digito2 > 9 else digito2
    
    return int(cpf[9]) == digito1 and int(cpf[10]) == digito2


def validar_data(data_str):
    """Valida data no formato dd-mm-aaaa."""
    try:
        datetime.strptime(data_str, "%d-%m-%Y")
        return True
    except ValueError:
        return False


def filtrar_usuario_por_cpf(usuarios, cpf):
    """Busca um usuário pelo CPF."""
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None


# ============= PERSISTÊNCIA DE DADOS =============

def salvar_dados(usuarios, contas, proximo_numero_conta):
    """Salva usuários e contas em arquivo JSON."""
    dados = {
        "usuarios": usuarios,
        "contas": contas,
        "proximo_numero_conta": proximo_numero_conta
    }
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)


def carregar_dados():
    """Carrega usuários e contas do arquivo JSON."""
    usuarios = []
    contas = []
    proximo_numero_conta = 1
    
    if ARQUIVO_DADOS.exists():
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
                dados = json.load(f)
                usuarios = dados.get("usuarios", [])
                contas = dados.get("contas", [])
                proximo_numero_conta = dados.get("proximo_numero_conta", 1)
        except (json.JSONDecodeError, KeyError):
            pass
    
    return usuarios, contas, proximo_numero_conta


# ============= SISTEMA DE LOGS E AUDITORIA =============

def mascarar_dados_sensiveis(valor):
    """Mascara dados sensíveis como CPF, valores bancários e senhas."""
    if valor is None:
        return "None"
    
    # Converter para string
    valor_str = str(valor)
    
    # Mascarar CPF (padrão: 123.456.789-00 ou 12345678900)
    valor_str = re.sub(r'\b(\d{3})\.?(\d{3})\.?(\d{3})\-?(\d{2})\b', r'\1.***.***.***-**', valor_str)
    
    # Mascarar valores monetários grandes (provavelmente saldos/valores)
    # Substitui números com 4+ dígitos por ****
    valor_str = re.sub(r'\b\d{4,}\b', '****', valor_str)
    
    # Mascarar endereço se contiver rua/avenida (reduz a apenas tipo e parcial)
    if 'endereco' in valor_str.lower():
        valor_str = re.sub(r'(rua|avenida|av\.|r\.)\s+[^,]+', r'\1 ****', valor_str, flags=re.IGNORECASE)
    
    return valor_str


def registrar_log(tipo_transacao, nome_funcao, status, duracao, args, kwargs, resultado=None, erro=None):
    """Registra operação em log.txt com formato padronizado e dados mascarados."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    
    # Preparar argumentos mascarados
    args_mascarados = []
    for arg in args:
        if isinstance(arg, dict) and arg.get("numero_conta"):
            args_mascarados.append(f"conta_numero={arg.get('numero_conta')}")
        elif isinstance(arg, (int, str, float)) and len(str(arg)) < 50:
            args_mascarados.append(mascarar_dados_sensiveis(arg))
        elif isinstance(arg, list):
            args_mascarados.append(f"lista({len(arg)} items)")
        else:
            args_mascarados.append(type(arg).__name__)
    
    args_str = ", ".join(args_mascarados) if args_mascarados else "sem_args"
    
    # Preparar resultado
    resultado_str = mascarar_dados_sensiveis(resultado) if resultado else "None"
    
    # Montar linha de log
    linha_log = f"[{timestamp}] {nome_funcao:20} | {tipo_transacao:25} | ARGS: {args_str:40} | {status:6} | {duracao:.3f}s"
    
    if erro:
        linha_log += f" | ERRO: {erro}"
    
    # Escrever no arquivo
    try:
        with open(ARQUIVO_LOG, "a", encoding="utf-8") as f:
            f.write(linha_log + "\n")
    except Exception as e:
        print(f"[AVISO] Não foi possível registrar log: {e}")


def log_transacao(tipo_transacao):
    """Decorador que registra a data/hora, argumentos e resultado de transações em log.txt."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            inicio = datetime.now()
            try:
                resultado = func(*args, **kwargs)
                duracao = (datetime.now() - inicio).total_seconds()
                registrar_log(
                    tipo_transacao=tipo_transacao,
                    nome_funcao=func.__name__,
                    status="OK",
                    duracao=duracao,
                    args=args,
                    kwargs=kwargs,
                    resultado=resultado
                )
                return resultado
            except Exception as e:
                duracao = (datetime.now() - inicio).total_seconds()
                erro_info = f"{type(e).__name__}: {str(e)}"
                registrar_log(
                    tipo_transacao=tipo_transacao,
                    nome_funcao=func.__name__,
                    status="ERRO",
                    duracao=duracao,
                    args=args,
                    kwargs=kwargs,
                    erro=erro_info
                )
                raise
        return wrapper
    return decorator
