#CRUD executável de tb_aluno_acompanhante
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from util.db import SQL
from c_aluno_acompanhante import Incluiraluno
from u_aluno_acompanhante import AlterarAluno
from d_aluno_acompanhante import ExcluirAluno

class CRUD_aluno(tk.Tk):
   def __init__(self):
       super().__init__()
       # Criação de constantes
       self.PADX = 10
       self.PADY = 10


       self.title("CRUD - Tabela Alunos")


       # Primeira linha - Título
       titulo = tk.Label(self, text="Cadastro de Aluno", font='Helvetica 16 bold', fg='blue')
       titulo.grid(row=0, column=0, columnspan=3, padx=self.PADX, pady=self.PADY)


       # Segunda linha - Parâmetro de consulta
       lb_nome = tk.Label(self, text="Nome do aluno", font='Helvetica 12 bold', fg='blue')
       lb_nome.grid(row=1, column=0, padx=self.PADX, pady=self.PADY)


       self.nome_var = tk.StringVar()
       self.et_nome = ttk.Entry(self, textvariable=self.nome_var, font='Helvetica 16 bold', foreground='green')
       self.et_nome.grid(row=1, column=1, padx=self.PADX, pady=self.PADY)


       self.bt_consultar = tk.Button(self, text="Consultar", command=self.consultar, font='Helvetica 12 bold',
                                     fg='white', bg='blue')
       self.bt_consultar.grid(row=1, column=2, padx=self.PADX, pady=self.PADY)


       # Treeview para exibir os resultado da consulta no banco de dados
       style = ttk.Style()
       style.configure("Custom.Treeview", font=("Arial", 12), foreground="blue")
       self.tre_funcoes = ttk.Treeview(self, columns=("idt_aluno_acompanhante", "nme_aluno_acompanhante", "RA_aluno_acompanhante"), show="headings", style="Custom.Treeview")
       # Configurar as colunas
       self.tre_funcoes.heading("idt_aluno_acompanhante", text="Identificador")
       self.tre_funcoes.heading("nme_aluno_acompanhante", text="Nome do Aluno")
       self.tre_funcoes.heading("RA_aluno_acompanhante", text="RA")
       # Ajustar a largura das colunas
       self.tre_funcoes.column("idt_aluno_acompanhante", width=100)
       self.tre_funcoes.column("nme_aluno_acompanhante", width=400)
       self.tre_funcoes.column("RA_aluno_acompanhante", width=100)
       self.tre_funcoes.grid(row=3, column=0, columnspan=3, padx=self.PADX, pady=self.PADY)


       # Quarta linha com os botões de operações
       self.bt_incluir = tk.Button(self, text="Incluir", command=self.incluir, font='Helvetica 12 bold', fg='white',
                                   bg='blue')
       self.bt_incluir.grid(row=4, column=0, padx=self.PADX, pady=self.PADY)
       self.bt_alterar = tk.Button(self, text="Alterar", command=self.alterar, font='Helvetica 12 bold', fg='white',
                                   bg='blue')
       self.bt_alterar.grid(row=4, column=1, padx=self.PADX, pady=self.PADY)
       self.bt_excluir = tk.Button(self, text="Excluir", command=self.excluir, font='Helvetica 12 bold', fg='white',
                                   bg='blue')
       self.bt_excluir.grid(row=4, column=2, padx=self.PADX, pady=self.PADY)


       # Criando o objeto que irá acessar o banco de dados
       self.sql = SQL(esquema='bd_gestao_visitantes')


   def consultar(self):
       # Obter o termo de busca
       nome = self.nome_var.get()


       # Chamar a função da sua classe utilitária para buscar os registros
       cmd = "SELECT * FROM tb_aluno_acompanhante WHERE nme_aluno_acompanhante LIKE CONCAT('%', %s, '%') ORDER BY nme_aluno_acompanhante"
       funcoes = self.sql.get_list(cmd, [nome])


       self.limpar_tabela()
       for funcao in funcoes:
           self.tre_funcoes.insert("", tk.END, values=(funcao['idt_aluno_acompanhante'],funcao['nme_aluno_acompanhante'], funcao['RA_aluno_acompanhante']))




   def pegar_idt(self):
       selecao = self.tre_funcoes.selection()
       if selecao:
           linha = self.tre_funcoes.selection()[0]
           valores = self.tre_funcoes.item(linha, "values")
           return valores[0]
       else:
           return 0


   def limpar_tabela(self):
       for funcao in self.tre_funcoes.get_children():
           self.tre_funcoes.delete(funcao)


   def incluir(self):
       c = Incluiraluno(self)
       self.et_nome.delete(0, tk.END)
       self.limpar_tabela()

   def alterar(self):
       idt = self.pegar_idt()
       if idt != 0:
           u = AlterarAluno(self, idt)
           self.et_nome.delete(0, tk.END)
           self.limpar_tabela()
       else:
           messagebox.showerror("Erro: Escolha uma função", "Marque uma linha da tabela para selecionar a função")

   def excluir(self):
       idt = self.pegar_idt()
       if idt != 0:
           d = ExcluirAluno(self, idt)
           self.et_nome.delete(0, tk.END)
           self.limpar_tabela()
       else:
           messagebox.showerror("Erro: Escolha um projeto", "Marque uma linha da tabela para selecionar o projeto")


if __name__ == '__main__':
   app = CRUD_aluno()
   app.mainloop()
