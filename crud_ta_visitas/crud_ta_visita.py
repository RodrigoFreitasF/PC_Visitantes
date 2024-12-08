import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from tkcalendar import DateEntry

from crud_ta_visitas.c_visitas import IncluirVisitas
from crud_ta_visitas.checkout_visitas import CheckoutVisitas
from crud_ta_visitas.checkin_visitas import CheckinVisitas
from crud_ta_visitas.d_visitas import ExcluirVisitas
from crud_ta_visitas.u_visitas import AlterarVisitas
from util.db import SQL

from datetime import datetime


class CRUDta_visita(tk.Tk):
    def __init__(self):
        super().__init__()
        # Criação de constantes
        self.PADX = 20
        self.PADY = 10
        self.PADX_BOTAO = 30
        self.ROXO = "#662c92"

        # Título da janela
        self.title("Gerenciar Visitas")

        # Configurar o grid para melhor controle do espaço
        self.grid_columnconfigure(0, weight=0)  # Coluna do "Data de Visita"
        self.grid_columnconfigure(1, weight=1)  # Coluna do campo de texto
        self.grid_columnconfigure(6, weight=0)  # Coluna do botão "Consultar"

        # Primeira linha - Título
        titulo = tk.Label(self, text="Gerenciar Visitas", font='Helvetica 16 bold', fg=self.ROXO)
        titulo.grid(row=0, column=0, columnspan=6, padx=self.PADX, pady=self.PADY)

        # Segunda linha - Parâmetro de consulta
        lb_nome = tk.Label(self, text="Data de Visita", font='Helvetica 12 bold', fg=self.ROXO)
        lb_nome.grid(row=1, column=0, padx=self.PADX, pady=self.PADY, sticky="w")

        self.data = tk.StringVar()
        self.et_dta = DateEntry(
            self,
            textvariable=self.data,
            font='Helvetica 16 bold',
            width=12,
            date_pattern='dd/mm/yyyy',
            foreground='#ec0089',
            selectbackground='#ec0089', locale='pt_BR',firstweekday="sunday" ,
            weekendforeground='Red', weekendbackground='pink', headersforeground='#43054e',
        )
        self.et_dta.grid(row=1, column=1, columnspan=4, padx=self.PADX, pady=self.PADY, sticky="ew")
        self.et_dta.delete(0, tk.END)

        self.bt_consultar = tk.Button(self, text="Consultar", command=self.consultar, font='Helvetica 12 bold',
                                      fg='white', bg=self.ROXO, padx=self.PADX_BOTAO, cursor="hand2")
        self.bt_consultar.grid(row=1, column=5, padx=self.PADX, pady=self.PADY, sticky="ew")

        # Treeview para exibir os resultados da consulta no banco de dados
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Helvetica", 12), foreground=self.ROXO)
        self.tre_funcoes = ttk.Treeview(self,
                                        columns=("idt_visitas", "dta_visita", "hra_entrada_visita", "hra_saida_visita",
                                                 "cod_visitantes", "cod_locais", "cod_aluno_acompanhante"),
                                        show="headings", style="Custom.Treeview", height=20)

        # Configurar as colunas
        self.tre_funcoes.heading("idt_visitas", text="ID")
        self.tre_funcoes.heading("dta_visita", text="Data da Visita")
        self.tre_funcoes.heading("hra_entrada_visita", text="Hora de Entrada")
        self.tre_funcoes.heading("hra_saida_visita", text="Hora de Saída")
        self.tre_funcoes.heading("cod_visitantes", text="Nome Visitante")
        self.tre_funcoes.heading("cod_locais", text="Local")
        self.tre_funcoes.heading("cod_aluno_acompanhante", text="Nome Aluno Acompanhante")

        # Ajustar a largura das colunas
        self.tre_funcoes.column("idt_visitas", width=50, anchor=tk.CENTER)
        self.tre_funcoes.column("dta_visita", width=120, anchor=tk.CENTER)
        self.tre_funcoes.column("hra_entrada_visita", width=100, anchor=tk.CENTER)
        self.tre_funcoes.column("hra_saida_visita", width=100, anchor=tk.CENTER)
        self.tre_funcoes.column("cod_visitantes", width=200, anchor=tk.CENTER)
        self.tre_funcoes.column("cod_locais", width=200, anchor=tk.CENTER)
        self.tre_funcoes.column("cod_aluno_acompanhante", width=200, anchor=tk.CENTER)
        self.tre_funcoes.grid(row=3, column=0, columnspan=6, padx=self.PADX, pady=self.PADY)

        # Quarta linha com os botões de operações
        frame_botoes = tk.Frame(self)
        frame_botoes.grid(row=4, column=0, columnspan=6, padx=self.PADX, pady=self.PADY, sticky="ew")

        frame_botoes.columnconfigure(0, weight=1)
        frame_botoes.columnconfigure(1, weight=1)
        frame_botoes.columnconfigure(2, weight=1)
        frame_botoes.columnconfigure(3, weight=1)
        frame_botoes.columnconfigure(4, weight=1)
        frame_botoes.columnconfigure(5, weight=1)

        self.bt_voltar = tk.Button(frame_botoes, text="Voltar", command=self.voltar, font='Helvetica 12 bold',
                                   fg='white', bg=self.ROXO, cursor="hand2")
        self.bt_voltar.grid(row=0, column=0, pady=self.PADY, sticky="ew")

        self.bt_incluir = tk.Button(frame_botoes, text="Incluir", command=self.incluir, font='Helvetica 12 bold',
                                    fg='white', bg=self.ROXO, cursor="hand2")
        self.bt_incluir.grid(row=0, column=1, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.bt_alterar = tk.Button(frame_botoes, text="Alterar", command=self.alterar, font='Helvetica 12 bold',
                                    fg='white', bg=self.ROXO, cursor="hand2")
        self.bt_alterar.grid(row=0, column=2, pady=self.PADY, sticky="ew")

        self.bt_excluir = tk.Button(frame_botoes, text="Excluir", command=self.excluir, font='Helvetica 12 bold',
                                    fg='white', bg=self.ROXO, cursor="hand2")
        self.bt_excluir.grid(row=0, column=3, padx=self.PADX, pady=self.PADY, sticky="ew")

        self.bt_checkin = tk.Button(frame_botoes, text="Checkin", command=self.checkin, font='Helvetica 12 bold',
                                     fg='white', bg=self.ROXO, cursor="hand2")
        self.bt_checkin.grid(row=0, column=4, pady=self.PADY, sticky="ew")

        self.bt_checkout = tk.Button(frame_botoes, text="Checkout", command=self.checkout, font='Helvetica 12 bold',
                                     fg='white', bg=self.ROXO, cursor="hand2")
        self.bt_checkout.grid(row=0, column=5, padx=(self.PADY, 0), sticky="ew")

        # Criando o objeto que irá acessar o banco de dados
        self.sql = SQL(esquema='bd_gestao_visitantes')

    def consultar(self):
        data = self.et_dta.get()

        if data is not None and data != '':
            data = datetime.strptime(data, '%d/%m/%Y').date()
        else:
            data = None

        cmd = (
            "SELECT vta.idt_visitas, DATE_FORMAT(vta.dta_visita, '%d/%m/%Y') as data_visita, "
            "TIME_FORMAT(vta.hra_entrada_visita, '%H:%i') as hora_entrada, "
            "TIME_FORMAT(vta.hra_saida_visita, '%H:%i') as hora_saida, vte.nme_visitante, "
            "loc.nme_local, alu.nme_aluno_acompanhante "
            "FROM ta_visitas vta "
            "LEFT JOIN tb_visitantes vte ON vta.cod_visitantes=vte.idt_visitantes "
            "LEFT JOIN tb_locais loc ON vta.cod_locais=loc.idt_local "
            "LEFT JOIN tb_aluno_acompanhante alu ON vte.cod_aluno_acompanhante=alu.idt_aluno_acompanhante "
            "WHERE (%s IS NULL OR dta_visita = %s)"
        )

        funcoes = self.sql.get_list(cmd, [data, data])

        self.limpar_tabela()
        for funcao in funcoes:
            hra_ent = datetime.strptime(funcao['hora_entrada'], '%H:%M')
            hra_invalida = datetime.strptime('00:00', '%H:%M')

            if hra_ent == hra_invalida:
                funcao['hora_entrada'] = 'C.I.'
            if funcao['hora_saida'] is None:
                funcao['hora_saida'] = 'C.O.'
            if funcao['nme_aluno_acompanhante'] is None:
                funcao['nme_aluno_acompanhante'] = 'N. Acompanhado'

            self.tre_funcoes.insert("", tk.END,
                                    values=(funcao['idt_visitas'], funcao['data_visita'], funcao['hora_entrada'],
                                            funcao['hora_saida'], funcao['nme_visitante'],
                                            funcao['nme_local'], funcao['nme_aluno_acompanhante']))

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
        idt = self.pegar_idt()
        if idt != 0:
            u = AlterarVisitas(self, idt)
            self.et_dta.delete(0, tk.END)
            self.limpar_tabela()
        else:
            messagebox.showerror("Erro: Escolha uma função", "Marque uma linha da tabela para selecionar o projeto")

    def excluir(self):
        idt = self.pegar_idt()
        if idt != 0:
            d = ExcluirVisitas(self, idt)
            self.et_dta.delete(0, tk.END)
            self.limpar_tabela()
        else:
            messagebox.showerror("Erro: Escolha uma função", "Marque uma linha da tabela para selecionar a função")

    def checkout(self):
        idt = self.pegar_idt()
        if idt:
            CheckoutVisitas(self, idt)
            self.limpar_tabela()
        else:
            messagebox.showerror("Erro",
                                 "Selecione um registro para realizar o checkout.")

    def checkin(self):
        idt = self.pegar_idt()
        if idt:
            CheckinVisitas(self, idt)
            self.limpar_tabela()
        else:
            messagebox.showerror("Erro",
                                 "Selecione um registro para realizar o checkin.")

    def voltar(self):
        from menu_principal.tela_menu import MainMenu
        self.destroy()
        MainMenu()


if __name__ == '__main__':
    app = CRUDta_visita()
    app.mainloop()