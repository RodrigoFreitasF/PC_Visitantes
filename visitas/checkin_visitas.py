import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class CheckinVisitas:
    def __init__(self, janela_mestre, idt_visita):
        self.popup = tk.Toplevel(janela_mestre)
        self.popup.grab_set()
        self.popup.iconbitmap("../ceub.ico")

        self.sql = janela_mestre.sql  # Conexão com o banco de dados

        # Constantes
        self.PADX = 10
        self.PADY = 10
        self.ROXO = "#662c92"

        linha = 0

        # Título
        titulo = tk.Label(self.popup, text="Check-in de Visita", font='Helvetica 16 bold', fg=self.ROXO)
        titulo.grid(row=linha, column=0, columnspan=3, padx=self.PADX, pady=self.PADY)
        linha += 1

        # Instrução (Primeira linha)
        mensagem1 = tk.Label(
            self.popup,
            text="Confirmar Check-in?",
            font='Helvetica 12',
            fg=self.ROXO
        )
        mensagem1.grid(row=linha, column=0, columnspan=3, padx=self.PADX, pady=(self.PADY, 2))
        linha += 1

        # Instrução (Segunda linha)
        mensagem2 = tk.Label(
            self.popup,
            text="A hora de entrada será registrada automaticamente.",
            font='Helvetica 12',
            fg=self.ROXO
        )
        mensagem2.grid(row=linha, column=0, columnspan=3, padx=self.PADX, pady=(2, self.PADY))
        linha += 1

        # Botão para confirmar o check-in
        self.bt_confirmar = tk.Button(
            self.popup,
            text="Confirmar",
            command=lambda: self.confirmar_checkin(idt_visita),
            font='Helvetica 12 bold',
            fg='white',
            bg=self.ROXO,
            cursor="hand2"
        )
        self.bt_confirmar.grid(row=linha, column=0, columnspan=3, padx=self.PADX, pady=self.PADY, sticky="ew")
        linha += 1

    def confirmar_checkin(self, idt_visita):
        # Data e hora atual
        hora_entrada = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Comando SQL para atualizar a hora de entrada
        cmd = "UPDATE ta_visitas SET hra_entrada_visita = %s WHERE idt_visitas = %s"
        try:
            self.sql.upd_del(cmd, (hora_entrada, idt_visita))  # Atualiza a hora de entrada no banco
            messagebox.showinfo("Sucesso", "Check-in realizado com sucesso!")
            self.popup.destroy()  # Fecha a janela popup após o check-in
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao realizar o check-in: {str(e)}")
