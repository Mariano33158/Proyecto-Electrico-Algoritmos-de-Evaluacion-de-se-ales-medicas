import numpy as np
import pandas as pd

# Lista con las rutas exactas de tus 10 archivos TXT
archivos = [
    r'C:\Users\maria\Proyecto Electrico DUMA\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Audios 51a60\VOZ 51%\Voz51_waveform.txt',
    r'C:\Users\maria\Proyecto Electrico DUMA\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Audios 51a60\VOZ 52%\Voz52_waveform.txt',
    r'C:\Users\maria\Proyecto Electrico DUMA\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Audios 51a60\VOZ 53%\Voz53_waveform.txt',
    r'C:\Users\maria\Proyecto Electrico DUMA\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Audios 51a60\VOZ 54%\Voz54_waveform.txt',
    r'C:\Users\maria\Proyecto Electrico DUMA\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Audios 51a60\VOZ 55%\Voz55_waveform.txt',
    r'C:\Users\maria\Proyecto Electrico DUMA\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Audios 51a60\VOZ 56%\Voz56_waveform.txt',
    r'C:\Users\maria\Proyecto Electrico DUMA\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Audios 51a60\VOZ 57%\Voz57_waveform.txt',
    r'C:\Users\maria\Proyecto Electrico DUMA\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Audios 51a60\VOZ 58%\Voz58_waveform.txt',
    r'C:\Users\maria\Proyecto Electrico DUMA\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Audios 51a60\VOZ 59%\Voz59_waveform.txt',
    r'C:\Users\maria\Proyecto Electrico DUMA\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Audios 51a60\VOZ 60%\Voz60_waveform.txt'
]

# Leer todos los archivos y almacenar sus datos en una lista
datos_lista = []
for archivo in archivos:
    datos = pd.read_csv(archivo, sep='\t', decimal='.', header=0)
    datos_lista.append(datos)

# Encontrar el archivo con menos datos para usar como referencia
archivo_referencia = min(datos_lista, key=lambda x: len(x))
tiempo_referencia = archivo_referencia['Tiempo [s]'].values

# Interpolar amplitudes usando el tiempo del archivo más pequeño como referencia
amplitudes_interpoladas = []
for datos in datos_lista:
    amplitud_interp = np.interp(tiempo_referencia, datos['Tiempo [s]'], datos['Amplitud'])
    amplitudes_interpoladas.append(amplitud_interp)

# Calcular el promedio de amplitudes interpoladas
promedio_amplitud = np.mean(amplitudes_interpoladas, axis=0)

# Crear DataFrame con promedio interpolado
resultado_promedio = pd.DataFrame({
    'Tiempo [s]': tiempo_referencia,
    'Amplitud': promedio_amplitud
})

# Guardar resultado en un nuevo archivo TXT
resultado_promedio.to_csv('resultado_promedio.txt', sep='\t', index=False, float_format='%.6f')

print("Archivo resultado_promedio.txt creado exitosamente.")