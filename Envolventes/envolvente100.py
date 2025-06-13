import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import hilbert
from scipy.ndimage import maximum_filter1d
# 1. Ruta al archivo (ajusta a tu ruta real)
file_path = r'C:\Users\maria\Proyecto Electrico DUMA\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Envolventes\Voz100_waveform.txt'

data = np.loadtxt(file_path, skiprows=1)
t, x = data[:,0], data[:,1]

# 2. Envolvente cruda
env_raw = np.abs(hilbert(x))

# 3. Envelope morfológico (máximo sobre ventana deslizante)
fs = 1/np.mean(np.diff(t))           # frecuencia de muestreo
window_ms     = 50                   # ventana en milisegundos
window_samps  = max(1, int(window_ms*fs/1000))
env_morph     = maximum_filter1d(env_raw, size=window_samps)

# 4. (Opcional) ligero suavizado para eliminar escalones
from scipy.signal import savgol_filter
env_morph_sg = savgol_filter(env_morph, window_length=window_samps//2*2+1, polyorder=2)

# 5. Métricas
peak = env_morph_sg.max()
area = np.trapz(env_morph_sg, t)

# 6. Gráfica comparativa
plt.figure(figsize=(10,5))
plt.plot(t, x,        color='C0', alpha=0.4, label='Señal original')
plt.plot(t, env_raw,  color='C1', lw=1,   alpha=0.6, label='Envolvente cruda')
plt.plot(t, env_morph_sg, 'r', lw=2,         label='Envelope morfológico')

# Anotación
txt = f'Pico: {peak:.4f}\nÁrea: {area:.4f}'
plt.gca().text(0.95,0.95, txt,
               transform=plt.gca().transAxes,
               ha='right', va='top',
               bbox=dict(facecolor='white', alpha=0.8))

plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.title('Señal y envolvente morfológica (más fiel a picos)')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()