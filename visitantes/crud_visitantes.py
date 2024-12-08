import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from visitantes.c_visitantes import CadastrarVisitante
from visitantes.d_visitantes import ExcluirVisitante
from visitantes.u_visitantes import AlterarVisitante
from util.db import SQL


class CRUDVisitantes(tk.Tk):
    def __init__(self):
        super().__init__()
        # Criação de constantes
        self.PADX = 20
        self.PADY = 10
        self.PADX_BOTAO = 30
        self.ROXO = "#662c92"

        self.title("Gerenciar Visitantes")
        self.iconbitmap("../ceub.ico")

        # Configurar o grid para melhor controle do espaço
        self.grid_columnconfigure(0, weight=0)  # Coluna do "Nome do Visitante"
        self.grid_columnconfigure(1, weight=1)  # Coluna do campo de texto
        self.grid_columnconfigure(6, weight=0)  # Coluna do botão "Consultar"

        # Primeira linha - Título
        titulo = tk.Label(self, text="Gerenciar Visitantes", font='Helvetica 16 bold', fg=self.ROXO)
        titulo.grid(row=0, column=0, columnspan=6, padx=self.PADX, pady=self.PADY)

        # Segunda linha - Parâmetro de consulta
        lb_nome = tk.Label(self, text="Nome do Visitante", font='Helvetica 12 bold', fg=self.ROXO)
        lb_nome.grid(row=1, column=0, padx=self.PADX, pady=self.PADY, sticky="w")

        self.nome_var = tk.StringVar()
        self.et_nome = ttk.Entry(self, textvariable=self.nome_var, font='Helvetica 16 bold', foreground=self.ROXO)
        self.et_nome.grid(row=1, column=1, columnspan=4, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.bt_consultar = tk.Button(self, text="Consultar", command=self.consultar, font='Helvetica 12 bold',
                                      fg='white', bg=self.ROXO, padx=self.PADX_BOTAO, cursor="hand2")
        self.bt_consultar.grid(row=1, column=5, padx=self.PADX, pady=self.PADY, sticky="ew")

        # Treeview para exibir os resultado da consulta no banco de dados
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Arial", 12), foreground=self.ROXO)
        self.tre_visitantes = ttk.Treeview(self, columns=(
            "idt_visitante", "nme_visitante", "rg", "email", "pcd", "nme_aluno"),
                                           show="headings",
                                           style="Custom.Treeview")
        # Configurar as colunas
        self.tre_visitantes.heading("idt_visitante", text="Id")
        self.tre_visitantes.heading("nme_visitante", text="Nome do Visitante")
        self.tre_visitantes.heading("rg", text="RG")
        self.tre_visitantes.heading("email", text="Email")
        self.tre_visitantes.heading("pcd", text="PCD")
        self.tre_visitantes.heading("nme_aluno", text="Nome do Aluno Acompanhante")
        # Ajustar a largura das colunas
        self.tre_visitantes.column("idt_visitante", width=50, anchor="center")
        self.tre_visitantes.column("nme_visitante", width=300)
        self.tre_visitantes.column("rg", width=100, anchor="center")
        self.tre_visitantes.column("email", width=300, anchor="center")
        self.tre_visitantes.column("pcd", width=50, anchor="center")
        self.tre_visitantes.column("nme_aluno", width=300)
        self.tre_visitantes.grid(row=3, column=0, columnspan=6, padx=self.PADX, pady=self.PADY)

        # Quinta linha com os botões de operações
        frame_botoes = tk.Frame(self)
        frame_botoes.grid(row=4, column=0, columnspan=6, padx=self.PADX, pady=self.PADY, sticky="ew")

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

        # Chamar a função da sua classe utilitária para buscar os registros
        cmd = (
            "SELECT v.idt_visitantes, v.nme_visitante, v.rg_visitante, v.eml_visitante, v.pcd_visitante, a.nme_aluno_acompanhante "
            "FROM tb_visitantes v "
            "LEFT JOIN tb_aluno_acompanhante a ON v.cod_aluno_acompanhante = a.idt_aluno_acompanhante "
            "WHERE nme_visitante LIKE CONCAT('%', %s, '%') ORDER BY nme_visitante")
        visitantes = self.sql.get_list(cmd, [nome])

        self.limpar_tabela()
        for visitante in visitantes:
            nome_acompanhante = visitante['nme_aluno_acompanhante'] if visitante['nme_aluno_acompanhante'] else "-"
            email_visitante = visitante['eml_visitante'] if visitante['eml_visitante'] else "-"
            pcd_visitante = visitante['pcd_visitante'] if visitante['pcd_visitante'] else "-"
            self.tre_visitantes.insert("", tk.END, values=(
                visitante['idt_visitantes'], visitante['nme_visitante'], visitante['rg_visitante'],
                email_visitante, pcd_visitante, nome_acompanhante))

    def pegar_idt(self):
        selecao = self.tre_visitantes.selection()
        if selecao:
            linha = self.tre_visitantes.selection()[0]
            valores = self.tre_visitantes.item(linha, "values")
            return valores[0]
        else:
            return 0

    def limpar_tabela(self):
        for visitante in self.tre_visitantes.get_children():
            self.tre_visitantes.delete(visitante)

    def cadastrar(self):
        CadastrarVisitante(self)
        self.et_nome.delete(0, tk.END)
        self.limpar_tabela()

    def alterar(self):
        idt = self.pegar_idt()
        if idt != 0:
            AlterarVisitante(self, idt)
            self.et_nome.delete(0, tk.END)
            self.limpar_tabela()
        else:
            messagebox.showerror("Erro: Escolha um visitante", "Marque uma linha da tabela para selecionar o visitante")

    def excluir(self):
        idt = self.pegar_idt()
        if idt != 0:
            ExcluirVisitante(self, idt)
            self.et_nome.delete(0, tk.END)
            self.limpar_tabela()
        else:
            messagebox.showerror("Erro: Escolha um visitante", "Marque uma linha da tabela para selecionar o visitante")


if __name__ == '__main__':
    app = CRUDVisitantes()
    app.mainloop()
