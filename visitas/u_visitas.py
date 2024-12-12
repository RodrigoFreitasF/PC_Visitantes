import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
import util.validate as val


class AlterarVisitas:
    def __init__(self, janela_mestre, idt):
        # Cria uma nova janela (pop-up)
        self.popup = tk.Toplevel(janela_mestre)
        self.popup.grab_set()
        self.popup.iconbitmap("../ceub.ico")

        # Constantes
        self.PADX = 10
        self.PADY = 10
        self.ROXO = "#662c92"
        self.WIDTH = 30  # Largura padrão para os campos de entrada

        # Variáveis
        self.obrigatorios = []

        # Consultar dados da visita selecionada
        cmd = "SELECT * FROM ta_visitas WHERE idt_visitas = %s"
        visita = janela_mestre.sql.get_object(cmd, [idt])

        # Primeira linha - Título
        titulo = tk.Label(self.popup, text="Alterar Visita", font='Helvetica 16 bold', fg=self.ROXO)
        titulo.grid(row=0, column=0, columnspan=2, padx=self.PADX, pady=self.PADY)

        # Segunda linha - Data da visita
        lb_dta_visita = tk.Label(self.popup, text="Data da visita", font='Helvetica 12 bold', fg=self.ROXO)
        lb_dta_visita.grid(row=1, column=0, padx=self.PADX, pady=self.PADY)

        self.et_dta = DateEntry(self.popup, font='Helvetica 12', width=28, date_pattern='dd/mm/yyyy',
                                background='white', foreground=self.ROXO, headersforeground=self.ROXO)
        self.et_dta.set_date(visita['dta_visita'])
        self.obrigatorios.append([self.et_dta, lb_dta_visita.cget('text')])
        self.et_dta.grid(row=1, column=1, padx=self.PADX, pady=self.PADY, sticky="w")

        # Terceira linha - Hora de entrada
        lb_hra_ent = tk.Label(self.popup, text="Hora de entrada", font='Helvetica 12 bold', fg=self.ROXO)
        lb_hra_ent.grid(row=2, column=0, padx=self.PADX, pady=self.PADY)

        self.valor_hra_ent = tk.StringVar(value=visita['hra_entrada_visita'] if visita['hra_entrada_visita'] else "")
        self.et_hra_ent = ttk.Entry(self.popup, textvariable=self.valor_hra_ent, font='Helvetica 12',
                                    foreground=self.ROXO, width=self.WIDTH)
        self.et_hra_ent.grid(row=2, column=1, padx=self.PADX, pady=self.PADY, sticky="w")

        # Quarta linha - Código do visitante
        lb_visitante = tk.Label(self.popup, text="Visitante", font='Helvetica 12 bold', fg=self.ROXO)
        lb_visitante.grid(row=3, column=0, padx=self.PADX, pady=self.PADY)

        self.visitante_var = tk.StringVar()
        self.cb_visitante = ttk.Combobox(self.popup, textvariable=self.visitante_var, font='Helvetica 12',
                                         state="readonly", width=28)
        self.cb_visitante.grid(row=3, column=1, padx=self.PADX, pady=self.PADY, sticky="w")

        # Preencher combobox com os visitantes
        cmd = "SELECT idt_visitantes, nme_visitante FROM tb_visitantes ORDER BY nme_visitante"
        visitantes = janela_mestre.sql.get_list(cmd)
        self.cb_visitante['values'] = [
            f"{visitante['idt_visitantes']} - {visitante['nme_visitante']}" for visitante in visitantes
        ]

        # Selecionar visitante atual
        for visitante in self.cb_visitante['values']:
            if visitante.startswith(str(visita['cod_visitantes'])):
                self.cb_visitante.set(visitante)
                break
        self.obrigatorios.append([self.cb_visitante, lb_visitante.cget('text')])

        # Quinta linha - Local
        lb_local = tk.Label(self.popup, text="Local", font='Helvetica 12 bold', fg=self.ROXO)
        lb_local.grid(row=4, column=0, padx=self.PADX, pady=self.PADY)

        self.local_var = tk.StringVar()
        self.cb_local = ttk.Combobox(self.popup, textvariable=self.local_var, font='Helvetica 12',
                                     state="readonly", width=28)
        self.cb_local.grid(row=4, column=1, padx=self.PADX, pady=self.PADY, sticky="w")

        # Preencher combobox com os locais
        cmd = """SELECT lc.idt_local, lc.nme_local, cp.nme_campus 
                 FROM tb_locais lc 
                 JOIN tb_campus cp ON cp.idt_campus = lc.cod_campus 
                 ORDER BY nme_local"""
        locais = janela_mestre.sql.get_list(cmd)
        self.cb_local['values'] = [
            f"{local['idt_local']} - {local['nme_local']} - {local['nme_campus']}" for local in locais
        ]

        # Selecionar local atual
        for local in self.cb_local['values']:
            if local.startswith(str(visita['cod_locais'])):
                self.cb_local.set(local)
                break
        self.obrigatorios.append([self.cb_local, lb_local.cget('text')])

        # Sexta linha - Botão para salvar alterações
        self.bt_alterar = tk.Button(self.popup, text="Alterar", command=lambda: self.alterar(janela_mestre, idt),
                                    font='Helvetica 12 bold', fg='white', bg=self.ROXO, cursor="hand2")
        self.bt_alterar.grid(row=5, column=0, columnspan=2, padx=self.PADX, pady=self.PADY, sticky="ew")
        self.et_dta.focus()

    def alterar(self, janela_mestre, idt):
        retorno = val.todos_campos_preenchidos(self.obrigatorios)
        if retorno[0]:
            dta_visita = self.et_dta.get()
            dta_conv = datetime.strptime(dta_visita, '%d/%m/%Y').date()
            hra_entrada_visita = self.et_hra_ent.get() if self.et_hra_ent.get() != '' else None

            visitante_selecionado = self.visitante_var.get()
            idt_visitante = visitante_selecionado.split(" - ")[0] if visitante_selecionado else None

            local_selecionado = self.local_var.get()
            idt_local = local_selecionado.split(" - ")[0] if local_selecionado else None

            # Atualizar os dados no banco de dados
            cmd = """UPDATE ta_visitas 
                     SET dta_visita = %s, hra_entrada_visita = %s, cod_visitantes = %s, cod_locais = %s 
                     WHERE idt_visitas = %s"""
            janela_mestre.sql.upd_del(cmd, (dta_conv, hra_entrada_visita, idt_visitante, idt_local, idt))
            self.popup.destroy()
        else:
            messagebox.showerror("Erro: Campo(s) obrigatório(s)",
                                 "O(s) seguinte(s) campo(s) é/são obrigatório(s):\n" + retorno[1])
