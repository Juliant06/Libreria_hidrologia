# -*- coding: utf-8 -*-
"""
Created on Wed Dec 28 17:08:38 2022

@author: KELLY S DULCE MONCAYO

"""

import matplotlib.pyplot as plt
import pandas as pd        
import numpy as np
import openpyxl
import os

# ---------------------------------------------------------MODIFICAR
carpeta_entrada = r"C:\Users\Admin\SHI S.A.S\2022047 Unal Ajustes Argos Río Claro - Técnica - Técnica\02_SIG\01_Hidrologia\06_XLSX\7-Consistencia\Boxplot\input"
carpeta_salida = r"C:\Users\Admin\SHI S.A.S\2022047 Unal Ajustes Argos Río Claro - Técnica - Técnica\02_SIG\01_Hidrologia\06_XLSX\7-Consistencia\Boxplot\output"
# -----------------------------------------------------FIN MODIFICAR

# ------------------------------------------------------------BOXPLOT
for file in os.listdir(carpeta_entrada):
    
    if 'xls' in file.split('.')[-1]:
        
        # Lectura de las dos hojas de excel
        archivo = carpeta_entrada + os.sep + file
        df_diario = pd.DataFrame(pd.read_excel(archivo, sheet_name='diario', header=0))
        df_mensual = pd.DataFrame(pd.read_excel(archivo, sheet_name='mensual', header=0))
        #print(df_diario)
        #print(df_mensual)
       
       # BOXPLOT DIARIO
        nombre_archivo, _ = os.path.splitext(os.path.basename(archivo)) # Extraer el nombre del archivo  
        df_diario.boxplot(whis=5.0, figsize=(7,7)) # whis 5 hace que los bigotes sean alargados
        plt.title (nombre_archivo, fontsize=25)
        plt.ylabel('Caudal (m$^3$/s)', fontsize=15) # Tamaño y nombre del eje Y 
        plt.xlabel(' ', fontsize=15) # Tamaño y nombre del eje X  
        plt.xticks(fontsize=15) # Tamaño de la letra del eje X
        plt.yticks(fontsize=15) # Tamaño de la letra del eje Y
               
        
        # Guardar la figura en formato JPG en la carpeta de salida
        ruta_jpg_diario = os.path.join(carpeta_salida, f'{nombre_archivo}_diario.jpg')
        plt.savefig(ruta_jpg_diario, bbox_inches='tight')
       
        plt.show() # Mostrar la figura
        describe_diario = df_diario.describe()
        
        # Concatenar los resultados de describe() en un solo DataFrame
        resultados_describe = pd.concat([describe_diario], axis=1)
        ruta_excel = os.path.join(carpeta_salida, f'{nombre_archivo}_describe.xlsx')
        resultados_describe.to_excel(ruta_excel)
  
        # BOXPLOT MENSUAL
        Q = pd.pivot_table(df_mensual, values='Caudal', index='fecha', columns='mes') # Se obtiene un Dataframe con 12 columnas que corresponde a cada mes
        ax=Q.boxplot(showmeans=True,figsize=(10,7))
        plt.title(nombre_archivo, fontsize=25)
        plt.ylabel('Caudal(m$^3$/s)', fontsize=15)    
        plt.xlabel(' ')
        plt.xticks(np.arange(13),('','Ene.', 'Feb.', 'Mar.', 'Abr.', 'May.','Jun.','Jul.','Agos.','Sep.','Oct.','Nov.','Dic.'))
        plt.xticks(fontsize=15) # Tamaño de la letra del eje X
        plt.yticks(fontsize=15) # Tamaño de la letra del eje Y
        
       # Obtener colores automáticamente usados en el gráfico
        colores = [line.get_color() for line in ax.lines]
        markers = [line.get_marker() for line in ax.lines]
        
       # Agregar leyenda con los colores correctos
        plt.legend(handles=[plt.Line2D([0], [0], color=colores[0], linestyle='-', linewidth=2, label='Mediana', markersize=10),
                           plt.Line2D([0], [0], color='green', linestyle='None', marker='^', markersize=10, label='Media'),
                           plt.Line2D([0], [0], color=colores[3], linestyle='None', marker='o', markersize=10, markerfacecolor='none', label='Atípico')],
                  loc='upper right', handlelength=4)
       # markerfacecolor = 'none' hace que el relleno sea transparente
       
       # Guardar la figura en formato JPG en la carpeta de salida
        ruta_jpg_mensual = os.path.join(carpeta_salida, f'{nombre_archivo}_mensual.jpg')
        plt.savefig(ruta_jpg_mensual, bbox_inches='tight')
        plt.show() # Mostrar la figura   
        
# Mostrar todas las figuras al final del bucle
plt.show()        











