# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colaboratory.

# M1. Actvidad
Aldo Alafita A00827487

# **Introducción**
Este trabajo muestra una simulación de un mapa con un formato de cuadrícula en la cual de forma aleatoria se generan agentes de piso "sucios". Existen agentes aspiradora, los cuales tienen el objetivo de en caso de encontrar piso "sucio", limpiarlo.
Las aspiradoras se mueven de manera aleatoria una posición a la vez en cualquiera de sus ocho direcciones.
"""

!pip3 install mesa

"""# setup"""

# Commented out IPython magic to ensure Python compatibility.
# La clase `Model` se hace cargo de los atributos a nivel del modelo, maneja los agentes. 
# Cada modelo puede contener múltiples agentes y todos ellos son instancias de la clase `Agent`.
from mesa import Agent, Model 

# Debido a que necesitamos un solo agente por celda elegimos `SingleGrid` que fuerza un solo objeto por celda.
from mesa.space import MultiGrid

# Con `SimultaneousActivation` hacemos que todos los agentes se activen de manera simultanea.
from mesa.time import SimultaneousActivation

# Vamos a hacer uso de `DataCollector` para obtener el grid completo cada paso (o generación) y lo usaremos para graficarlo.
from mesa.datacollection import DataCollector

# mathplotlib lo usamos para graficar/visualizar como evoluciona el autómata celular.
# %matplotlib inline
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
plt.rcParams["animation.html"] = "jshtml"
matplotlib.rcParams['animation.embed_limit'] = 2**128

# Definimos los siguientes paquetes para manejar valores númericos.
import numpy as np
import pandas as pd
import random
# Definimos otros paquetes que vamos a usar para medir el tiempo de ejecución de nuestro algoritmo.
import time
import datetime

"""# clases"""

def get_grid(model):
    '''
    Esta es una función auxiliar que nos permite guardar el grid para cada uno de los agentes.
    param model: El modelo del cual optener el grid.
    return una matriz con la información del grid del agente.
    '''
    grid = np.zeros((model.grid.width, model.grid.height))
    for cell in model.grid.coord_iter():
        cell_content, x, y, = cell
        for content in cell_content:
          if isinstance(content, GameVacuum):
            grid[x][y] = 2
          else:
            grid[x][y] = content.live
    return grid

class GameVacuum(Agent):
  def __init__(self, unique_id, model):
      
        super().__init__(unique_id, model)
    
  def step(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False)
        new_position = self.random.choice(possible_steps)
        
        self.model.grid.move_agent(self, new_position)
        global contador
        contador = contador + 1

class GameLifeAgent(Agent):

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
        self.live = np.random.choice([0,1])
        self.next_state = None
    
    def step(self):
      cellmates = self.model.grid.get_cell_list_contents([self.pos])
      self.next_state = self.live
      if len(cellmates) > 1:
          self.next_state = 0
      else:
        if(self.next_state == 0):
          self.next_state = 0
        else:
          self.next_state = 1
        
       
    def advance(self):
        '''
        Define el nuevo estado calculado del método step.
        '''
        self.live = self.next_state
        global contador
        contador = contador + 1
            
class GameLifeModel(Model):
    '''
    Define el modelo del juego de la vida.
    '''

    def __init__(self, N, width, height, porcentaje):
        self.num_agents = (width * height * porcentaje) 
        self.grid = MultiGrid(width, height, torus=False)
        self.schedule = SimultaneousActivation(self)
        self.init_sucio = int(self.num_agents)

        for i in range(self.init_sucio):
          x = self.random.randrange(width)
          y = self.random.randrange(height)
          cellmates = self.grid.get_cell_list_contents((x,y))
          while len(cellmates) > 0:
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            cellmates = self.grid.get_cell_list_contents((x,y))
          a = GameLifeAgent((x, y), self)
          self.grid.place_agent(a, (x, y))
          self.schedule.add(a)

        for i in range(N):
          b = GameVacuum(i, self)
          self.grid.place_agent(b, (1, 1))
          self.schedule.add(b)
        

        # Aquí definimos con colector para obtener el grid completo.
        self.datacollector = DataCollector(
            model_reporters={"Grid": get_grid},
            agent_reporters={"Moves" : lambda a: getattr(a, 'moves', None)}
        )

    def celdasSucias(self):
      celdas_sucias = 0
      for celda in self.grid.coord_iter():
        cell_content, x, y = celda
        for content in cell_content:
          if  isinstance(content, GameLifeAgent):
            if content.live == 1:
              celdas_sucias = celdas_sucias + 1

  
      return celdas_sucias
   
    def step(self):
        '''
        En cada paso el colector tomará la información que se definió y almacenará el grid para luego graficarlo.
        '''
        self.datacollector.collect(self)
        self.schedule.step()

"""# Variables e inicio """

# Definimos el tamaño del Grid
GRID_SIZE_M = 10
GRID_SIZE_N = 10
# Definimos el número de Agentes a correr
NUM_AGENTES = 3

P_CELDAS_SUCIAS = 0.1

TIEMPO_MAX_EJECUCION = 0.9
# Registramos el tiempo de inicio y corremos el modelo
contador = 0
start_time = time.time()
tiempo_inicio = str(datetime.timedelta(seconds=TIEMPO_MAX_EJECUCION))
model = GameLifeModel(NUM_AGENTES, GRID_SIZE_M, GRID_SIZE_N,P_CELDAS_SUCIAS)

while((time.time()- start_time) < TIEMPO_MAX_EJECUCION and model.celdasSucias() > 0):
  model.step()

# Imprimimos el tiempo que le tomó correr al modelo.
tiempo_ejecucion = str(datetime.timedelta(seconds=(time.time() - start_time)))
print("Tiempo de ejecución: " + tiempo_ejecucion)
celdas_restantes = str((model.celdasSucias()*100)/(GRID_SIZE_M * GRID_SIZE_N))
print("Porcentaje de celdas sucias: " + celdas_restantes)
print("Numero de movimiento realizados por todos los agentes: " + str(contador))

"""# Despliegue

"""

all_grid = model.datacollector.get_model_vars_dataframe()

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# 
# fig, axs = plt.subplots(figsize=(7,7))
# axs.set_xticks([])
# axs.set_yticks([])
# patch = plt.imshow(all_grid.iloc[0][0], cmap='Greys')
# 
# def animate(i):
#     patch.set_data(all_grid.iloc[i][0])
#     
# anim = animation.FuncAnimation(fig, animate, frames=len(all_grid))

anim

"""# **Conclusiones**
Observando los resultados de la simulación, se puede concluir que un sistema de agentes que se mueven de manera aleatoria puede llegar a tener un desempeño no tan eficiente al momento de realizar su trabajo. Al no tener un patron de seguimiento, las aspiradores recorren grandes cantidades de distancia, sin limpiar piso sucio. Esto en terminos reales puede traducirse como gasto inecesario de recursos como tiempo y electricidad.
Una solución para un rendimiento mas eficiente, seria recorrer toda la cuadrícula limpiando una fila a la vez.

"""
