# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 11:38:58 2024

@author: KELLY
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

# Ruta de la carpeta de entrada y salida
input_folder = r"C:\Users\Admin\SHI S.A.S\2022047 Unal Ajustes Argos Río Claro - Técnica - Técnica\02_SIG\01_Hidrologia\06_XLSX\7-Consistencia\Oultliers\input"
output_folder = r"C:\Users\Admin\SHI S.A.S\2022047 Unal Ajustes Argos Río Claro - Técnica - Técnica\02_SIG\01_Hidrologia\06_XLSX\7-Consistencia\Oultliers\output"

# Definir la función con las carpetas de interes donde se realizaran los calculos
def analyze_excel_files(input_folder, output_folder):
    excel_files = [file for file in os.listdir(input_folder) if file.endswith('.xlsx')] # Archivos de excel en la carpeta de entrada
    
    # Procesar cada archivo de excel
    for file in excel_files:
        # Leer el archivo de excel
        file_path = os.path.join(input_folder, file)
        df = pd.read_excel(file_path)
        
        # Extraer las columnas de interés
        column_names = df.columns.values
        year = df.iloc[:, 0].values # Primera columna como dataframe
        data = df.iloc[:, 1].values # Segunda columna como dataframe
        
        # Calcular los límites con un 10% de significancia
        log_data = np.log(data) # Logaritmo natural a los datos
        n = len(log_data) # Longitud o tamaño del registro
        mean = np.mean(log_data) # Media del registro
        std_dev = np.std(log_data, ddof=1) # Desviación estandar del registro
        Kn = -3.62201 + (6.2844 * (n ** 0.25)) - (2.49835 * (n ** 0.5)) + (0.491436 * (n ** 0.75)) - (0.037911 * n)  # Grubbs-Beck
        upper_limit = np.exp(mean + Kn * std_dev)
        lower_limit = np.exp(mean - Kn * std_dev)
        
        # Calcular si cada punto es menor que el límite inferior o mayor que al límite superior
        below_lower_limit = data < lower_limit
        above_upper_limit = data > upper_limit
        
        # Guardar los outliers
        outlier_below = [(year[i], round(data[i], 1)) for i, val in enumerate(below_lower_limit) if val]
        outlier_above = [(year[i], round(data[i], 1)) for i, val in enumerate(above_upper_limit) if val]
        
        # Iterar sobre las filas del dataframe
        for i, row in df.iterrows():
            valor_actual = row['Precipitación (mm)']
                
            # Comparar si el valor actual es mayor al límite superior
            if valor_actual > upper_limit:
                df.at[i, 'Precipitación (mm)'] = 'Mayor'
            # Comparar si el valor actual es menor al límite inferior
            elif valor_actual < lower_limit:
                df.at[i, 'Precipitación (mm)'] = 'Menor'
        
        # Guardar el dataframe modificado en un archivo de excel
        df.to_excel(os.path.join(output_folder, f'modificado_{file}'), index=False)
        
        # Graficar los resultados
        plt.figure(figsize=(10, 8)) # Marco del gráfico
        #plt.plot(year, data) # une los puntos con una linea
        plt.scatter(year, data, color='blue', label=column_names[1]) # Agrega la dispersión de puntos, X, Y, color, título de los ejes
        plt.xticks(fontsize=14) # Tamaño de letra de las etiquetas del eje X
        plt.yticks(fontsize=14) # Tamaño de letra de las etiquetas del eje Y
                
        # Aplicar colores según la comparación
        outlier_for_label = []
        
        for outlier in outlier_below:
            plt.scatter(outlier[0], outlier[1], color='magenta')  # outlier [0] es coordenada X y [1] es coordenada Y
            outlier_for_label += [outlier[0], outlier[1]]
        
        for outlier in outlier_above:
            plt.scatter(outlier[0], outlier[1], color='magenta')  # outlier [0] es coordenada X y [1] es coordenada Y
            outlier_for_label += [outlier[0], outlier[1]]
            
        if len(outlier_for_label) > 0:
            plt.scatter([outlier_for_label[0]], [outlier_for_label[1]], color='magenta', label = 'Outlier')
      
        plt.axhline(y=upper_limit, color='red', linestyle='--', label='Límite Superior') # Grafica línea horizontal
        plt.axhline(y=lower_limit, color='green', linestyle='--', label='Límite Inferior') # Grafica línea horizontal
        
        filename = os.path.splitext(file)[0] # Obtener el nombre del archivo sin la extensión
        plt.xlabel('Año', fontsize=14)
        plt.ylabel(column_names[1], fontsize=14)
        plt.title(f'Prueba de Grubs-Beck para Outliers en {filename}', fontsize=16, fontweight='bold')
        #loc='left para alinear a la izquierda
        plt.legend()
        plt.grid(True)
        
        # Guardar la gráfica
        output_plot_path = os.path.join(output_folder, f'{os.path.splitext(file)[0]}_plot.png')
        plt.savefig(output_plot_path)
        plt.close()
        
        # Escribir los datos en un archivo de texto
        output_text_path = os.path.join(output_folder, f'{os.path.splitext(file)[0]}_data.txt')
        with open(output_text_path, 'w') as f:
            f.write(f'Valor mínimo: {min(data)}\n')
            f.write(f'Valor máximo: {max(data)}\n')
            f.write('El límite inferior es: ' + str(lower_limit) +'\n' )
            f.write('El límite superior es: ' + str(upper_limit) +'\n')
            f.write('Outlier: ' + str(outlier_below) +'\n')
            f.write('Outlier: ' + str(outlier_above))
        
        print(f'Análisis finalizado. Gráfica guardada en {output_plot_path}')

# Ejecutar análisis
analyze_excel_files(input_folder, output_folder)



