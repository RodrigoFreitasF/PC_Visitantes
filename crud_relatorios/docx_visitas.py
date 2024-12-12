import os
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.shared import RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches
from util.db import SQL

def gerar_relatorio_visitas():
    # Conexão com o banco de dados
    sql = SQL(esquema='bd_gestao_visitantes')

    # Consulta para "visitas por mês"
    cmd_visitas_mes = """
        SELECT YEAR(dta_visita) AS ano, MONTH(dta_visita) AS mes, COUNT(*) AS total_visitas
        FROM ta_visitas
        GROUP BY YEAR(dta_visita), MONTH(dta_visita)
        ORDER BY ano DESC, mes DESC;
    """
    visitas_mes = sql.get_list(cmd_visitas_mes)

    # Dicionário com os meses
    meses = {
        1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril', 5: 'Maio', 6: 'Junho',
        7: 'Julho', 8: 'Agosto', 9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
    }

    doc = Document()

    logo_path = 'logo_CEUB.png'
    try:
        doc.add_picture(logo_path, width=Inches(1.5))
        last_paragraph = doc.paragraphs[-1]
        last_paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.LEFT
    except FileNotFoundError:
        print(f"Arquivo de logo '{logo_path}' não encontrado. O relatório será gerado sem o logo.")

    # Título do relatório
    title = doc.add_heading('RELATÓRIO DE VISITAS 2024', 0)
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    doc.add_paragraph('\n')
    #para digitar texto no documento
    doc.add_paragraph("Este é um documento de relatório para as visitas do CEUB.")

    # Tabela de visitas por mês
    doc.add_heading('Visitas por Mês', level=1)
    table = doc.add_table(rows=1, cols=2)  # 1 linha de cabeçalho, 2 colunas (Mês e Visitas)
    table.style = 'Table Grid'

    # Cabeçalho da tabela
    hdr_cells = table.rows[0].cells
    hdr_cells[0].text = 'Mês'
    hdr_cells[1].text = 'Visitas'

    # Cabeçalho
    for cell in hdr_cells:
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)  # Branco
        tc_pr = cell._element.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:fill'), "6A0DAD")  # Roxo no formato hexadecimal
        tc_pr.append(shd)

    # total de visitas do ano
    total_visitas_ano = 0

    # Criar e preencher a tabela
    for i in range(1, 13):  # Para cada mês de 1 a 12
        row_cells = table.add_row().cells
        row_cells[0].text = meses[i]  # Nome do mês

        # Verificar se há dados para o mês
        visitas_encontradas = next((row['total_visitas'] for row in visitas_mes if row['mes'] == i), None)
        if visitas_encontradas:
            row_cells[1].text = str(visitas_encontradas)
            total_visitas_ano += visitas_encontradas
        else:
            row_cells[1].text = 'SEM DADOS'
        for cell in row_cells:
            cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER

    # Linha do total de visitas
    total_row = table.add_row().cells
    total_row[0].text = 'Total de Visitas'
    total_row[1].text = str(total_visitas_ano)

    for cell in total_row:
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        tc_pr = cell._element.get_or_add_tcPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:fill'), "D8BFD8")  # Cor lilás clara no formato hexadecimal
        tc_pr.append(shd)

    # Salvar o arquivo
    relatorio_path = 'relatorio_visitas_2024.docx'
    doc.save(relatorio_path)
    print(f"Relatório salvo como '{relatorio_path}'.")

    # Abrir o arquivo automaticamente
    try:
        if os.name == 'nt':  # Windows
            os.startfile(relatorio_path)
        elif os.name == 'posix':  # macOS ou Linux
            os.system(f'open {relatorio_path}')  # Para macOS
            # Para Linux, use: os.system(f'xdg-open {relatorio_path}')
    except Exception as e:
        print(f"Erro ao abrir o arquivo: {e}")



