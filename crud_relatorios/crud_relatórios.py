import tkinter as tk
from tkinter import font, messagebox
from crud_relatorios.docx_visitas import gerar_relatorio_visitas

class CRUDRelatorios(tk.Tk):
    def __init__(self):
        super().__init__()

        self.ROXO_ESCURO = "#43054e"
        self.ROXO = "#662c92"

        self.title("Relatórios")
        self.geometry("600x400")
        self.resizable(False, False)

        self.title_font = font.Font(family="Arial", size=22, weight="bold")
        self.button_font = font.Font(family="Arial", size=14, weight="bold")

        main_frame = tk.Frame(self, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True)

        header_frame = tk.Frame(main_frame, bg=self.ROXO_ESCURO)
        header_frame.pack(fill=tk.X)

        header_label = tk.Label(
            header_frame,
            text="Relatórios de Visitas",
            font=self.title_font,
            bg=self.ROXO_ESCURO,
            fg='white'
        )
        header_label.pack(side=tk.LEFT, padx=20, pady=10)

        body_frame = tk.Frame(main_frame, bg='white')
        body_frame.pack(expand=True)

        excel_button = tk.Button(
            body_frame,
            text="Relatório em Excel (Data Inicial - Final)",
            font=self.button_font,
            bg=self.ROXO,
            fg='white',
            command=self.extrair_relatorio_excel, # Gera o relatório ao clicar
            width=40
        )
        excel_button.pack(pady=20)

        word_button = tk.Button(
            body_frame,
            text="Relatório em Word (Estatística Anual)",
            font=self.button_font,
            bg=self.ROXO,
            fg='white',
            command=self.extrair_relatorio_word,  # Gera o relatório ao clicar
            width=40
        )
        word_button.pack(pady=20)

        back_button = tk.Button(
            main_frame,
            text="Voltar ao Menu",
            command=self.voltar_menu,
            font=self.button_font,
            bg=self.ROXO,
            fg='white'
        )
        back_button.pack(pady=20)

    def extrair_relatorio_excel(self):
        messagebox.showinfo("Relatório em Excel", "Redirecionando para a geração de relatório em Excel.")

    def extrair_relatorio_word(self):
        self.destroy()
        gerar_relatorio_visitas()

    def voltar_menu(self):
        self.destroy()
        from menu_principal.tela_menu import MainMenu
        MainMenu()

if __name__ == "__main__":
    app = CRUDRelatorios()
    app.mainloop()
