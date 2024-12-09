import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import util.validate as val


class CadastrarLocal:
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
        titulo = tk.Label(self.popup, text="Cadastrar Local", font='Helvetica 16 bold', fg=self.ROXO)
        titulo.grid(row=0, column=0, columnspan=4, padx=self.PADX, pady=self.PADY)

        # Segunda linha - Receber o nome do bloco
        lb_nome = tk.Label(self.popup, text="Nome do Bloco", font='Helvetica 12 bold', fg=self.ROXO)
        lb_nome.grid(row=1, column=0, padx=self.PADX, pady=self.PADY)

        self.nome_var = tk.StringVar()
        self.et_nome = ttk.Entry(self.popup, textvariable=self.nome_var, font='Helvetica 16 bold',
                                 foreground=self.ROXO, width=30)
        val.limitar_tamanho(self.et_nome, 45)
        self.obrigatorios.append([self.et_nome, lb_nome.cget('text')])
        self.et_nome.grid(row=1, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)

        # Adicionar o campo "Campus"
        lb_campus = tk.Label(self.popup, text="Campus", font='Helvetica 12 bold', fg=self.ROXO)
        lb_campus.grid(row=2, column=0, padx=self.PADX, pady=self.PADY)

        self.campus_var = tk.StringVar()
        self.cb_campus = ttk.Combobox(self.popup, textvariable=self.campus_var, font='Helvetica 16 bold',
                                       foreground=self.ROXO, width=28, state="readonly")
        # Consultar o banco de dados para obter os campus
        cmd = "SELECT nme_campus FROM tb_campus ORDER BY nme_campus"
        campus = janela_mestre.sql.get_list(cmd)
        self.cb_campus['values'] = [campus_item['nme_campus'] for campus_item in campus]
        self.cb_campus.grid(row=2, column=1, columnspan=3, padx=self.PADX, pady=self.PADY)

        # Botão para cadastrar um novo local
        self.bt_salvar = tk.Button(self.popup, text="Cadastrar", command=lambda: self.salvar(janela_mestre),
                                   font='Helvetica 12 bold', fg='white', bg=self.ROXO)
        self.bt_salvar.grid(row=3, column=0, columnspan=4, padx=self.PADX, pady=self.PADY, sticky="ew")
        self.et_nome.focus()

    def salvar(self, janela_mestre):
        retorno = val.todos_campos_preenchidos(self.obrigatorios)
        if retorno[0]:
            nome = self.nome_var.get()
            campus_selecionado = self.campus_var.get()  # Aqui pegamos o campus
            if campus_selecionado:
                # Buscamos o id do campus na tabela
                cmd_campus = "SELECT idt_campus FROM tb_campus WHERE nme_campus = %s"
                campus_resultado = janela_mestre.sql.get_list(cmd_campus, (campus_selecionado,))

                if campus_resultado:
                    campus_id = campus_resultado[0]['idt_campus']  # Pega o idt_campus da consulta
                else:
                    campus_id = None  # Caso não encontre o campus, você pode tratar isso adequadamente
            else:
                campus_id = None  # Caso o campus não seja selecionado, trata como None

            cmd = ("INSERT INTO "
                   "tb_locais (nme_local, cod_campus) "
                   "VALUES (%s, %s)")
            janela_mestre.sql.insert(cmd, (nome, campus_id))

            
            self.popup.destroy()
        else:
            messagebox.showerror("Erro: Campo(s) obrigatório(s)",
                                 "O(s) seguinte(s) campo(s) é/são obrigatório(s):\n" + retorno[1])
