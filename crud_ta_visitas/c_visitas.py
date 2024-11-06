#Create de ta_visitas

import tkinter as tk
from tkinter import ttk, IntVar, Checkbutton
from tkinter import messagebox

from tktimepicker import AnalogPicker, AnalogThemes

#from jupyterlab.extensions import entry

#import dateconverter

import util.validate as val
from tkcalendar import DateEntry

from datetime import datetime

class IncluirVisitas:
    def __init__(self, janela_mestre):
        # Cria uma nova janela (pop-up)
        self.popup = tk.Toplevel(janela_mestre)
        self.popup.grab_set()

        # Constantes
        PADX = 10
        PADY = 10
        self.obrigatorios = []

        # Primeira linha - Título
        titulo = tk.Label(self.popup, text="Incluir Visitas", font='Helvetica 16 bold', fg='blue')
        titulo.grid(row=0, column=0, columnspan=3, padx=PADX, pady=PADY)

        # Segunda linha - Receber a data da visita
        '''lb_nome = tk.Label(self.popup, text="Dia da visita", font='Helvetica 12 bold', fg='blue')
        lb_nome.grid(row=1, column=0, padx=PADX, pady=PADY)

        self.nome_var = tk.StringVar()
        self.et_nome = ttk.Entry(self.popup, textvariable=self.nome_var, font='Helvetica 16 bold', foreground='green', width=30)
        val.limitar_tamanho(self.et_nome, 50)
        self.obrigatorios.append([self.et_nome, lb_nome.cget('text')])
        self.et_nome.grid(row=1, column=1, columnspan=2, padx=PADX, pady=PADY)'''

        # Terceira linha - Receber a data da visita
        lb_dta_visita = tk.Label(self.popup, text="Data da visita", font='Helvetica 12 bold', fg='blue')
        lb_dta_visita.grid(row=2, column=0, padx=PADX, pady=PADY)

        lb_hra_ent = tk.Label(self.popup, text="Hora de entrada", font='Helvetica 12 bold', fg='blue')
        lb_hra_ent.grid(row=3, column=0, padx=PADX, pady=PADY)

        self.valor_dta = tk.StringVar()
        self.et_valor = DateEntry(self.popup, textvariable=self.valor_dta, font='Helvetica 16 bold', foreground='green',
                                  width=10, date_pattern='dd/mm/yyyy', date_format='%d/%m/%Y')
        self.obrigatorios.append([self.et_valor, lb_dta_visita.cget('text')])
        self.et_valor.grid(row=2, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")

        #Input de hora de entrada
        self.valor_hra_ent = tk.StringVar()
        self.et_valor2 = ttk.Entry(self.popup, textvariable=self.valor_hra_ent, font='Helvetica 16 bold', foreground='green',
                                   width=10)
        self.et_valor2.grid(row=3, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")

        # Quarta linha - Botão para incluir uma nova função
        self.bt_salvar = tk.Button(self.popup, text="Incluir Novo Projeto", command=lambda: self.salvar(janela_mestre),
                                   font='Helvetica 12 bold',
                                   fg='white',
                                   bg='blue')
        self.bt_salvar.grid(row=4, column=0, columnspan=3, padx=PADX, pady=PADY)
        self.et_nome.focus()

    # Botão para confirmar a inclusão
    def salvar(self, janela_mestre):
        retorno = val.todos_campos_preenchidos(self.obrigatorios)
        if retorno[0]:
            nome = self.nome_var.get()
            valor1 = self.valor_dta.get()
            valor1conv = datetime.strptime(valor1, '%d/%m/%Y').date()
            valor2 = self.valor_hra_ent.get()
            valor2conv = datetime.strptime(valor2, '%d/%m/%Y').date()
            # Inserir os dados no banco de dados
            cmd = "insert into ta_visitas (dta_visita, hra_entrada_visita, hra_saida_visita, cod_visitantes, cod_campus) values (%s, %s, %s, %s, %s)"
            if valor2 == '':
                id = janela_mestre.sql.insert(cmd, (nome, valor1conv, None))
            else:
                id = janela_mestre.sql.insert(cmd, (nome, valor1conv,valor2conv))
            # Fechar a janela pop-up
            self.popup.destroy()
        else:
            messagebox.showerror("Erro: Campo(s) obrigatório(s)",
                                 "O(s) seguinte(s) campo(s) é/são obrigatório(s):\n" + retorno[1])