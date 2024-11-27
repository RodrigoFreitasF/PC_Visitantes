# Utilizando tkinter para criar o menu principal

import tkinter as tk
from tkinter import messagebox, ttk

from crud_tb_visitantes.crud_visitantes import CRUDVisitantes


class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestão de Visitantes - Menu")
        self.geometry("800x500")
        self.configure(bg="#f0f0f0")  # Cor de fundo para a janela principal

        # Header
        header_frame = tk.Frame(self, bg="#43054e", height=70)
        header_frame.pack(fill="x", side="top")

        header_label = tk.Label(
            header_frame,
            text="Sistema de Gestão de Visitantes",
            bg="#43054e",
            fg="white",
            font=("Arial", 20, "bold"),
        )
        header_label.pack(expand=True)

        # Menu grid
        menu_frame = tk.Frame(self, bg="#f0f0f0", padx=20, pady=20)
        menu_frame.pack(expand=True, fill="both")

        menu_items = [
            {"icon": "📋", "title": "Consultar Visitas", "action": self.consultar_visitas},
            {"icon": "👥", "title": "Consultar Visitantes", "action": self.consultar_visitantes},
            {"icon": "🛡️", "title": "Usuários do Sistema", "action": self.consultar_usuarios},
        ]

        for item in menu_items:
            self.create_menu_item(menu_frame, item["icon"], item["title"], item["action"])

    def create_menu_item(self, parent, icon, title, action):
        """Cria um item estilizado para o menu."""
        frame = tk.Frame(
            parent,
            bg="white",
            relief="raised",
            bd=1,
            padx=10,
            pady=10,
        )
        frame.pack(side="top", fill="x", padx=10, pady=10)

        # Ícone
        icon_label = tk.Label(frame, text=icon, font=("Arial", 24), bg="white")
        icon_label.pack(side="left", padx=10)

        # Título
        title_label = tk.Label(
            frame, text=title, font=("Arial", 16, "bold"), bg="white", fg="#1a237e"
        )
        title_label.pack(side="top", anchor="w")

        # Botão
        button = tk.Button(
            frame,
            text="Acessar",
            bg="#662c92",
            fg="white",
            font=("Arial", 12),
            command=action,
            relief="flat",
            overrelief="raised",
            padx=10,
            pady=5,
        )
        button.pack(side="right", padx=10)

    def consultar_visitas(self):
        messagebox.showinfo("Consultar Visitas", "Redirecionando para a tela de consulta de visitas.")

    def consultar_visitantes(self):
        CRUDVisitantes()

    def consultar_usuarios(self):
        messagebox.showinfo("Usuários do Sistema", "Redirecionando para a tela de gerenciamento de usuários.")


if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
