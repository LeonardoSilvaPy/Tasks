import customtkinter as ctk
import json
import os
from datetime import datetime
from task_graph import show_task_graph  # Importa a função de gráficos do novo arquivo
from report import open_report_window 

class TaskManager:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Gerenciador de Tarefas")
        self.window.attributes('-fullscreen', True)
        
        # Variável para controlar o estado da tela cheia
        self.is_fullscreen = True

        self.tasks = []  # Inicializa a lista de tarefas
        self.setup_ui()  # Configura a interface do usuário
        
        # Configuração do tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Atualiza o caminho do JSON
        self.json_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'tasks.json')
        print(f"Caminho do JSON: {self.json_path}")  # Para depuração

        self.tasks = self.load_tasks()

        # Frame principal
        self.main_frame = ctk.CTkFrame(self.window)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Configuração de cores
        self.colors = {
            "urgent": "#FF6B6B",    # Vermelho
            "pending": "#1E90FF",   # Azul
            "completed": "#6BCB77",  # Verde
            "redo": "#FFD93D"       # Amarelo escuro
        }

        # Modificar o task_list para um CTkScrollableFrame
        self.task_list = ctk.CTkScrollableFrame(self.main_frame, width=600, height=300)
        self.task_list.pack(pady=10, fill="both", expand=True)

        # Frame para botões
        self.button_frame = ctk.CTkFrame(self.main_frame)
        self.button_frame.pack(pady=10)

        # Botões
        self.add_button = ctk.CTkButton(self.button_frame, text="Adicionar Tarefa", command=self.add_task_window)
        self.add_button.pack(side="left", padx=5)

        # Botão para mostrar gráficos
        self.graph_button = ctk.CTkButton(self.button_frame, text="Mostrar Gráficos", command=self.show_graphs)
        self.graph_button.pack(side="left", padx=5)

        # Botão para alternar tela cheia
        self.exit_fullscreen_button = ctk.CTkButton(self.button_frame, text="Sair do Modo Cheia", command=self.toggle_fullscreen)
        self.exit_fullscreen_button.pack(side="left", padx=5)

        # Adiciona o evento de tecla para sair do modo tela cheia
        self.window.bind("<Escape>", self.toggle_fullscreen)

        self.report_button = ctk.CTkButton(self.button_frame, text="Relatório", command=self.open_report)
        self.report_button.pack(side="left", padx=10)

        self.update_task_list()

    def setup_ui(self):
        pass

    def open_report(self):
        open_report_window(self)  # Chama a função correta para abrir o relatório

    def run(self):
        self.window.mainloop()

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen  # Alterna o estado
        self.window.attributes('-fullscreen', self.is_fullscreen)  # Atualiza o modo de tela cheia
        
        # Atualiza o texto do botão
        if self.is_fullscreen:
            self.exit_fullscreen_button.configure(text="Sair do Modo Tela Cheia")
        else:
            self.exit_fullscreen_button.configure(text="Modo Tela Cheia")

    def load_tasks(self):
        try:
            with open(self.json_path, "r") as file:
                tasks = json.load(file)
                print(f"Tarefas carregadas: {tasks}")  # Para depuração
                # Garantir que cada tarefa tenha a chave 'level'
                for task in tasks:
                    if "level" not in task:
                        task["level"] = 1  # Define um nível padrão para tarefas pendentes
                return tasks
        except FileNotFoundError:
            print("Arquivo tasks.json não encontrado.")  # Mensagem se o arquivo não for encontrado
            return []
        except json.JSONDecodeError:
            print("Erro ao decodificar o arquivo JSON.")  # Mensagem se houver erro de decodificação
            return []

    def save_tasks(self):
        with open(self.json_path, "w") as file:
            json.dump(self.tasks, file, indent=4)
            print(f"Tarefas salvas no {self.json_path}")  # Para depuração


    def add_task_window(self):
        dialog = ctk.CTkToplevel()
        dialog.title("Adicionar Tarefa")
        dialog.geometry("500x200")  # Aumentando a largura da janela
        dialog.lift()  # Levanta a janela acima da janela principal
        dialog.focus_force()  # Força o foco na nova janela

        label = ctk.CTkLabel(dialog, text="Digite a descrição da tarefa:")
        label.pack(pady=10)

        entry = ctk.CTkTextbox(dialog, width=450, height=90)  # Campo de texto semelhante ao de edição
        entry.pack(pady=10, padx=20)

        confirm_button = ctk.CTkButton(dialog, text="Adicionar", 
                                       command=lambda: self.confirm_add_task(entry.get("1.0", "end-1c"), dialog))
        confirm_button.pack(pady=10)

    def confirm_add_task(self, task_desc, dialog):
        if task_desc:
            new_task = {
                "description": task_desc.upper(),  # Armazenar em letras maiúsculas
                "status": "pending",
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "priority": "normal",
                "level": 1  # Nível padrão para tarefas pendentes
            }
            self.tasks.insert(0, new_task)
            self.save_tasks()
            self.update_task_list()
        dialog.destroy()  # Fecha a janela após adicionar a tarefa

    def complete_task_window(self):
        pending_tasks = [task for task in self.tasks if task["status"] == "pending"]
        if not pending_tasks:
            self.show_message("Não há tarefas pendentes!")
            return
            
        dialog = ctk.CTkToplevel()
        dialog.title("Concluir Tarefa")
        dialog.geometry("400x300")
        
        for i, task in enumerate(pending_tasks):
            btn = ctk.CTkButton(dialog, text=task["description"], 
                                command=lambda t=task: self.complete_task(t, dialog))
            btn.pack(pady=5)

    def complete_task(self, task, dialog):
        task["status"] = "completed"
        task["completion_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task["level"] = 0  # Atualiza o nível para concluída
        self.save_tasks()
        self.update_task_list()
        dialog.destroy()

    def remove_task_window(self):
        dialog = ctk.CTkToplevel()
        dialog.title("Remover Tarefa")
        dialog.geometry("400x300")
        
        for task in self.tasks:
            btn = ctk.CTkButton(dialog, text=task["description"], 
                                command=lambda t=task: self.remove_task(t, dialog))
            btn.pack(pady=5)

    def remove_task(self, task, dialog):
        self.tasks.remove(task)
        self.save_tasks()
        self.update_task_list()
        dialog.destroy()

    def update_task_list(self):
        # Limpar frame atual
        for widget in self.task_list.winfo_children():
            widget.destroy()
            
        # Organizar tarefas por prioridade e status
        # Ordenar as tarefas pelo nível
        sorted_tasks = sorted(self.tasks, key=lambda t: t["level"], reverse=True)

        # Criar frames para cada tarefa com cores correspondentes
        for task in sorted_tasks:
            task_frame = ctk.CTkFrame(self.task_list)
            task_frame.pack(fill="x", pady=2, padx=5)
            
            # Definir cor baseada no status/prioridade
            if task.get("priority") == "urgent":
                bg_color = self.colors["urgent"]
            elif task["status"] == "completed":
                bg_color = self.colors["completed"]
            elif task.get("priority") == "redo":
                bg_color = self.colors["redo"]
            else:
                bg_color = self.colors["pending"]
                
            task_label = ctk.CTkLabel(
                task_frame,
                text=f"{task['description']} ({task['date']})",
                fg_color=bg_color,
                corner_radius=8,
                height=60
            )
            task_label.pack(side="left", fill="x", expand=True, padx=5, pady=2)
            
            # Adicionar menu de contexto ao clicar
            task_label.bind("<Button-1>", lambda e, t=task: self.show_task_options(t))

    def show_task_options(self, task):
        dialog = ctk.CTkToplevel()
        dialog.title("Opções da Tarefa")
        dialog.geometry("300x250")
        dialog.transient(self.window)
        dialog.grab_set()
        dialog.focus_force()
        
        options = [
            ("Marcar como Concluída", lambda: self.complete_task(task, dialog)),
            ("Marcar como Urgente", lambda: self.mark_urgent(task, dialog)),
            ("Editar Tarefa", lambda: self.edit_task(task, dialog)),
            ("Excluir Tarefa", lambda: self.remove_task(task, dialog))
        ]
        
        # Adicionar a opção "Refazer Tarefa" e "Despriorizar" se necessário
        if task["status"] == "completed":
            options.append(("Refazer Tarefa", lambda: self.redo_task(task, dialog)))
        if task.get("priority") in ["urgent", "redo"]:
            options.append(("Despriorizar", lambda: self.deprioritize_task(task, dialog)))
        
        for text, command in options:
            button = ctk.CTkButton(dialog, text=text, command=command)
            button.pack(pady=5)

    def mark_urgent(self, task, dialog):
        task["priority"] = "urgent"
        task["level"] = 3
        self.save_tasks()
        self.update_task_list()
        dialog.destroy()

    def edit_task(self, task, options_dialog):
        edit_dialog = ctk.CTkToplevel()
        edit_dialog.title("Editar Tarefa")
        edit_dialog.geometry("400x200")
        edit_dialog.transient(self.window)  # Torna a janela de edição uma janela filha
        edit_dialog.grab_set()  # Desativa a janela principal até que a janela de edição seja fechada
        edit_dialog.focus_force()  # Foca na nova janela para garantir que ela esteja em primeiro plano

        label = ctk.CTkLabel(edit_dialog, text="Digite a nova descrição da tarefa:")
        label.pack(pady=10)

        entry = ctk.CTkTextbox(edit_dialog, width=350, height=80)  # Campo de texto semelhante ao de adicionar
        entry.insert("1.0", task["description"])  # Insere a descrição atual da tarefa
        entry.pack(pady=10, padx=20)

        confirm_button = ctk.CTkButton(edit_dialog, text="Salvar", 
                                         command=lambda: self.confirm_edit_task(task, entry.get("1.0", "end-1c"), edit_dialog, options_dialog))
        confirm_button.pack(pady=10)

    def confirm_edit_task(self, task, new_desc, edit_dialog, options_dialog):
        if new_desc:
            task["description"] = new_desc.upper()  # Atualiza a descrição em letras maiúsculas
            self.save_tasks()
            self.update_task_list()
        edit_dialog.destroy()  # Fecha a janela de edição após salvar
        options_dialog.destroy()  # Fecha a janela de opções também

    def redo_task(self, task, dialog):
        task["status"] = "pending"
        task["priority"] = "redo"
        task["level"] = 2
        self.save_tasks()
        self.update_task_list()
        dialog.destroy()

    def deprioritize_task(self, task, dialog):
        task["priority"] = "normal"
        task["level"] = 1
        self.save_tasks()
        self.update_task_list()
        dialog.destroy()

    def show_graphs(self):
        show_task_graph(self.tasks, self.colors)  # Chama a função do gráfico com as tarefas e cores

    def show_message(self, message):
        dialog = ctk.CTkToplevel()
        dialog.title("Aviso")
        dialog.geometry("300x100")
        
        label = ctk.CTkLabel(dialog, text=message)
        label.pack(pady=20)
        
        close_button = ctk.CTkButton(dialog, text="Fechar", command=dialog.destroy)
        close_button.pack(pady=10)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    task_manager = TaskManager()
    task_manager.run()
