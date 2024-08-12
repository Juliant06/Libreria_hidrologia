#%%
import pandas as pd
import numpy as np
import pyhomogeneity as ph
import pymannkendall as pm
import os
import matplotlib.pyplot as plt

# %%

def mann_kendall(df,var):

    # se agregan los datos para realizar el test
    if var == 'pptn':
        df_res = df.resample('YE').sum()

    else:
        df_res = df.resample('YE').mean()

    data = np.array(df.iloc[:,0])

    results = pm.original_test(data)

    return results


def media_movil(datos, ventana):
    media_movil = []
    for i in range(len(datos) - ventana + 1):
        media = np.mean(datos[i:i+ventana])
        media_movil.append(media)
    return media_movil

def pettit(df,var):

    if var == 'pptn':
        df_res = df.resample('YE').sum()

    else:
        df_res = df.resample('YE').mean()

    data = np.array(df_res.iloc[:,0])

    result = ph.pettitt_test(data)

    return result





