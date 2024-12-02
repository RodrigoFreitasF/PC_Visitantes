import tkinter as tk
from tkinter import Toplevel, messagebox
from datetime import datetime

class CheckoutVisitas:
    def __init__(self, janela_mestre, idt_visita):
        self.popup = Toplevel(janela_mestre)
        self.popup.grab_set()

        self.sql = janela_mestre.sql  # Conexão com o banco de dados

        # Constantes de cores
        cor_btn = '#43054e'
        fonte_btn = 'Jakob 12 bold'
        cor_titulo = '#bf0087'

        # Título
        titulo = tk.Label(self.popup, text="Checkout de Visita", font='Helvetica 16 bold', fg=cor_titulo)
        titulo.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        # Instrução
        mensagem = tk.Label(self.popup, text="Confirmar checkout? A hora de saída será registrada.", font='Helvetica 12', fg=cor_titulo)
        mensagem.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Botão para confirmar o checkout
        self.bt_checkout = tk.Button(self.popup, text="Confirmar Checkout", command=lambda: self.confirmar_checkout(idt_visita),
                                      font=fonte_btn, fg='white', bg=cor_btn)
        self.bt_checkout.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def confirmar_checkout(self, idt_visita):
        # Data e hora atual
        hora_saida = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Comando SQL para atualizar a hora de saída
        cmd = "UPDATE ta_visitas SET hra_saida_visita = %s WHERE idt_visitas = %s"
        try:
            self.sql.upd_del(cmd, (hora_saida, idt_visita))  # Atualiza a hora de saída no banco
            messagebox.showinfo("Sucesso", "Checkout realizado com sucesso!")
            self.popup.destroy()  # Fecha a janela popup após o checkout
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao realizar o checkout: {str(e)}")
