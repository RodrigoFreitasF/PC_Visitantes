import tkinter as tk
from tkinter import filedialog
import mysql.connector
import openpyxl


def conectar_banco(localhost, root, admin, bd_gestao_visitantes):
    """Conecta ao banco de dados MySQL e retorna a conexão."""
    try:
        mydb = mysql.connector.connect(
            host=localhost,
            user=root,
            password=admin,
            database=bd_gestao_visitantes
        )
        return mydb
    except mysql.connector.Error as err:
        print(f"Erro ao conectar ao banco de dados: {err}")
        return None


def executar_consulta(mydb, ano, tabela):
    """Executa a consulta SQL e retorna os resultados."""
    mycursor = mydb.cursor()
    sql = f"SELECT MONTH(dta_visita) AS mes, COUNT(*) AS visitas FROM ta_visitas WHERE YEAR(dta_visita) = 2024 GROUP BY mes;"
    mycursor.execute(sql)
    return mycursor.fetchall()


def criar_tela(ano, tabela):
    """Cria a interface gráfica e permite salvar os dados em um arquivo Excel."""

    def salvar_dados():
        """Salva os dados em um arquivo Excel."""
        workbook = openpyxl.Workbook()
        worksheet = workbook.active

        # Escreve o cabeçalho
        worksheet.append(['Mês', 'Visitas'])

        # Escreve os dados
        for mes, visitas in dados.items():
            worksheet.append([mes, visitas])

        # Permite ao usuário escolher o nome do arquivo
        arquivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx")])

        if arquivo:
            workbook.save(arquivo)
            print("Dados salvos com sucesso!")
        else:
            print("Operação de salvamento cancelada.")

    # Conectar ao banco de dados
    mydb = conectar_banco("localhost", "root", "admin", "bd_gestao_visitantes")
    if not mydb:
        return

    # Executar a consulta
    resultado = executar_consulta(mydb, ano, tabela)

    # Criar dicionário de dados
    dados = {linha[0]: linha[1] for linha in resultado}

    # Criar a interface
    root = tk.Tk()
    root.title("Tabela Dinâmica Anual")

    # Criar um label para exibir o ano e a tabela
    label_ano_tabela = tk.Label(root, text=f"Ano: {ano} - Tabela: {tabela}")
    label_ano_tabela.pack()

    # Criar uma listbox para exibir os dados
    listbox = tk.Listbox(root)
    for mes, visitas in dados.items():
        listbox.insert(tk.END, f"Mês {mes}: {visitas} visitas")
    listbox.pack()

    # Botão para salvar os dados
    botao_salvar = tk.Button(root, text="Salvar Dados", command=salvar_dados)
    botao_salvar.pack()

    root.mainloop()


# Solicitar entrada do usuário
ano = int(input("Digite o ano: "))
tabela = input("Digite o nome da tabela: ")
criar_tela(ano, tabela)
