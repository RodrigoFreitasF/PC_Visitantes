import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class ExcluirLocal:
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
        linha = 0

        # Buscar dados do local
        cmd = (
            "SELECT l.idt_local, l.nme_local, c.idt_campus, c.nme_campus "
            "FROM tb_locais l "
            "LEFT JOIN tb_campus c ON l.cod_campus = c.idt_campus "
            "WHERE l.idt_local = %s"
        )
        funcao = janela_mestre.sql.get_object(cmd, [idt])

        # Primeira linha - Título
        titulo = tk.Label(self.popup, text="Excluir Local", font='Helvetica 16 bold', fg=self.ROXO)
        titulo.grid(row=linha, column=0, columnspan=4, padx=self.PADX, pady=self.PADY)
        linha += 1

        # Segunda linha - Mostrar o identificador do local (readonly)
        lb_idt = tk.Label(self.popup, text="Identificador", font='Helvetica 12 bold', fg=self.ROXO)
        lb_idt.grid(row=linha, column=0, padx=self.PADX, pady=self.PADY)

        self.idt_var = tk.StringVar()
        self.idt_var.set(funcao['idt_local'])
        self.et_idt = ttk.Label(self.popup, textvariable=self.idt_var, font='Helvetica 16 bold',
                                foreground=self.ROXO, width=5)
        self.et_idt.grid(row=linha, column=1, columnspan=2, padx=self.PADX, pady=self.PADY, sticky="W")
        linha += 1

        # Terceira linha - Nome do Local
        lb_nome = tk.Label(self.popup, text="Nome", font='Helvetica 12 bold', fg=self.ROXO)
        lb_nome.grid(row=linha, column=0, padx=self.PADX, pady=self.PADY)

        self.nome_var = tk.StringVar()
        self.nome_var.set(funcao['nme_local'])
        self.et_nome = ttk.Label(self.popup, textvariable=self.nome_var, font='Helvetica 16 bold',
                                 foreground=self.ROXO, width=28)
        self.et_nome.grid(row=linha, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)
        linha += 1

        # Quarta linha - Campus
        lb_campus = tk.Label(self.popup, text="Campus", font='Helvetica 12 bold', fg=self.ROXO)
        lb_campus.grid(row=linha, column=0, padx=self.PADX, pady=self.PADY)

        self.campus_var = tk.StringVar()
        campus = f"{funcao['idt_campus']} - {funcao['nme_campus']}" if funcao['idt_campus'] else "Não Vinculado"
        self.campus_var.set(campus)
        self.et_campus = ttk.Label(self.popup, textvariable=self.campus_var, font='Helvetica 16 bold',
                                   foreground=self.ROXO, width=28)
        self.et_campus.grid(row=linha, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)
        linha += 1

        # Quinta linha - Botão Excluir
        self.bt_excluir = tk.Button(self.popup, text="Excluir", command=lambda: self.excluir(janela_mestre),
                                    font='Helvetica 12 bold',
                                    fg='white',
                                    bg=self.ROXO,
                                    cursor="hand2")
        self.bt_excluir.grid(row=linha, column=0, columnspan=4, padx=self.PADX, pady=self.PADY, sticky="ew")

    def excluir(self, janela_mestre):
        resposta = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este local?")
        if resposta:
            idt = int(self.idt_var.get())
            # Excluir os dados no banco de dados
            cmd = "DELETE FROM tb_locais WHERE idt_local = %s"
            janela_mestre.sql.upd_del(cmd, [idt])
            # Fechar a janela pop-up
            self.popup.destroy()
