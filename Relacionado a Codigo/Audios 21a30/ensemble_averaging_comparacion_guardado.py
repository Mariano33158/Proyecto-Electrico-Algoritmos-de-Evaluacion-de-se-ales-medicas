
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pywt

# --- PARTE 1: Ensemble Averaging (Promedio de señales) ---

archivos = [
    r'C:\\Users\\usuario\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\\Audios 21a30\\VOZ 21%\\Voz 21_waveform.txt',
    r'C:\\Users\\usuario\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\\Audios 21a30\\VOZ 22%\\Voz22_waveform.txt',
    r'C:\\Users\\usuario\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\\Audios 21a30\\VOZ 23%\\Voz23_waveform.txt',
    r'C:\\Users\\usuario\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\\Audios 21a30\\VOZ 24%\\Voz24_waveform.txt',
    r'C:\\Users\\usuario\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\\Audios 21a30\\VOZ 25%\\Voz25_waveform.txt',
    r'C:\\Users\\usuario\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\\Audios 21a30\\VOZ 26%\\Voz26_waveform.txt',
    r'C:\\Users\\usuario\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\\Audios 21a30\\VOZ 27%\\Voz27_waveform.txt',
    r'C:\\Users\\usuario\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\\Audios 21a30\\VOZ 28%\\Voz28_waveform.txt',
    r'C:\\Users\\usuario\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\\Audios 21a30\\VOZ 29%\\Voz29_waveform.txt',
    r'C:\\Users\\usuario\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\\Audios 21a30\\VOZ 30%\\Voz30_waveform.txt'
]

# Leer archivos
datos_lista = [pd.read_csv(f, sep='\t', decimal='.') for f in archivos]

# Tiempo de referencia
tiempo_ref = min(datos_lista, key=len)['Tiempo [s]'].values

# Interpolación
interpoladas = [
    np.interp(tiempo_ref, df['Tiempo [s]'], df['Amplitud']) for df in datos_lista
]

# Promedio (ensemble averaging)
promedio_amplitud = np.mean(interpoladas, axis=0)

# Guardar resultado
resultado = pd.DataFrame({'Tiempo [s]': tiempo_ref, 'Amplitud': promedio_amplitud})
resultado.to_csv('resultado_promedio.txt', sep='\t', index=False)
resultado.to_excel('resultado_promedio.xlsx', index=False)
print("==> 'resultado_promedio.txt' y 'resultado_promedio.xlsx' guardados.")

# --- PARTE 2: Comparación de métodos de reducción de ruido ---

# Cargar resultado
data = pd.read_csv('resultado_promedio.txt', delimiter='\t')
data.columns = ['Tiempo', 'Amplitud']

# Parámetro de ventana
window_size = 10

# 1. Media Móvil
data['Media_Movil'] = data['Amplitud'].rolling(window=window_size, center=True).mean()

# 2. Filtro de Mediana
data['Mediana'] = data['Amplitud'].rolling(window=window_size, center=True).median()

# 3. Transformada Wavelet (DWT)
coeffs = pywt.wavedec(data['Amplitud'], 'db4', level=4)
coeffs[1:] = [pywt.threshold(c, np.std(c), mode='soft') for c in coeffs[1:]]
data['Wavelet'] = pywt.waverec(coeffs, 'db4')[:len(data)]

# --- PARTE 3: Guardar resultados ---

# Guardar cada método como .txt y .xlsx
data[['Tiempo', 'Media_Movil']].dropna().to_csv('resultado_media_movil.txt', sep='\t', index=False)
data[['Tiempo', 'Media_Movil']].dropna().to_excel('resultado_media_movil.xlsx', index=False)

data[['Tiempo', 'Mediana']].dropna().to_csv('resultado_mediana.txt', sep='\t', index=False)
data[['Tiempo', 'Mediana']].dropna().to_excel('resultado_mediana.xlsx', index=False)

data[['Tiempo', 'Wavelet']].to_csv('resultado_wavelet.txt', sep='\t', index=False)
data[['Tiempo', 'Wavelet']].to_excel('resultado_wavelet.xlsx', index=False)

print("==> Archivos filtrados (.txt y .xlsx) guardados correctamente.")

# --- PARTE 4: Graficar comparación de métodos ---

plt.figure(figsize=(12, 6))
plt.plot(data['Tiempo'], data['Amplitud'], label='Promedio (Ensemble Averaging)', linewidth=2)
plt.plot(data['Tiempo'], data['Media_Movil'], label='Media Móvil', linestyle='dashed')
plt.plot(data['Tiempo'], data['Mediana'], label='Mediana', linestyle='dotted')
plt.plot(data['Tiempo'], data['Wavelet'], label='Wavelet', linestyle='dashdot')

plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')
plt.title('Comparación de Métodos de Reducción de Ruido')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
