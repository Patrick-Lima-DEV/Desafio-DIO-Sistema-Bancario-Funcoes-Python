import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
from datetime import datetime
from pathlib import Path

# Importar do novo layout modular
from utils import (
    validar_cpf,
    validar_data,
    filtrar_usuario_por_cpf,
    carregar_dados,
    registrar_consulta_extrato,
    AGENCIA_PADRAO,
    ARQUIVO_DADOS,
    ARQUIVO_LOG,
    LIMITE_SAQUE,
    LIMITE_SAQUES_DIARIOS,
)
from models import (
    usuarios,
    contas,
    proximo_numero_conta,
    salvar_dados,
    criar_usuario_dados,
    criar_conta_dados,
    obter_conta_por_numero,
    depositar_dados,
    sacar_dados,
    transferir_dados,
    verificar_reset_saques_diarios,
    ContaIterador,
    gerar_transacoes,
)




# ============= FUNÇÕES WRAPPER PARA A INTERFACE =============

def criar_usuario(nome, cpf, data_nascimento, endereco):
    """Wrapper para criar novo usuário."""
    try:
        if not validar_cpf(cpf):
            return False, "CPF inválido!"
        
        if filtrar_usuario_por_cpf(usuarios, cpf):
            return False, "CPF já cadastrado!"
        
        if not validar_data(data_nascimento):
            return False, "Data inválida! Use formato dd-mm-aaaa"
        
        usuario = {
            "nome": nome,
            "cpf": cpf,
            "data_nascimento": data_nascimento,
            "endereco": endereco,
            "data_criacao": datetime.now().isoformat(),
        }
        usuarios.append(usuario)
        salvar_dados()
        return True, "Usuário criado com sucesso!"
    except Exception as e:
        return False, str(e)


def criar_conta(cpf):
    """Wrapper para criar nova conta."""
    global proximo_numero_conta
    try:
        if not usuarios:
            return False, "Cadastre um usuário antes de criar uma conta."
        
        usuario = filtrar_usuario_por_cpf(usuarios, cpf)
        if not usuario:
            return False, "Usuário não encontrado."
        
        conta = {
            "agencia": AGENCIA_PADRAO,
            "numero_conta": proximo_numero_conta,
            "usuario": usuario,
            "saldo": 0,
            "extrato": "",
            "saques_realizados": 0,
            "data_criacao": datetime.now().isoformat(),
        }
        contas.append(conta)
        numero_criado = proximo_numero_conta
        proximo_numero_conta += 1
        salvar_dados()
        return True, f"Conta criada com sucesso! Número: {numero_criado}"
    except Exception as e:
        return False, str(e)


def depositar(numero_conta, valor):
    """Wrapper para depósito."""
    try:
        if valor <= 0:
            return False, "Valor deve ser maior que zero."
        
        for conta in contas:
            if conta["numero_conta"] == numero_conta:
                timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                conta["saldo"] += valor
                conta["extrato"] += f"[{timestamp}] Depósito: R$ {valor:.2f}\n"
                salvar_dados()
                return True, f"Depósito de R$ {valor:.2f} realizado com sucesso!"
        
        return False, "Conta não encontrada."
    except Exception as e:
        return False, str(e)


def sacar(numero_conta, valor):
    """Wrapper para saque."""
    try:
        if valor <= 0:
            return False, "Valor deve ser maior que zero."
        
        for conta in contas:
            if conta["numero_conta"] == numero_conta:
                # Verificar se deve resetar saques diários
                verificar_reset_saques_diarios(conta)
                
                if valor > conta["saldo"]:
                    return False, "Saldo insuficiente."
                
                if valor > LIMITE_SAQUE:
                    return False, f"Limite de saque é R$ {LIMITE_SAQUE:.2f}"
                
                if conta["saques_realizados"] >= LIMITE_SAQUES_DIARIOS:
                    return False, "Limite de saques diários atingido."
                
                timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                conta["saldo"] -= valor
                conta["extrato"] += f"[{timestamp}] Saque: R$ {valor:.2f}\n"
                conta["saques_realizados"] += 1
                salvar_dados()
                return True, f"Saque de R$ {valor:.2f} realizado com sucesso!"
        
        return False, "Conta não encontrada."
    except Exception as e:
        return False, str(e)


