import numpy as np
import pandas as pd
import random
import gr4j as gr
import funcion_objetivo as fo

def parametros():
    # Se aplican los intervalos sugeridos en (Perrin, 2003)
    X1 = random.uniform(100, 3000) #100 - 1200
    X2 = random.uniform(-5, 3) #-5 - 3
    X3 = random.uniform(20, 300) #20 - 300
    X4 = random.uniform(1.1, 2.9) #1.1-2.9

    return [X1,X2,X3,X4]


def poblacion_inicial(muestra:int) -> list:
    """ Funcion que genera una poblacion inicial de arreglos
    de parametros aleatorios.


    Args:
        muestra (int): Numero de arreglos de parametros que buscan generar

    Returns:
        (list): Regresa una lista con todos los arreglos de parametros generados
    """    
    # genera una lista con la poblacion segun la muestra indicada
    poblacion = [parametros() for _ in range(muestra)]
    return poblacion

def datos_cuenca(
        area:float,etp:list,
        pptn:list,
        ):
    
    
    return area,etp,pptn

def fitness(
        poblacion:list, etp:list,
        pptn:list, q_obs:list,
        area: float
        ) -> list:
    """Funcion que genera el fitness o valor calificativo 
    de cada grupo de parametros generados en la poblacion inicial.
    A partir de correr el modelo GR4J para cada conjunto de parametros.
    El valor del nash corresponde al fitness.

    Args:
        poblacion (list): Lista con los conjuntos de parametros generados.
        etp (list): Lista con los valores de la evapotranspiracion potencial.
        pptn (list): Lista con los valores de precipitacion de la zona.
        q_obs (list): Caudal observado con el cual se quiere comparar las salidas del modelo
        area (float): area de la cuenca de interes

    Returns:
        list: Regresa una lista de tuplas, cada tupla contiene los parametros utilizados
        y el nash correspondiente a cada uno.
    """    
    
 
    # para la estimacion del fitness
    # Se aplica el Nash como calificacion

    # datos de la cuenca

    #Lista vacia que almacena las salidas de simulacion
    almac_fitness = []

    # ciclo for que itera sobre la poblacion
    for i in range(len(poblacion)):

        # Extrae los parametros que contiene cada miembro de
        # la poblacion
        params = poblacion[i]

        dic_params = {

        'X1':params[0],  # 100-1200
        'X2':params[1],  # -5 a 3
        'X3':params[2],  # 20-300
        'X4':params[3],  # 1.1-2.9

        }

        # se define el diccionario de condiciones iniciales
        cond_iniciales = {

        'production_store': 0.6,
        'routing_store': 0.68

        }

        q_simulado = np.array(gr.gr4j(
            pptn,
            etp,
            dic_params,
            cond_iniciales
        ))

        q_simulado_escalado = q_simulado*(area)/86.4

        # Se calcula el nash, el cual será el calificador de fitness
        nash = fo.nash(q_obs,q_simulado_escalado)
        # Se almacena cada salida de la poblacion con su respectivo fitness
        resultado_fitness = (params,nash)

        # almacenamiento de resultados
        # Solo se mantienen resultados con Nash positivo
        if nash > 0:
            almac_fitness.append(resultado_fitness)

    return almac_fitness

def run_gr4j(
        params: list,
        pptn:list,
        etp:list,
        area: float,
        ) -> list:
    """ Funcion que corre el modelo gr4j

    Args:
        params (list): Lista de parametros
        pptn (list): Lista de precipitacion
        etp (list): Lista de evapotranspiracion potencial
        area (float): area de la cuenca de interes

    Returns:
        list: Regresa una lista con los caudales simulados.
    """        
    
    dic_params = {

        'X1':params[0],  # 100-1200
        'X2':params[1],  # -5 a 3
        'X3':params[2],  # 20-300
        'X4':params[3],  # 1.1-2.9

        }

        # se define el diccionario de condiciones iniciales
    cond_iniciales = {

        'production_store': 0.6,
        'routing_store': 0.68

        }

    q_simulado = np.array(gr.gr4j(
            pptn,
            etp,
            dic_params,
            cond_iniciales
        ))

    q_simulado_escalado = q_simulado*(area)/86.4

    return q_simulado_escalado

