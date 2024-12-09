import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class ExcluirUsuario:
    def __init__(self, janela_mestre, idt_usuario):
        # Cria uma nova janela (pop-up)
        self.popup = tk.Toplevel(janela_mestre)
        self.popup.grab_set()
        self.popup.iconbitmap("../ceub.ico")

        # Constantes
        self.PADX = 10
        self.PADY = 10
        self.ROXO = "#662c92"

        # Variáveis
        linha = 0

        # Buscar dados do usuário
        cmd = (
            "SELECT idt_usuarios, nme_usuario, crd_usuario, sts_usuario "
            "FROM tb_usuarios "
            "WHERE idt_usuarios = %s"
        )
        usuario = janela_mestre.sql.get_object(cmd, [idt_usuario])

        # Primeira linha - Título
        titulo = tk.Label(self.popup, text="Excluir Usuário", font='Helvetica 16 bold', fg=self.ROXO)
        titulo.grid(row=linha, column=0, columnspan=4, padx=self.PADX, pady=self.PADY)
        linha += 1

        # Segunda linha - Mostrar o identificador do usuário (readonly)
        lb_idt = tk.Label(self.popup, text="Identificador", font='Helvetica 12 bold', fg=self.ROXO)
        lb_idt.grid(row=linha, column=0, padx=self.PADX, pady=self.PADY)

        self.idt_var = tk.StringVar()
        self.idt_var.set(usuario['idt_usuarios'])
        self.et_idt = ttk.Label(self.popup, textvariable=self.idt_var, font='Helvetica 16 bold',
                                foreground=self.ROXO, width=5)
        self.et_idt.grid(row=linha, column=1, columnspan=2, padx=self.PADX, pady=self.PADY, sticky="W")
        linha += 1

        # Terceira linha - Nome do Usuário
        lb_nome = tk.Label(self.popup, text="Nome", font='Helvetica 12 bold', fg=self.ROXO)
        lb_nome.grid(row=linha, column=0, padx=self.PADX, pady=self.PADY)

        self.nome_var = tk.StringVar()
        self.nome_var.set(usuario['nme_usuario'])
        self.et_nome = ttk.Label(self.popup, textvariable=self.nome_var, font='Helvetica 16 bold',
                                 foreground=self.ROXO, width=28)
        self.et_nome.grid(row=linha, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)
        linha += 1

        # Quarta linha - Credencial (Usuário para login)
        lb_user = tk.Label(self.popup, text="Usuário", font='Helvetica 12 bold', fg=self.ROXO)
        lb_user.grid(row=linha, column=0, padx=self.PADX, pady=self.PADY)

        self.user_var = tk.StringVar()
        self.user_var.set(usuario['crd_usuario'])
        self.et_user = ttk.Label(self.popup, textvariable=self.user_var, font='Helvetica 16 bold',
                                 foreground=self.ROXO, width=28)
        self.et_user.grid(row=linha, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)
        linha += 1

        # Quinta linha - Status
        lb_status = tk.Label(self.popup, text="Status", font='Helvetica 12 bold', fg=self.ROXO)
        lb_status.grid(row=linha, column=0, padx=self.PADX, pady=self.PADY)

        self.status_var = tk.StringVar()
        status_map_reverse = {"A": "Administrador", "S": "Segurança", "R": "Recepção"}
        self.status_var.set(status_map_reverse.get(usuario['sts_usuario'], ""))
        self.et_status = ttk.Label(self.popup, textvariable=self.status_var, font='Helvetica 16 bold',
                                   foreground=self.ROXO, width=28)
        self.et_status.grid(row=linha, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)
        linha += 1

        # Sexta linha - Botão Excluir
        self.bt_excluir = tk.Button(self.popup, text="Excluir", command=lambda: self.excluir(janela_mestre),
                                    font='Helvetica 12 bold',
                                    fg='white',
                                    bg=self.ROXO,
                                    cursor="hand2")
        self.bt_excluir.grid(row=linha, column=0, columnspan=4, padx=self.PADX, pady=self.PADY, sticky="ew")

    def excluir(self, janela_mestre):
        resposta = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este usuário?")
        if resposta:
            idt_usuario = int(self.idt_var.get())
            # Excluir os dados no banco de dados
            cmd = "DELETE FROM tb_usuarios WHERE idt_usuarios = %s"
            janela_mestre.sql.upd_del(cmd, [idt_usuario])
            # Fechar a janela pop-up
            self.popup.destroy()
            messagebox.showinfo("Sucesso", "Usuário excluído com sucesso!")
