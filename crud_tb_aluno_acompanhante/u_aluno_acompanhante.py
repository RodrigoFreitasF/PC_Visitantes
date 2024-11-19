import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import util.validate as val

class AlterarAluno:
    def __init__(self, janela_mestre, idt):
        # Cria uma nova janela (pop-up)
        self.popup = tk.Toplevel(janela_mestre)
        self.popup.grab_set()

        # Constantes
        PADX = 10
        PADY = 10

        # Variáveis
        self.obrigatorios = []
        linha = 0

        # Buscar dados que já estão na base
        cmd = "SELECT * FROM tb_aluno_acompanhante WHERE idt_aluno_acompanhante = %s"  # ERRO CORRIGIDO: nome da tabela corrigido
        funcao = janela_mestre.sql.get_object(cmd, [idt])

        # Primeira linha - Título
        titulo = tk.Label(self.popup, text="Alterar Dados do Aluno", font='Helvetica 16 bold', fg='blue')
        titulo.grid(row=linha, column=0, columnspan=3, padx=PADX, pady=PADY)
        linha += 1

        # Segunda linha - Mostrar o identificador da função (readonly)
        lb_idt = tk.Label(self.popup, text="Identificador", font='Helvetica 12 bold', fg='blue')
        lb_idt.grid(row=linha, column=0, padx=PADX, pady=PADY)

        self.idt_var = tk.StringVar()
        self.idt_var.set(funcao['idt_aluno_acompanhante'])
        self.et_idt = ttk.Entry(self.popup, textvariable=self.idt_var, font='Helvetica 16 bold',
                                foreground='green', width=5, state="readonly")
        self.et_idt.grid(row=linha, column=1, columnspan=2, padx=PADX, pady=PADY, sticky="W")
        linha += 1

        # Terceira linha - Receber o Nome do Aluno
        lb_nome = tk.Label(self.popup, text="Nome do aluno", font='Helvetica 12 bold', fg='blue')
        lb_nome.grid(row=linha, column=0, padx=PADX, pady=PADY)

        self.nome_var = tk.StringVar()
        self.nome_var.set(funcao['nme_aluno_acompanhante'])
        self.et_nome = ttk.Entry(self.popup, textvariable=self.nome_var, font='Helvetica 16 bold',
                                 foreground='green', width=30)
        val.limitar_tamanho(self.et_nome, 50)
        self.obrigatorios.append([self.et_nome, lb_nome.cget('text')])
        self.et_nome.grid(row=linha, column=1, columnspan=2, padx=PADX, pady=PADY)
        linha += 1

        # Recebe o RA do aluno
        lb_RA = tk.Label(self.popup, text="RA do Aluno", font='Helvetica 12 bold', fg='blue')
        lb_RA.grid(row=linha, column=0, padx=PADX, pady=PADY)

        self.RA_var = tk.StringVar()
        self.RA_var.set(funcao['RA_aluno_acompanhante'])
        self.et_RA = ttk.Entry(self.popup, textvariable=self.RA_var, font='Helvetica 16 bold',
                               foreground='green', width=30)
        val.limitar_tamanho(self.et_RA, 50)
        self.obrigatorios.append([self.et_RA, lb_RA.cget('text')])  # ERRO CORRIGIDO: Nome do label correto para RA
        self.et_RA.grid(row=linha, column=1, columnspan=2, padx=PADX, pady=PADY)
        linha += 1

        # Botão para salvar alterações
        self.bt_alterar = tk.Button(self.popup, text="Alterar o Projeto", command=lambda: self.alterar(janela_mestre),
                                    font='Helvetica 12 bold',
                                    fg='white',
                                    bg='blue')
        self.bt_alterar.grid(row=linha, column=0, columnspan=3, padx=PADX, pady=PADY)
        self.et_nome.focus()

    # Botão para confirmar a alteração
    def alterar(self, janela_mestre):
        retorno = val.todos_campos_preenchidos(self.obrigatorios)
        if retorno[0]:
            idt = int(self.idt_var.get())
            nome = self.nome_var.get()  # ERRO CORRIGIDO: 'nome' agora usa 'self.nome_var.get()'
            RA = self.RA_var.get()  # ERRO CORRIGIDO: 'RA' agora usa 'self.RA_var.get()'

            # Alterar os dados no banco de dados
            cmd = "UPDATE tb_aluno_acompanhante SET nme_aluno_acompanhante = %s, RA_aluno_acompanhante = %s WHERE idt_aluno_acompanhante = %s"
            # ERRO CORRIGIDO: Nome da coluna corrigido para 'nme_aluno_acompanhante'
            id = janela_mestre.sql.upd_del(cmd, (nome, RA, idt))

            # Fechar a janela pop-up
            self.popup.destroy()
            messagebox.showinfo("Sucesso", "Aluno alterado com sucesso!")
        else:
            messagebox.showerror("Erro: Campos obrigatórios",
                                 "O(s) seguinte(s) campo(s) é/são obrigatório(s):\n" + retorno[1])

