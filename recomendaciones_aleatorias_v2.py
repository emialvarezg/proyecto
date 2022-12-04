# -*- coding: utf-8 -*-
pip install spotipy --upgrade

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import networkx as nx
import random
import statistics
import matplotlib.pyplot as plt
from collections import Counter

os.environ['SPOTIPY_CLIENT_ID'] ='ed651235a94342d1b3bcdf3ab85692d3'
os.environ ['SPOTIPY_CLIENT_SECRET']='3790e770a3a84bdc95ba458dbbf7d937'

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

# función f para ajustar recomendaciones respecto a un parámetro a
def f(p,a):
  if a==0 or p==0:
    return 1
  if a>0:
    return (p**a)/(100**a)
  else:
    return p**a

#ejemplo 
#si el link es 
link = 'https://open.spotify.com/artist/3PP6ghmOlDl2jaKaH0avUN?si=51_amCT-TU-CHtMrj7EfIQ'
#definan
bcnr = 'spotify:artist:3PP6ghmOlDl2jaKaH0avUN?si=51_amCT-TU-CHtMrj7EfIQ'

#más artistas
juanaMol = 'spotify:artist:76hliHkgP5eIbVqLT7NmQ3?si=51_amCT-TU-CHtMrj7EfIQ'
bh = 'spotify:artist:56ZTgzPBDge0OvCGgMO3OY?si=49ywZQ-_R5aR96c06Vk4qw'
swans = 'spotify:artist:79S80ZWgVhIPMCHuvl6SkA?si=hfBYkqCrSIqSbFtLacS2xw'
cp = 'spotify:artist:4Ge8xMJNwt6EEXOzVXju9a?si=3HWIhlbSS1OyMVJPgxXShA' 
björk = 'spotify:artist:7w29UYBi0qsHi5RTcv3lmA?si=xoCxuA73QS-CeXFokgi9UQ'
billie = 'spotify:artist:6qqNVTkY8uBg9cP3Jd7DAH?si=BxuqVYG3QWiJOY346umyqg'
mcr = 'spotify:artist:7FBcuc1gsnv6Y1nwFtNRCb?si=O_r2H39sQUyxtMSnq0lLSw'
bm = 'spotify:artist:7Hvq85OU8T7Hsd63zNBwaL?si=I5OFhlsaQqGBbiNN8CmJZw'

#ingresar artista
recs=sp.artist_related_artists(cp)

#seleccionar a (-1 < a < 1)
# a<0 hace más probable obtener recomendaciones menos populares, a>0 regresa artistas con popularidad similar al inicial
a=0

#vértices
vertices=[]
for i in range(len(recs['artists'])):
  vertices.append({'name':recs['artists'][i]['name'],'popularity':recs['artists'][i]['popularity'],'uri':recs['artists'][i]['uri']})
  links=[]

for artist in vertices:
  if np.random.uniform() < f(artist['popularity'],a):
    links.append(artist['uri'])

for l in links:
  recs=sp.artist_related_artists(l)
  for i in range(len(recs['artists'])):
    vertices.append({'name':recs['artists'][i]['name'],'popularity':recs['artists'][i]['popularity'],'uri':recs['artists'][i]['uri']})

#quitamos repetidos
vert = []
for i in vertices:
  if i not in vert:
    vert.append(i) 
print(len(vert))


#función para obtener información de un artista seleccionado
def info(name,info):
  for artist in vert:
    if artist['name'] == name:
      return artist[info]

#construimos la gráfica con los vértices y aristas previamente seleccionados
G= nx.complete_graph([artist['name'] for artist in vert])
print(G,nx.is_connected(G))

#función para definir vector de probabilidades para un vértice considerando popularidad
def vect_prob(vertice):
  v = list(G.neighbors(vertice))
  prob=[]
  for vec in v:
    pop=info(vec,'popularity')
    prob.append(f(pop,a))
  return [(1/sum(prob))*i for i in prob]

#caminata aleatoria
n=10000
burn=2000
v_0 = random.choices(list(G.nodes()))[0]
vertices_visitados = [v_0]
for i in range(n):
  p=vect_prob(v_0)
  v = random.choices(list(G.neighbors(v_0)),weights=p)[0]
  vertices_visitados.append(v)
  v_0=v

vertices_visitados
frec = Counter(vertices_visitados[burn:])
frecuencia= dict(frec)
#frecuencia
pi=[]
for v in list(G.nodes()):
  if v in frecuencia:
    pi.append(frecuencia[v])
  else:
    pi.append(0)
#aproximamos la distribución estacionaria evaluada en un estado con el número de veces que se visitó el vertice
#entre el total de pasos de la caminata (sin el periodo de quemado)
d_est = [(1/(n-burn))*i for i in pi]
print(sum(d_est))

#Este bloque genera una recomendación mediante una muestra de tamaño 1 de la distribución estacionaria
rec = random.choices(list(G.nodes()),weights=d_est)[0]
print(rec,info(rec,'popularity'))
print('link:',info(rec,'uri'))
frecuencia[rec]

#ordenamos los vértices de mayor a menor según su número de apariciones en la caminata aleatoria
orden = sorted([[frecuencia[list(G.nodes())[i]], list(G.nodes())[i], (n-burn)*d_est[i]] for i in range(len(list(G.nodes())))],reverse=True)
dic_orden = {}
for i in range(len(orden)):
  dic_orden[orden[i][1]]=i+1

#Generamos una muestra de la distribución estacionaria para grafcar
muestra = [random.choices(list(G.nodes()),weights=d_est)[0] for i in range(n-burn)]
frec_muestra = dict(Counter(muestra))
#ordenamos la muestra por frecuencia
muestra_ord=dict(sorted(frec_muestra.items(), key = lambda item: item[1],reverse=True))
muestra_ord
lista1=[]
lista2=[]
lista3=[]
lista4=[]
for i in dic_orden:
  if i in muestra_ord:
    lista1.append(dic_orden[i])
    lista2.append(muestra_ord[i])
    lista3.append(frecuencia[i])
    lista4.append(info(i,'popularity'))

#Comparamos la frecuencia en la caminata y la popularidad
plt.scatter(lista1,lista3),plt.scatter(lista1,lista4)
plt.title('Frecuencia y popularidad')
plt.xlabel('Vértices ordenados')

#Comparamos la frecuencia en la muestra y la popularidad
plt.scatter(lista1,lista2),plt.scatter(lista1,lista4)
plt.title('Muestra y popularidad')
plt.xlabel('Vértices ordenados')
