
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import CheckButtons
import pywt

# ————————————————
# 1. Definir rutas de los dos archivos de texto
# ————————————————
file_path1 = 'C:\\Users\\maria\\Proyecto Electrico DUMA\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\\Audios 21a30\\VOZ 30%\\Voz30_waveform.txt'
file_path2 = 'C:\\Users\\maria\\Proyecto Electrico DUMA\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\\Audios 51a60\\VOZ 60%\\Voz60_waveform.txt'

# ————————————————
# 2. Cargar ambos archivos como sin encabezado y asignar nombres
# ————————————————
# header=None -> leer todo como datos. Luego names= define columnas manualmente.
data1 = pd.read_csv(
    file_path1,
    delimiter="\t",
    header=None,
    names=["Tiempo", "Amplitud"],
    dtype=str,
    low_memory=False
)
data2 = pd.read_csv(
    file_path2,
    delimiter="\t",
    header=None,
    names=["Tiempo", "Amplitud"],
    dtype=str,
    low_memory=False
)

# ————————————————
# 3. Convertir columnas a numérico y eliminar filas inválidas
# ————————————————
for df in (data1, data2):
    # Intentar convertir a número, los errores pasan a NaN
    df["Tiempo"] = pd.to_numeric(df["Tiempo"], errors="coerce")
    df["Amplitud"] = pd.to_numeric(df["Amplitud"], errors="coerce")
    # Eliminar cualquier fila que tenga NaN en Tiempo o Amplitud
    df.dropna(subset=["Tiempo", "Amplitud"], inplace=True)

# ————————————————
# 4. Filtrar valores no significativos (Amplitud == 0)
# ————————————————
data1 = data1[data1["Amplitud"] != 0]
data2 = data2[data2["Amplitud"] != 0]

# ————————————————
# 5. Aplicar métodos de reducción de ruido (Media Móvil, Mediana, Wavelet)
# ————————————————
window_size = 10  # Ajusta según tu caso

# 5.1. Media Móvil
data1["Media_Movil"] = data1["Amplitud"].rolling(window=window_size, center=True).mean()
data2["Media_Movil"] = data2["Amplitud"].rolling(window=window_size, center=True).mean()

# 5.2. Filtro de Mediana
data1["Mediana"] = data1["Amplitud"].rolling(window=window_size, center=True).median()
data2["Mediana"] = data2["Amplitud"].rolling(window=window_size, center=True).median()

# 5.3. Transformada Wavelet Discreta (DWT) con umbral suave
# Señal 1
coeffs1 = pywt.wavedec(data1["Amplitud"], 'db4', level=4)
coeffs1[1:] = [pywt.threshold(c, np.std(c), mode='soft') for c in coeffs1[1:]]
wavelet_rec1 = pywt.waverec(coeffs1, 'db4')
data1["Wavelet"] = wavelet_rec1[: len(data1)]

# Señal 2
coeffs2 = pywt.wavedec(data2["Amplitud"], 'db4', level=4)
coeffs2[1:] = [pywt.threshold(c, np.std(c), mode='soft') for c in coeffs2[1:]]
wavelet_rec2 = pywt.waverec(coeffs2, 'db4')
data2["Wavelet"] = wavelet_rec2[: len(data2)]

# ————————————————
# 6. Graficar ambas señales con todos los métodos y CheckButtons
# ————————————————
fig, ax = plt.subplots(figsize=(12, 6))
plt.subplots_adjust(left=0.30)  # Espacio a la izquierda para CheckButtons

lines = {
    # Señal 1
    "Orig. Señal 1": ax.plot(
        data1["Tiempo"], data1["Amplitud"], label="Señal 1 (Original)", alpha=0.5
    )[0],
    "Media Móvil 1": ax.plot(
        data1["Tiempo"], data1["Media_Movil"], label="Señal 1 (Media Móvil)", linestyle="--"
    )[0],
    "Mediana 1": ax.plot(
        data1["Tiempo"], data1["Mediana"], label="Señal 1 (Mediana)", linestyle=":"
    )[0],
    "Wavelet 1": ax.plot(
        data1["Tiempo"], data1["Wavelet"], label="Señal 1 (Wavelet)", linestyle="-."
    )[0],

    # Señal 2
    "Orig. Señal 2": ax.plot(
        data2["Tiempo"], data2["Amplitud"], label="Señal 2 (Original)", alpha=0.5
    )[0],
    "Media Móvil 2": ax.plot(
        data2["Tiempo"], data2["Media_Movil"], label="Señal 2 (Media Móvil)", linestyle="--"
    )[0],
    "Mediana 2": ax.plot(
        data2["Tiempo"], data2["Mediana"], label="Señal 2 (Mediana)", linestyle=":"
    )[0],
    "Wavelet 2": ax.plot(
        data2["Tiempo"], data2["Wavelet"], label="Señal 2 (Wavelet)", linestyle="-."
    )[0],
}

ax.set_xlabel("Tiempo [s]")
ax.set_ylabel("Amplitud")
ax.set_title("Comparación de Dos Señales con Varios Métodos de Reducción de Ruido")
ax.grid(True)
ax.legend(loc="upper right", fontsize="small")

# CheckButtons para alternar visibilidad
rax = plt.axes([0.02, 0.25, 0.25, 0.50])
labels = list(lines.keys())
visibility = [True] * len(labels)
check = CheckButtons(rax, labels, visibility)

def toggle_visibility(label):
    line = lines[label]
    line.set_visible(not line.get_visible())
    plt.draw()

check.on_clicked(toggle_visibility)

plt.show()