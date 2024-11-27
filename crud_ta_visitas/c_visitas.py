#Create de ta_visitas

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import util.validate as val
from tkcalendar import DateEntry
from datetime import datetime

class IncluirVisitas:
    def __init__(self, janela_mestre):
        # Cria uma nova janela (pop-up)
        self.popup = tk.Toplevel(janela_mestre)
        self.popup.grab_set()

        # Constantes de cores
        cor_btn = '#43054e'
        fonte_btn = 'Jakob 12 bold'
        cor_dados = '#662c92'
        cor_titulo = '#bf0087'

        # Constantes
        PADX = 10
        PADY = 10
        self.obrigatorios = []

        # Primeira linha - Título
        titulo = tk.Label(self.popup, text="Incluir Visitas", font='Helvetica 16 bold', fg=cor_titulo)
        titulo.grid(row=0, column=0, columnspan=3, padx=PADX, pady=PADY)

        #Receber a data da visita
        lb_dta_visita = tk.Label(self.popup, text="Data da visita", font='Helvetica 12 bold', fg=cor_titulo)
        lb_dta_visita.grid(row=2, column=0, padx=PADX, pady=PADY)

        self.valor_dta = ttk.Style()
        self.et_dta = DateEntry(self.popup, textvariable=self.valor_dta, font='Helvetica 16 bold',
                                width=10, date_pattern='dd/mm/yyyy', date_format='%d/%m/%Y', locale='pt_BR',firstweekday="sunday" ,
                                foreground='#ec0089', weekendforeground='Red', weekendbackground='pink', headersforeground='#43054e',
                                selectbackground='#ec0089')
        self.obrigatorios.append([self.et_dta, lb_dta_visita.cget('text')])
        self.et_dta.grid(row=2, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")

        #Input de hora de entrada
        lb_hra_ent = tk.Label(self.popup, text="Hora de entrada", font='Helvetica 12 bold', fg=cor_titulo)
        lb_hra_ent.grid(row=3, column=0, padx=PADX, pady=PADY)

        self.valor_hra_ent = tk.StringVar()
        self.et_hra_ent = ttk.Entry(self.popup, textvariable=self.valor_hra_ent, font='Helvetica 16 bold', foreground=cor_dados,
                                   width=10)
        self.et_hra_ent.grid(row=3, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")

        #input de código do visitante
        lb_cod_visitante = tk.Label(self.popup, text="IDT do visitante", font='Helvetica 12 bold', fg=cor_titulo)
        lb_cod_visitante.grid(row=5, column=0, padx=PADX, pady=PADY)
        self.valor_cod_visitante = tk.StringVar()
        self.et_cod_visitante = ttk.Entry(self.popup, textvariable=self.valor_cod_visitante, font='Helvetica 16 bold',
                                          foreground=cor_dados,
                                          width=10)
        self.et_cod_visitante.grid(row=5, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")

        # input de código do campus
        lb_cod_campus = tk.Label(self.popup, text="Código do Local", font='Helvetica 12 bold', fg=cor_titulo)
        lb_cod_campus.grid(row=6, column=0, padx=PADX, pady=PADY)
        self.valor_cod_campus = tk.StringVar()
        self.et_cod_campus = ttk.Entry(self.popup, textvariable=self.valor_cod_campus, font='Helvetica 16 bold',
                                       foreground=cor_dados, width=10)
        self.et_cod_campus.grid(row=6, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")

        #Botão para incluir uma nova função
        self.bt_salvar = tk.Button(self.popup, text="Incluir nova visita", command=lambda: self.salvar(janela_mestre),
                                   font=fonte_btn, fg='white', bg=cor_btn)
        self.bt_salvar.grid(row=7, column=0, columnspan=3, padx=PADX, pady=PADY)
        self.et_dta.focus()

    # Botão para confirmar a inclusão
    def salvar(self, janela_mestre):
        retorno = val.todos_campos_preenchidos(self.obrigatorios)
        if retorno[0]:
            dta_visita = self.et_dta.get()
            dta_conv = datetime.strptime(dta_visita, '%d/%m/%Y').date()
            hra_entrada_visita = self.et_hra_ent.get()
            hra_saida_visita = None #deverá ser preenchido pelo usuário quando o visitante realizar o checkout
            cod_visitante = self.valor_cod_visitante.get()
            cod_campus = self.valor_cod_campus.get()

            # Inserir os dados no banco de dados
            cmd = "insert into ta_visitas (dta_visita, hra_entrada_visita, hra_saida_visita, cod_visitantes, cod_locais) values (%s, %s, %s, %s, %s)"
            if hra_saida_visita == '':
                id = janela_mestre.sql.insert(cmd, (dta_conv, hra_entrada_visita, None, cod_visitante, cod_campus))
            else:
                id = janela_mestre.sql.insert(cmd, (dta_conv, hra_entrada_visita, hra_saida_visita, cod_visitante, cod_campus))
            # Fechar a janela pop-up
            self.popup.destroy()
        else:
            messagebox.showerror("Erro: Campo(s) obrigatório(s)",
                                 "O(s) seguinte(s) campo(s) é/são obrigatório(s):\n" + retorno[1])