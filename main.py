# 1- uma tela com um botão de carregar vídeo
# Aqui será criada uma interface gráfica onde haverá um botão para o usuário carregar um vídeo de sua escolha.
import tkinter as tk
from tkinter import filedialog

def carregar_video():
    caminho_video = filedialog.askopenfilename(
        title="Selecione o vídeo",
        filetypes=[("Arquivos de vídeo", "*.mp4 *.avi *.mov *.mkv"), ("Todos os arquivos", "*.*")]
    )
    if caminho_video:
        print(f"Vídeo selecionado: {caminho_video}")

# Criação da janela principal
janela = tk.Tk()
janela.title("Carregar Vídeo")
janela.geometry("300x150")

# Botão para carregar vídeo
botao_carregar = tk.Button(janela, text="Carregar Vídeo", command=carregar_video)
botao_carregar.pack(expand=True)

janela.mainloop()