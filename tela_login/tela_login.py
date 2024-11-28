import tkinter as tk
from tkinter import ttk, messagebox, font
import bcrypt
import mysql.connector
from mysql.connector import Error

def conectar_banco():
    ## Conectar ao banco de dados (bd_gestao_visitantes) ##
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="pwd",
            database="schema"
        )
        return conn
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return None

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Sistema de Gestão de Visitantes - Uniceub")
        self.geometry("800x500")
        self.resizable(False, False)
        self.configure(bg="#43054e")  # Cor de fundo padrão do Uniceub #

        # Fontes personalizadas #
        self.title_font = font.Font(family="Arial", size=26, weight="bold")
        self.label_font = font.Font(family="Arial", size=12)
        self.button_font = font.Font(family="Arial", size=12, weight="bold")

        # Configurar o layout #
        self.create_layout()

    def create_layout(self):
        # Criação do layout principal da tela de login #

        # Frame principal para organizar os elementos #
        main_frame = tk.Frame(self, bg="#43054e")
        main_frame.pack(expand=True, fill="both")

        # Parte esquerda da tela- Bem-vindo ao Sistema de Gestão de Visitantes #
        left_frame = tk.Frame(main_frame, bg="#43054e", width=400, height=500)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        welcome_label = tk.Label(
            left_frame,
            text="Bem-vindo ao\nSistema de Gestão\nde Visitantes",
            font=("Arial", 23, "bold"),
            bg="#43054e",
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
            fg="#43054e"
        )
        login_title.pack(pady=70)

        # Campos de entrada com estilo #
        self.usuario_input = ttk.Entry(right_frame, font=self.label_font)
        self.usuario_input.pack(pady=10, padx=40, fill=tk.X)

        self.senha_input = ttk.Entry(right_frame, font=self.label_font, show="*")
        self.senha_input.pack(pady=10, padx=40, fill=tk.X)

        self.usuario_input.pack(pady=10, fill=tk.X)
        self.usuario_input.insert(0, "Nome de usuário")

        self.senha_input.insert(0, "Senha")
        self.senha_input.pack(pady=10, fill=tk.X)


        # Botão de login com estilo #
        login_button = tk.Button(
            right_frame,
            text="ENTRAR",
            font=self.button_font,
            bg="#662c92",
            fg="white",
            command=self.verificar_login
        )
        login_button.pack(pady=10, padx=50, fill=tk.X)

        # Botões adicionais com estilo #
        forgot_password = tk.Button(
            right_frame,
            text="Esqueceu a senha?",
            font=self.label_font,
            fg="#1a237e",
            bg="white",
            borderwidth=0,
            command=self.abrir_recuperacao_senha
        )
        forgot_password.pack(pady=5)

        register_button = tk.Button(
            right_frame,
            text="Registrar novo usuário",
            font=self.label_font,
            fg="#1a237e",
            bg="white",
            borderwidth=0,
            command=self.abrir_registro
        )
        register_button.pack(pady=1)

    def verificar_login(self):
        # Verificação de credenciais do usuário #
        usuario = self.usuario_input.get()
        senha = self.senha_input.get()

        if not usuario or not senha:
            messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos!")
            return

        conn = conectar_banco()
        if not conn:
            messagebox.showerror("Erro", "Erro ao conectar ao banco de dados!")
            return

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT senha FROM usuarios WHERE usuario = %s", (usuario,))
            resultado = cursor.fetchone()

            if resultado and bcrypt.checkpw(senha.encode('utf-8'), resultado[0].encode('utf-8')):
                messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            else:
                messagebox.showwarning("Erro", "Usuário ou senha incorretos!")
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao verificar login: {e}")
        finally:
            conn.close()

    def abrir_recuperacao_senha(self):
        RecuperarSenhaDialog(self)

    def abrir_registro(self):
        RegistroDialog(self)


class RegistroDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Registro de novo usuário")
        self.geometry("400x400")
        self.configure(bg="white")

        # Layout principal #
        layout = tk.Frame(self, bg="white")
        layout.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Título #
        titulo = tk.Label(
            layout,
            text="Registro de novo usuário",
            font=("Arial", 14, "bold"),
            fg="#43054e",
            bg="white"
        )
        titulo.pack(pady=10)

        # Campos de entrada #
        self.nome_input = ttk.Entry(layout, font=("Arial", 10))
        self.nome_input.insert(0, "Nome completo")
        self.nome_input.pack(pady=10, fill=tk.X)

        self.email_input = ttk.Entry(layout, font=("Arial", 10))
        self.email_input.insert(0, "Email")
        self.email_input.pack(pady=10, fill=tk.X)

        self.usuario_input = ttk.Entry(layout, font=("Arial", 10))
        self.usuario_input.insert(0, "Nome de usuário")
        self.usuario_input.pack(pady=10, fill=tk.X)

        self.senha_input = ttk.Entry(layout, font=("Arial", 10))
        self.senha_input.insert(0, "Senha")
        self.senha_input.pack(pady=10, fill=tk.X)

        self.confirmar_senha_input = ttk.Entry(layout, font=("Arial", 10))
        self.confirmar_senha_input.insert(0, "Confirmar senha")
        self.confirmar_senha_input.pack(pady=10, fill=tk.X)

        # Botão de registro #
        registrar_button = tk.Button(
            layout,
            text="Registrar",
            font=("Arial", 14, "bold"),
            bg="#662c92",
            fg="white",
            command=self.registrar
        )
        registrar_button.pack(pady=20)

    def registrar(self):
        # Registrar novo usuário no banco de dados #
        nome = self.nome_input.get()
        email = self.email_input.get()
        usuario = self.usuario_input.get()
        senha = self.senha_input.get()
        confirmar_senha = self.confirmar_senha_input.get()

        # Validações básicas de senha #
        if not all([nome, email, usuario, senha, confirmar_senha]):
            messagebox.showwarning("Erro", "Todos os campos são obrigatórios!")
            return

        if senha != confirmar_senha:
            messagebox.showwarning("Erro", "As senhas não coincidem!")
            return

        if len(senha) < 6:
            messagebox.showwarning("Erro", "A senha deve ter pelo menos 6 caracteres!")
            return

        # Usar criptografia de senha #
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        # Conectar ao banco de dados e registrar #
        conn = conectar_banco()
        if not conn:
            messagebox.showerror("Erro", "Erro ao conectar ao banco de dados!")
            return

        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuarios (nome, email, usuario, senha) 
                VALUES (%s, %s, %s, %s)
            """, (nome, email, usuario, senha_hash.decode('utf-8')))
            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
            self.destroy()
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao registrar usuário: {e}")
        finally:
            conn.close()


class RecuperarSenhaDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Recuperar Senha")
        self.geometry("400x300")
        self.configure(bg="white")

        # Título #
        tk.Label(
            self,
            text="Recuperação de senha",
            font=("Arial", 12, "bold"),
            fg="#43054e",
            bg="white"
        ).pack(pady=5)

        # Campo de email #
        self.email_input = ttk.Entry(self, font=("Arial", 10))
        self.email_input.pack(pady=20, padx=20, fill=tk.X)

        self.email_input.pack(pady=10, fill=tk.X)
        self.email_input.insert(0, "E-mail cadastrado")


        # Botão de envio #
        tk.Button(
            self,
            text="ENVIAR",
            font=("Arial", 10, "bold"),
            bg="#662c92",
            fg="white",
            command=self.enviar_email_recuperacao
        ).pack(pady=5)

    def enviar_email_recuperacao(self):
        # Envio de e-mail de recuperação de senha #
        email = self.email_input.get()
        if not email:
            messagebox.showwarning("Erro", "Por favor, digite seu email!")
            return

        conn = conectar_banco()
        if not conn:
            messagebox.showerror("Erro", "Erro ao conectar ao banco de dados!")
            return

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            usuario = cursor.fetchone()

            if usuario:
                messagebox.showinfo("Sucesso", "Um email de recuperação foi enviado.")
                self.destroy()
            else:
                messagebox.showwarning("Erro", "Email não encontrado no sistema.")
        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao verificar email: {e}")
        finally:
            conn.close()


if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
