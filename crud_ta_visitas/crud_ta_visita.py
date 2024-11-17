#CRUD executável de ta_visitas

import tkinter as tk
from datetime import datetime
from tkinter import ttk
from tkinter import messagebox

from util.db import SQL
from c_visitas import IncluirVisitas

#from u_projeto import AlterarProjeto
#from d_projeto import ExcluirProjeto

class CRUDta_visita(tk.Tk):
    def __init__(self):
        super().__init__()
        # Criação de constantes
        self.PADX = 10
        self.PADY = 10

        self.title("CRUD - Tabela de Visitas")

        # Primeira linha - Título
        titulo = tk.Label(self, text="Cadastro / consulta de visitas", font='Helvetica 16 bold', fg='blue')
        titulo.grid(row=0, column=0, columnspan=3, padx=self.PADX, pady=self.PADY)

        # Segunda linha - Parâmetro de consulta
        lb_nome = tk.Label(self, text="Data de visita", font='Helvetica 12 bold', fg='blue')
        lb_nome.grid(row=1, column=0, padx=self.PADX, pady=self.PADY)

        self.data = tk.StringVar()
        self.et_dta = ttk.Entry(self, textvariable=self.data, font='Helvetica 16 bold', foreground='green')
        self.et_dta.grid(row=1, column=1, padx=self.PADX, pady=self.PADY)

        self.bt_consultar = tk.Button(self, text="Consultar", command=self.consultar, font='Helvetica 12 bold',
                                      fg='white', bg='purple')
        self.bt_consultar.grid(row=1, column=2, padx=self.PADX, pady=self.PADY)

        # Treeview para exibir os resultado da consulta no banco de dados
        style = ttk.Style()
        style.theme_use('clam')

        style.configure("Custom.Treeview", font=("Arial", 12), foreground="blue")
        self.tre_funcoes = ttk.Treeview(self, columns=("idt_visitas", "dta_visita", "hra_entrada_visita", "hra_saida_visita",
                                                       "cod_visitantes", "cod_campus", "cod_aluno_acompanhante"), show="headings", style="Custom.Treeview",height=20)

        # Configurar as colunas
        self.tre_funcoes.heading("idt_visitas", text="IDT da visita")
        self.tre_funcoes.heading("dta_visita", text="Data da visita")
        self.tre_funcoes.heading("hra_entrada_visita", text="Hora de entrada")
        self.tre_funcoes.heading("hra_saida_visita", text="Hora de saída")
        self.tre_funcoes.heading("cod_visitantes", text="IDT do visitante") #PCD
        self.tre_funcoes.heading("cod_campus", text="Campus")
        self.tre_funcoes.heading("cod_aluno_acompanhante", text="Aluno acompanhando")

        # Ajustar a largura das colunas
        self.tre_funcoes.column("idt_visitas", width=15, anchor=tk.CENTER)
        self.tre_funcoes.column("dta_visita", width=250, anchor=tk.CENTER)
        self.tre_funcoes.column("hra_entrada_visita", width=100, anchor=tk.CENTER)
        self.tre_funcoes.column("hra_saida_visita", width=120, anchor=tk.CENTER)
        self.tre_funcoes.column("cod_visitantes", width=125, anchor=tk.CENTER)
        self.tre_funcoes.column("cod_campus", width=55, anchor=tk.CENTER)
        self.tre_funcoes.column("cod_aluno_acompanhante", width=150, anchor=tk.CENTER)
        self.tre_funcoes.grid(row=3, column=0, columnspan=15, padx=self.PADX, pady=self.PADY)

        super().geometry("1000x650") #Tamanho geral da interface

        # Quarta linha com os botões de operações
        self.bt_incluir = tk.Button(self, text="Incluir", command=self.incluir, font='Helvetica 12 bold', fg='white',
                                    bg='purple',width=15)
        self.bt_incluir.grid(row=4, column=0, padx=self.PADX, pady=self.PADY)
        self.bt_alterar = tk.Button(self, text="Alterar", command=self.alterar, font='Helvetica 12 bold', fg='white',
                                    bg='purple',width=15)
        self.bt_alterar.grid(row=4, column=1, padx=self.PADX, pady=self.PADY)
        self.bt_excluir = tk.Button(self, text="Excluir", command=self.excluir, font='Helvetica 12 bold', fg='white',
                                    bg='purple',width=15)
        self.bt_excluir.grid(row=4, column=2, padx=self.PADX, pady=self.PADY)
        self.bt_insert_visitante = tk.Button(self, text="Excluir", command=self.excluir, font='Helvetica 12 bold', fg='black',
                                    bg='yellow', width=15)
        self.bt_insert_visitante.grid(row=4, column=4, padx=self.PADX, pady=self.PADY)

        # Criando o objeto que irá acessar o banco de dados
        self.sql = SQL(esquema='bd_gestao_visitantes', pwd='81975907')

    def consultar(self):
        # Obter o termo de busca
        nome = self.et_dta.get()

        # Chamar a função da sua classe utilitária para buscar os registros

        cmd = (
            "SELECT idt_visitas as IDT, DATE_FORMAT(dta_visita, '%d/%m/%Y') as Data_Visitas, TIME_FORMAT(hra_entrada_visita, '%H:%i') as Hora_De_Entrada, TIME_FORMAT(hra_saida_visita, '%H:%i') as Hora_de_Saida, cod_visitantes as Visitante, cod_campus as Campus, cod_aluno_acompanhante as Aluno "
            "From ta_visitas WHERE dta_visita LIKE CONCAT(%s, '%', '%', '%', '%')")

        funcoes = self.sql.get_list(cmd, [nome])

        self.limpar_tabela()
        for funcao in funcoes:
            self.tre_funcoes.insert("", tk.END, values=(funcao['IDT'], funcao['Data_Visitas'], funcao['Hora_De_Entrada'],
                                                        funcao['Hora_de_Saida'], funcao['Visitante'],
                                                        funcao['Campus'], funcao['Aluno']))

    def pegar_idt(self):
        selecao = self.tre_funcoes.selection()
        if selecao:
            linha = self.tre_funcoes.selection()[0]
            valores = self.tre_funcoes.item(linha, "values")
            return valores[0]
        else:
            return 0

    def limpar_tabela(self):
        for funcao in self.tre_funcoes.get_children():
            self.tre_funcoes.delete(funcao)

    def incluir(self):
        c = IncluirVisitas(self)
        self.et_dta.delete(0, tk.END)
        self.limpar_tabela()

    def alterar(self):
        pass

    def excluir(self):
        pass


if __name__ == '__main__':
    app = CRUDta_visita()
    app.mainloop()
