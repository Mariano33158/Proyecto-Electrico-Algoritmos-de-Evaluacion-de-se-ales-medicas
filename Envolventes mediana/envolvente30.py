import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import hilbert, medfilt

# 1. Ruta al archivo (ajusta a tu ruta real)
file_path = r'C:\Users\maria\Proyecto Electrico DUMA\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Envolventes\Voz30_waveform.txt'

# 2. Cargar datos, saltando la primera fila de encabezado
data = np.loadtxt(file_path, skiprows=1)
t = data[:, 0]
x = data[:, 1]

# 3. Filtrado de mediana para reducción de ruido
window_size = 11             # debe ser impar; ajusta según necesites
x_smooth = medfilt(x, window_size)

# 4. Cálculo de la envolvente sobre la señal filtrada por mediana
analytic_signal = hilbert(x_smooth)
envelope = np.abs(analytic_signal)

# 5. Calcular métricas de la envolvente
peak_value = envelope.max()
area = np.trapz(envelope, t)

# 6. Graficar señal suavizada (mediana) y su envolvente
plt.figure(figsize=(10, 5))
plt.plot(t, x_smooth,      label='Señal suavizada (mediana)', alpha=0.8)
plt.plot(t, envelope, 'r', lw=2, label='Envolvente')

# 7. Anotar pico y área en la gráfica
textstr = f'Valor pico: {peak_value:.4f}\nÁrea envolvente: {area:.4f}'
plt.gca().text(
    0.95, 0.95, textstr,
    transform=plt.gca().transAxes,
    verticalalignment='top',
    horizontalalignment='right',
    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
)

plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.title('Señal filtrada por mediana y su envolvente con métricas')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()