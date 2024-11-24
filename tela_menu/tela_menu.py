import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QFrame, QMessageBox)  # Adicionado QMessageBox
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt


class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestão de Visitantes - Menu")
        self.setFixedSize(800, 500)
        self.setWindowIcon(QIcon("logoCEUB.png"))

        # Configurar widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Header
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #43054e; color: white;")
        header_layout = QVBoxLayout()
        header_label = QLabel("Sistema de Gestão de Visitantes")
        header_label.setAlignment(Qt.AlignCenter)
        header_label.setFont(QFont("Arial", 22, QFont.Bold))
        header_layout.addWidget(header_label)
        header_frame.setLayout(header_layout)

        # Menu grid
        menu_grid = QVBoxLayout() if self.width() < 768 else QHBoxLayout()

        # Adicionar itens ao menu
        menu_items = [
            {"icon": "📋", "title": "Consultar Visitas",
             "action": self.consultar_visitas},
            {"icon": "👥", "title": "Consultar Visitantes",
             "action": self.consultar_visitantes},
            {"icon": "🛡️", "title": "Usuários do Sistema",
             "action": self.consultar_usuarios},
        ]

        for item in menu_items:
            menu_item_frame = self.create_menu_item(item["icon"], item["title"], item["action"])
            menu_grid.addWidget(menu_item_frame)

        # Adicionar elementos ao layout principal
        main_layout.addWidget(header_frame)
        for i in range(menu_grid.count()):
            main_layout.addLayout(menu_grid)

    def create_menu_item(self, icon, title, action):
        """Cria um item de menu estilizado."""
        frame = QFrame()
        frame.setStyleSheet("""
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
        """)
        layout = QVBoxLayout()

        # Ícone
        icon_label = QLabel(icon)
        icon_label.setFont(QFont("Arial", 38))
        icon_label.setAlignment(Qt.AlignCenter)

        # Título
        title_label = QLabel(title)
        title_label.setFont(QFont("Arial", 10, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color: #1a237e;")

        # Botão
        button = QPushButton("Acessar")
        button.setStyleSheet("""
            background-color: #662c92;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
        """)
        button.clicked.connect(action)

        # Adicionar elementos ao layout
        layout.addWidget(icon_label)
        layout.addWidget(title_label)
        layout.addWidget(button)

        frame.setLayout(layout)
        return frame

    def consultar_visitas(self):
        QMessageBox.information(self, "Consultar Visitas", "Redirecionando para a tela de consulta de visitas.")

    def consultar_visitantes(self):
        QMessageBox.information(self, "Consultar Visitantes", "Redirecionando para a tela de consulta de visitantes.")

    def consultar_usuarios(self):
        QMessageBox.information(self, "Usuários do Sistema", "Redirecionando para a tela de gerenciamento de usuários.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec_())
