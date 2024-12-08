from tkinter import messagebox, font
import tkinter as tk

from locais.crud_locais import CRUDLocais
from visitas.crud_ta_visita import CRUDVisitas
from visitantes.crud_visitantes import CRUDVisitantes


class MainMenu(tk.Tk):
    def __init__(self):
        super().__init__()

        self.ROXO_ESCURO = "#43054e"
        self.ROXO = "#662c92"

        self.title("Sistema de Gestão de Visitantes - Menu")
        self.geometry("800x500")
        self.resizable(False, False)
        self.iconbitmap("../ceub.ico")

        self.title_font = font.Font(family="Arial", size=22, weight="bold")
        self.item_emoji_font = font.Font(family="Arial", size=50)
        self.item_title_font = font.Font(family="Arial", size=18, weight="bold")
        self.button_font = font.Font(family="Arial", size=12, weight="bold")

        main_frame = tk.Frame(self, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True)

        header_frame = tk.Frame(main_frame, bg=self.ROXO_ESCURO)
        header_frame.pack(fill=tk.X)

        header_label = tk.Label(
            header_frame,
            text="Sistema de Gestão de Visitantes",
            font=self.title_font,
            bg=self.ROXO_ESCURO,
            fg='white'
        )
        header_label.pack(side=tk.LEFT, padx=20, pady=10)

        logout_button = tk.Button(
            header_frame,
            text="Desconectar",
            command=self.logout,
            font=self.button_font,
            bg=self.ROXO,
            fg='white',
            relief=tk.FLAT,
            cursor="hand2"
        )
        logout_button.pack(side=tk.RIGHT, padx=20, pady=10)

        menu_frame = tk.Frame(main_frame, bg='white')
        menu_frame.pack(expand=True)

        menu_items = [
            {"emoji": "📋", "title": "Gerenciar Visitas", "action": self.consultar_visitas},
            {"emoji": "👥", "title": "Gerenciar Visitantes", "action": self.consultar_visitantes},
            {"emoji": "🏢", "title": "Gerenciar Locais", "action": self.consultar_locais},
            {"emoji": "🧑🏽", "title": "Usuários do Sistema", "action": self.consultar_usuarios},
        ]

        inner_frame = tk.Frame(menu_frame, bg='white')
        inner_frame.pack(expand=True)

        for idx, item in enumerate(menu_items):
            row = idx // 2
            col = idx % 2
            self.criar_item_menu(inner_frame, item, row, col)

    def criar_item_menu(self, parent, item, row, col):
        item_frame = tk.Frame(
            parent,
            bg='white',
            cursor="hand2"
        )
        item_frame.grid(row=row, column=col, padx=60, pady=20, sticky="nsew")

        item_frame.bind("<Button-1>", lambda e: item["action"]())

        emoji_label = tk.Label(
            item_frame,
            text=item["emoji"],
            font=self.item_emoji_font,
            bg='white',
            anchor='center'
        )
        emoji_label.pack(pady=10)

        title_label = tk.Label(
            item_frame,
            text=item["title"],
            font=self.item_title_font,
            fg=self.ROXO_ESCURO,
            bg='white'
        )
        title_label.pack(pady=10)

        emoji_label.bind("<Button-1>", lambda e: item["action"]())
        title_label.bind("<Button-1>", lambda e: item["action"]())

        parent.grid_columnconfigure(col, weight=1)
        parent.grid_rowconfigure(row, weight=1)

    def consultar_visitas(self):
        self.destroy()
        CRUDVisitas()

    def consultar_visitantes(self):
        self.destroy()
        CRUDVisitantes()

    def consultar_locais(self):
        self.destroy()
        CRUDLocais()

    def consultar_usuarios(self):
        messagebox.showinfo("Usuários do Sistema", "Redirecionando para a tela de gerenciamento de usuários.")

    def logout(self):
        from login.tela_login import TelaLogin
        resposta = messagebox.askyesno("Desconectar", "Tem certeza que deseja sair?")
        if resposta:
            self.destroy()
            TelaLogin()


if __name__ == "__main__":
    app = MainMenu()
    app.mainloop()
