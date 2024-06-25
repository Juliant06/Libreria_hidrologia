# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 16:07:34 2024

@author: KELLY
"""
import os
import pandas as pd
from scipy.stats import kendalltau

# Ruta carpeta de entrada y salida "/"
carpeta_entrada = r"C:\Users\Admin\SHI S.A.S\2022047 Unal Ajustes Argos Río Claro - Técnica - Técnica\02_SIG\01_Hidrologia\06_XLSX\7-Consistencia\Tendencia\input"
carpeta_salida = r"C:\Users\Admin\SHI S.A.S\2022047 Unal Ajustes Argos Río Claro - Técnica - Técnica\02_SIG\01_Hidrologia\06_XLSX\7-Consistencia\Tendencia\output"

# Función para realizar la prueba de tendencia de Mann-Kendall para los archivos de excel una carpeta
def prueba_mann_kendall(carpeta_entrada, carpeta_salida):
        
    # Obtener la lista de archivos en la carpeta de entrada
    archivos_excel = [archivo for archivo in os.listdir(carpeta_entrada) if archivo.endswith('.xlsx')]
    
    # Iterar sobre cada archivo
    for archivo in archivos_excel:
        # Leer el archivo Excel
        ruta_archivo_entrada = os.path.join(carpeta_entrada, archivo)
        datos_excel = pd.read_excel(ruta_archivo_entrada)
        
        # Cada archivo tiene dos columnas como Tiempo y Panual
        tiempo = datos_excel["Tiempo"]
        datos = datos_excel["Precipitación (mm)"]
        
        # Realizar la prueba de tendencia de Mann-Kendall
        estadistico, p_valor = kendalltau(tiempo, datos)
        
        # Guardar los resultados en un archivo de texto en la carpeta de salida
        nombre_archivo_salida = os.path.splitext(archivo)[0] + "_resultado.txt"
        ruta_archivo_salida = os.path.join(carpeta_salida, nombre_archivo_salida)
        
        with open(ruta_archivo_salida, "w") as f:
            f.write(f"Resultados de la prueba de tendencia de Mann-Kendall para {archivo}:\n")
            #f.write("Estadístico de la prueba: {}\n".format(estadistico))
            f.write("Estadístico |Z|: {}\n".format(p_valor))
            f.write("Significancia: 0.05\n")
            f.write("\n")
            f.write("Interpretación del estadístico |Z|:\n")
            alpha = 0.05
            if p_valor > alpha:
                f.write("No se puede rechazar la hipótesis nula. No hay tendencia significativa.\n")
            else:
                f.write("Se rechaza la hipótesis nula. Hay tendencia significativa.\n")
        
        print(f"Resultados almacenados en: {ruta_archivo_salida}")

# Llamar a la función para realizar la prueba de Mann-Kendall y almacenar los resultados
prueba_mann_kendall(carpeta_entrada, carpeta_salida)



