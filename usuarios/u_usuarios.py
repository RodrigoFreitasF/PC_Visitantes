import tkinter as tk
from tkinter import ttk, messagebox

import util.validate as val
import bcrypt


class AlterarUsuario:
    def __init__(self, janela_mestre, idt_usuarios):
        self.popup = tk.Toplevel(janela_mestre)
        self.popup.grab_set()
        self.popup.iconbitmap("../ceub.ico")

        self.PADX = 10
        self.PADY = 10
        self.ROXO = "#662c92"

        self.obrigatorios = []
        linha = 0

        cmd = (
            "SELECT idt_usuarios, nme_usuario, crd_usuario, sts_usuario "
            "FROM tb_usuarios WHERE idt_usuarios = %s")
        usuario = janela_mestre.sql.get_object(cmd, [idt_usuarios])

        titulo = tk.Label(self.popup, text="Alterar Usuário", font='Helvetica 16 bold', fg=self.ROXO)
        titulo.grid(row=linha, column=0, columnspan=4, padx=self.PADX, pady=self.PADY)
        linha += 1

        lb_idt = tk.Label(self.popup, text="ID do Usuário", font='Helvetica 12 bold', fg=self.ROXO)
        lb_idt.grid(row=linha, column=0, padx=self.PADX, pady=self.PADY)

        self.idt_var = tk.StringVar(value=usuario['idt_usuarios'])
        self.et_idt = ttk.Entry(self.popup, textvariable=self.idt_var, font='Helvetica 16 bold',
                                foreground=self.ROXO, width=10, state="readonly")
        self.et_idt.grid(row=linha, column=1, columnspan=3, padx=self.PADX, pady=self.PADY, sticky="w")
        linha += 1

        lb_nome = tk.Label(self.popup, text="Nome", font='Helvetica 12 bold', fg=self.ROXO)
        lb_nome.grid(row=linha, column=0, padx=self.PADX, pady=self.PADY)

        self.nome_var = tk.StringVar(value=usuario['nme_usuario'])
        self.et_nome = ttk.Entry(self.popup, textvariable=self.nome_var, font='Helvetica 16 bold',
                                 foreground=self.ROXO, width=30)
        val.limitar_tamanho(self.et_nome, 100)
        self.obrigatorios.append([self.et_nome, lb_nome.cget('text')])
        self.et_nome.grid(row=linha, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)
        linha += 1

        lb_user = tk.Label(self.popup, text="Usuário", font='Helvetica 12 bold', fg=self.ROXO)
        lb_user.grid(row=linha, column=0, padx=self.PADX, pady=self.PADY)

        self.user_var = tk.StringVar(value=usuario['crd_usuario'])
        self.et_user = ttk.Entry(self.popup, textvariable=self.user_var, font='Helvetica 16 bold',
                                 foreground=self.ROXO, width=30)
        val.limitar_tamanho(self.et_user, 45)
        self.obrigatorios.append([self.et_user, lb_user.cget('text')])
        self.et_user.grid(row=linha, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)
        linha += 1

        lb_status = tk.Label(self.popup, text="Status", font='Helvetica 12 bold', fg=self.ROXO)
        lb_status.grid(row=linha, column=0, padx=self.PADX, pady=self.PADY)

        self.status_var = tk.StringVar()
        status_map_reverse = {"A": "Administrador", "S": "Segurança", "R": "Recepção"}
        self.status_var.set(status_map_reverse.get(usuario['sts_usuario'], ""))

        self.cb_status = ttk.Combobox(
            self.popup,
            textvariable=self.status_var,
            font='Helvetica 16 bold',
            values=["Administrador", "Segurança", "Recepção"],
            state="readonly",
            width=28
        )
        self.obrigatorios.append([self.cb_status, lb_status.cget('text')])
        self.cb_status.grid(row=linha, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)
        linha += 1

        lb_senha = tk.Label(self.popup, text="Nova Senha", font='Helvetica 12 bold', fg=self.ROXO)
        lb_senha.grid(row=linha, column=0, padx=self.PADX, pady=self.PADY)

        self.senha_var = tk.StringVar()
        self.et_senha = ttk.Entry(self.popup, textvariable=self.senha_var, font='Helvetica 16 bold',
                                  foreground=self.ROXO, width=30, show="*")
        val.limitar_tamanho(self.et_senha, 50)
        self.et_senha.grid(row=linha, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)
        linha += 1

        self.bt_alterar = tk.Button(
            self.popup,
            text="Salvar Alterações",
            command=lambda: self.alterar(janela_mestre),
            font='Helvetica 12 bold',
            fg='white',
            bg=self.ROXO,
            cursor="hand2"
        )
        self.bt_alterar.grid(row=linha, column=0, columnspan=4, padx=self.PADX, pady=self.PADY, sticky="ew")
        self.et_nome.focus()

    def alterar(self, janela_mestre):
        retorno = val.todos_campos_preenchidos(self.obrigatorios)
        if retorno[0]:
            idt_usuarios = self.idt_var.get()
            nome = self.nome_var.get()
            user = self.user_var.get()
            status = self.status_var.get()
            senha = self.senha_var.get().strip()

            status_map = {"Administrador": "A", "Segurança": "S", "Recepção": "R"}
            status = status_map.get(status)

            if senha:
                senha_encriptografada = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
                cmd = (
                    "UPDATE tb_usuarios "
                    "SET nme_usuario = %s, crd_usuario = %s, sts_usuario = %s, pwd_usuario = %s "
                    "WHERE idt_usuarios = %s")
                params = (nome, user, status, senha_encriptografada, idt_usuarios)
            else:
                cmd = (
                    "UPDATE tb_usuarios "
                    "SET nme_usuario = %s, crd_usuario = %s, sts_usuario = %s "
                    "WHERE idt_usuarios = %s")
                params = (nome, user, status, idt_usuarios)

            janela_mestre.sql.upd_del(cmd, params)

            messagebox.showinfo("Sucesso", "Usuário alterado com sucesso!")
            self.popup.destroy()
        else:
            messagebox.showerror(
                "Erro: Campo(s) obrigatório(s)",
                "O(s) seguinte(s) campo(s) é/são obrigatório(s):\n" + retorno[1]
            )
