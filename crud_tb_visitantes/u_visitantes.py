import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import util.validate as val


class AlterarVisitante:
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
        titulo = tk.Label(self.popup, text="Alterar Visitante", font='Helvetica 16 bold', fg=self.ROXO)
        titulo.grid(row=linha, column=0, columnspan=4, padx=PADX, pady=PADY)
        linha += 1

        # Segunda linha - Mostrar o identificador do visitante (readonly)
        lb_idt = tk.Label(self.popup, text="Identificador", font='Helvetica 12 bold', fg=self.ROXO)
        lb_idt.grid(row=linha, column=0, padx=PADX, pady=PADY)

        self.idt_var = tk.StringVar()
        self.idt_var.set(funcao['idt_visitantes'])
        self.et_idt = ttk.Entry(self.popup, textvariable=self.idt_var, font='Helvetica 16 bold',
                                foreground=self.ROXO, width=5, state="readonly")
        self.et_idt.grid(row=linha, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")
        linha += 1

        # Terceira linha - Receber o Nome do Visitante
        lb_nome = tk.Label(self.popup, text="Nome", font='Helvetica 12 bold', fg=self.ROXO)
        lb_nome.grid(row=linha, column=0, padx=PADX, pady=PADY)

        self.nome_var = tk.StringVar()
        self.nome_var.set(funcao['nme_visitante'])
        self.et_nome = ttk.Entry(self.popup, textvariable=self.nome_var, font='Helvetica 16 bold',
                                 foreground=self.ROXO, width=30)
        val.limitar_tamanho(self.et_nome, 45)
        self.obrigatorios.append([self.et_nome, lb_nome.cget('text')])
        self.et_nome.grid(row=linha, column=1, columnspan=3, padx=PADX, pady=PADY)
        linha += 1

        # Quarta linha - Receber o RG do visitante
        lb_rg = tk.Label(self.popup, text="RG", font='Helvetica 12 bold', fg=self.ROXO)
        lb_rg.grid(row=linha, column=0, padx=PADX, pady=PADY)

        self.rg_var = tk.StringVar()
        self.rg_var.set(funcao['rg_visitante'])
        self.et_rg = ttk.Entry(self.popup, textvariable=self.rg_var, font='Helvetica 16 bold',
                               foreground=self.ROXO, width=30)
        val.limitar_tamanho(self.et_rg, 10)
        self.obrigatorios.append([self.et_rg, lb_rg.cget('text')])
        self.et_rg.grid(row=linha, column=1, columnspan=3, padx=PADX, pady=PADY)
        linha += 1

        # Quinta linha - Receber o Email do visitante
        lb_email = tk.Label(self.popup, text="Email", font='Helvetica 12 bold', fg=self.ROXO)
        lb_email.grid(row=linha, column=0, padx=PADX, pady=PADY)

        self.email_var = tk.StringVar()
        self.email_var.set(funcao['eml_visitante'] if funcao['eml_visitante'] else "")
        self.et_email = ttk.Entry(self.popup, textvariable=self.email_var, font='Helvetica 16 bold',
                                  foreground=self.ROXO, width=30)
        val.limitar_tamanho(self.et_email, 45)
        self.et_email.grid(row=linha, column=1, columnspan=3, padx=PADX, pady=PADY)
        linha += 1

        # Sexta linha - Seleção PCD
        lb_pcd = tk.Label(self.popup, text="PCD", font='Helvetica 12 bold', fg=self.ROXO)
        lb_pcd.grid(row=linha, column=0, padx=PADX, pady=PADY)

        self.pcd_var = tk.StringVar()
        self.pcd_var.set(funcao['pcd_visitante'] if funcao['pcd_visitante'] else "")
        self.cb_pcd = ttk.Combobox(self.popup, textvariable=self.pcd_var, font='Helvetica 16 bold',
                                   foreground=self.ROXO, width=28, state="readonly")
        self.cb_pcd['values'] = ["Sim", "Não"]
        self.cb_pcd.grid(row=linha, column=1, columnspan=3, padx=PADX, pady=PADY)
        linha += 1

        # Sétima linha - Seleção do aluno acompanhante
        lb_acompanhante = tk.Label(self.popup, text="Acompanhante", font='Helvetica 12 bold', fg=self.ROXO)
        lb_acompanhante.grid(row=linha, column=0, padx=PADX, pady=PADY)

        self.acompanhante_var = tk.StringVar()
        acompanhante = f"{funcao['idt_aluno_acompanhante']} - {funcao['nme_aluno_acompanhante']}" if funcao[
            'idt_aluno_acompanhante'] else ""
        self.acompanhante_var.set(acompanhante)
        self.cb_acompanhante = ttk.Combobox(self.popup, textvariable=self.acompanhante_var, font='Helvetica 16 bold',
                                            width=28, state="readonly", foreground=self.ROXO)
        self.cb_acompanhante.grid(row=linha, column=1, columnspan=3, padx=PADX, pady=PADY)

        # Consultar o banco de dados para obter os acompanhantes
        cmd = "SELECT idt_aluno_acompanhante, nme_aluno_acompanhante FROM tb_aluno_acompanhante ORDER BY nme_aluno_acompanhante"
        alunos = janela_mestre.sql.get_list(cmd)

        self.cb_acompanhante['values'] = [
            f"{acompanhante['idt_aluno_acompanhante']} - {acompanhante['nme_aluno_acompanhante']}" for
            acompanhante in
            alunos]
        linha += 1

        # Oitava linha - Botão para salvar alterações
        self.bt_alterar = tk.Button(self.popup, text="Alterar", command=lambda: self.alterar(janela_mestre),
                                    font='Helvetica 12 bold',
                                    fg='white',
                                    bg=self.ROXO)
        self.bt_alterar.grid(row=linha, column=0, columnspan=4, padx=PADX, pady=PADY, sticky="ew")
        self.et_nome.focus()

    # Botão para confirmar a alteração
    def alterar(self, janela_mestre):
        retorno = val.todos_campos_preenchidos(self.obrigatorios)
        if retorno[0]:
            nome = self.nome_var.get()
            rg = self.rg_var.get()
            email = self.email_var.get()
            pcd = self.pcd_var.get()
            pcd_valor = "S" if pcd == "Sim" else "N"
            acompanhante_selecionado = self.acompanhante_var.get()
            if acompanhante_selecionado:
                idt_acompanhante = acompanhante_selecionado.split(" - ")[0]
            else:
                idt_acompanhante = None
            idt = int(self.idt_var.get())
            # Alterar os dados no banco de dados
            cmd = ("UPDATE tb_visitantes SET nme_visitante = %s, rg_visitante = %s, eml_visitante = %s, "
                   "pcd_visitante = %s, cod_aluno_acompanhante = %s "
                   "WHERE idt_visitantes = %s")
            janela_mestre.sql.upd_del(cmd, (nome, rg, email, pcd_valor, idt_acompanhante, idt))
            # Fechar a janela pop-up
            self.popup.destroy()
        else:
            messagebox.showerror("Erro: Campo(s) obrigatório(s)",
                                 "O(s) seguinte(s) campo(s) é/são obrigatório(s):\n" + retorno[1])
