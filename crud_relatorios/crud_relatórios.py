import tkinter as tk
from tkinter import font, messagebox
from crud_relatorios.docx_visitas import gerar_relatorio_visitas


class CRUDRelatorios(tk.Tk):
    def __init__(self, usuario_logado):
        super().__init__()

        self.ROXO_ESCURO = "#43054e"
        self.ROXO = "#662c92"

        self.usuario_logado = usuario_logado
        self.title("Relatório em Word")
        self.resizable(False, False)
        self.iconbitmap("../ceub.ico")

        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=12, weight="bold")

        main_frame = tk.Frame(self, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Cabeçalho
        header_frame = tk.Frame(main_frame, bg='white')
        header_frame.pack(fill=tk.X)

        header_label = tk.Label(
            header_frame,
            text="Relatório de Visitas",
            font=self.title_font,
            fg=self.ROXO,
            bg='white'
        )
        header_label.pack(padx=20, pady=(20, 0))

        # Corpo principal
        body_frame = tk.Frame(main_frame, bg='white')
        body_frame.pack(expand=True, padx=20, pady=20)

        # Botão para relatório Word
        word_button = tk.Button(
            body_frame,
            text="Relatório em Word (Estatística Anual)",
            font=self.button_font,
            bg=self.ROXO,
            fg='white',
            command=self.extrair_relatorio_word,
            cursor='hand2'
        )
        word_button.pack(fill=tk.X, pady=10)

        # Botão para voltar ao menu
        back_button = tk.Button(
            body_frame,
            text="Voltar ao Menu",
            command=self.voltar_menu,
            font=self.button_font,
            bg=self.ROXO,
            fg='white',
            cursor = 'hand2'
        )
        back_button.pack(fill=tk.X, pady=10)

    def extrair_relatorio_word(self):
        self.destroy()
        gerar_relatorio_visitas()

    def voltar_menu(self):
        self.destroy()
        from menu_principal.tela_menu import MainMenu
        MainMenu(self.usuario_logado)


if __name__ == "__main__":
    app = CRUDRelatorios()
    app.mainloop()
