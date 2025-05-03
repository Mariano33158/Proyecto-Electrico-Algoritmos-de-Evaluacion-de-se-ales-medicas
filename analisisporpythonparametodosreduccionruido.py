import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
import pywt

# Cargar los datos del archivo
file_path = "C:/Users/maria/Proyecto Electrico DUMA/Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas/School-La-Riviera_waveform.txt"
data = pd.read_csv(file_path, delimiter="\t")

# Renombrar columnas si es necesario
data.columns = ["Tiempo", "Amplitud"]

# Filtrar datos que sean realmente significativos (excluir valores nulos o constantes)
data = data[data["Amplitud"] != 0]

# Aplicar métodos de reducción de ruido

# 1. Media Móvil
window_size = 10  # Tamaño de la ventana
data["Media_Movil"] = data["Amplitud"].rolling(window=window_size, center=True).mean()

# 2. Filtro de Mediana
data["Mediana"] = data["Amplitud"].rolling(window=window_size, center=True).median()

# 3. Transformada Wavelet (DWT)
coeffs = pywt.wavedec(data["Amplitud"], 'db4', level=4)
coeffs[1:] = [pywt.threshold(c, np.std(c), mode='soft') for c in coeffs[1:]]  # Umbralización
data["Wavelet"] = pywt.waverec(coeffs, 'db4')[:len(data)]  # Ajustar tamaño si es necesario

# Graficar la señal y los métodos filtrados
fig, ax = plt.subplots(figsize=(12, 6))
plt.subplots_adjust(left=0.2)

lines = {
    "Original": ax.plot(data["Tiempo"], data["Amplitud"], label="Original", alpha=0.5)[0],
    "Media Móvil": ax.plot(data["Tiempo"], data["Media_Movil"], label="Media Móvil", linestyle="dashed")[0],
    "Mediana": ax.plot(data["Tiempo"], data["Mediana"], label="Mediana", linestyle="dotted")[0],
    "Wavelet": ax.plot(data["Tiempo"], data["Wavelet"], label="Wavelet", linestyle="dashdot")[0]
}

plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud")
plt.title("Comparación de Métodos de Reducción de Ruido")
plt.grid()
plt.legend()

# Crear CheckButtons
rax = plt.axes([0.02, 0.4, 0.15, 0.2])
check = CheckButtons(rax, list(lines.keys()), [True, True, True, True])

def func(label):
    line = lines[label]
    line.set_visible(not line.get_visible())
    plt.draw()

check.on_clicked(func)
plt.show()
