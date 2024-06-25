#%%

import pandas as pd
import numpy as np
import os

#import matplotlib.pyplot as plt
#import seaborn as sns

# ----------------------------------------------MODIFICAR
carpeta_entrada = r"C:\Users\Admin\OneDrive - SHI S.A.S\01_Hidrologia\06_XLSX\5-Qambientales\Q95\ArchivosClasificados"
carpeta_salida = r"C:\Users\Admin\OneDrive - SHI S.A.S\01_Hidrologia\06_XLSX\5-Qambientales\Q95\ArchivosCaudales"
# ----------------------------------------------FIN MODIFICAR

for file in os.listdir(carpeta_entrada):

    if 'xls' in file.split('.')[-1]:

        archivo = carpeta_entrada + os.sep + file

        df_humedo = pd.DataFrame(pd.read_excel(archivo, sheet_name='Humedo', header=0))
        df_normal = pd.DataFrame(pd.read_excel(archivo, sheet_name='Normal', header=0))
        df_calido = pd.DataFrame(pd.read_excel(archivo, sheet_name='Calido', header=0))

        mes = df_humedo['Mes'].unique().tolist()
        #print(mes)
        #df_humedo['Mes'].value_counts()

        #Pone True donde mes=1
        #df_humedo['1'] = pd.Series( np.array(df_humedo['Mes']==1) )

        #df_humedo['1'] = np.where(df_humedo['Mes']==1, df_humedo['Caudal (m3/s)'], np.nan)

        #i=df_humedo['Mes'].count().tolist()


        #----------------------------------------Caudales fase húmeda por mes
        for k in mes:
            for i in range(len (df_humedo['Mes']) ):
                if k == df_humedo['Mes'][i]:
                    df_humedo['{}'.format(k)] = np.where(df_humedo['Mes']==k, df_humedo['Caudal (m3/s)'], np.nan) 

        #print(df_humedo)    

        #----------------------------------------Caudales fase cálida por mes
        for l in mes:
            for j in range(len (df_normal['Mes']) ):
                if l == df_normal['Mes'][j]:
                    df_normal['{}'.format(l)] = np.where(df_normal['Mes']==l, df_normal['Caudal (m3/s)'], np.nan) 

        #print(df_normal)

        #----------------------------------------Caudales fase normal por mes
        for n in mes:
            for h in range(len (df_calido['Mes']) ):
                if n == df_calido['Mes'][h]:
                    df_calido['{}'.format(n)] = np.where(df_calido['Mes']==n, df_calido['Caudal (m3/s)'], np.nan) 

        #print(df_calido)


        #----------------------------------------Fase húmeda caudales ordenados

        #Nuevo dataframe para valores ordenados
        q95_hum =  pd.DataFrame()
        q95_hum['Orden'] = np.arange(1, len(df_humedo)+1)

        #Para llenar las columnas se deben pasar a array y luego a series
        for k in mes:
            q95_hum['{}'.format(k)] = pd.Series( np.array( df_humedo['{}'.format(k)].sort_values(ascending=False) ) )

        #Lista con el números de registros por mes    
        ListaContarHumedo = []
        for n in mes:
            contar = q95_hum['{}'.format(n)].count()
            ListaContarHumedo.append(contar)
        print('último num húmedo: ',ListaContarHumedo)

        #----------------------------------------Fase cálida caudales ordenados

        #Nuevo dataframe para valores ordenados
        q95_cal =  pd.DataFrame()
        q95_cal['Orden'] = np.arange(1, len(df_calido)+1)

        #Para llenar las columnas se deben pasar a array y luego a series
        for l in mes:
            q95_cal['{}'.format(l)] = pd.Series( np.array( df_calido['{}'.format(l)].sort_values(ascending=False) ) )

        #Lista con el números de registros por mes    
        ListaContarCalido = []
        for m in mes:
            contar2 = q95_cal['{}'.format(m)].count()
            ListaContarCalido.append(contar2)
        print('último num cálido: ',ListaContarCalido)
        
        #----------------------------------------Fase normal caudales ordenados

        #Nuevo dataframe para valores ordenados
        q95_nor =  pd.DataFrame()
        q95_nor['Orden'] = np.arange(1, len(df_normal)+1)

        #Para llenar las columnas se deben pasar a array y luego a series
        for p in mes:
            q95_nor['{}'.format(p)] = pd.Series( np.array( df_normal['{}'.format(p)].sort_values(ascending=False) ) )

        #Lista con el números de registros por mes    
        ListaContarNormal = []
        for q in mes:
            contar3 = q95_nor['{}'.format(q)].count()
            ListaContarNormal.append(contar3)
        print('último num normal: ',ListaContarNormal)

        #------------------ Generar columnas Weibull
            
        ListaWeibull = ['1_Weibull', '2_Weibull', '3_Weibull', '4_Weibull','5_Weibull','6_Weibull',
                        '7_Weibull', '8_Weibull','9_Weibull','10_Weibull','11_Weibull','12_Weibull']

        #Ensayo solo para enero húmedo
        #FALTA PARA TODOS LOS MESES Y QUE IGNORE LOS NaN
        ListaValoresWeibull = []

        for r in range(12):
            #print(r)
            valores_weibull_h = (q95_hum['Orden'] * 100 ) / (ListaContarHumedo[r] + 1)
            valores_weibull_c = (q95_cal['Orden'] * 100 ) / (ListaContarCalido[r] + 1)
            valores_weibull_n = (q95_nor['Orden'] * 100 ) / (ListaContarNormal[r] + 1)
            
            q95_hum[ListaWeibull[r]] = valores_weibull_h[:ListaContarHumedo[r]]
            q95_cal[ListaWeibull[r]] = valores_weibull_c[:ListaContarCalido[r]]
            q95_nor[ListaWeibull[r]] = valores_weibull_n[:ListaContarNormal[r]]

        #----------------------------------------Resumen de datos

        resumen_q95_hum = {}
        resumen_q95_cal= {}
        resumen_q95_nor = {}

        for i in range(12):
            # Extraer columnas de caudal y probabilidad para cada mes
            df_aux = q95_hum[[q95_hum.columns[i+1], q95_hum.columns[i+13]]]

            # Eliminar datos nan
            df_aux = df_aux.dropna()
            
            #Añadir dato del 95%
            nueva_fila = [None,95]
            nueva_fila = {list(df_aux.columns)[i]:nueva_fila[i] for i in range(2)}
            nueva_fila = pd.DataFrame(nueva_fila, index=[0])

            # Usar el método loc para agregar la nueva fila
            df_aux = pd.concat([df_aux, nueva_fila], ignore_index=True)
            df_aux = df_aux.sort_values(by = list(df_aux.columns)[1])
            df_aux = df_aux.reset_index(drop=True)
            df_aux = df_aux.interpolate()

            # Extraer valor

            df_95 = df_aux[df_aux[list(df_aux.columns)[1]] == 95]
            resumen_q95_hum[list(df_aux.columns)[0]] = df_95[list(df_aux.columns)[0]][df_95.index[0]]

        for i in range(12):
            # Extraer columnas de caudal y probabilidad para cada mes
            df_aux = q95_cal[[q95_cal.columns[i+1], q95_cal.columns[i+13]]]

            # Eliminar datos nan
            df_aux = df_aux.dropna()
            
            #Añadir dato del 95%
            nueva_fila = [None,95]
            nueva_fila = {list(df_aux.columns)[i]:nueva_fila[i] for i in range(2)}
            nueva_fila = pd.DataFrame(nueva_fila, index=[0])

            # Usar el método loc para agregar la nueva fila
            df_aux = pd.concat([df_aux, nueva_fila], ignore_index=True)
            df_aux = df_aux.sort_values(by = list(df_aux.columns)[1])
            df_aux = df_aux.reset_index(drop=True)
            df_aux = df_aux.interpolate()

            # Extraer valor

            df_95 = df_aux[df_aux[list(df_aux.columns)[1]] == 95]
            resumen_q95_cal[list(df_aux.columns)[0]] = df_95[list(df_aux.columns)[0]][df_95.index[0]]

        for i in range(12):
            # Extraer columnas de caudal y probabilidad para cada mes
            df_aux = q95_nor[[q95_nor.columns[i+1], q95_nor.columns[i+13]]]

            # Eliminar datos nan
            df_aux = df_aux.dropna()
            
            #Añadir dato del 95%
            nueva_fila = [None,95]
            nueva_fila = {list(df_aux.columns)[i]:nueva_fila[i] for i in range(2)}
            nueva_fila = pd.DataFrame(nueva_fila, index=[0])

            # Usar el método loc para agregar la nueva fila
            df_aux = pd.concat([df_aux, nueva_fila], ignore_index=True)
            df_aux = df_aux.sort_values(by = list(df_aux.columns)[1])
            df_aux = df_aux.reset_index(drop=True)
            df_aux = df_aux.interpolate()

            # Extraer valor

            df_95 = df_aux[df_aux[list(df_aux.columns)[1]] == 95]
            resumen_q95_nor[list(df_aux.columns)[0]] = df_95[list(df_aux.columns)[0]][df_95.index[0]]

        #----------------------------------------Resumen 95%

        resumen_q95_hum = pd.DataFrame(resumen_q95_hum, index = ['Húmedo (m3/s)'])
        resumen_q95_cal= pd.DataFrame(resumen_q95_cal, index = ['Cálido (m3/s)'])
        resumen_q95_nor = pd.DataFrame(resumen_q95_nor, index = ['Neutro (m3/s)'])

        resumen_todos = pd.concat([resumen_q95_hum, resumen_q95_cal, resumen_q95_nor])
        resumen_todos = resumen_todos[[str(i) for i in range (1,13)]]


        #-----------EXPORTAR----------------------------------------------

        file_salida = carpeta_salida + os.sep + 'Caudales_' + archivo.split(os.sep)[-1].split('.')[0] + '.xlsx'
        
        #Se genera en la misma carpeta que está el código
        with pd.ExcelWriter(file_salida) as writer:
            df_humedo.to_excel(writer, sheet_name='humedo', index=False)  
            df_normal.to_excel(writer, sheet_name='normal',index=False) 
            df_calido.to_excel(writer, sheet_name='calido',index=False) 
            q95_hum.to_excel(writer, sheet_name='humedo_ordenado',index=False)  
            q95_cal.to_excel(writer, sheet_name='calido_ordenado',index=False) 
            q95_nor.to_excel(writer, sheet_name='normal_ordenado',index=False) 
            resumen_todos.to_excel(writer, sheet_name='resumen95')
        
#%%
