import tkinter as tk
from tkinter import messagebox, font

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestão de Visitantes - Menu")
        self.root.geometry("800x500")
        self.root.resizable(False, False)

        # Configurar estilos #
        self.configurar_estilos()

        # Criar frame principal #
        main_frame = tk.Frame(root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Criar cabeçalho #
        header_frame = tk.Frame(main_frame, bg='#43054e')
        header_frame.pack(fill=tk.X)

        header_label = tk.Label(
            header_frame,
            text="Sistema de Gestão de Visitantes",
            font=self.title_font,
            bg='#43054e',
            fg='white'
        )
        header_label.pack(pady=20)

        # Criar frame de itens de menu #
        menu_frame = tk.Frame(main_frame, bg='white')
        menu_frame.pack(expand=True)

        # Configuração de itens de menu #
        menu_items = [
            {
                "emoji": "📋",
                "title": "Consultar Visitas",
                "action": self.consultar_visitas
            },
            {
                "emoji": "👥",
                "title": "Consultar Visitantes",
                "action": self.consultar_visitantes
            },
            {
                "emoji": "🛡️",
                "title": "Usuários do Sistema",
                "action": self.consultar_usuarios
            }
        ]

        # Criar itens de menu com mais espaçamento #
        inner_frame = tk.Frame(menu_frame, bg='white')
        inner_frame.pack(expand=True)

        for item in menu_items:
            self.criar_item_menu(inner_frame, item)

    def configurar_estilos(self):
       # Configurar fontes e estilos personalizados #
        self.title_font = font.Font(family="Arial", size=22, weight="bold")
        self.item_emoji_font = font.Font(family="Arial", size=38)
        self.item_title_font = font.Font(family="Arial", size=14, weight="bold")
        self.button_font = font.Font(family="Arial", size=12, weight="bold")

    def criar_item_menu(self, parent, item):
        ## Criar item de menu estilizado ##
        # Frame do item com espaçamento aumentado #
        item_frame = tk.Frame(
            parent,
            bg='white',
            highlightbackground='#CCCCCC',
            highlightcolor='#CCCCCC',
            highlightthickness=0,
            bd=0
        )
        item_frame.pack(side=tk.LEFT, padx=20, pady=20)  # Aumentar espaçamento horizontal e vertical

        ## Criar um container para o emoji centralizado ##
        emoji_container = tk.Frame(item_frame, bg='white', height=40)
        emoji_container.pack(fill=tk.X)

        # Emoji centralizado #
        emoji_label = tk.Label(
            emoji_container,
            text=item["emoji"],
            font=self.item_emoji_font,
            bg='white',
            anchor='center'
        )
        emoji_label.pack(expand=True)

        # Título com tamanho de fonte aumentado #
        title_label = tk.Label(
            item_frame,
            text=item["title"],
            font=self.item_title_font,
            fg='#1a237e',
            bg='white'
        )
        title_label.pack(pady=10)  # Adicionar padding vertical #

        # Botão com tamanho de texto aumentado #
        button = tk.Button(
            item_frame,
            text="Acessar",
            command=item["action"],
            bg='#662c92',
            fg='white',
            relief=tk.FLAT,
            font=self.button_font,
            padx=5,
            pady=5
        )
        button.pack(pady=5)

    def consultar_visitas(self):
        # Espaço reservado para consulta de visitas #
        messagebox.showinfo("Consultar Visitas", "Redirecionando para a tela de consulta de visitas.")

    def consultar_visitantes(self):
        # Espaço reservado para consulta de visitantes #
        messagebox.showinfo("Consultar Visitantes", "Redirecionando para a tela de consulta de visitantes.")

    def consultar_usuarios(self):
        # Espaço reservado para gerenciamento de usuários #
        messagebox.showinfo("Usuários do Sistema", "Redirecionando para a tela de gerenciamento de usuários.")

def main():
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
