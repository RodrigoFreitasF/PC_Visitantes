import tkinter as tk
from tkinter import messagebox

class ExcluirLocais:
    def __init__(self, janela_mestre, idt):
        # Cria uma nova janela (pop-up)
        self.popup = tk.Toplevel(janela_mestre)
        self.popup.grab_set()

        # Constantes
        PADX = 10
        PADY = 10

        # Constantes de cores
        cor_btn = '#43054e'
        fonte_btn = 'Jakob 12 bold'
        cor_dados = '#662c92'
        cor_titulo = '#bf0087'

        # Variáveis
        linha = 0

        # Buscar dados que já estão na base
        cmd = "SELECT * FROM tb_locais WHERE idt_local = %s"
        local = janela_mestre.sql.get_object(cmd, [idt])

        # Primeira linha - Título
        titulo = tk.Label(self.popup, text="Excluir Local", font='Helvetica 16 bold', fg=cor_titulo)
        titulo.grid(row=1, column=0, columnspan=3, padx=PADX, pady=PADY)

        # Segunda linha - Identificador do local
        lb_idt = tk.Label(self.popup, text="IDT do local", font='Helvetica 12 bold', fg=cor_titulo)
        lb_idt.grid(row=2, column=0, padx=PADX, pady=PADY)

        self.idt_var = tk.StringVar()
        self.idt_var.set(local['idt_local'])
        self.lb_dado_idt = tk.Label(self.popup, textvariable=self.idt_var, font='Helvetica 16 bold',
                                    foreground=cor_dados)
        self.lb_dado_idt.grid(row=2, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")

        # Terceira linha - Nome do local
        lb_nome = tk.Label(self.popup, text="Nome do local", font='Helvetica 12 bold', fg=cor_titulo)
        lb_nome.grid(row=3, column=0, padx=PADX, pady=PADY)

        self.nome_var = tk.StringVar()
        self.nome_var.set(local['nme_local'])

        self.lb_dado_nome = tk.Label(self.popup, textvariable=self.nome_var, font='Helvetica 16 bold',
                                     foreground=cor_dados)
        self.lb_dado_nome.grid(row=3, column=1, columnspan=2, padx=PADX, pady=PADY)

        # Quarta Linha - Código do campus
        lb_cod_campus = tk.Label(self.popup, text="Código do campus", font='Helvetica 12 bold', fg=cor_titulo)
        lb_cod_campus.grid(row=4, column=0, padx=PADX, pady=PADY)

        self.cod_campus_var = tk.StringVar()
        self.cod_campus_var.set(local['cod_campus'])

        self.lb_dado_cod_campus = tk.Label(self.popup, textvariable=self.cod_campus_var, font='Helvetica 16 bold',
                                          foreground=cor_dados)
        self.lb_dado_cod_campus.grid(row=4, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")

        # Operação de Excluir
        self.bt_excluir = tk.Button(self.popup, text="Excluir o local", command=lambda: self.excluir(janela_mestre),
                                    font='Helvetica 12 bold',
                                    fg='white',
                                    bg=cor_btn)
        self.bt_excluir.grid(row=5, column=0, columnspan=3, padx=PADX, pady=PADY)
        self.bt_excluir.focus()

    # Botão para confirmar a exclusão
    def excluir(self, janela_mestre):
        resposta = messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este local?")
        if resposta:
            idt = int(self.idt_var.get())
            # Excluir os dados no banco de dados
            cmd = "DELETE FROM tb_locais WHERE idt_local = %s"
            num_reg = janela_mestre.sql.upd_del(cmd, [idt])
            # Fechar a janela pop-up
            self.popup.destroy()
