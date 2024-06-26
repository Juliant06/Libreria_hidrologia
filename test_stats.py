# Test estadisticos para revisar
# cambios en la media, outliers, tendencias y homogeneidad
import numpy as np
import pandas as pd

#Analisis de Outliers (Kelly)
 
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
    
        