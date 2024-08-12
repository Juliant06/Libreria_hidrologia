#%%
# Importar librerias necesarias
import numpy as np
import pandas as pd
import xarray as xr
import geopandas as gpd
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
#%%


# Recorrido donde se encuentra el archiivo netcdf 
# Solo cambie lo que está dentro de las comillas, no quite la r
path = r'C:\Users\F-8143\OneDrive - SHI S.A.S\datos_chirps\data.nc'

ds = xr.open_dataset(path)

# %%
def julian_to_datetime(chirps_ds):
    """ Formatea el eje del tiempo de Julian hacia datetime stamp.
        Este formateo, solo sirve para los datos de chirps descargados
        de la base de datos iridl...


    Args:
        chirps_ds (dataset): dataset que contiene los datos

    Returns:
        dataset: regresa el dataset con las fechas formateadas
    """
    chirps_ds['T'] = [pd.to_datetime(x,origin='julian',  unit='D') for x in np.array(chirps_ds.variables['T'])]

    return chirps_ds

# Actualiza el dataset a al sistema horario utilizado 


def seleccion_pixel(coordenadas, 
                    ds,
                    nombre_estacion,
                    descargar=False):
    """     Funcion que selecciona un pixel de chirps a partir de 
    las coordenadas de una estacion de IDEAM.

    Args:
        coordenadas (tupla): tupla que contiene las coordendas.
        La primera posición es longitud y la segunda latitud
        ds (dataset):  Dataset que contiene los datos de chirps
        nombre_estacion (string):  nombre de la estacion que se utilizó
        para delimitar el pixel
        descargar (booleano): True si desea descargar los datos 
        en formato excel. False por defecto

    Returns:
        Dataframe: Regresa el dataframe que contiene la serie de tiempo del pixel
    """
    # selecciona las coordenadas
    lon, lat = coordenadas

    #Busca el pixel
    pixel = ds['prcp'].sel(X=lon,
                           Y=lat,
                           method='nearest')
    
    

    serie_pixel = pixel.to_pandas()
    df_pixel = pd.DataFrame(serie_pixel,
                                columns = [nombre_estacion])
    
    if descargar:
        # Descarga el dataset
        df_pixel.to_excel('datos_chirps_{}.xlsx'.format(nombre_estacion))

    return df_pixel

        
def shape_pixeles(ds):

    """Función que genera un shape con la ubicación de los puntos
    de los pixeles de Chirps

    Args:
        ds(dataset): Dataset que contiene los datos de chirps
    """    

    contador = 0
    #Crea dataframe vacio
    df = pd.DataFrame({})

    # Asigna Columnas al dataframe
    df['Lat'] = []
    df['Lon'] = []

    # Ciclo que itera sobre los puntos y extrae las coordenadas
    for i in range(len(ds['Y'])):
        for j in range(len(ds['X'])):

            df.at[contador,'Lat'] = ds['Y'][i]
            df.at[contador,'Lon'] = ds['X'][j]

            contador += 1

    # Creación de geodataframe

    gdf = gpd.GeoDataFrame(data=df,
                           geometry=gpd.points_from_xy(df.Lon,df.Lat),
                           crs='EPSG:4326')

    gdf.to_file('Malla_puntos_chirps')

def ciclo_anual(df):

    """ Calcula el ciclo anual 

    Returns:
        _type_: _description_
    """    

    # Chequea que el indice esté en formato pandas timestamp

    if type(df.index) is pd.DatetimeIndex:
        #Convierte el índice en formato datetime
        df.index = pd.to_datetime(df.index)

    df_res = df.resample('M').sum()
    # Extraccion de dataframe aplicando filtro de datos completos mayores a 10%
    df_ciclo = df_res.groupby(df_res.index.month).mean()
    return df_ciclo


def graficos(df_ideam, 
             pixel_chirps,
             nombre_estacion,
             guardar = False):
    
    """ Funcion que compara y grafica los ciclos anuales de una estacion
        de ideam contra el pixel más cercano de chirps

    """
    # Aplica la función ciclo anual a los datos

    df_ideam_ciclo = ciclo_anual(df_ideam)
    df_chirps_ciclo = ciclo_anual(pixel_chirps)

    # Gráficos

    nombre_estacion

    fig,ax = plt.subplots(1,
                     figsize=(15,8),
                     facecolor="whitesmoke")

    ax.plot(df_ideam_ciclo,
            label=nombre_estacion)
    ax.plot(df_chirps_ciclo,
            label='Chirps')
    
    ax.set_ylabel('Precipitación ($mm$)',
                  fontsize=15)
    
    ax.set_title(('Ciclo anual ideam vs chirps Estación {}'.format(nombre_estacion)),
                 fontsize=17,
                 fontweight='bold')
    
    ax.grid(color = 'black', 
            linestyle = '--', 
            linewidth = 0.5)
    
    ax.tick_params(axis='both', which='major', labelsize=16)
    ax.legend(fontsize=14)
    mes = [
           'Ene','Feb','Mar',
           'Abr','May','Jun',
           'Jul','Ago','Sep',
           'Oct','Nov','Dic'
           ]
    

    ax.set_xticks(np.arange(1,13),mes)

    if guardar:
        plt.savefig('Comparacion_ciclo_anual_{}'.format(nombre_estacion))



# %%
