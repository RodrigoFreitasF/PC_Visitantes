#Delete de ta_visitas

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime

class ExcluirVisitas:
    def __init__(self, janela_mestre, idt):
        # Cria uma nova janela (pop-up)
        self.popup = tk.Toplevel(janela_mestre)
        self.popup.grab_set()

        # Constantes
        PADX = 10
        PADY = 10

        # Variáveis
        linha = 0

        # Buscar dados que já estão na base
        cmd = "SELECT * FROM ta_visitas WHERE idt_visitas = %s"
        funcao = janela_mestre.sql.get_object(cmd, [idt])

        # Primeira linha - Título
        titulo = tk.Label(self.popup, text="Excluir Visita", font='Helvetica 16 bold', fg='blue')
        titulo.grid(row=1, column=0, columnspan=3, padx=PADX, pady=PADY)

        # Segunda linha - Identificador da função
        lb_idt = tk.Label(self.popup, text="IDT da visita", font='Helvetica 12 bold', fg='blue')
        lb_idt.grid(row=2, column=0, padx=PADX, pady=PADY)

        self.idt_var = tk.StringVar()
        self.idt_var.set(funcao['idt_visitas'])
        self.lb_dado_idt = tk.Label(self.popup, textvariable=self.idt_var, font='Helvetica 16 bold',
                                    foreground='green')
        self.lb_dado_idt.grid(row=2, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")

        # Terceira linha - Receber a data da visita
        lb_nome = tk.Label(self.popup, text="Data da visita", font='Helvetica 12 bold', fg='blue')
        lb_nome.grid(row=3, column=0, padx=PADX, pady=PADY)

        self.nome_var = tk.StringVar()

        data_sql = funcao['dta_visita']
        dataf = datetime.strptime(str(data_sql), '%Y-%m-%d').date()
        self.nome_var.set(dataf.strftime('%d/%m/%Y'))

        self.lb_dado_nome = tk.Label(self.popup, textvariable=self.nome_var, font='Helvetica 16 bold',
                                     foreground='green')
        self.lb_dado_nome.grid(row=3, column=1, columnspan=2, padx=PADX, pady=PADY)

        # Receber a hora de entrada
        lb_valor = tk.Label(self.popup, text="Hora de entrada", font='Helvetica 12 bold', fg='blue')
        lb_valor.grid(row=4, column=0, padx=PADX, pady=PADY)

        self.valor_var = tk.StringVar()

        hora_sql = funcao['hra_entrada_visita']
        horaef = datetime.strptime(str(hora_sql), '%H:%M:%S').time()
        self.valor_var.set(horaef.strftime('%H:%M'))

        self.lb_dado_valor = tk.Label(self.popup, textvariable=self.valor_var, font='Helvetica 16 bold',
                                      foreground='green')
        self.lb_dado_valor.grid(row=4, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")

        # Receber a hora de saida
        lb_hra_saida = tk.Label(self.popup, text="Hora de saida", font='Helvetica 12 bold', fg='blue')
        lb_hra_saida.grid(row=5, column=0, padx=PADX, pady=PADY)

        self.valor_var2 = tk.StringVar()

        hora_sql2 = funcao['hra_saida_visita']
        horasf = datetime.strptime(str(hora_sql2), '%H:%M:%S').time()
        self.valor_var2.set(horasf.strftime('%H:%M'))
        self.lb_dado_valor = tk.Label(self.popup, textvariable=self.valor_var2, font='Helvetica 16 bold',
                                      foreground='green')
        self.lb_dado_valor.grid(row=5, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")

        '''# Quinta linha - Data fim projeto
        lb_valor = tk.Label(self.popup, text="Data final do projeto", font='Helvetica 12 bold', fg='blue')
        lb_valor.grid(row=5, column=0, padx=PADX, pady=PADY)

        self.valor_var = tk.StringVar()
        self.valor_var.set(funcao['dta_fim_projeto'])
        self.lb_dado_valor = tk.Label(self.popup, textvariable=self.valor_var, font='Helvetica 16 bold',
                                      foreground='green')
        self.lb_dado_valor.grid(row=5, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")'''

        # Quinta Linha - Operação de Excluir
        self.bt_excluir = tk.Button(self.popup, text="Excluir o registro", command=lambda: self.excluir(janela_mestre),
                                    font='Helvetica 12 bold',
                                    fg='white',
                                    bg='blue')
        self.bt_excluir.grid(row=6, column=0, columnspan=3, padx=PADX, pady=PADY)
        self.bt_excluir.focus()


    # Botão para confirmar a exclusão
    def excluir(self, janela_mestre):
        resposta = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este registro de visita?")
        if resposta:
            idt = int(self.idt_var.get())
            # Excluir os dados no banco de dados
            cmd = "DELETE FROM ta_visitas WHERE idt_visitas = %s"
            num_reg = janela_mestre.sql.upd_del(cmd, [idt])
            # Fechar a janela pop-up
            self.popup.destroy()
