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

"""
Recomendaciones
"""
#ejemplo 
#si el link es 
link = 'https://open.spotify.com/artist/3PP6ghmOlDl2jaKaH0avUN?si=51_amCT-TU-CHtMrj7EfIQ'
#definan
bcnr = 'spotify:artist:3PP6ghmOlDl2jaKaH0avUN?si=51_amCT-TU-CHtMrj7EfIQ'
#más artistas
bm = 'spotify:artist:7Hvq85OU8T7Hsd63zNBwaL?si=I5OFhlsaQqGBbiNN8CmJZw'
kglw = 'spotify:artist:6XYvaoDGE0VmRt83Jss9Sn?si=aa1U_cvuSPu_DTJNKGLOxA' 
cabizbajo = 'spotify:artist:3sZkCrbHsAo7OS6CuB7F6Q?si=YfgV_NCHQnCseocsceHlRg' 
portishead = 'spotify:artist:6liAMWkVf5LH7YR9yfFy1Y?si=US2xEeFWTMWFx3EkJe4rVw'
death_grips = 'spotify:artist:5RADpgYLOuS2ZxDq7ggYYH?si=zRTJhcWgTAC2zHeL4ec7OA'
björk = 'spotify:artist:7w29UYBi0qsHi5RTcv3lmA?si=xoCxuA73QS-CeXFokgi9UQ'
grupo_jejeje = 'spotify:artist:6jByJTW6DZkHpVQ2SG3fXL?si=hJm6azWqSFaKbQXktGkAMQ'
deafheaven = 'spotify:artist:4XpPveeg7RuYS3CgLo75t9?si=rEd-XaR8Qs2-CgE-V2MyQQ'
slowdive = 'spotify:artist:72X6FHxaShda0XeQw3vbeF?si=Bmu3lGxQQW-iQRaI2eJDVA'
crj = 'spotify:artist:6sFIWsNpZYqfjUpaCgueju?si=gPppciZRTFaSF5NHheROfQ'
b_3000 = 'spotify:artist:6LtXxYMIiKSy2EGHnz1f5j?si=VRKu_kC-TsCiAAgyV9RO7g'
snow_s = 'spotify:artist:6TsAG8Ve1icEC8ydeHm3C8?si=Zs2jsgXWQeWsMzooRPvVRA'
gybe = 'spotify:artist:4svpOyfmQKuWpHLjgy4cdK?si=vwPlFISITsmlimeG3y8yvQ'
chat_pile = 'spotify:artist:4yRSUmhuSJ3KcIMljdh4fH?si=adESipy6Rb6CaVObiw0Y-A'
cp = 'spotify:artist:4Ge8xMJNwt6EEXOzVXju9a?si=3HWIhlbSS1OyMVJPgxXShA'
ww = 'spotify:artist:0ABk515kENDyATUdpCKVfW?si=LEqoH2maQIK8nPOyXxvAMA'
om = 'spotify:artist:4hCgC4FnYZLBgQPUMLOoiI?si=09GZrs5AToeHFXxfAXlUhA'
bh = 'spotify:artist:56ZTgzPBDge0OvCGgMO3OY?si=49ywZQ-_R5aR96c06Vk4qw'
swans = 'spotify:artist:79S80ZWgVhIPMCHuvl6SkA?si=hfBYkqCrSIqSbFtLacS2xw'
mabe_f = 'spotify:artist:7yHfb2D8qIBgrzclpSsTeo?si=QYAitEmTTAyL8Jb_mSI0UA'
billie = 'spotify:artist:6qqNVTkY8uBg9cP3Jd7DAH?si=BxuqVYG3QWiJOY346umyqg'
mcr = 'spotify:artist:7FBcuc1gsnv6Y1nwFtNRCb?si=O_r2H39sQUyxtMSnq0lLSw'
jane_r = 'spotify:artist:2rLGlNI6htigNxx172qxLu?si=pUnSPZVXQ8Cmt198_d4QUQ'

#ingresar artista
recs=sp.artist_related_artists(cp)

#seleccionar a (-1 < a < 1, preferentemente valores cercanos a 0)
# a<0 hace más probable obtener recomendaciones menos populares, a>0 regresa artistas con popularidad similar al inicial
a=-0.5

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

#función para obtener información de un artista seleccionado
def info(name,info):
  for artist in vert:
    if artist['name'] == name:
      return artist[info]


#seleccionamos aristas aleatoriamente
e=[]
for artist in vert:
  for art in vert:
    if art != artist and np.random.uniform() < f(art['popularity'],a): 
      e.append((artist['name'],art['name']))
print(len(e))
#quitamos repetidos
edges = []
for i in e:
  if  (i[1],i[0]) not in edges:
    edges.append(i) 
print(len(edges))

#construimos la gráfica con los vértices y aristas previamente seleccionados
G=nx.Graph()
G.add_nodes_from([artist['name'] for artist in vert])
G.add_edges_from(edges)
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
v_0 = random.choices(list(G.nodes()))[0]
vertices_visitados = [v_0]
for i in range(n):
  p=vect_prob(v_0)
  v = random.choices(list(G.neighbors(v_0)),weights=p)[0]
  vertices_visitados.append(v)
  v_0=v

#la moda de la caminata aleatoria es la recomendación
vv = Counter(vertices_visitados)
rec = vv.most_common(1)

print(rec[0][0],info(rec[0][0],'popularity'),rec[0][1])
print('link:',info(rec[0][0],'uri'))

