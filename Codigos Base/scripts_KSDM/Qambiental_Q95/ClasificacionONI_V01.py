#%%
# -*- coding: utf-8 -*-
"""
Created on Mon Dic 11 13:30:16 2023

@author: Admin
"""


import matplotlib.pyplot as plt
import pandas as pd
import os

#------------------------------------------- DATOS DE ENTRADA

# Carpeta donde se encuentran los archivos de entrada
path_files = r"C:\Users\KELLY\OneDrive - SHI S.A.S\01_Hidrologia\06_XLSX\5-Qambientales\Q95\ArchivosEntrada"

# Carpeta donde se almacenan los archivos de salida
path_save = r"C:\Users\KELLY\OneDrive - SHI S.A.S\01_Hidrologia\06_XLSX\5-Qambientales\Q95\ArchivosClasificados"

# Carpeta que contiene el ONI
path_ONI = r"C:\Users\KELLY\OneDrive - SHI S.A.S\01_Hidrologia\06_XLSX\5-Qambientales\Q95\ONI.xlsx"

#------------------------------------------- FIN DATOS DE ENTRADA

# Periodos consecutivos necesarios para considerar una temporada con anomalía (por definición 5)

# Analizar cada archivo

for archivo in os.listdir(path_files):
    
    # Leer datos ONI
    
    df_oni = pd.read_excel(path_ONI)
    df_oni = pd.melt(df_oni, id_vars=['Year'], var_name='Month', value_name='ONI')
    df_oni['FechaFiltro'] = pd.to_datetime(df_oni[['Year', 'Month']].assign(DAY=1))
    df_oni = df_oni[['FechaFiltro','ONI']]
    df_oni = df_oni.sort_values(by='FechaFiltro')
    df_oni = df_oni.reset_index()

    # Niño
    df_oni['niño'] = 1*(df_oni['ONI'] >= 0.5) + (df_oni['ONI'].shift(1) >= 0.5) + (df_oni['ONI'].shift(2) >= 0.5) + (df_oni['ONI'].shift(3) >= 0.5) + (df_oni['ONI'].shift(4) >= 0.5)
    df_oni['niño'] = (df_oni['niño'] >= 5)*1

    # Niña
    df_oni['niña'] = 1*(df_oni['ONI'] <= -0.5) + (df_oni['ONI'].shift(1) <= -0.5) + (df_oni['ONI'].shift(2) <= -0.5) + (df_oni['ONI'].shift(3) <= -0.5) + (df_oni['ONI'].shift(4) <= -0.5)
    df_oni['niña'] = (df_oni['niña'] >= 5)*1

    # Neutro
    df_oni['neutro'] = ((df_oni['niña'] + df_oni['niño']) < 1)*1

    #Leer archivos

    if 'xls' in archivo.split('.')[-1]:
        df = pd.read_excel(path_files + os.sep +archivo, sheet_name='Tanques', header=30, skiprows=[0])
        df = df[['Fecha', 'simulado']]
        df = df.dropna()
        df['FechaFiltro'] = pd.to_datetime(df['Fecha']).dt.to_period('M').dt.to_timestamp()
        df2 = pd.merge(df, df_oni, on='FechaFiltro', how='left')
        df2['Año'] = df2.Fecha.dt.year
        df2['Mes'] = df2.Fecha.dt.month

        nino = df2[df2['niño'] == 1].copy()
        nino = nino[['Fecha','Año','Mes','simulado','ONI']]
        nino.columns = ['Fecha','Año','Mes','Caudal (m3/s)','ONI']

        nina = df2[df2['niña'] == 1].copy()
        nina = nina[['Fecha','Año','Mes','simulado','ONI']]
        nina.columns = ['Fecha','Año','Mes','Caudal (m3/s)','ONI']

        neutro = df2[df2['neutro'] == 1].copy()
        neutro = neutro[['Fecha','Año','Mes','simulado','ONI']]
        neutro.columns = ['Fecha','Año','Mes','Caudal (m3/s)','ONI']

        #Archivo salida
        archivo_excel = path_save + os.sep + 'resultados_' + "".join(archivo.split('.')[:-1]) + '.xlsx'

        # Crear un escritor de Excel
        with pd.ExcelWriter(archivo_excel, engine='xlsxwriter') as writer:
            # Exportar cada DataFrame a una pestaña diferente
            nino.to_excel(writer, sheet_name='Calido', index=False)
            nina.to_excel(writer, sheet_name='Humedo', index=False)
            neutro.to_excel(writer, sheet_name='Normal', index=False)

    
#%%
