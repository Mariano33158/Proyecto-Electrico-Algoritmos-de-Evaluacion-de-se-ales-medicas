import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert

# 1. Ruta al archivo 
file_path = r'C:\Users\maria\Proyecto Electrico DUMA\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Envolventes\Voz50_waveform.txt'

# 2. Cargar datos, saltando la primera fila de encabezado
data = np.loadtxt(file_path, skiprows=1)  

t = data[:, 0]   # tiempo en segundos
x = data[:, 1]   # amplitud

# 3. Calcular envolvente con la transformada de Hilbert
analytic_signal = hilbert(x)
envelope = np.abs(analytic_signal)

# 4. Calcular valor pico y área antes de graficar
peak_value = envelope.max()
area = np.trapz(envelope, t)

# 5. Graficar señal y envolvente
plt.figure(figsize=(10, 5))
plt.plot(t, x, label='Señal original')
plt.plot(t, envelope, 'r', lw=2, label='Envolvente')

# 6. Añadir texto con pico y área en la esquina superior derecha
textstr = f'Valor pico: {peak_value:.4f}\nÁrea bajo envolvente: {area:.4f}'
plt.gca().text(
    0.95, 0.95, textstr,
    transform=plt.gca().transAxes,
    verticalalignment='top',
    horizontalalignment='right',
    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
)

plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.title('Señal y su envolvente con métricas')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
