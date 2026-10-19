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

import os
import tempfile
import threading
import moviepy.editor as mp
import speech_recognition as sr

def extrair_audio_e_transcrever(caminho_video):
    try:
        # Extrair áudio do vídeo usando moviepy
        video = mp.VideoFileClip(caminho_video)
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_audio_file:
            tmp_audio_path = tmp_audio_file.name
        video.audio.write_audiofile(tmp_audio_path, codec='pcm_s16le')
        
        # Transcrever áudio usando speech_recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(tmp_audio_path) as source:
            audio = recognizer.record(source)

        try:
            texto = recognizer.recognize_google(audio, language="pt-BR")
        except sr.UnknownValueError:
            texto = "Não foi possível transcrever o áudio."
        except sr.RequestError:
            texto = "Erro no serviço de reconhecimento de fala."

        # Salvar a transcrição em um arquivo .txt
        pasta, nome_arquivo = os.path.split(caminho_video)
        nome_base, _ = os.path.splitext(nome_arquivo)
        caminho_txt = os.path.join(pasta, f"{nome_base}_transcricao.txt")
        with open(caminho_txt, "w", encoding="utf-8") as f:
            f.write(texto)
        print(f"Transcrição salva em: {caminho_txt}")
        os.remove(tmp_audio_path)
    except Exception as e:
        print(f"Erro ao processar vídeo: {e}")

def carregar_video():
    caminho_video = filedialog.askopenfilename(
        title="Selecione o vídeo",
        filetypes=[("Arquivos de vídeo", "*.mp4 *.avi *.mov *.mkv"), ("Todos os arquivos", "*.*")]
    )
    if caminho_video:
        print(f"Vídeo selecionado: {caminho_video}")
        threading.Thread(target=extrair_audio_e_transcrever, args=(caminho_video,)).start()

# Adiciona um rótulo de status para mostrar o temporizador
label_status = tk.Label(janela, text="")
label_status.pack(expand=True)

transcrevendo = False
contador_segundos = 0
temporizador_id = None

def atualizar_temporizador():
    global contador_segundos, temporizador_id, transcrevendo
    if transcrevendo:
        minutos = contador_segundos // 60
        segundos = contador_segundos % 60
        label_status.config(text=f"Transcrevendo... Tempo: {minutos:02d}:{segundos:02d}")
        contador_segundos += 1
        temporizador_id = janela.after(1000, atualizar_temporizador)
    else:
        label_status.config(text="Transcrição finalizada!")

def extrair_audio_e_transcrever_com_status(caminho_video):
    global transcrevendo, temporizador_id, contador_segundos
    try:
        extrair_audio_e_transcrever(caminho_video)
    finally:
        transcrevendo = False
        if temporizador_id:
            janela.after_cancel(temporizador_id)
        label_status.config(text="Transcrição finalizada!")

def carregar_video():
    global transcrevendo, contador_segundos, temporizador_id
    caminho_video = filedialog.askopenfilename(
        title="Selecione o vídeo",
        filetypes=[("Arquivos de vídeo", "*.mp4 *.avi *.mov *.mkv"), ("Todos os arquivos", "*.*")]
    )
    if caminho_video:
        print(f"Vídeo selecionado: {caminho_video}")
        transcrevendo = True
        contador_segundos = 0
        label_status.config(text="Transcrevendo... Tempo: 00:00")
        atualizar_temporizador()
        threading.Thread(target=extrair_audio_e_transcrever_com_status, args=(caminho_video,), daemon=True).start()

botao_carregar.config(command=carregar_video)



janela.mainloop()