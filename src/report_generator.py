from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_report(tasks):
    pdf_path = "relatorio_tarefas.pdf"  # Caminho onde o PDF será salvo
    c = canvas.Canvas(pdf_path, pagesize=letter)
    width, height = letter  # Obtém as dimensões da página

    c.drawString(100, height - 50, "Relatório de Tarefas")  # Título do relatório

    y = height - 70  # Posição inicial para escrever as tarefas
    for task in tasks:
        c.drawString(100, y, f"Descrição: {task['description']}, Status: {task['status']}, Data: {task['date']}")
        y -= 20  # Move para a próxima linha

    c.save()  # Salva o PDF
