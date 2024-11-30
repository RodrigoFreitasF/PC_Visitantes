import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import util.validate as val


class ExcluirVisitante:
    def __init__(self, janela_mestre, idt):
        # Cria uma nova janela (pop-up)
        self.popup = tk.Toplevel(janela_mestre)
        self.popup.grab_set()

        # Constantes
        PADX = 10
        PADY = 10
        self.ROXO = "#662c92"

        # Variáveis
        self.obrigatorios = []
        linha = 0

        # Buscar dados que já estão na base
        cmd = (
            "SELECT v.idt_visitantes, v.nme_visitante, v.rg_visitante, v.eml_visitante, v.pcd_visitante, "
            "a.idt_aluno_acompanhante, a.nme_aluno_acompanhante "
            "FROM tb_visitantes v "
            "LEFT JOIN tb_aluno_acompanhante a ON v.cod_aluno_acompanhante = a.idt_aluno_acompanhante "
            "WHERE v.idt_visitantes = %s")
        funcao = janela_mestre.sql.get_object(cmd, [idt])

        # Primeira linha - Título
        titulo = tk.Label(self.popup, text="Excluir Visitante", font='Helvetica 16 bold', fg=self.ROXO)
        titulo.grid(row=linha, column=0, columnspan=4, padx=PADX, pady=PADY)
        linha += 1

        # Segunda linha - Mostrar o identificador do visitante (readonly)
        lb_idt = tk.Label(self.popup, text="Identificador", font='Helvetica 12 bold', fg=self.ROXO)
        lb_idt.grid(row=linha, column=0, padx=PADX, pady=PADY)

        self.idt_var = tk.StringVar()
        self.idt_var.set(funcao['idt_visitantes'])
        self.et_idt = ttk.Label(self.popup, textvariable=self.idt_var, font='Helvetica 16 bold',
                                foreground=self.ROXO, width=5)
        self.et_idt.grid(row=linha, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")
        linha += 1

        # Terceira linha - Receber o Nome do Visitante
        lb_nome = tk.Label(self.popup, text="Nome", font='Helvetica 12 bold', fg=self.ROXO)
        lb_nome.grid(row=linha, column=0, padx=PADX, pady=PADY)

        self.nome_var = tk.StringVar()
        self.nome_var.set(funcao['nme_visitante'])
        self.et_nome = ttk.Label(self.popup, textvariable=self.nome_var, font='Helvetica 16 bold',
                                 foreground=self.ROXO, width=28)
        self.et_nome.grid(row=linha, column=1, columnspan=3, padx=PADX, pady=PADY)
        linha += 1

        # Quarta linha - Receber o RG do visitante
        lb_rg = tk.Label(self.popup, text="RG", font='Helvetica 12 bold', fg=self.ROXO)
        lb_rg.grid(row=linha, column=0, padx=PADX, pady=PADY)

        self.rg_var = tk.StringVar()
        self.rg_var.set(funcao['rg_visitante'])
        self.et_rg = ttk.Label(self.popup, textvariable=self.rg_var, font='Helvetica 16 bold',
                               foreground=self.ROXO, width=28)
        self.et_rg.grid(row=linha, column=1, columnspan=3, padx=PADX, pady=PADY)
        linha += 1

        # Quinta linha - Receber o Email do visitante
        lb_email = tk.Label(self.popup, text="Email", font='Helvetica 12 bold', fg=self.ROXO)
        lb_email.grid(row=linha, column=0, padx=PADX, pady=PADY)

        self.email_var = tk.StringVar()
        self.email_var.set(funcao['eml_visitante'] if funcao['eml_visitante'] else "")
        self.et_email = ttk.Label(self.popup, textvariable=self.email_var, font='Helvetica 16 bold',
                                  foreground=self.ROXO, width=28)
        self.et_email.grid(row=linha, column=1, columnspan=3, padx=PADX, pady=PADY)
        linha += 1

        # Sexta linha - Receber PCD
        lb_pcd = tk.Label(self.popup, text="PCD", font='Helvetica 12 bold', fg=self.ROXO)
        lb_pcd.grid(row=linha, column=0, padx=PADX, pady=PADY)

        self.pcd_var = tk.StringVar()
        self.pcd_var.set(funcao['pcd_visitante'] if funcao['pcd_visitante'] else "")
        self.cb_pcd = ttk.Label(self.popup, textvariable=self.pcd_var, font='Helvetica 16 bold',
                                foreground=self.ROXO, width=28)
        self.cb_pcd.grid(row=linha, column=1, columnspan=3, padx=PADX, pady=PADY)
        linha += 1

        # Sétima linha - Receber aluno acompanhante
        lb_acompanhante = tk.Label(self.popup, text="Acompanhante", font='Helvetica 12 bold', fg=self.ROXO)
        lb_acompanhante.grid(row=linha, column=0, padx=PADX, pady=PADY)

        self.acompanhante_var = tk.StringVar()
        acompanhante = f"{funcao['idt_aluno_acompanhante']} - {funcao['nme_aluno_acompanhante']}" if funcao[
            'idt_aluno_acompanhante'] else ""
        self.acompanhante_var.set(acompanhante)
        self.cb_acompanhante = ttk.Label(self.popup, textvariable=self.acompanhante_var, font='Helvetica 16 bold',
                                         foreground=self.ROXO, width=28)
        self.cb_acompanhante.grid(row=linha, column=1, columnspan=3, padx=PADX, pady=PADY)
        linha += 1

        # Oitava linha - Operação de Excluir
        self.bt_excluir = tk.Button(self.popup, text="Excluir", command=lambda: self.excluir(janela_mestre),
                                    font='Helvetica 12 bold',
                                    fg='white',
                                    bg=self.ROXO)
        self.bt_excluir.grid(row=linha, column=0, columnspan=4, padx=PADX, pady=PADY, sticky="ew")
        self.et_nome.focus()

        # Botão para confirmar a exclusão

    def excluir(self, janela_mestre):
        resposta = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este visitante?")
        if resposta:
            idt = int(self.idt_var.get())
            # Excluir os dados no banco de dados
            cmd = "DELETE FROM ta_visitas WHERE cod_visitantes = %s"
            janela_mestre.sql.upd_del(cmd, [idt])

            cmd = "DELETE FROM tb_visitantes WHERE idt_visitantes = %s"
            janela_mestre.sql.upd_del(cmd, [idt])
            # Fechar a janela pop-up
            self.popup.destroy()
