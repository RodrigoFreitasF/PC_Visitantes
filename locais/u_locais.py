import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import util.validate as val


class AlterarLocal:
    def __init__(self, janela_mestre, idt):
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
        linha = 0

        # Buscar dados que já estão na base
        cmd = (
            "SELECT l.idt_local, l.nme_local, l.cod_campus, c.nme_campus "
            "FROM tb_locais l "
            "LEFT JOIN tb_campus c ON l.cod_campus = c.idt_campus "
            "WHERE l.idt_local = %s")
        funcao = janela_mestre.sql.get_object(cmd, [idt])

        # Primeira linha - Título
        titulo = tk.Label(self.popup, text="Alterar Local", font='Helvetica 16 bold', fg=self.ROXO)
        titulo.grid(row=linha, column=0, columnspan=4, padx=self.PADX, pady=self.PADY)
        linha += 1

        # Segunda linha - Mostrar o identificador do local (readonly)
        lb_idt = tk.Label(self.popup, text="Identificador", font='Helvetica 12 bold', fg=self.ROXO)
        lb_idt.grid(row=linha, column=0, padx=self.PADX, pady=self.PADY)

        self.idt_var = tk.StringVar()
        self.idt_var.set(funcao['idt_local'])
        self.et_idt = ttk.Entry(self.popup, textvariable=self.idt_var, font='Helvetica 16 bold',
                                foreground=self.ROXO, width=5, state="readonly")
        self.et_idt.grid(row=linha, column=1, columnspan=2, padx=self.PADX, pady=self.PADY, sticky="W")
        linha += 1

        # Terceira linha - Receber o Nome do Local
        lb_nome = tk.Label(self.popup, text="Nome do Local", font='Helvetica 12 bold', fg=self.ROXO)
        lb_nome.grid(row=linha, column=0, padx=self.PADX, pady=self.PADY)

        self.nome_var = tk.StringVar()
        self.nome_var.set(funcao['nme_local'])
        self.et_nome = ttk.Entry(self.popup, textvariable=self.nome_var, font='Helvetica 16 bold',
                                 foreground=self.ROXO, width=30)
        val.limitar_tamanho(self.et_nome, 45)
        self.obrigatorios.append([self.et_nome, lb_nome.cget('text')])
        self.et_nome.grid(row=linha, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)
        linha += 1

        # Quarta linha - Seleção do Campus
        lb_campus = tk.Label(self.popup, text="Campus", font='Helvetica 12 bold', fg=self.ROXO)
        lb_campus.grid(row=linha, column=0, padx=self.PADX, pady=self.PADY)

        self.campus_var = tk.StringVar()
        campus_atual = f"{funcao['cod_campus']} - {funcao['nme_campus']}" if funcao['cod_campus'] else ""
        self.campus_var.set(campus_atual)
        self.cb_campus = ttk.Combobox(self.popup, textvariable=self.campus_var, font='Helvetica 16 bold',
                                      width=28, state="readonly", foreground=self.ROXO)

        # Consultar o banco de dados para obter os campi
        cmd = "SELECT idt_campus, nme_campus FROM tb_campus ORDER BY nme_campus"
        campi = janela_mestre.sql.get_list(cmd)

        self.cb_campus['values'] = [
            f"{campus['idt_campus']} - {campus['nme_campus']}" for campus in campi]
        self.cb_campus.grid(row=linha, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)
        self.obrigatorios.append([self.cb_campus, lb_campus.cget('text')])
        linha += 1

        # Quinta linha - Botão para salvar alterações
        self.bt_alterar = tk.Button(self.popup, text="Alterar", command=lambda: self.alterar(janela_mestre),
                                    font='Helvetica 12 bold',
                                    fg='white',
                                    bg=self.ROXO,
                                    cursor="hand2")
        self.bt_alterar.grid(row=linha, column=0, columnspan=4, padx=self.PADX, pady=self.PADY, sticky="ew")
        self.et_nome.focus()

    def alterar(self, janela_mestre):
        retorno = val.todos_campos_preenchidos(self.obrigatorios)
        if retorno[0]:
            nome = self.nome_var.get()
            campus_selecionado = self.campus_var.get()
            idt_campus = campus_selecionado.split(" - ")[0] if campus_selecionado else None
            idt_local = int(self.idt_var.get())
            cmd = "UPDATE tb_locais SET nme_local = %s, cod_campus = %s WHERE idt_local = %s"
            janela_mestre.sql.upd_del(cmd, (nome, idt_campus, idt_local))
            self.popup.destroy()
        else:
            messagebox.showerror("Erro: Campo(s) obrigatório(s)",
                                 "O(s) seguinte(s) campo(s) é/são obrigatório(s):\n" + retorno[1])
