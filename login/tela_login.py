import tkinter as tk
from tkinter import ttk, font, messagebox

import bcrypt
from login.cadastrar_usuario import CadastrarUsuario
from menu_principal.tela_menu import MainMenu
from util.db import SQL


class TelaLogin(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("800x500")
        self.resizable(False, False)
        self.iconbitmap("../ceub.ico")

        # Criação de constantes
        self.PADX = 20
        self.PADY = 10
        self.ROXO_ESCURO = "#43054e"
        self.ROXO = "#662c92"

        # Fontes personalizadas #
        self.title_font = font.Font(family="Arial", size=26, weight="bold")
        self.label_font = font.Font(family="Arial", size=12)
        self.button_font = font.Font(family="Arial", size=12, weight="bold")

        self.title("Sistema de Gestão de Visitantes - Uniceub")

        main_frame = tk.Frame(self, bg=self.ROXO_ESCURO)
        main_frame.pack(expand=True, fill="both")

        # Parte esquerda da tela - Bem-vindo ao Sistema de Gestão de Visitantes #
        left_frame = tk.Frame(main_frame, bg=self.ROXO_ESCURO, width=400, height=500)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        welcome_label = tk.Label(
            left_frame,
            text="Bem-vindo ao\nSistema de Gestão\nde Visitantes",
            font=self.title_font,
            bg=self.ROXO_ESCURO,
            fg="white",
            justify="center"
        )
        welcome_label.pack(expand=True, fill=tk.BOTH, pady=30)

        # Parte direita da tela - Login no sistema #
        right_frame = tk.Frame(main_frame, bg="white", width=300, height=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Título do login #
        login_title = tk.Label(
            right_frame,
            text="Login",
            font=self.title_font,
            bg="white",
            fg=self.ROXO_ESCURO
        )
        login_title.pack(pady=70)

        self.usuario_label = tk.Label(right_frame, text="Usuário", font=self.label_font, bg="white",
                                      fg=self.ROXO_ESCURO)
        self.usuario_label.pack(padx=40, anchor="w")
        self.usuario_input = ttk.Entry(right_frame, font=self.label_font)
        self.usuario_input.pack(pady=(5, 15), padx=40, fill=tk.X)

        self.senha_label = tk.Label(right_frame, text="Senha", font=self.label_font, bg="white", fg=self.ROXO_ESCURO)
        self.senha_label.pack(padx=40, anchor="w")
        self.senha_input = ttk.Entry(right_frame, show="*", font=self.label_font)
        self.senha_input.pack(pady=(5, 15), padx=40, fill=tk.X)

        # Botão de login com estilo #
        login_button = tk.Button(
            right_frame,
            text="Entrar",
            font=self.button_font,
            bg=self.ROXO,
            fg="white",
            command=self.verificar_login,
            cursor="hand2"
        )
        login_button.pack(pady=10, padx=40, fill=tk.X)

        register_button = tk.Button(
            right_frame,
            text="Ainda não tem conta? Cadastre-se",
            fg="#1a237e",
            font=self.label_font,
            bg="white",
            borderwidth=0,
            command=self.cadastrar_usuario,
            cursor="hand2"
        )
        register_button.pack(pady=1)

        # Criando o objeto que irá acessar o banco de dados
        self.sql = SQL(esquema='bd_gestao_visitantes')

    def verificar_login(self):
        # Verificação de credenciais do usuário
        usuario = self.usuario_input.get()
        senha = self.senha_input.get()

        if not usuario or not senha:
            messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos!")
            return

        # Consulta para obter o hash da senha armazenado no banco
        cmd = "SELECT pwd_usuario FROM tb_usuarios WHERE crd_usuario = %s"

        try:
            hash_armazenado = self.sql.get_string(cmd, [usuario])

            if bcrypt.checkpw(senha.encode('utf-8'), hash_armazenado.encode('utf-8')):
                self.destroy()
                MainMenu()
            else:
                messagebox.showwarning("Erro", "Usuário ou senha incorretos!")
        except Exception:
            messagebox.showwarning("Erro", "Usuário não encontrado!")

    def cadastrar_usuario(self):
        CadastrarUsuario(self)


if __name__ == '__main__':
    app = TelaLogin()
    app.mainloop()
