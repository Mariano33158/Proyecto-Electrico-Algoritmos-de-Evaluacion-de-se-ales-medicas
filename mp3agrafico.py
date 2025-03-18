#Proyecto eléctrico Evaluación de algoritmos de procesamiento de señales para validación de instrumentación biomédica
#Programa para pasar de MP3 a graficos de amplitud vs tiempo y para sacar los pares de datos ordenados en un archivo de texto
#Kevin Aguilar Huertas B70131
#Mariano Segura Chaves C17416

import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

def plot_audio_waveform(filename):
    # Cargar el audio con librosa
    data, sample_rate = librosa.load(filename, sr=None)
    
    # Calcular el tiempo
    duration = len(data) / sample_rate
    time = np.linspace(0., duration, len(data))
    
    # Guardar pares tiempo-amplitud en un archivo TXT
    txt_filename = filename.replace('.mp3', '_waveform.txt')
    with open(txt_filename, 'w') as f:
        f.write("Tiempo [s]\tAmplitud\n")
        for t, amp in zip(time, data):
            f.write(f"{t:.6f}\t{amp:.6f}\n")
    
    print(f"Datos guardados en '{txt_filename}'")
    
    # Graficar la forma de onda
    plt.figure(figsize=(10, 4))
    librosa.display.waveshow(data, sr=sample_rate, alpha=0.6)
    plt.xlabel('Tiempo [s]')
    plt.ylabel('Amplitud')
    plt.title('Forma de onda del audio')
    plt.grid(True)
    plt.show()

# Ejemplo de uso
plot_audio_waveform('School-La-Riviera.mp3')
