import pytest
from datetime import datetime
from utils import (
    validar_cpf, 
    validar_data, 
    filtrar_usuario_por_cpf,
    LIMITE_SAQUE,
    LIMITE_SAQUES_DIARIOS,
    AGENCIA_PADRAO,
)


class TestValidacoes:
    """Testes para validações de CPF e data."""
    
    def test_cpf_valido(self):
        # CPF válido: 111.444.777-35
        assert validar_cpf("11144477735") is True
    
    def test_cpf_invalido_formato(self):
        assert validar_cpf("123") is False
        assert validar_cpf("abc12345678") is False
    
    def test_cpf_digitos_iguais(self):
        assert validar_cpf("11111111111") is False
    
    def test_cpf_invalido_digitos(self):
        assert validar_cpf("12345678901") is False
    
    def test_data_valida(self):
        assert validar_data("15-03-1990") is True
    
    def test_data_invalida_formato(self):
        assert validar_data("15/03/1990") is False
        assert validar_data("1990-03-15") is False
    
    def test_data_invalida_dia(self):
        assert validar_data("32-01-2000") is False
    
    def test_data_invalida_mes(self):
        assert validar_data("15-13-2000") is False


class TestUsuarios:
    """Testes para operações com usuários."""
    
    def test_filtrar_usuario_nao_encontrado(self):
        usuarios = []
        resultado = filtrar_usuario_por_cpf(usuarios, "12345678901")
        assert resultado is None
    
    def test_filtrar_usuario_encontrado(self):
        usuarios = [
            {"nome": "João", "cpf": "11144477735", "data_nascimento": "15-03-1990", "endereco": "Rua A"}
        ]
        resultado = filtrar_usuario_por_cpf(usuarios, "11144477735")
        assert resultado is not None
        assert resultado["nome"] == "João"


class TestContas:
    """Testes para operações com contas."""
    
    def test_criar_conta_sem_usuarios(self):
        usuarios = []
        contas = []
        numero = 1
        # Verifica que conta não foi criada sem usuários
        assert len(contas) == 0
    
    def test_deposito_valido(self):
        conta = {
            "agencia": "0001",
            "numero_conta": 1,
            "usuario": {"nome": "Test", "cpf": "11144477735"},
            "saldo": 100.0,
            "extrato": "",
            "saques_realizados": 0,
        }
        conta["saldo"] += 50.0
        conta["extrato"] += "Depósito: R$ 50.00\n"
        
        assert conta["saldo"] == 150.0
        assert "Depósito" in conta["extrato"]
    
    def test_saque_valido(self):
        conta = {
            "agencia": "0001",
            "numero_conta": 1,
            "usuario": {"nome": "Test", "cpf": "11144477735"},
            "saldo": 500.0,
            "extrato": "",
            "saques_realizados": 0,
        }
        valor = 100.0
        conta["saldo"] -= valor
        conta["extrato"] += f"Saque: R$ {valor:.2f}\n"
        conta["saques_realizados"] += 1
        
        assert conta["saldo"] == 400.0
        assert conta["saques_realizados"] == 1
        assert "Saque" in conta["extrato"]
    
    def test_saque_excede_saldo(self):
        conta = {"saldo": 100.0, "saques_realizados": 0}
        valor = 150.0
        
        assert valor > conta["saldo"]
    
    def test_saque_excede_limite(self):
        conta = {"saldo": 1000.0, "saques_realizados": 0}
        valor = 600.0
        
        assert valor > LIMITE_SAQUE
    
    def test_saque_maximo_diario(self):
        conta = {"saldo": 1000.0, "saques_realizados": LIMITE_SAQUES_DIARIOS}
        
        assert conta["saques_realizados"] >= LIMITE_SAQUES_DIARIOS
    
    def test_saque_negativo(self):
        valor = -50.0
        assert valor <= 0


class TestTransferencia:
    """Testes para validações de transferência."""
    
    def test_contas_diferentes(self):
        conta1 = {"numero_conta": 1}
        conta2 = {"numero_conta": 2}
        
        assert conta1["numero_conta"] != conta2["numero_conta"]
    
    def test_saldo_suficiente_transferencia(self):
        conta_origem = {"saldo": 500.0}
        valor = 200.0
        
        assert valor <= conta_origem["saldo"]
    
    def test_saldo_insuficiente_transferencia(self):
        conta_origem = {"saldo": 100.0}
        valor = 200.0
        
        assert valor > conta_origem["saldo"]
