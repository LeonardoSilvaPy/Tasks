import matplotlib.pyplot as plt
import customtkinter as ctk

def show_task_graph(tasks, colors):
    graph_window = ctk.CTkToplevel()  # Cria uma nova janela
    graph_window.title("Gráficos de Tarefas")
    graph_window.attributes('-fullscreen', True)  # Define para abrir em tela cheia
    
    # Contagem das tarefas por categoria
    task_count = {
        "urgent": sum(1 for task in tasks if task["priority"] == "urgent"),
        "redo": sum(1 for task in tasks if task["priority"] == "redo"),
        "pending": sum(1 for task in tasks if task["status"] == "pending" and task["priority"] not in ["urgent", "redo"]),
        "completed": sum(1 for task in tasks if task["status"] == "completed")
    }

    # Remover categorias vazias
    task_count = {k: v for k, v in task_count.items() if v > 0}

    labels = list(task_count.keys())
    sizes = list(task_count.values())
    color_values = [colors[label] for label in labels]
    
    # Função para exibir a quantidade e a porcentagem
    def autopct_func(pct):
        total = sum(sizes)
        count = int(round(pct * total / 100.0))
        return f'{pct:.1f}% ({count})'
    
    fig, ax = plt.subplots()
    # Ajustar wedgeprops para adicionar espaçamento maior
    wedgeprops = {'edgecolor': 'white', 'linewidth': 3}  # Aumente o linewidth para dobrar o espaçamento
    ax.pie(sizes, labels=labels, colors=color_values, autopct=autopct_func, startangle=90, wedgeprops=wedgeprops)
    
    plt.show()
