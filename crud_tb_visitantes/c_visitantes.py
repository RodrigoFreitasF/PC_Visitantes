import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import util.validate as val


class CadastrarVisitante:
    def __init__(self, janela_mestre):
        # Cria uma nova janela (pop-up)
        self.popup = tk.Toplevel(janela_mestre)
        self.popup.grab_set()

        # Constantes
        self.PADX = 10
        self.PADY = 10
        self.ROXO = "#662c92"

        # Variáveis
        self.obrigatorios = []

        # Primeira linha - Título
        titulo = tk.Label(self.popup, text="Cadastrar Visitante", font='Helvetica 16 bold', fg=self.ROXO)
        titulo.grid(row=0, column=0, columnspan=4, padx=self.PADX, pady=self.PADY)

        # Segunda linha - Receber o nome do visitante
        lb_nome = tk.Label(self.popup, text="Nome", font='Helvetica 12 bold', fg=self.ROXO)
        lb_nome.grid(row=1, column=0, padx=self.PADX, pady=self.PADY)

        self.nome_var = tk.StringVar()
        self.et_nome = ttk.Entry(self.popup, textvariable=self.nome_var, font='Helvetica 16 bold',
                                 foreground=self.ROXO, width=30)
        val.limitar_tamanho(self.et_nome, 45)
        self.obrigatorios.append([self.et_nome, lb_nome.cget('text')])
        self.et_nome.grid(row=1, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)

        # Terceira linha - Receber o RG do visitante
        lb_rg = tk.Label(self.popup, text="RG", font='Helvetica 12 bold', fg=self.ROXO)
        lb_rg.grid(row=2, column=0, padx=self.PADX, pady=self.PADY)

        self.rg_var = tk.StringVar()
        self.et_rg = ttk.Entry(self.popup, textvariable=self.rg_var, font='Helvetica 16 bold',
                               foreground=self.ROXO, width=30)
        val.limitar_tamanho(self.et_rg, 10)
        self.obrigatorios.append([self.et_rg, lb_rg.cget('text')])
        self.et_rg.grid(row=2, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)

        # Quarta linha - Receber o Email do visitante
        lb_email = tk.Label(self.popup, text="Email", font='Helvetica 12 bold', fg=self.ROXO)
        lb_email.grid(row=3, column=0, padx=self.PADX, pady=self.PADY)

        self.email_var = tk.StringVar()
        self.et_email = ttk.Entry(self.popup, textvariable=self.email_var, font='Helvetica 16 bold',
                                  foreground=self.ROXO, width=30)
        val.limitar_tamanho(self.et_email, 45)
        self.et_email.grid(row=3, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)

        # Quinta linha - Seleção PCD
        lb_pcd = tk.Label(self.popup, text="PCD", font='Helvetica 12 bold', fg=self.ROXO)
        lb_pcd.grid(row=4, column=0, padx=self.PADX, pady=self.PADY)

        self.pcd_var = tk.StringVar()
        self.cb_pcd = ttk.Combobox(self.popup, textvariable=self.pcd_var, font='Helvetica 16 bold',
                                   foreground=self.ROXO, width=28, state="readonly")
        self.cb_pcd['values'] = ["Sim", "Não"]
        self.cb_pcd.grid(row=4, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)

        # Sexta linha - Seleção do aluno acompanhante
        lb_acompanhante = tk.Label(self.popup, text="Acompanhante", font='Helvetica 12 bold', fg=self.ROXO)
        lb_acompanhante.grid(row=5, column=0, padx=self.PADX, pady=self.PADY)

        self.acompanhante_var = tk.StringVar()
        self.cb_acompanhante = ttk.Combobox(self.popup, textvariable=self.acompanhante_var, font='Helvetica 16 bold',
                                            width=28, state="readonly")
        self.cb_acompanhante.grid(row=5, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)

        # Consultar o banco de dados para obter os acompanhantes
        cmd = "SELECT idt_aluno_acompanhante, nme_aluno_acompanhante FROM tb_aluno_acompanhante ORDER BY nme_aluno_acompanhante"
        alunos = janela_mestre.sql.get_list(cmd)

        self.cb_acompanhante['values'] = [
            f"{acompanhante['idt_aluno_acompanhante']} - {acompanhante['nme_aluno_acompanhante']}" for
            acompanhante in
            alunos]

        # Sétima linha - Botão para cadastrar um novo visitante
        self.bt_salvar = tk.Button(self.popup, text="Cadastrar", command=lambda: self.salvar(janela_mestre),
                                   font='Helvetica 12 bold', fg='white', bg=self.ROXO, cursor="hand2")
        self.bt_salvar.grid(row=6, column=0, columnspan=4, padx=self.PADX, pady=self.PADY, sticky="ew")
        self.et_nome.focus()

    # Botão para confirmar a inclusão
    def salvar(self, janela_mestre):
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

            cmd = ("INSERT INTO "
                   "tb_visitantes (nme_visitante, rg_visitante, eml_visitante, pcd_visitante, cod_aluno_acompanhante) "
                   "VALUES (%s, %s, %s, %s, %s)")
            janela_mestre.sql.insert(cmd, (nome, rg, email, pcd_valor, idt_acompanhante))

            # Fechar a janela pop-up
            self.popup.destroy()
        else:
            messagebox.showerror("Erro: Campo(s) obrigatório(s)",
                                 "O(s) seguinte(s) campo(s) é/são obrigatório(s):\n" + retorno[1])
