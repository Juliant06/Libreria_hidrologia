import pandas as pd
import numpy as np
import re
import geopandas as gpd

# llenado de estaciones
def llenar_na(df):
    # Seleccion de fechas
    fecha_inicio = df.index[0]
    fecha_final = df.index[-1]
    # Generacion lista con fecha
    rango_fechas = pd.date_range(fecha_inicio,fecha_final,freq='d')
    # re-index de datos 
    df = df.reindex(rango_fechas)

    return df

# Leer archivos data
# Funcion para leer archivos de IDEAM en data

def read_data(archivo):

    # Lectura de los datos
    df = pd.read_csv(archivo,
                     sep='|',
                     index_col='Fecha')
    
    # Formato timestamp para el indice
    df.index = pd.to_datetime(df.index)
    # Cambio de nombre en la columna
    # Se nombre la columna con el codigo de la estacion
    pattern = r'@(\d+)' # Patron de regex para la extraccion del codigo

    match = re.search(pattern,archivo)[1]
    # Se aplica el cambio de nombre
    df.rename(columns = {'Valor':match}, 
                       inplace = True)
    
    #Se rellena el dataframe
    df_lleno = llenar_na(df) 
    
    return df_lleno

def pptn_media_anual(df,
                     umbral=0.1):
    
    # Se rellena el dataframe con datos NA
    df_lleno = llenar_na(df)

    #Se agregan los datos faltantes de manera anual
    df_faltantes = df_lleno.isna().resample('YE').sum()/365
    # Se agregan los datos de manera anual 
    df_anual = df_lleno.resample('YE').sum()
    # Filtro de datos
    datos_anuales = df_anual[df_faltantes < umbral].dropna()
    # Estimacion de la media anual
    media_anual = np.mean(datos_anuales)
    
    return media_anual



def razon_normal(df):

    cols = list(df.columns)

    Ns = [pptn_media_anual(df[col]) for col in cols]
    dic_media_pptn = {k:v for k,v in zip(cols,Ns)}

    for col in cols:
        # Crea una copia de la lista de columnas 
        # se actualiza cada vez que se corre el codigo
        col2 = list(df.columns)
        col2.remove(col)
        for date in df.index:
            Nx = dic_media_pptn[col]
            #Lista de columnas a revisar
            # Lista de valores medios mulianuales
            Ns = [dic_media_pptn[col] for col in col2]
            # Verifica si el punto esta vacio
            if pd.isna(df.at[date,col]):
                # Esta linea extrae los valores de precipitacion de las otras columnas
                Pi = [df.at[date,col] for col in col2]
                # Se realiza un calculo parcial del metodo de razon normal
                parte_1 = [(Nx/Ni)*Pi for Ni,Pi in zip(Ns,Pi)]
                # Se realiza el relleno de la precipitacion, se ignoran los Na en otras columnas
                Px = np.nanmean(parte_1)
                # Se actualiza el valor de precipitacion
                df.at[date,col] = Px
    
    return df

def info_estacion(df:pd.DataFrame,codigo:int) -> dict:

    # Este codigo es temporal 
    # Se busca una menera mas eficiente
    # De acceder a la información almacenada 
    # En el catálogo de estaciones de IDEAM

    # Se convierte el codigo de la variable a entero
    # Es la forma en la cual el CNE lo lee
    codigo = int(codigo)

    cne = pd.read_csv('Cat_logo_Nacional_de_Estaciones_del_IDEAM_20240627.csv',
                      index_col='Codigo')
    # Extracción de coordenadas en texto plano
    cne_index = cne.index
    # Chequeo si el código está en el CNE
    if codigo not in cne_index:
        raise Exception("Código no encontrado en el registro del catálogo")
    coord_cne = cne.at[codigo, 'Ubicación']

    # Patron de regex para la extracción de las coordenadas
    patron = r'-?\d+\.\d+'
    coordenadas = re.findall(patron,coord_cne) 

    #Almacenamiento de las coordenadas y altitud de la estacion
    #Se convierten las coordenadas a flotante
    estacion = cne.at[codigo, 'Nombre']
    coord_y = float(coordenadas[0])
    coord_x = float(coordenadas[1])
    altitud = cne.at[codigo,'Altitud']
    pptn_media = pptn_media_anual(df)
    registro = len(df)
    faltantes = df.isna().sum().iloc[0]
    fecha_inicial = df.index[0]
    fecha_final = df.index[-1]
    

    # Creación de diccionario con los datos extraidos
    dic_informacion = {
        'Nombre': estacion,
        'Y': coord_y,
        'X': coord_x,
        'altitud': altitud,
        'pptn_media_anual': pptn_media,
        'registro': registro,
        'Faltantes':faltantes,
        'Fecha inicial': fecha_inicial,
        'Fecha final': fecha_final,
    }

    return dic_informacion

def shape_estaciones(df):

    # creacion de un geodataframe 
    # El cual contiene la informacion de las estaciones
    gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df.X, df.Y), 
    crs="EPSG:4326"
    )

    # Se convierte el sistema coordenado del geodataframe
    gdf.to_crs('EPSG:9377',inplace=True)
    
    gdf['X'] = gdf.get_coordinates()['x']
    gdf['Y'] = gdf.get_coordinates()['y']

    # Se crea shape con geodataframe


    return gdf

def ciclo_anual(df:pd.DataFrame, umbral:float) -> pd.DataFrame:

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



    

    

    