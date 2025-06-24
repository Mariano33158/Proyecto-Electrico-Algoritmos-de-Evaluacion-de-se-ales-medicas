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
    r'C:\\Users\\usuario\\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\\Audios 11a20\\VOZ 11%\\Voz11_waveform.txt',
    r'C:\\Users\\usuario\\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\\Audios 11a20\\VOZ 12%\\Voz12_waveform.txt',
    r'C:\\Users\\usuario\\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\\Audios 11a20\\VOZ 13%\\Voz13_waveform.txt',
    r'C:\\Users\\usuario\\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\\Audios 11a20\\VOZ 14%\\Voz14_waveform.txt',
    r'C:\\Users\\usuario\\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\\Audios 11a20\\VOZ 15%\\Voz 15_waveform.txt',
    r'C:\\Users\\usuario\\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\\Audios 11a20\\VOZ 16%\\Voz16_waveform.txt',
    r'C:\\Users\\usuario\\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\\Audios 11a20\\VOZ 17%\\Voz17_waveform.txt',
    r'C:\\Users\\usuario\\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\\Audios 11a20\\VOZ 18%\\Voz18_waveform.txt',
    r'C:\\Users\\usuario\\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\\Audios 11a20\\VOZ 19%\\Voz19_waveform.txt',
    r'C:\\Users\\usuario\\Desktop\\UCR\\I-25\\Proyecto eléctrico\\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\\Audios 11a20\\VOZ 20%\\Voz20_waveform.txt'
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