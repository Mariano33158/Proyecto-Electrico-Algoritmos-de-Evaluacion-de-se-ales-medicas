import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert, medfilt
import pywt
# 1. Ruta al archivo (ajusta a tu ruta real)
file_path = r'C:\Users\maria\Proyecto Electrico DUMA\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Envolventes\Voz40_waveform.txt'

# 2. Cargar datos, saltando la primera fila de encabezado
data = np.loadtxt(file_path, skiprows=1)
t = data[:, 0]
x = data[:, 1]

# 3. Reducción de ruido con DWT + umbral suave
wavelet = 'db4'
level   = 4
# Descomposición
coeffs = pywt.wavedec(x, wavelet, level=level)
# Umbral suave en cada detalle (excepto coeficiente de aproximación)
coeffs[1:] = [pywt.threshold(c, np.std(c), mode='soft') for c in coeffs[1:]]
# Reconstrucción
x_smooth = pywt.waverec(coeffs, wavelet)
# Aseguramos que la longitud sea la misma que la señal original
x_smooth = x_smooth[:len(x)]

# 4. Cálculo de la envolvente sobre la señal filtrada
analytic_signal = hilbert(x_smooth)
envelope = np.abs(analytic_signal)

# 5. Métricas de la envolvente
peak_value = envelope.max()
area       = np.trapz(envelope, t)

# 6. Graficar señal filtrada y su envolvente
plt.figure(figsize=(10, 5))
plt.plot(t, x_smooth,      label='Señal DWT-suavizada', alpha=0.8)
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
plt.title('Señal DWT-suavizada y su envolvente con métricas')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()