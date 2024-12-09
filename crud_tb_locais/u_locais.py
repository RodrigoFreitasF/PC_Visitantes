import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import util.validate as val


class AlterarBlocos:
    def __init__(self, janela_mestre, idt):
        self.popup = tk.Toplevel(janela_mestre)
        self.popup.grab_set()

        PADX = 10
        PADY = 10

        # Constantes de cores
        cor_btn = '#43054e'
        fonte_btn = 'Jakob 12 bold'
        cor_dados = '#662c92'
        cor_titulo = '#bf0087'

        self.obrigatorios = []
        linha = 0

        cmd = "SELECT * FROM tb_locais WHERE idt_local = %s"
        funcao = janela_mestre.sql.get_object(cmd, [idt])

        # Título
        titulo = tk.Label(self.popup, text="Alterar Bloco", font='Helvetica 16 bold', fg=cor_titulo)
        titulo.grid(row=1, column=0, columnspan=3, padx=PADX, pady=PADY)

        # Idt do local
        lb_idt = tk.Label(self.popup, text="Identificador", font='Helvetica 12 bold', fg=cor_titulo)
        lb_idt.grid(row=2, column=0, padx=PADX, pady=PADY)

        self.idt_var = tk.StringVar()
        self.idt_var.set(funcao['idt_local'])
        self.et_idt = ttk.Entry(self.popup, textvariable=self.idt_var, font='Helvetica 16 bold',
                                foreground=cor_dados, width=5, state="readonly")
        self.et_idt.grid(row=2, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")

        # Nome do bloco
        lb_nome = tk.Label(self.popup, text="Nome do Bloco", font='Helvetica 12 bold', fg=cor_titulo)
        lb_nome.grid(row=3, column=0, padx=PADX, pady=PADY)

        self.valor_nome = tk.StringVar()
        self.valor_nome.set(funcao['nme_local'])
        self.et_nome = ttk.Entry(self.popup, textvariable=self.valor_nome, font='Helvetica 16 bold', foreground=cor_dados,
                                 width=20)
        self.obrigatorios.append([self.et_nome])
        self.et_nome.grid(row=3, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")

        # Código do campus
        lb_campus = tk.Label(self.popup, text="Código do Campus", font='Helvetica 12 bold', fg=cor_titulo)
        lb_campus.grid(row=4, column=0, padx=PADX, pady=PADY)

        self.valor_campus = tk.StringVar()
        self.valor_campus.set(funcao['cod_campus'])
        self.et_campus = ttk.Entry(self.popup, textvariable=self.valor_campus, font='Helvetica 16 bold',
                                   foreground=cor_dados, width=10)
        self.obrigatorios.append([self.et_campus])
        self.et_campus.grid(row=4, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")

        # Botão para salvar alterações
        self.bt_alterar = tk.Button(self.popup, text="Salvar Alterações", command=lambda: self.alterar(janela_mestre),
                                    font='Helvetica 12 bold',
                                    fg='white',
                                    bg=cor_btn)
        self.bt_alterar.grid(row=5, column=0, columnspan=3, padx=PADX, pady=PADY)
        self.et_idt.focus()

    # Executar a alteração
    def alterar(self, janela_mestre):
        retorno = val.todos_campos_preenchidos(self.obrigatorios)
        if retorno[0]:
            idt = int(self.idt_var.get())
            nome = self.valor_nome.get()
            campus = self.valor_campus.get()

            cmd = "UPDATE tb_locais SET nme_local = %s, cod_campus = %s WHERE idt_local = %s"
            num_reg = janela_mestre.sql.upd_del(cmd, (nome, campus, idt))
            self.popup.destroy()
        else:
            messagebox.showerror("Erro: Campo(s) obrigatório(s)",
                                 "O(s) seguinte(s) campo(s) é/são obrigatório(s):\n" + retorno[1])
