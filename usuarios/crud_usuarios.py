import tkinter as tk
from tkinter import ttk, messagebox

from usuarios.c_usuarios import CadastrarUsuario
from usuarios.d_usuarios import ExcluirUsuario
from usuarios.u_usuarios import AlterarUsuario
from util.db import SQL


class CRUDUsuarios(tk.Tk):
    def __init__(self, usuario_logado):
        super().__init__()

        self.usuario_logado = usuario_logado
        self.PADX = 20
        self.PADY = 10
        self.ROXO = "#662c92"

        self.title("Gerenciar Usuários")
        self.iconbitmap("../ceub.ico")

        # Configurar o grid para melhor controle do espaço
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(4, weight=0)
        self.grid_rowconfigure(2, weight=1)

        # Primeira linha - Título
        titulo = tk.Label(self, text="Gerenciar Usuários", font='Helvetica 16 bold', fg=self.ROXO)
        titulo.grid(row=0, column=0, columnspan=4, padx=self.PADX, pady=self.PADY)

        # Segunda linha - Parâmetro de consulta
        lb_nome = tk.Label(self, text="Nome do Usuário", font='Helvetica 12 bold', fg=self.ROXO)
        lb_nome.grid(row=1, column=0, padx=self.PADX, pady=self.PADY, sticky="w")

        self.nome_var = tk.StringVar()
        self.et_nome = ttk.Entry(self, textvariable=self.nome_var, font='Helvetica 16 bold', foreground=self.ROXO)
        self.et_nome.grid(row=1, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.bt_consultar = tk.Button(
            self, text="Consultar", command=self.consultar, font='Helvetica 12 bold',
            fg='white', bg=self.ROXO, padx=30, cursor="hand2"
        )
        self.bt_consultar.grid(row=1, column=3, padx=self.PADX, pady=self.PADY, sticky="ew")

        # Treeview para exibir os usuários
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Arial", 12), foreground=self.ROXO)
        self.tre_usuarios = ttk.Treeview(
            self,
            columns=("idt_usuarios", "nme_usuario", "crd_usuario", "sts_usuario"),
            show="headings",
            style="Custom.Treeview"
        )

        # Configurar as colunas
        self.tre_usuarios.heading("idt_usuarios", text="ID")
        self.tre_usuarios.heading("nme_usuario", text="Nome")
        self.tre_usuarios.heading("crd_usuario", text="Usuário")
        self.tre_usuarios.heading("sts_usuario", text="Status")

        # Ajustar a largura das colunas
        self.tre_usuarios.column("idt_usuarios", width=50, anchor="center")
        self.tre_usuarios.column("nme_usuario", width=200)
        self.tre_usuarios.column("crd_usuario", width=100)
        self.tre_usuarios.column("sts_usuario", width=150, anchor="center")

        self.tre_usuarios.grid(row=2, column=0, columnspan=4, padx=self.PADX, pady=self.PADY, sticky="nsew")

        # Quarta linha com os botões de operações
        frame_botoes = tk.Frame(self)
        frame_botoes.grid(row=3, column=0, columnspan=4, padx=self.PADX, pady=self.PADY, sticky="ew")

        frame_botoes.columnconfigure(0, weight=1)
        frame_botoes.columnconfigure(1, weight=1)
        frame_botoes.columnconfigure(2, weight=1)
        frame_botoes.columnconfigure(3, weight=1)

        self.bt_voltar = tk.Button(frame_botoes, text="Voltar", command=self.voltar, font='Helvetica 12 bold',
                                   fg='white', bg=self.ROXO, cursor="hand2")
        self.bt_voltar.grid(row=0, column=0, pady=self.PADY, sticky="ew")

        self.bt_cadastrar = tk.Button(frame_botoes, text="Cadastrar", command=self.cadastrar, font='Helvetica 12 bold',
                                      fg='white', bg=self.ROXO, cursor="hand2")
        self.bt_cadastrar.grid(row=0, column=1, padx=(self.PADX, 0), pady=self.PADY, sticky="ew")

        self.bt_alterar = tk.Button(frame_botoes, text="Alterar", command=self.alterar, font='Helvetica 12 bold',
                                    fg='white', bg=self.ROXO, cursor="hand2")
        self.bt_alterar.grid(row=0, column=2, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.bt_excluir = tk.Button(frame_botoes, text="Excluir", command=self.excluir, font='Helvetica 12 bold',
                                    fg='white', bg=self.ROXO, cursor="hand2")
        self.bt_excluir.grid(row=0, column=3, pady=self.PADY, sticky="ew")

        # Conexão com o banco de dados
        self.sql = SQL(esquema='bd_gestao_visitantes')

    def voltar(self):
        from menu_principal.tela_menu import MainMenu
        self.destroy()
        MainMenu(self.usuario_logado)

    def consultar(self):
        nome = self.nome_var.get()
        cmd = (
            "SELECT idt_usuarios, nme_usuario, crd_usuario, sts_usuario "
            "FROM tb_usuarios "
            "WHERE nme_usuario LIKE CONCAT('%', %s, '%') "
            "ORDER BY nme_usuario"
        )
        try:
            usuarios = self.sql.get_list(cmd, [nome])
            self.limpar_tabela()

            status_legenda = {
                'A': 'Administrador',
                'R': 'Recepção',
                'S': 'Segurança'
            }

            for usuario in usuarios:
                self.tre_usuarios.insert("", tk.END, values=(usuario['idt_usuarios'],
                                                             usuario['nme_usuario'],
                                                             usuario['crd_usuario'],
                                                             status_legenda.get(usuario['sts_usuario'])))
        except Exception as e:
            messagebox.showerror("Erro ao consultar usuários", str(e))

    def limpar_tabela(self):
        for usuario in self.tre_usuarios.get_children():
            self.tre_usuarios.delete(usuario)

    def pegar_idt(self):
        selecao = self.tre_usuarios.selection()
        if selecao:
            linha = self.tre_usuarios.selection()[0]
            valores = self.tre_usuarios.item(linha, "values")
            return valores[0]
        else:
            return 0

    def cadastrar(self):
        CadastrarUsuario(self)
        self.et_nome.delete(0, tk.END)
        self.limpar_tabela()

    def alterar(self):
        idt = self.pegar_idt()
        if idt != 0:
            AlterarUsuario(self, idt)
            self.et_nome.delete(0, tk.END)
            self.limpar_tabela()
        else:
            messagebox.showerror("Erro: Escolha um usuário", "Marque uma linha da tabela para selecionar o usuário")

    def excluir(self):
        idt = self.pegar_idt()
        if idt != 0:
            ExcluirUsuario(self, idt)
            self.et_nome.delete(0, tk.END)
            self.limpar_tabela()
        else:
            messagebox.showerror("Erro: Escolha um usuário", "Marque uma linha da tabela para selecionar o usuário")


if __name__ == '__main__':
    app = CRUDUsuarios()
    app.mainloop()
