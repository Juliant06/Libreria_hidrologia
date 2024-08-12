# Librerias a utilizar
import numpy as np
import pandas as pd



def llenar_na(df:pd.DataFrame) -> pd.DataFrame:
    """Funcion que rellena los valores vacios de los datos con valores NaN

    Args:
        df (pd.DataFrame): Datos del IDEAM donde la fecha es el índice y la única columna es el valor
        de la precipitación

    Returns:
        pd.DataFrame: Dataframe con sus correspondientes valores NaN
    """    
    # Seleccion de fechas
    fecha_inicio = df.index[0]
    fecha_final = df.index[-1]
    # Generacion lista con fecha
    rango_fechas = pd.date_range(fecha_inicio,fecha_final,freq='d')
    # re-index de datos 
    df = df.reindex(rango_fechas)

    return df

def ciclo_anual(df:pd.DataFrame, umbral:float) -> pd.DataFrame:
    """Funcion que genera el ciclo anual asociado a una estacion.

    Args:
        df (pd.DataFrame): Datos de precipitación, donde el índice es una fecha y 
        la unica columna es la de la precipitacion
        umbral (float): Umbral de datos faltantes por mes para estimar la precipitacion.
        Se recomienda 0.1, es decir, 10% de datos faltantes

    Returns:
        pd.DataFrame: Vector con la precipitación media multianual de cada mes.
    """    

    # Se rellena el dataframe con datos NA
    df_lleno = llenar_na(df)
    #Se agregan los datos faltantes de manera mensual
    df_faltantes = df_lleno.isna().resample('ME').sum()/31
    # Se agregan los datos de manera mensual
    df_mensual = df_lleno.resample('ME').sum()
    # Filtro de datos
    datos_mensual = df_mensual[df_faltantes < umbral]
    #Generacion del ciclo anual
    ciclo_anual = datos_mensual.groupby(datos_mensual.index.month).mean()
    # Estimacion de la media anual
    
    return ciclo_anual
