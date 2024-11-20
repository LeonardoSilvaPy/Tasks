import customtkinter as ctk
import os
from report_generator import generate_report  # Verifique se esse arquivo existe e está correto

def open_report_window(self):
    dialog = ctk.CTkToplevel(self.window)
    dialog.title("Relatório de Tarefas")
    dialog.geometry("600x400")

    # Adiciona um título ao relatório
    title_label = ctk.CTkLabel(dialog, text="Relatório de Tarefas", font=("Helvetica", 16))
    title_label.pack(pady=10)

    # Exibe um resumo das tarefas
    report_text = ctk.CTkTextbox(dialog, width=580, height=250)
    report_text.pack(pady=10)

    # Popula o TextBox com as tarefas
    for task in self.tasks:
        report_text.insert("end", f"Descrição: {task['description']}, Status: {task['status']}, Data: {task['date']}\n")

    # Botões para visualizar e salvar o relatório
    view_button = ctk.CTkButton(dialog, text="Visualizar Relatório", command=self.view_report)
    view_button.pack(side="left", padx=20, pady=20)

    save_button = ctk.CTkButton(dialog, text="Salvar Relatório", command=self.save_report)
    save_button.pack(side="left", padx=20, pady=20)

    close_button = ctk.CTkButton(dialog, text="Fechar", command=dialog.destroy)
    close_button.pack(side="left", padx=20, pady=20)

def view_report(self):
    pdf_path = "relatorio_tarefas.pdf"
    generate_report(self.tasks)
    os.startfile(pdf_path)

def save_report(self):
    pdf_path = "relatorio_tarefas.pdf"
    generate_report(self.tasks)
    self.show_message("Relatório salvo como 'relatorio_tarefas.pdf'!")  # Mensagem de confirmação
