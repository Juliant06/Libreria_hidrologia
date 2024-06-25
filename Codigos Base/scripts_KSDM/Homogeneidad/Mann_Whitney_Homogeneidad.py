# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 15:23:47 2024

@author: KELLY
"""
import os
import pandas as pd
from scipy.stats import mannwhitneyu

# Ruta carpeta de entrada y salida
carpeta_entrada = r"C:\Users\Admin\SHI S.A.S\2022047 Unal Ajustes Argos Río Claro - Técnica - Técnica\02_SIG\01_Hidrologia\06_XLSX\7-Consistencia\Homogeneidad\input"
carpeta_salida = r"C:\Users\Admin\SHI S.A.S\2022047 Unal Ajustes Argos Río Claro - Técnica - Técnica\02_SIG\01_Hidrologia\06_XLSX\7-Consistencia\Homogeneidad\output"

# Función para realizar la prueba de Mann-Whitney para los archivos en una carpeta
def prueba_mann_whitney(carpeta_entrada, carpeta_salida):
    # Obtener la lista de archivos en la carpeta de entrada
    archivos_excel = [archivo for archivo in os.listdir(carpeta_entrada) if archivo.endswith('.xlsx')]
    
    # Iterar sobre cada archivo
    for archivo in archivos_excel:
        # Leer el archivo Excel
        ruta_archivo_entrada = os.path.join(carpeta_entrada, archivo)
        datos_excel = pd.read_excel(ruta_archivo_entrada)
        datos_sin_nan = datos_excel.dropna()
        
        # Supongamos que tienes dos columnas en tu archivo Excel llamadas "grupo1" y "grupo2"
        grupo1 = datos_sin_nan["grupo1"]
        grupo2 = datos_sin_nan["grupo2"]
         
        
        # Realizar la prueba de Mann-Whitney
        estadistico, p_valor = mannwhitneyu(grupo1, grupo2)
        
        # Guardar los resultados en un archivo de texto en la carpeta de salida
        nombre_archivo_salida = os.path.splitext(archivo)[0] + "_resultado.txt"
        ruta_archivo_salida = os.path.join(carpeta_salida, nombre_archivo_salida)
        
        with open(ruta_archivo_salida, "w") as f:
            f.write(f"Resultados de la prueba de Mann-Whitney para {archivo}:\n")
            #f.write("Estadístico de la prueba: {}\n".format(estadistico))
            f.write("Estadístico U: {}\n".format(p_valor))
            f.write("Significancia: 0,05 \n")
            f.write("\n")
            f.write("Interpretación del estadístico U:\n")
            alpha = 0.05
            if p_valor > alpha:
                f.write("No se puede rechazar la hipótesis nula. Los grupos son homogéneos.\n")
            else:
                f.write("Se rechaza la hipótesis nula. Los grupos no son homogéneos.\n")
        
        print(f"Resultados almacenados en: {ruta_archivo_salida}")

# Rutas de la carpeta de entrada y de la carpeta de salida
#carpeta_entrada = "ruta/a/tu/carpeta_entrada"  # Ruta a tu carpeta de entrada
#carpeta_salida = "ruta/a/tu/carpeta_salida"  # Ruta a tu carpeta de salida

# Llamar a la función para realizar la prueba de Mann-Whitney y almacenar los resultados
prueba_mann_whitney(carpeta_entrada, carpeta_salida)


