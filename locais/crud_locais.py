import tkinter as tk
from tkinter import ttk, messagebox

from locais.c_locais import CadastrarLocal
from locais.u_locais import AlterarLocal
from locais.d_locais import ExcluirLocal
from util.db import SQL


class CRUDLocais(tk.Tk):
    def __init__(self):
        super().__init__()
        # Criação de constantes
        self.PADX = 20
        self.PADY = 10
        self.PADX_BOTAO = 30
        self.ROXO = "#662c92"

        self.title("Gerenciar Locais")
        self.iconbitmap("../ceub.ico")

        # Configurar o grid para melhor controle do espaço
        self.grid_columnconfigure(0, weight=0)  # Coluna do "Nome do Local"
        self.grid_columnconfigure(1, weight=1)  # Coluna do campo de texto
        self.grid_columnconfigure(4, weight=0)  # Coluna do botão "Consultar"

        # Primeira linha - Título
        titulo = tk.Label(self, text="Gerenciar Locais", font='Helvetica 16 bold', fg=self.ROXO)
        titulo.grid(row=0, column=0, columnspan=4, padx=self.PADX, pady=self.PADY)

        # Segunda linha - Parâmetro de consulta
        lb_nome = tk.Label(self, text="Nome do Local", font='Helvetica 12 bold', fg=self.ROXO)
        lb_nome.grid(row=1, column=0, padx=self.PADX, pady=self.PADY, sticky="w")

        self.nome_var = tk.StringVar()
        self.et_nome = ttk.Entry(self, textvariable=self.nome_var, font='Helvetica 16 bold', foreground=self.ROXO)
        self.et_nome.grid(row=1, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.bt_consultar = tk.Button(self, text="Consultar", command=self.consultar, font='Helvetica 12 bold',
                                      fg='white', bg=self.ROXO, padx=self.PADX_BOTAO, cursor="hand2")
        self.bt_consultar.grid(row=1, column=3, padx=self.PADX, pady=self.PADY, sticky="ew")

        # Treeview para exibir os resultados da consulta no banco de dados
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Arial", 12), foreground=self.ROXO)
        self.tre_locais = ttk.Treeview(self, columns=("idt_local", "nme_local", "nme_campus", "end_campus"),
                                       show="headings", style="Custom.Treeview")
        # Configurar as colunas
        self.tre_locais.heading("idt_local", text="Id")
        self.tre_locais.heading("nme_local", text="Nome do Local")
        self.tre_locais.heading("nme_campus", text="Nome do Campus")
        self.tre_locais.heading("end_campus", text="Endereço do Campus")
        # Ajustar a largura das colunas
        self.tre_locais.column("idt_local", width=50, anchor="center")
        self.tre_locais.column("nme_local", width=250)
        self.tre_locais.column("nme_campus", width=250)
        self.tre_locais.column("end_campus", width=250)
        self.tre_locais.grid(row=3, column=0, columnspan=4, padx=self.PADX, pady=self.PADY)

        # Quarta linha com os botões de operações
        frame_botoes = tk.Frame(self)
        frame_botoes.grid(row=4, column=0, columnspan=4, padx=self.PADX, pady=self.PADY, sticky="ew")

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

        # Criando o objeto que irá acessar o banco de dados
        self.sql = SQL(esquema='bd_gestao_visitantes')

    def voltar(self):
        from menu_principal.tela_menu import MainMenu
        self.destroy()
        MainMenu()

    def consultar(self):
        # Obter o termo de busca
        nome = self.nome_var.get()

        # Comando SQL para buscar os registros
        cmd = (
            "SELECT l.idt_local, l.nme_local, c.nme_campus, c.end_campus "
            "FROM tb_locais l "
            "JOIN tb_campus c ON l.cod_campus = c.idt_campus "
            "WHERE l.nme_local LIKE CONCAT('%', %s, '%') "
            "ORDER BY l.nme_local")
        locais = self.sql.get_list(cmd, [nome])

        self.limpar_tabela()
        for local in locais:
            self.tre_locais.insert("", tk.END, values=(
                local['idt_local'], local['nme_local'], local['nme_campus'], local['end_campus']))

    def pegar_idt(self):
        selecao = self.tre_locais.selection()
        if selecao:
            linha = self.tre_locais.selection()[0]
            valores = self.tre_locais.item(linha, "values")
            return valores[0]
        else:
            return 0

    def limpar_tabela(self):
        for local in self.tre_locais.get_children():
            self.tre_locais.delete(local)

    def cadastrar(self):
        CadastrarLocal(self)
        self.et_nome.delete(0, tk.END)
        self.limpar_tabela()

    def alterar(self):
        idt = self.pegar_idt()
        if idt != 0:
            AlterarLocal(self, idt)
            self.et_nome.delete(0, tk.END)
            self.limpar_tabela()
        else:
            messagebox.showerror("Erro: Escolha um local", "Marque uma linha da tabela para selecionar o local")

    def excluir(self):
        idt = self.pegar_idt()
        if idt != 0:
            ExcluirLocal(self, idt)
            self.et_nome.delete(0, tk.END)
            self.limpar_tabela()
        else:
            messagebox.showerror("Erro: Escolha um local", "Marque uma linha da tabela para selecionar o local")


if __name__ == '__main__':
    app = CRUDLocais()
    app.mainloop()
