#Create de tb_aluno_acompanhante
import tkinter as tk
from tkinter import ttk, IntVar, Checkbutton
from tkinter import messagebox
import util.validate as val


class Incluiraluno:
   def __init__(self, janela_mestre):
       # Cria uma nova janela (pop-up)
       self.popup = tk.Toplevel(janela_mestre)
       self.popup.grab_set()


       # Constantes
       PADX = 10
       PADY = 10
       self.obrigatorios = []


       # Primeira linha - Título
       titulo = tk.Label(self.popup, text="Incluir Aluno", font='Helvetica 16 bold', fg='blue')
       titulo.grid(row=0, column=0, columnspan=3, padx=PADX, pady=PADY)


       # Segunda linha - Receber o Nome do Projeto
       lb_nome = tk.Label(self.popup, text="Nome do Aluno", font='Helvetica 12 bold', fg='blue')
       lb_nome.grid(row=1, column=0, padx=PADX, pady=PADY)


       self.nome_var = tk.StringVar()
       self.et_nome = ttk.Entry(self.popup, textvariable=self.nome_var, font='Helvetica 16 bold', foreground='green', width=30)
       val.limitar_tamanho(self.et_nome, 50)
       self.obrigatorios.append([self.et_nome, lb_nome.cget('text')])
       self.et_nome.grid(row=1, column=1, columnspan=2, padx=PADX, pady=PADY)


       # Terceira linha - Receber o RA
       lb_RA = tk.Label(self.popup, text="RA", font='Helvetica 12 bold', fg='blue')
       lb_RA.grid(row=2, column=0, padx=PADX, pady=PADY)

       self.RA_var = tk.StringVar()

       # Função de validação para aceitar apenas números
       def somente_numeros(texto):
           return texto.isdigit() or texto == ""

       vcmd = (self.popup.register(somente_numeros), '%P')

       self.et_RA = ttk.Entry(self.popup, textvariable=self.RA_var, font='Helvetica 16 bold', foreground='green', width=30, validate="key", validatecommand=vcmd)
       val.limitar_tamanho(self.et_RA, 50)
       self.obrigatorios.append([self.et_RA, lb_RA.cget('text')])
       self.et_RA.grid(row=2, column=1, columnspan=2, padx=PADX, pady=PADY)


       # Quarta linha - Botão para incluir uma nova função
       self.bt_salvar = tk.Button(self.popup, text="Incluir Novo Aluno", command=lambda: self.salvar(janela_mestre),
                                  font='Helvetica 12 bold',
                                  fg='white',
                                  bg='blue')
       self.bt_salvar.grid(row=4, column=0, columnspan=3, padx=PADX, pady=PADY)
       self.et_nome.focus()


   # Botão para confirmar a inclusão
   def salvar(self, janela_mestre):
       retorno = val.todos_campos_preenchidos(self.obrigatorios)
       if retorno[0]:
           nome = self.nome_var.get()
           RA = self.et_RA.get()

           try:
               # Inserir os dados no banco de dados
               cmd = "INSERT INTO tb_aluno_acompanhante (nme_aluno_acompanhante, RA_aluno_acompanhante) VALUES (%s, %s)"
               id = janela_mestre.sql.insert(cmd, (nome, RA))

               # Verifique se a função `insert` ou `execute` confirma a transação automaticamente;
               # caso contrário, adicione `janela_mestre.sql.commit()` aqui.
               self.popup.destroy()
           except Exception as e:
               messagebox.showerror("Erro ao incluir aluno", f"Ocorreu um erro: {e}")
       else:
           messagebox.showerror("Erro: Campo(s) obrigatório(s)",
                                "O(s) seguinte(s) campo(s) é/são obrigatório(s):\n" + retorno[1])