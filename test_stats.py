# Test estadisticos para revisar
# cambios en la media, outliers, tendencias y homogeneidad
import numpy as np
import pandas as pd
from scipy.stats import mannwhitneyu
import pyhomogeneity as ph
import pymannkendall as pm
#Analisis de Outliers (Kelly)
#
def outliers(df,col):

    # Agrega los datos de manera anual para tener lluvia acumulada
    df_resample = df.resample('YE').sum()
    #Crea una serie de datos en numpy
    data = np.array(df_resample[col])

    # Remueve los valores que son iguales a 0
    clean_data = data[data > 0]

    log_data = np.log(clean_data) # Logaritmo natural a los datos
    n = len(log_data) # Longitud o tamaño del registro
    mean = np.mean(log_data) # Media del registro
    std_dev = np.std(log_data, ddof=1) # Desviación estandar del registro
    Kn = -3.62201 + (6.2844 * (n ** 0.25)) - (2.49835 * (n ** 0.5)) + \
        (0.491436 * (n ** 0.75)) - (0.037911 * n)  # Grubbs-Beck
    
    #Definición de los límites superiores e inferiores
    upper_limit = np.exp(mean + Kn * std_dev)
    lower_limit = np.exp(mean - Kn * std_dev)
    
    # Calcular si cada punto es menor que el límite
    #  inferior o mayor que al límite superior
    # below_lower_limit = data < lower_limit
    # above_upper_limit = data > upper_limit

    superior = df_resample[df_resample[col] > upper_limit]
    inferior = df_resample[df_resample[col] < lower_limit]

    return superior, inferior

def mann_whitney(df,col):

    #Se agregan los datos manera anual para el análisis
    df_resample = df.resample('YE').sum()
    #Crea una serie de datos en numpy
    data = np.array(df_resample[col])
    # Se parte el array de datos en 2 para realizar la prueba
    array_1, array_2 = np.array_split(data,2)

    #Se aplica la prueba
    estadistico, p_valor = mannwhitneyu(array_1,
                                        array_2)
    # Se define la significancia estadística de la prueba
    alpha = 0.05
    # Se define si se acepta la hipotesis nula
    # Si p_valor > alpha no se puede rechazar la hipotesis nula,
    # Es decir que los datos son homogéneos
    # De lo contrario se rechaza y no son homogéneos.
    if p_valor > alpha:
        hipotesis = 'Homogéneos'
    else:
        hipotesis = 'No Homogéneos'
    # Se almacenan los resultados en un diccionario
    # Con los resultadmos más relevantes.
    resultados = {
        'estadistico':estadistico,
        'p_valor': p_valor,
        'hipotesis': hipotesis,
    }

    return resultados

def mann_kendall(df,
                 col,
                 var):
    # se agregan los datos de manera anual

    # Se Consulta la variable a analizar
    if var == 'pptn':
        df_res = df.resample('YE').sum()

    else:
        df_res = df.resample('YE').mean()
    # Se crea el arreglo de datos a analizar
    data = np.array(df_res[col])
    # Se aplica la prueba de Mann-Kendall
    results = pm.original_test(data)

    #Se almacenan los resultados mas relevantes
    # En un diccionario de resultados
    
    dic_resultados={
        'tendencia': results[0],
        'h':results[1],
        'p_valor': results[2]
    }

    return dic_resultados


def media_movil(datos, ventana):
    media_movil = []
    for i in range(len(datos) - ventana + 1):
        media = np.mean(datos[i:i+ventana])
        media_movil.append(media)
    return media_movil

def pettit(df,var):
    # se agregan los datos de manera anual
    # Se consulta la variable a analizar
    if var == 'pptn':
        df_res = df.resample('YE').sum()

    else:
        df_res = df.resample('YE').mean()
    # Se genera el arreglo de datos a analizar
    data = np.array(df_res.iloc[:,0])
    # Se aplica la prueba de pettitt
    result = ph.pettitt_test(data)

    #Se almacenan los resultados mas relevantes
    # En un diccionario de resultados
    dic_resultados = {
        'h' : result[0],
        'punto_cambio' : result[1],
        'p_valor':result[2]
    }
    return dic_resultados  


# Agregar calidad de datos faltantes 
print('something')