#Universidad de Costa Rica
#Escuela de Ingeniería Eléctrica
#Proyecto Eléctrico (IE0499)

#Evaluación de algoritmos de procesamiento de
#señales para validación de instrumentación
#biomédica

#Mariano Segura (C17416)
#Kevin Aguilar (B70131)

import numpy as np
import pandas as pd

# Lista con las rutas exactas de tus 10 archivos TXT
archivos = [
    r'C:\\Users\\usuario\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Audios 0a10\\VOZ 1%\\Voz 01_1_waveform.txt',
    r'C:\\Users\\usuario\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Audios 0a10\\VOZ 2%\\Voz 05_02_waveform.txt',
    r'C:\\Users\\usuario\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Audios 0a10\\VOZ 3%\\Voz 06_3_waveform.txt',
    r'C:\\Users\\usuario\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Audios 0a10\\VOZ 4%\\Voz 04_4_waveform.txt',
    r'C:\\Users\\usuario\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Audios 0a10\\VOZ 5%\\Voz 02_05_waveform.txt',
    r'C:\\Users\\usuario\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Audios 0a10\\VOZ 6%\\Voz 03_6_waveform.txt',
    r'C:\\Users\\usuario\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Audios 0a10\\VOZ 7%\\Voz 07_7_waveform.txt',
    r'C:\\Users\\usuario\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Audios 0a10\\VOZ 8%\\Voz 08_8_waveform.txt',
    r'C:\\Users\\usuario\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Audios 0a10\\VOZ 9%\\Voz 09_9_waveform.txt',
    r'C:\\Users\\usuario\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Audios 0a10\\VOZ 10%\\Voz 10_10_waveform.txt'
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