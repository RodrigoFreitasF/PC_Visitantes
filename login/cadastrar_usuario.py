import tkinter as tk
from re import match
from tkinter import ttk, messagebox

import bcrypt

import util.validate as val


class CadastrarUsuario:
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
        titulo = tk.Label(self.popup, text="Cadastrar Usuário", font='Helvetica 16 bold', fg=self.ROXO)
        titulo.grid(row=0, column=0, columnspan=4, padx=self.PADX, pady=self.PADY)

        # Segunda linha - Receber o nome do usuário
        lb_nome = tk.Label(self.popup, text="Nome", font='Helvetica 12 bold', fg=self.ROXO)
        lb_nome.grid(row=1, column=0, padx=self.PADX, pady=self.PADY)

        self.nome_var = tk.StringVar()
        self.et_nome = ttk.Entry(self.popup, textvariable=self.nome_var, font='Helvetica 16 bold',
                                 foreground=self.ROXO, width=30)
        val.limitar_tamanho(self.et_nome, 100)
        self.obrigatorios.append([self.et_nome, lb_nome.cget('text')])
        self.et_nome.grid(row=1, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)

        # Terceira linha - Receber o usuário
        lb_user = tk.Label(self.popup, text="Usuário", font='Helvetica 12 bold', fg=self.ROXO)
        lb_user.grid(row=2, column=0, padx=self.PADX, pady=self.PADY)

        self.user_var = tk.StringVar()
        self.et_user = ttk.Entry(self.popup, textvariable=self.user_var, font='Helvetica 16 bold',
                                 foreground=self.ROXO, width=30)
        val.limitar_tamanho(self.et_user, 45)
        self.obrigatorios.append([self.et_user, lb_user.cget('text')])
        self.et_user.grid(row=2, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)

        # Quarta linha - Receber a senha do usuário
        lb_senha = tk.Label(self.popup, text="Senha", font='Helvetica 12 bold', fg=self.ROXO)
        lb_senha.grid(row=3, column=0, padx=self.PADX, pady=self.PADY)

        self.senha_var = tk.StringVar()
        self.et_senha = ttk.Entry(self.popup, show="*", textvariable=self.senha_var, font='Helvetica 16 bold',
                                  foreground=self.ROXO, width=30)
        val.limitar_tamanho(self.et_senha, 45)
        self.et_senha.grid(row=3, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)

        # # Quinta linha - Seleção Status
        # lb_status = tk.Label(self.popup, text="Status", font='Helvetica 12 bold', fg=self.ROXO)
        # lb_status.grid(row=4, column=0, padx=self.PADX, pady=self.PADY)
        #
        # self.status_var = tk.StringVar()
        # self.cb_status = ttk.Combobox(self.popup, textvariable=self.status_var, font='Helvetica 16 bold',
        #                               foreground=self.ROXO, width=28, state="readonly")
        # self.cb_status['values'] = ["Administrador", "Supervisor", "Recepção"]
        # self.cb_status.grid(row=4, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)

        # Quinta linha - Botão para cadastrar um novo usuário
        self.bt_salvar = tk.Button(self.popup, text="Cadastrar", command=lambda: self.salvar(janela_mestre),
                                   font='Helvetica 12 bold', fg='white', bg=self.ROXO)
        self.bt_salvar.grid(row=4, column=0, columnspan=4, padx=self.PADX, pady=self.PADY, sticky="ew")
        self.et_nome.focus()

    # Botão para confirmar a inclusão
    def salvar(self, janela_mestre):
        retorno = val.todos_campos_preenchidos(self.obrigatorios)
        if retorno[0]:
            nome = self.nome_var.get()
            user = self.user_var.get()
            senha = self.senha_var.get()
            senha_encriptografada = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
            status = "R"
            # status = self.status_var.get()
            # match status:
            #     case "Administrador" : status = "A"
            #     case "Supervisor" : status = "S"
            #     case "Recepção" : status = "R"

            cmd = ("INSERT INTO "
                   "tb_usuarios (nme_usuario, sts_usuario, pwd_usuario, crd_usuario) "
                   "VALUES (%s, %s, %s, %s)")
            print(senha_encriptografada)
            janela_mestre.sql.insert(cmd, (nome, status, senha_encriptografada, user))


            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

            # Fechar a janela pop-up
            self.popup.destroy()
        else:
            messagebox.showerror("Erro: Campo(s) obrigatório(s)",
                                 "O(s) seguinte(s) campo(s) é/são obrigatório(s):\n" + retorno[1])
