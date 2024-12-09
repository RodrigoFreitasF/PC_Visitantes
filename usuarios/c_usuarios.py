import tkinter as tk
from tkinter import ttk, messagebox
import bcrypt

import util.validate as val


class CadastrarUsuario:
    def __init__(self, janela_mestre):
        # Cria uma nova janela (pop-up)
        self.popup = tk.Toplevel(janela_mestre)
        self.popup.grab_set()
        self.popup.iconbitmap("../ceub.ico")

        # Constantes
        self.PADX = 10
        self.PADY = 10
        self.ROXO = "#662c92"

        # Variáveis
        self.obrigatorios = []

        # Primeira linha - Título
        titulo = tk.Label(self.popup, text="Cadastrar Usuário", font='Helvetica 16 bold', fg=self.ROXO)
        titulo.grid(row=0, column=0, columnspan=4, padx=self.PADX, pady=self.PADY)

        # Segunda linha - Nome
        lb_nome = tk.Label(self.popup, text="Nome", font='Helvetica 12 bold', fg=self.ROXO)
        lb_nome.grid(row=1, column=0, padx=self.PADX, pady=self.PADY)

        self.nome_var = tk.StringVar()
        self.et_nome = ttk.Entry(self.popup, textvariable=self.nome_var, font='Helvetica 16 bold',
                                 foreground=self.ROXO, width=30)
        val.limitar_tamanho(self.et_nome, 100)
        self.obrigatorios.append([self.et_nome, lb_nome.cget('text')])
        self.et_nome.grid(row=1, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)

        # Terceira linha - Usuário
        lb_user = tk.Label(self.popup, text="Usuário", font='Helvetica 12 bold', fg=self.ROXO)
        lb_user.grid(row=2, column=0, padx=self.PADX, pady=self.PADY)

        self.user_var = tk.StringVar()
        self.et_user = ttk.Entry(self.popup, textvariable=self.user_var, font='Helvetica 16 bold',
                                 foreground=self.ROXO, width=30)
        val.limitar_tamanho(self.et_user, 45)
        self.obrigatorios.append([self.et_user, lb_user.cget('text')])
        self.et_user.grid(row=2, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)

        # Quarta linha - Senha
        lb_senha = tk.Label(self.popup, text="Senha", font='Helvetica 12 bold', fg=self.ROXO)
        lb_senha.grid(row=3, column=0, padx=self.PADX, pady=self.PADY)

        self.senha_var = tk.StringVar()
        self.et_senha = ttk.Entry(self.popup, show="*", textvariable=self.senha_var, font='Helvetica 16 bold',
                                  foreground=self.ROXO, width=30)
        val.limitar_tamanho(self.et_senha, 45)
        self.obrigatorios.append([self.et_senha, lb_senha.cget('text')])
        self.et_senha.grid(row=3, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)

        # Quinta linha - Select para status
        lb_status = tk.Label(self.popup, text="Status", font='Helvetica 12 bold', fg=self.ROXO)
        lb_status.grid(row=4, column=0, padx=self.PADX, pady=self.PADY)

        self.status_var = tk.StringVar()
        self.cb_status = ttk.Combobox(
            self.popup,
            textvariable=self.status_var,
            font='Helvetica 16 bold',
            values=["Administrador", "Segurança", "Recepção"],
            state="readonly",
            width=28
        )
        self.obrigatorios.append([self.cb_status, lb_status.cget('text')])
        self.cb_status.grid(row=4, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)

        # Sexta linha - Botão para cadastrar
        self.bt_salvar = tk.Button(
            self.popup,
            text="Cadastrar",
            command=lambda: self.salvar(janela_mestre),
            font='Helvetica 12 bold',
            fg='white',
            bg=self.ROXO,
            cursor="hand2"
        )
        self.bt_salvar.grid(row=5, column=0, columnspan=4, padx=self.PADX, pady=self.PADY, sticky="ew")
        self.et_nome.focus()

    def salvar(self, janela_mestre):
        retorno = val.todos_campos_preenchidos(self.obrigatorios)
        if retorno[0]:
            nome = self.nome_var.get()
            user = self.user_var.get()
            senha = self.senha_var.get()
            senha_encriptografada = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
            status = self.status_var.get()

            # Mapear o status para as strings do banco
            status_map = {"Administrador": "A", "Segurança": "S", "Recepção": "R"}
            status = status_map.get(status)

            cmd = ("INSERT INTO "
                   "tb_usuarios (nme_usuario, sts_usuario, pwd_usuario, crd_usuario) "
                   "VALUES (%s, %s, %s, %s)")
            janela_mestre.sql.insert(cmd, (nome, status, senha_encriptografada, user))

            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

            # Fechar a janela pop-up
            self.popup.destroy()
        else:
            messagebox.showerror(
                "Erro: Campo(s) obrigatório(s)",
                "O(s) seguinte(s) campo(s) é/são obrigatório(s):\n" + retorno[1]
            )