def seleccion(resultados: list) -> list:
    """Funcion que genera la seleccion de los padres de la siguiente generacion.

    Args:
        resultados (list): Se ingresan la lista de tuplas obtenidas
        de la funcion `fitness`

    Returns:
        list: Regresa los dos arreglos de parametros seleccionados.
    """    
    # Aplica la funcion de seleccion del modula random
    # Devuelve los dos padres seleccionados (grupos de parametros)
    # 
    return random.choices(
        # Se ingresa la poblacion    
        population= [muestra[0] for muestra in resultados],
        # De los resultados se extrae el arreglo con los Nash
        # que funcionan como fitness en este caso
        weights=[fitness[1] for fitness in resultados],
        k=2
    )

# Creacion del cruce
def apareamiento(padre1: list, padre2: list) -> tuple:
    """Funcion que cruza los dos arreglos de parametros seleccionados.


    Args:
        padre1 (list): Arreglo de parametros obtenido de la funcion `seleccion`
        padre2 (list): Arreglo de parametros obtenido de la funcion `seleccion`

    Returns:
        tuple: Regresa dos arreglos de parametros obtenidos de 
    """     
    # Se estima la longitud del array de parametros
    length = len(padre1)
    # Se genera un numero  aleatoria a partir del cual truncar
    # los arreglos y generar los cruces
    p = random.randint(1, length-1)
    # Se genera el cruce
    cruce1 = padre1[0:p] + padre2[p:]
    cruce2 = padre2[0:p] + padre1[p:]
    return cruce1, cruce2
# Mutacion

def mutacion(padre: list, num: int = 1, probabilidad:float = 0.5) -> list:
    """Funcion que genera la mutacion de cada uno de los hijos. 

    Args:
        padre (list): _description_
        num (int, optional): _description_. Defaults to 1.
        probabilidad (float, optional): _description_. Defaults to 0.5.

    Returns:
        list: _description_
    """    
    for _ in range(num):
        # Esta linea genera un valor aleatorio de indice segun la longitud
        # del array suministrado
        indice = random.randrange(len(padre))
        # Corre la funcion de parametros para generar un nuevo set aleatorio
        # Con el indice logra extraer el que va a ser modificado
        parametros_mutacion = parametros()
        # Condicional para chequear si un numero aleatorio es mayor a la condicion de mutacion
        num_aleatorio = random.random()

        if num_aleatorio < probabilidad:
            padre[indice] = parametros_mutacion[indice]
        
    return padre

def main_loop(
        funcion_poblacion: poblacion_inicial,
        fitness_func: fitness,
        funcion_seleccion: seleccion,
        funcion_apareamiento: apareamiento,
        funcion_mutacion: mutacion,
        umbral_nash:float,
        pptn: list,
        area: float,
        q_obs: list,
        etp: list,
        limite_generacion: int = 100,
        ) -> tuple:
    
    poblacion = funcion_poblacion(100)

    

    for i in range(limite_generacion):
        
        resultados_fitness = fitness_func(
            poblacion,
            etp,
            pptn,
            q_obs,
            area
        )
        
        poblacion_fitness = [fitness[0] for fitness in resultados_fitness]
        nash = [fitness[1] for fitness in resultados_fitness]
        # print(poblacion_fitness)
        # print(nash)

        poblacion_sorted = sorted(
            resultados_fitness,
            key=lambda x: x[1],
            reverse=True
        )
        # Chequea si la primera combinacion de parametros 
        # Supera el umbral establecido
        if poblacion_sorted[0][1] >= umbral_nash:
            break

        # Proxima generacion 

        proxima_generacion = poblacion_fitness[0:2]

        # Ciclo para pasar a la siguiente generacion
        for j in range(int(len(poblacion)/2)-1):
            
            # Seleccion de padres de la siguiente generacion
            padres = seleccion(resultados_fitness)

            # Reproduccion entre los padres
            hijo_1, hijo_2 = apareamiento(padre1=padres[0], padre2=padres[1])
            # Aplicacion de la mutacion
            hijo1_mutado = mutacion(hijo_1,probabilidad=0.25)
            hijo2_mutado = mutacion(hijo_2,probabilidad=0.25)
            # Almacenamiento de la siguiente generacion
            proxima_generacion += [hijo1_mutado, hijo2_mutado]

        poblacion = proxima_generacion 

    resultados_poblacion_final = fitness_func(
            poblacion,
            etp,
            pptn,
            q_obs,
            area
        )


    resultados = sorted(
        resultados_poblacion_final,
        key=lambda x: x[1],
        reverse=True
    )

    print('Generacion:',i)
    return resultados