def transferir(numero_origem, numero_destino, valor):
    """Wrapper para transferência."""
    try:
        if valor <= 0:
            return False, "Valor deve ser maior que zero."
        
        if numero_origem == numero_destino:
            return False, "Não é possível transferir para a mesma conta."
        
        conta_origem = None
        conta_destino = None
        
        for conta in contas:
            if conta["numero_conta"] == numero_origem:
                conta_origem = conta
            if conta["numero_conta"] == numero_destino:
                conta_destino = conta
        
        if not conta_origem:
            return False, "Conta de origem não encontrada."
        
        if not conta_destino:
            return False, "Conta de destino não encontrada."
        
        if valor > conta_origem["saldo"]:
            return False, "Saldo insuficiente."
        
        timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        conta_origem["saldo"] -= valor
        conta_origem["extrato"] += f"[{timestamp}] Transferência enviada: R$ {valor:.2f} para Agência {conta_destino['agencia']} Conta {conta_destino['numero_conta']}\n"
        
        conta_destino["saldo"] += valor
        conta_destino["extrato"] += f"[{timestamp}] Transferência recebida: R$ {valor:.2f} de Agência {conta_origem['agencia']} Conta {conta_origem['numero_conta']}\n"
        
        salvar_dados()
        return True, "Transferência realizada com sucesso!"
    except Exception as e:
        return False, str(e)


def obter_extrato(numero_conta):
    """Wrapper para obter extrato."""
    for conta in contas:
        if conta["numero_conta"] == numero_conta:
            extrato = conta["extrato"] if conta["extrato"] else "Não foram realizadas movimentações."
            saldo = conta["saldo"]
            return extrato, saldo
    return None, None


# ============= INTERFACE GRÁFICA =============

class BancoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema Bancário - Interface Gráfica")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)
        self.root.configure(bg="#f0f0f0")
        
        carregar_dados()
        self.criar_menu_principal()
    
    def limpar_janela(self):
        """Limpa todos os widgets da janela."""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def voltar_menu(self):
        """Volta para o menu principal."""
        self.limpar_janela()
        self.criar_menu_principal()
    
    def criar_menu_principal(self):
        """Cria o menu principal."""
        self.limpar_janela()
        
        frame_titulo = tk.Frame(self.root, bg="#2c3e50", height=80)
        frame_titulo.pack(fill=tk.X)
        
        label_titulo = tk.Label(frame_titulo, text="Sistema Bancário", font=("Arial", 24, "bold"), bg="#2c3e50", fg="white")
        label_titulo.pack(pady=20)
        
        frame_botoes = tk.Frame(self.root, bg="#f0f0f0")
        frame_botoes.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        botoes = [
            ("👤 Criar Usuário", self.tela_criar_usuario),
            ("🏦 Criar Conta", self.tela_criar_conta),
            ("📋 Listar Contas", self.tela_listar_contas),
            ("💰 Depositar", self.tela_depositar),
            ("💸 Sacar", self.tela_sacar),
            ("🔄 Transferir", self.tela_transferir),
            ("📄 Extrato", self.tela_extrato),
            ("❌ Sair", self.root.quit),
        ]
        
        for i, (texto, comando) in enumerate(botoes):
            btn = tk.Button(frame_botoes, text=texto, command=comando, font=("Arial", 12), 
                           bg="#3498db", fg="white", height=2, relief=tk.RAISED, cursor="hand2")
            
            # Organizar em 2 colunas
            frame_botoes.columnconfigure(0, weight=1)
            frame_botoes.columnconfigure(1, weight=1)
            
            row = i // 2
            col = i % 2
            btn.grid(row=row, column=col, sticky="ew", padx=10, pady=10)
            
            btn.bind("<Enter>", lambda e: e.widget.config(bg="#2980b9"))
            btn.bind("<Leave>", lambda e: e.widget.config(bg="#3498db"))
    
    def tela_criar_usuario(self):
        """Tela para criar novo usuário."""
        self.limpar_janela()
        
        label_titulo = tk.Label(self.root, text="Criar Novo Usuário", font=("Arial", 18, "bold"), bg="#f0f0f0")
        label_titulo.pack(pady=10)
        
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        campos = [
            ("Nome Completo:", "nome"),
            ("CPF (11 dígitos):", "cpf"),
            ("Data de Nascimento (dd-mm-aaaa):", "data"),
            ("Endereço:", "endereco"),
        ]
        
        entries = {}
        for label_text, key in campos:
            label = tk.Label(frame, text=label_text, font=("Arial", 10), bg="#f0f0f0")
            label.pack(anchor="w", pady=(10, 0))
            entry = tk.Entry(frame, font=("Arial", 10), width=40)
            entry.pack(anchor="w", pady=(0, 5))
            entries[key] = entry
        
        def salvar():
            nome = entries["nome"].get().strip()
            cpf = entries["cpf"].get().strip()
            data = entries["data"].get().strip()
            endereco = entries["endereco"].get().strip()
            
            if not all([nome, cpf, data, endereco]):
                messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
                return
            
            sucesso, mensagem = criar_usuario(nome, cpf, data, endereco)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.voltar_menu()
            else:
                messagebox.showerror("Erro", mensagem)
        
        frame_botoes = tk.Frame(self.root, bg="#f0f0f0")
        frame_botoes.pack(pady=20)
        
        btn_salvar = tk.Button(frame_botoes, text="Criar Usuário", command=salvar, 
                              font=("Arial", 11), bg="#27ae60", fg="white", padx=20)
        btn_salvar.pack(side=tk.LEFT, padx=5)
        
        btn_voltar = tk.Button(frame_botoes, text="Voltar", command=self.voltar_menu, 
                              font=("Arial", 11), bg="#95a5a6", fg="white", padx=20)
        btn_voltar.pack(side=tk.LEFT, padx=5)
    
    def tela_criar_conta(self):
        """Tela para criar nova conta."""
        self.limpar_janela()
        
        label_titulo = tk.Label(self.root, text="Criar Nova Conta", font=("Arial", 18, "bold"), bg="#f0f0f0")
        label_titulo.pack(pady=10)
        
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        label = tk.Label(frame, text="CPF do Titular:", font=("Arial", 10), bg="#f0f0f0")
        label.pack(anchor="w", pady=(10, 0))
        entry_cpf = tk.Entry(frame, font=("Arial", 10), width=40)
        entry_cpf.pack(anchor="w", pady=(0, 5))
        
        def salvar():
            cpf = entry_cpf.get().strip()
            if not cpf:
                messagebox.showerror("Erro", "CPF é obrigatório!")
                return
            
            sucesso, mensagem = criar_conta(cpf)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.voltar_menu()
            else:
                messagebox.showerror("Erro", mensagem)
        
        frame_botoes = tk.Frame(self.root, bg="#f0f0f0")
        frame_botoes.pack(pady=20)
        
        btn_salvar = tk.Button(frame_botoes, text="Criar Conta", command=salvar, 
                              font=("Arial", 11), bg="#27ae60", fg="white", padx=20)
        btn_salvar.pack(side=tk.LEFT, padx=5)
        
        btn_voltar = tk.Button(frame_botoes, text="Voltar", command=self.voltar_menu, 
                              font=("Arial", 11), bg="#95a5a6", fg="white", padx=20)
        btn_voltar.pack(side=tk.LEFT, padx=5)
    
    def tela_listar_contas(self):
        """Tela para listar contas."""
        self.limpar_janela()
        
        label_titulo = tk.Label(self.root, text="Contas Cadastradas", font=("Arial", 18, "bold"), bg="#f0f0f0")
        label_titulo.pack(pady=10)
        
        if not contas:
            label_vazio = tk.Label(self.root, text="Nenhuma conta cadastrada.", font=("Arial", 12), bg="#f0f0f0")
            label_vazio.pack(pady=50)
        else:
            frame_tabela = tk.Frame(self.root, bg="#f0f0f0")
            frame_tabela.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            
            # Treeview com Scrollbar
            columns = ("agencia", "numero", "titular", "saldo")
            tree = ttk.Treeview(frame_tabela, columns=columns, show="headings")
            
            tree.heading("agencia", text="Agência")
            tree.heading("numero", text="Conta")
            tree.heading("titular", text="Titular")
            tree.heading("saldo", text="Saldo")
            
            tree.column("agencia", width=100, anchor="center")
            tree.column("numero", width=100, anchor="center")
            tree.column("titular", width=300, anchor="w")
            tree.column("saldo", width=150, anchor="e")
            
            scrollbar = ttk.Scrollbar(frame_tabela, orient=tk.VERTICAL, command=tree.yview)
            tree.configure(yscroll=scrollbar.set)
            
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            # Contas
            for conta in contas:
                tree.insert("", tk.END, values=(
                    conta["agencia"],
                    str(conta["numero_conta"]),
                    conta["usuario"]["nome"],
                    f"R$ {conta['saldo']:.2f}"
                ))
        
        btn_voltar = tk.Button(self.root, text="Voltar", command=self.voltar_menu, 
                              font=("Arial", 11), bg="#95a5a6", fg="white", padx=20)
        btn_voltar.pack(pady=10)
    
    def tela_depositar(self):
        """Tela para depositar."""
        self.limpar_janela()
        
        label_titulo = tk.Label(self.root, text="Realizar Depósito", font=("Arial", 18, "bold"), bg="#f0f0f0")
        label_titulo.pack(pady=10)
        
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        label_conta = tk.Label(frame, text="Número da Conta:", font=("Arial", 10), bg="#f0f0f0")
        label_conta.pack(anchor="w", pady=(10, 0))
        entry_conta = tk.Entry(frame, font=("Arial", 10), width=40)
        entry_conta.pack(anchor="w", pady=(0, 10))
        
        label_valor = tk.Label(frame, text="Valor do Depósito:", font=("Arial", 10), bg="#f0f0f0")
        label_valor.pack(anchor="w", pady=(10, 0))
        entry_valor = tk.Entry(frame, font=("Arial", 10), width=40)
        entry_valor.pack(anchor="w", pady=(0, 5))
        
        def executar():
            try:
                numero_conta = int(entry_conta.get().strip())
                valor = float(entry_valor.get().strip())
            except ValueError:
                messagebox.showerror("Erro", "Valores inválidos!")
                return
            
            sucesso, mensagem = depositar(numero_conta, valor)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.voltar_menu()
            else:
                messagebox.showerror("Erro", mensagem)
        
        frame_botoes = tk.Frame(self.root, bg="#f0f0f0")
        frame_botoes.pack(pady=20)
        
        btn_depositar = tk.Button(frame_botoes, text="Depositar", command=executar, 
                                 font=("Arial", 11), bg="#27ae60", fg="white", padx=20)
        btn_depositar.pack(side=tk.LEFT, padx=5)
        
        btn_voltar = tk.Button(frame_botoes, text="Voltar", command=self.voltar_menu, 
                              font=("Arial", 11), bg="#95a5a6", fg="white", padx=20)
        btn_voltar.pack(side=tk.LEFT, padx=5)
    
    def tela_sacar(self):
        """Tela para sacar."""
        self.limpar_janela()
        
        label_titulo = tk.Label(self.root, text="Realizar Saque", font=("Arial", 18, "bold"), bg="#f0f0f0")
        label_titulo.pack(pady=10)
        
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        label_conta = tk.Label(frame, text="Número da Conta:", font=("Arial", 10), bg="#f0f0f0")
        label_conta.pack(anchor="w", pady=(10, 0))
        entry_conta = tk.Entry(frame, font=("Arial", 10), width=40)
        entry_conta.pack(anchor="w", pady=(0, 10))
        
        label_valor = tk.Label(frame, text="Valor do Saque:", font=("Arial", 10), bg="#f0f0f0")
        label_valor.pack(anchor="w", pady=(10, 0))
        entry_valor = tk.Entry(frame, font=("Arial", 10), width=40)
        entry_valor.pack(anchor="w", pady=(0, 5))
        
        def executar():
            try:
                numero_conta = int(entry_conta.get().strip())
                valor = float(entry_valor.get().strip())
            except ValueError:
                messagebox.showerror("Erro", "Valores inválidos!")
                return
            
            sucesso, mensagem = sacar(numero_conta, valor)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.voltar_menu()
            else:
                messagebox.showerror("Erro", mensagem)
        
        frame_botoes = tk.Frame(self.root, bg="#f0f0f0")
        frame_botoes.pack(pady=20)
        
        btn_sacar = tk.Button(frame_botoes, text="Sacar", command=executar, 
                             font=("Arial", 11), bg="#e74c3c", fg="white", padx=20)
        btn_sacar.pack(side=tk.LEFT, padx=5)
        
        btn_voltar = tk.Button(frame_botoes, text="Voltar", command=self.voltar_menu, 
                              font=("Arial", 11), bg="#95a5a6", fg="white", padx=20)
        btn_voltar.pack(side=tk.LEFT, padx=5)
    
    def tela_transferir(self):
        """Tela para transferir."""
        self.limpar_janela()
        
        label_titulo = tk.Label(self.root, text="Realizar Transferência", font=("Arial", 18, "bold"), bg="#f0f0f0")
        label_titulo.pack(pady=10)
        
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        label_origem = tk.Label(frame, text="Conta de Origem:", font=("Arial", 10), bg="#f0f0f0")
        label_origem.pack(anchor="w", pady=(10, 0))
        entry_origem = tk.Entry(frame, font=("Arial", 10), width=40)
        entry_origem.pack(anchor="w", pady=(0, 10))
        
        label_destino = tk.Label(frame, text="Conta de Destino:", font=("Arial", 10), bg="#f0f0f0")
        label_destino.pack(anchor="w", pady=(10, 0))
        entry_destino = tk.Entry(frame, font=("Arial", 10), width=40)
        entry_destino.pack(anchor="w", pady=(0, 10))
        
        label_valor = tk.Label(frame, text="Valor da Transferência:", font=("Arial", 10), bg="#f0f0f0")
        label_valor.pack(anchor="w", pady=(10, 0))
        entry_valor = tk.Entry(frame, font=("Arial", 10), width=40)
        entry_valor.pack(anchor="w", pady=(0, 5))
        
        def executar():
            try:
                numero_origem = int(entry_origem.get().strip())
                numero_destino = int(entry_destino.get().strip())
                valor = float(entry_valor.get().strip())
            except ValueError:
                messagebox.showerror("Erro", "Valores inválidos!")
                return
            
            sucesso, mensagem = transferir(numero_origem, numero_destino, valor)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self.voltar_menu()
            else:
                messagebox.showerror("Erro", mensagem)
        
        frame_botoes = tk.Frame(self.root, bg="#f0f0f0")
        frame_botoes.pack(pady=20)
        
        btn_transferir = tk.Button(frame_botoes, text="Transferir", command=executar, 
                                  font=("Arial", 11), bg="#27ae60", fg="white", padx=20)
        btn_transferir.pack(side=tk.LEFT, padx=5)
        
        btn_voltar = tk.Button(frame_botoes, text="Voltar", command=self.voltar_menu, 
                              font=("Arial", 11), bg="#95a5a6", fg="white", padx=20)
        btn_voltar.pack(side=tk.LEFT, padx=5)
    
    def tela_extrato(self):
        """Tela para visualizar extrato."""
        self.limpar_janela()
        
        label_titulo = tk.Label(self.root, text="Visualizar Extrato", font=("Arial", 18, "bold"), bg="#f0f0f0")
        label_titulo.pack(pady=10)
        
        frame = tk.Frame(self.root, bg="#f0f0f0")
        frame.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        
        label_conta = tk.Label(frame, text="Número da Conta:", font=("Arial", 10), bg="#f0f0f0")
        label_conta.pack(anchor="w", pady=(10, 0))
        entry_conta = tk.Entry(frame, font=("Arial", 10), width=40)
        entry_conta.pack(anchor="w", pady=(0, 10))
        
        text_extrato = scrolledtext.ScrolledText(frame, font=("Arial", 9), height=12, width=60, bg="white")
        text_extrato.pack(fill=tk.BOTH, expand=True, pady=10)
        
        def buscar():
            try:
                numero_conta = int(entry_conta.get().strip())
            except ValueError:
                messagebox.showerror("Erro", "Número de conta inválido!")
                return
            
            extrato, saldo = obter_extrato(numero_conta)
            if extrato is None:
                messagebox.showerror("Erro", "Conta não encontrada!")
            else:
                # Registrar consulta de extrato no log
                for conta in contas:
                    if conta.get("numero_conta") == numero_conta:
                        titular = conta.get("usuario", {}).get("nome", "Desconhecido")
                        registrar_consulta_extrato(numero_conta, titular)
                        break
                
                texto = f"================ EXTRATO ================\n"
                texto += f"{extrato}\n"
                texto += f"Saldo: R$ {saldo:.2f}\n"
                texto += f"========================================="
                text_extrato.delete("1.0", tk.END)
                text_extrato.insert("1.0", texto)
        
        frame_botoes = tk.Frame(self.root, bg="#f0f0f0")
        frame_botoes.pack(pady=10)
        
        btn_buscar = tk.Button(frame_botoes, text="Buscar Extrato", command=buscar, 
                              font=("Arial", 11), bg="#3498db", fg="white", padx=20)
        btn_buscar.pack(side=tk.LEFT, padx=5)
        
        btn_voltar = tk.Button(frame_botoes, text="Voltar", command=self.voltar_menu, 
                              font=("Arial", 11), bg="#95a5a6", fg="white", padx=20)
        btn_voltar.pack(side=tk.LEFT, padx=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = BancoGUI(root)
    root.mainloop()
