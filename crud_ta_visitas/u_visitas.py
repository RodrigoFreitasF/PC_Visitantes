#Update de ta_visitas

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import util.validate as val
from tkcalendar import DateEntry
from datetime import datetime

class AlterarVisitas:
    def __init__(self, janela_mestre, idt):
        self.popup = tk.Toplevel(janela_mestre)
        self.popup.grab_set()

        PADX = 10
        PADY = 10

        # Constantes de cores
        cor_btn = '#43054e'
        fonte_btn = 'Jakob 12 bold'
        cor_dados = '#662c92'
        cor_titulo = '#bf0087'

        self.obrigatorios = []
        linha = 0

        cmd = "SELECT * FROM ta_visitas WHERE idt_visitas = %s"
        funcao = janela_mestre.sql.get_object(cmd, [idt])

        #Título
        titulo = tk.Label(self.popup, text="Alterar Visita", font='Helvetica 16 bold', fg=cor_titulo)
        titulo.grid(row=1, column=0, columnspan=3, padx=PADX, pady=PADY)

        #Idt da visita (readonly)
        lb_idt = tk.Label(self.popup, text="Identificador", font='Helvetica 12 bold', fg=cor_titulo)
        lb_idt.grid(row=2, column=0, padx=PADX, pady=PADY)

        self.idt_var = tk.StringVar()
        self.idt_var.set(funcao['idt_visitas'])
        self.et_idt = ttk.Entry(self.popup, textvariable=self.idt_var, font='Helvetica 16 bold',
                                foreground=cor_dados, width=5, state="readonly")
        self.et_idt.grid(row=2, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")

        #Data de visita
        lb_data = tk.Label(self.popup, text="Data de visita", font='Helvetica 12 bold', fg=cor_titulo)
        lb_data.grid(row=5, column=0, padx=PADX, pady=PADY)

        self.valor_data = tk.StringVar()
        self.valor_data.set((funcao['dta_visita']))
        self.et_data = DateEntry(self.popup, textvariable=self.valor_data, font='Helvetica 16 bold',
                                width=10, date_pattern='dd/mm/yyyy', date_format='%d/%m/%Y', locale='pt_BR',firstweekday="sunday" ,
                                foreground='#ec0089', weekendforeground='Red', weekendbackground='pink', headersforeground='#43054e',
                                selectbackground='#ec0089')
        self.obrigatorios.append([self.et_data])
        self.et_data.grid(row=5, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")

        #Hora de entrada
        lb_hra_ent = tk.Label(self.popup, text="Hora de entrada", font='Helvetica 12 bold', fg=cor_titulo)
        lb_hra_ent.grid(row=6, column=0, padx=PADX, pady=PADY)

        self.valor_hra_ent = tk.StringVar()
        self.et_hra_ent = ttk.Entry(self.popup, textvariable=self.valor_hra_ent, font='Helvetica 16 bold', foreground=cor_dados,
                                 width=10)
        self.obrigatorios.append([self.et_hra_ent])
        self.et_hra_ent.grid(row=6, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")

        #Hora de saída
        lb_hra_saida = tk.Label(self.popup, text="Hora de saída", font='Helvetica 12 bold', fg=cor_titulo)
        lb_hra_saida.grid(row=7, column=0, padx=PADX, pady=PADY)

        self.valor_hra_saida = tk.StringVar()
        self.et_hra_saida = ttk.Entry(self.popup, textvariable=self.valor_hra_saida, font='Helvetica 16 bold',
                                    foreground=cor_dados,
                                    width=10)
        self.obrigatorios.append([self.et_hra_saida])
        self.et_hra_saida.grid(row=7, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")

        #Alterar visitante
        lb_visitante = tk.Label(self.popup, text="Codigo do Visitante", font='Helvetica 12 bold', fg=cor_titulo)
        lb_visitante.grid(row=8, column=0, padx=PADX, pady=PADY)

        self.valor_visitante = tk.StringVar()
        self.valor_visitante.set(funcao['cod_campus'])
        self.et_visitante = ttk.Entry(self.popup, textvariable=self.valor_visitante, font='Helvetica 16 bold',
                                    foreground=cor_dados, width=10)
        self.obrigatorios.append([self.et_visitante])
        self.et_visitante.grid(row=8, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")

        #Alterar Campus
        lb_campus = tk.Label(self.popup, text="Codigo do campus", font='Helvetica 12 bold', fg=cor_titulo)
        lb_campus.grid(row=9, column=0, padx=PADX, pady=PADY)

        self.valor_campus = tk.StringVar()
        self.valor_campus.set(funcao['cod_campus'])
        self.et_campus = ttk.Entry(self.popup, textvariable=self.valor_campus, font='Helvetica 16 bold',
                                      foreground=cor_dados, width=10)
        self.obrigatorios.append([self.et_campus])
        self.et_campus.grid(row=9, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")

        #Botão para salvar alterações
        self.bt_alterar = tk.Button(self.popup, text="Alterar a Função", command=lambda: self.alterar(janela_mestre),
                                    font='Helvetica 12 bold',
                                    fg='white',
                                    bg=cor_btn)
        self.bt_alterar.grid(row=10, column=0, columnspan=3, padx=PADX, pady=PADY)
        self.et_idt.focus()

    # executar a alteração
    def alterar(self, janela_mestre):
        retorno = val.todos_campos_preenchidos(self.obrigatorios)
        if retorno[0]:
            idt = int(self.idt_var.get())
            data1 = self.valor_data.get()
            data1conv = datetime.strptime(data1, '%d/%m/%Y').date()
            hra_ent = self.valor_hra_ent.get()
            hra_entrada = datetime.strptime(hra_ent, '%H:%M').time()
            hra_sai = self.valor_hra_saida.get()
            hra_saida = datetime.strptime(hra_sai, '%H:%M').time()
            visitante = self.valor_visitante.get()
            campus = self.valor_campus.get()

            cmd = "UPDATE ta_visitas SET dta_visita = %s, hra_entrada_visita = %s, hra_saida_visita = %s, cod_visitantes = %s, cod_campus = %s WHERE idt_visitas = %s"
            num_reg = janela_mestre.sql.upd_del(cmd, (data1conv, hra_entrada, hra_saida, visitante, campus, idt))
            self.popup.destroy()
        else:
            messagebox.showerror("Erro: Campo(s) obrigatório(s)",
                                 "O(s) seguinte(s) campo(s) é/são obrigatório(s):\n" + retorno[1])