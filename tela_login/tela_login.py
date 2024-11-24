import sys
import bcrypt
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QLabel,
                             QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout,
                             QFrame, QMessageBox, QDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QIcon
import mysql.connector
from mysql.connector import Error


def conectar_banco():
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


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestão de Visitantes - Uniceub")
        self.setFixedSize(800, 500)
        self.setWindowIcon(QIcon('logoCEUB.png'))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # Parte esquerda - Logo
        left_frame = QFrame()
        left_frame.setStyleSheet("background-color: #43054e;")
        left_layout = QVBoxLayout()

        logo_label = QLabel()
        logo_label.setAlignment(Qt.AlignCenter)

        welcome_label = QLabel("Bem-vindo ao\nSistema de Gestão\nde Visitantes")
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet("color: white; font-size: 40px;")
        welcome_label.setWordWrap(True)

        left_layout.addWidget(logo_label)
        left_layout.addWidget(welcome_label)
        left_frame.setLayout(left_layout)

        # Parte direita - Login
        right_frame = QFrame()
        right_frame.setStyleSheet("background-color: white;")
        right_layout = QVBoxLayout()

        login_title = QLabel("Login")
        login_title.setAlignment(Qt.AlignCenter)
        login_title.setStyleSheet("""
            font-size: 28px;
            color: #43054e;
            margin: 20px;
            font-weight: bold;
        """)

        form_container = QFrame()
        form_layout = QVBoxLayout()

        # Campos de entrada
        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText("Digite seu usuário")
        self.senha_input = QLineEdit()
        self.senha_input.setPlaceholderText("Digite sua senha")
        self.senha_input.setEchoMode(QLineEdit.Password)

        style = """
            QLineEdit {
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
                margin: 5px 0;
            }
            QLineEdit:focus {
                border: 2px solid #43054e;
            }
        """
        self.usuario_input.setStyleSheet(style)
        self.senha_input.setStyleSheet(style)

        # Botões
        self.login_button = QPushButton("ENTRAR")
        self.login_button.setStyleSheet("""
            QPushButton {
                background-color: #662c92;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #283593;
            }
        """)
        self.login_button.clicked.connect(self.verificar_login)

        self.forgot_password = QPushButton("Esqueceu a senha?")
        self.register_button = QPushButton("Registrar novo usuário")

        button_style = """
            QPushButton {
                color: #1a237e;
                border: none;
                font-size: 14px;
                text-decoration: underline;
            }
            QPushButton:hover {
                color: #283593;
            }
        """
        self.forgot_password.setStyleSheet(button_style)
        self.register_button.setStyleSheet(button_style)

        self.forgot_password.clicked.connect(self.abrir_recuperacao_senha)
        self.register_button.clicked.connect(self.abrir_registro)

        # Montando o layout
        form_layout.addWidget(login_title)
        form_layout.addWidget(self.usuario_input)
        form_layout.addWidget(self.senha_input)
        form_layout.addWidget(self.login_button)
        form_layout.addWidget(self.forgot_password)
        form_layout.addWidget(self.register_button)
        form_layout.setAlignment(Qt.AlignCenter)
        form_container.setLayout(form_layout)

        right_layout.addStretch()
        right_layout.addWidget(form_container)
        right_layout.addStretch()

        right_frame.setLayout(right_layout)

        main_layout.addWidget(left_frame, 1)
        main_layout.addWidget(right_frame, 1)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

    def verificar_login(self):
        usuario = self.usuario_input.text()
        senha = self.senha_input.text()

        if not usuario or not senha:
            QMessageBox.warning(
                self,
                "Campos Vazios",
                "Por favor, preencha todos os campos!",
                QMessageBox.Ok
            )
            return

        conn = conectar_banco()
        if not conn:
            QMessageBox.critical(self, "Erro", "Erro ao conectar ao banco de dados!")
            return

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT senha FROM usuarios WHERE usuario = %s", (usuario,))
            resultado = cursor.fetchone()

            if resultado and bcrypt.checkpw(senha.encode('utf-8'), resultado[0].encode('utf-8')):
                QMessageBox.information(
                    self,
                    "Sucesso",
                    "Login realizado com sucesso!",
                    QMessageBox.Ok
                )
            else:
                QMessageBox.warning(
                    self,
                    "Erro",
                    "Usuário ou senha incorretos!",
                    QMessageBox.Ok
                )
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "Erro", f"Erro ao verificar login: {e}")
        finally:
            conn.close()

    def abrir_recuperacao_senha(self):
        dialog = RecuperarSenhaDialog(self)
        dialog.exec_()

    def abrir_registro(self):
        dialog = RegistroDialog(self)
        dialog.exec_()


class RecuperarSenhaDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Recuperar Senha")
        self.setFixedSize(400, 300)
        self.setWindowIcon(QIcon('logoCEUB.png'))

        layout = QVBoxLayout()

        # Título
        titulo = QLabel("Recuperação de Senha")
        titulo.setStyleSheet("""
            font-size: 20px;
            color: #43054e;
            margin: 10px;
            font-weight: bold;
        """)
        titulo.setAlignment(Qt.AlignCenter)

        # Campo de email
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Digite seu email cadastrado")
        self.email_input.setStyleSheet("""
            QLineEdit {
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 12px;
                margin: 5px 0;
            }
            QLineEdit:focus {
                border: 2px solid #43054e;
            }
        """)

        # Botão de enviar
        self.enviar_button = QPushButton("Enviar Email de Recuperação")
        self.enviar_button.setStyleSheet("""
            QPushButton {
                background-color: #662c92;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 5px;
                font-size: 16px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #283593;
            }
        """)
        self.enviar_button.clicked.connect(self.enviar_email_recuperacao)

        # Adicionar widgets ao layout
        layout.addWidget(titulo)
        layout.addWidget(QLabel("Digite seu email cadastrado:"))
        layout.addWidget(self.email_input)
        layout.addWidget(self.enviar_button)

        self.setLayout(layout)

    def enviar_email_recuperacao(self):
        email = self.email_input.text()

        if not email:
            QMessageBox.warning(self, "Erro", "Por favor, digite seu email!")
            return

        conn = conectar_banco()
        if not conn:
            QMessageBox.critical(self, "Erro", "Erro ao conectar ao banco de dados!")
            return

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
            usuario = cursor.fetchone()

            if usuario:
                # Aqui você implementaria o envio real do email
                QMessageBox.information(
                    self,
                    "Sucesso",
                    "Um email de recuperação foi enviado para seu endereço.",
                    QMessageBox.Ok
                )
                self.accept()
            else:
                QMessageBox.warning(
                    self,
                    "Erro",
                    "Email não encontrado no sistema.",
                    QMessageBox.Ok
                )
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "Erro", f"Erro ao verificar email: {e}")
        finally:
            conn.close()


class RegistroDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registro de Novo Usuário")
        self.setFixedSize(500, 500)
        self.setWindowIcon(QIcon('logoCEUB.png'))

        layout = QVBoxLayout()

        # Título
        titulo = QLabel("Registro de Novo Usuário")
        titulo.setStyleSheet("""
            font-size: 20px;
            color: #43054e;
            margin: 10px;
            font-weight: bold;
        """)
        titulo.setAlignment(Qt.AlignCenter)

        # Campos de entrada
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Nome completo")
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText("Nome de usuário")
        self.senha_input = QLineEdit()
        self.senha_input.setPlaceholderText("Senha")
        self.senha_input.setEchoMode(QLineEdit.Password)
        self.confirmar_senha_input = QLineEdit()
        self.confirmar_senha_input.setPlaceholderText("Confirmar senha")
        self.confirmar_senha_input.setEchoMode(QLineEdit.Password)

        # Estilo para os campos
        style = """
            QLineEdit {
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 5px;
                font-size: 11px;
                margin: 5px 0;
            }
            QLineEdit:focus {
                border: 2px solid #43054e;
            }
        """
        self.nome_input.setStyleSheet(style)
        self.email_input.setStyleSheet(style)
        self.usuario_input.setStyleSheet(style)
        self.senha_input.setStyleSheet(style)
        self.confirmar_senha_input.setStyleSheet(style)

        # Botão de registro
        self.registrar_button = QPushButton("Registrar")
        self.registrar_button.setStyleSheet("""
            QPushButton {
                background-color: #662c92;
                color: white;
                padding: 12px;
                border: none;
                border-radius: 5px;
                font-size: 14px;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #283593;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """)
        self.registrar_button.clicked.connect(self.registrar)

        # Adicionar widgets ao layout
        layout.addWidget(titulo)
        layout.addWidget(self.nome_input)
        layout.addWidget(self.email_input)
        layout.addWidget(self.usuario_input)
        layout.addWidget(self.senha_input)
        layout.addWidget(self.confirmar_senha_input)
        layout.addWidget(self.registrar_button)

        self.setLayout(layout)

    def registrar(self):
        nome = self.nome_input.text()
        email = self.email_input.text()
        usuario = self.usuario_input.text()
        senha = self.senha_input.text()
        confirmar_senha = self.confirmar_senha_input.text()

        # Validações
        if not all([nome, email, usuario, senha, confirmar_senha]):
            QMessageBox.warning(self, "Erro", "Todos os campos são obrigatórios!")
            return

        if senha != confirmar_senha:
            QMessageBox.warning(self, "Erro", "As senhas não coincidem!")
            return

        if len(senha) < 6:
            QMessageBox.warning(self, "Erro", "A senha deve ter pelo menos 6 caracteres!")
            return

        # Criptografar senha
        senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())

        # Conectar ao banco e registrar
        conn = conectar_banco()
        if not conn:
            QMessageBox.critical(self, "Erro", "Erro ao conectar ao banco de dados!")
            return

        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuarios (nome, email, usuario, senha) 
                VALUES (%s, %s, %s, %s)
            """, (nome, email, usuario, senha_hash.decode('utf-8')))
            conn.commit()
            QMessageBox.information(self, "Sucesso", "Usuário registrado com sucesso!")
            self.accept()
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "Erro", f"Erro ao registrar usuário: {e}")
        finally:
            conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    font = QFont("Segoe UI", 10)
    app.setFont(font)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec_())
