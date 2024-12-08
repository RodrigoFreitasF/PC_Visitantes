import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime


class ExcluirVisitas:
    def __init__(self, janela_mestre, idt):
        # Cria uma nova janela (pop-up)
        self.popup = tk.Toplevel(janela_mestre)
        self.popup.grab_set()
        self.popup.iconbitmap("../ceub.ico")

        # Constantes
        self.PADX = 10
        self.PADY = 10
        self.ROXO = "#662c92"

        linha = 0

        # Buscar dados que já estão na base
        cmd = (
            "SELECT v.idt_visitas, v.dta_visita, v.hra_entrada_visita, v.hra_saida_visita, "
            "lc.nme_local, vt.nme_visitante "
            "FROM ta_visitas v "
            "LEFT JOIN tb_visitantes vt ON v.cod_visitantes = vt.idt_visitantes "
            "LEFT JOIN tb_locais lc ON v.cod_locais = lc.idt_local "
            "WHERE v.idt_visitas = %s"
        )
        funcao = janela_mestre.sql.get_object(cmd, [idt])

        # Primeira linha - Título
        titulo = tk.Label(self.popup, text="Excluir Visita", font='Helvetica 16 bold', fg=self.ROXO)
        titulo.grid(row=linha, column=0, columnspan=4, padx=self.PADX, pady=self.PADY)
        linha += 1

        # Segunda linha - Mostrar o identificador da visita
        lb_idt = tk.Label(self.popup, text="Identificador", font='Helvetica 12 bold', fg=self.ROXO)
        lb_idt.grid(row=linha, column=0, padx=self.PADX, pady=self.PADY)

        self.idt_var = tk.StringVar()
        self.idt_var.set(funcao['idt_visitas'])
        self.et_idt = ttk.Label(self.popup, textvariable=self.idt_var, font='Helvetica 16 bold',
                                foreground=self.ROXO, width=5)
        self.et_idt.grid(row=linha, column=1, columnspan=2, padx=self.PADX, pady=self.PADY, sticky="W")
        linha += 1

        # Terceira linha - Nome do visitante
        lb_visitante = tk.Label(self.popup, text="Visitante", font='Helvetica 12 bold', fg=self.ROXO)
        lb_visitante.grid(row=linha, column=0, padx=self.PADX, pady=self.PADY)

        self.visitante_var = tk.StringVar()
        self.visitante_var.set(funcao['nme_visitante'])
        self.et_visitante = ttk.Label(self.popup, textvariable=self.visitante_var, font='Helvetica 16 bold',
                                      foreground=self.ROXO, width=28)
        self.et_visitante.grid(row=linha, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)
        linha += 1

        # Quarta linha - Data da visita
        lb_data = tk.Label(self.popup, text="Data", font='Helvetica 12 bold', fg=self.ROXO)
        lb_data.grid(row=linha, column=0, padx=self.PADX, pady=self.PADY)

        self.data_var = tk.StringVar()
        data_sql = funcao['dta_visita']
        self.data_var.set(datetime.strptime(str(data_sql), '%Y-%m-%d').strftime('%d/%m/%Y'))
        self.et_data = ttk.Label(self.popup, textvariable=self.data_var, font='Helvetica 16 bold',
                                 foreground=self.ROXO, width=28)
        self.et_data.grid(row=linha, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)
        linha += 1

        # Quinta linha - Hora de entrada
        lb_hora_entrada = tk.Label(self.popup, text="Hora de Entrada", font='Helvetica 12 bold', fg=self.ROXO)
        lb_hora_entrada.grid(row=linha, column=0, padx=self.PADX, pady=self.PADY)

        self.hora_entrada_var = tk.StringVar()
        self.hora_entrada_var.set(funcao['hra_entrada_visita'] if funcao['hra_entrada_visita'] else "Não registrada")
        self.et_hora_entrada = ttk.Label(self.popup, textvariable=self.hora_entrada_var, font='Helvetica 16 bold',
                                         foreground=self.ROXO, width=28)
        self.et_hora_entrada.grid(row=linha, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)
        linha += 1

        # Sexta linha - Hora de saída
        lb_hora_saida = tk.Label(self.popup, text="Hora de Saída", font='Helvetica 12 bold', fg=self.ROXO)
        lb_hora_saida.grid(row=linha, column=0, padx=self.PADX, pady=self.PADY)

        self.hora_saida_var = tk.StringVar()
        self.hora_saida_var.set(funcao['hra_saida_visita'] if funcao['hra_saida_visita'] else "Não registrada")
        self.et_hora_saida = ttk.Label(self.popup, textvariable=self.hora_saida_var, font='Helvetica 16 bold',
                                       foreground=self.ROXO, width=28)
        self.et_hora_saida.grid(row=linha, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)
        linha += 1

        # Sétima linha - Local da visita
        lb_local = tk.Label(self.popup, text="Local", font='Helvetica 12 bold', fg=self.ROXO)
        lb_local.grid(row=linha, column=0, padx=self.PADX, pady=self.PADY)

        self.local_var = tk.StringVar()
        self.local_var.set(funcao['nme_local'])
        self.et_local = ttk.Label(self.popup, textvariable=self.local_var, font='Helvetica 16 bold',
                                  foreground=self.ROXO, width=28)
        self.et_local.grid(row=linha, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)
        linha += 1

        # Oitava linha - Botão para excluir
        self.bt_excluir = tk.Button(self.popup, text="Excluir", command=lambda: self.excluir(janela_mestre),
                                    font='Helvetica 12 bold',
                                    fg='white',
                                    bg=self.ROXO,
                                    cursor="hand2")
        self.bt_excluir.grid(row=linha, column=0, columnspan=4, padx=self.PADX, pady=self.PADY, sticky="ew")
        self.et_visitante.focus()

    def excluir(self, janela_mestre):
        resposta = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir esta visita?")
        if resposta:
            idt = int(self.idt_var.get())
            # Excluir os dados no banco de dados
            cmd = "DELETE FROM ta_visitas WHERE idt_visitas = %s"
            janela_mestre.sql.upd_del(cmd, [idt])
            # Fechar a janela pop-up
            self.popup.destroy()
