#Proyecto eléctrico Evaluación de algoritmos de procesamiento de señales para validación de instrumentación biomédica
#Programa para pasar de Archivos .txt a archivos xlsx de excel para tener una mejor visualización de datos
#Mariano Segura Chaves C17416
#Kevin Aguilar Huertas B70131
import pandas as pd

def txt_to_excel(txt_filename):
    # Leer el archivo TXT
    data = pd.read_csv(txt_filename, sep='\t', engine='python')
    
    # Definir el nombre del archivo Excel
    excel_filename = txt_filename.replace('.txt', '.xlsx')
    
    # Guardar en Excel
    data.to_excel(excel_filename, index=False)
    
    print(f"Datos guardados en '{excel_filename}'")

# Ejemplo de uso
txt_to_excel('C:\\Users\\usuario\\Desktop\\UCR\\I-25\\Proyecto eléctrico\REPOSITORIO_CODES\\Proyecto-Electrico-Algoritmos-de-Evaluacion-de-se-ales-medicas\Audios 11a20\\VOZ 13%\\Voz13_waveform.txt')
