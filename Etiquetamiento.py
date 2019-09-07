'''
Este programa implementa la representacion de una grafica en forma Matricial
Tambien implementa el algoritmo de Etiquetamiento para obtener el
flujo maximo de una red.

Autor: Diana Tadeo G.
'''
import random
import networkx as nx #*******Si no se desea mostrar Grafica, se borra*******
import matplotlib.pyplot as plt#*******Si no se desea mostrar Grafica, se borra*******

'''
Clase que reprresenta una Grafica dirigida con atributo
de capacidad.
''' 
class GraphMatrix: 

	def __init__(self,tam, maxim): 
		
		graph=[]
		edges=[]
		distance={}
		for t in range(tam):
			row= [0 for i in range(tam)]
			graph.append(row)
		# Se rellena la matriz con valores aleatorios de capacidad
		# para representar la direccion de las aristas, si la 
		# capacidad es positiva, la arista sale desde el nodo (fila) en
		# el que se enucntre el valor positivo, si la capacidad es,
		# negativa, la arista entra hacia el nodo (fila) en donde esta
		# el valor negativo.
		for i in range(tam):
			distance[i]=-1
			for j in range(tam):
				if graph[i][j] == 0:
					if j==(i+1):
						#print ('entra')
						graph[i][j]= random.randint(1,maxim)
						graph[j][i]=random.randint(-maxim,-1)
					elif i!=j:#para evitar loops
						c= random.randint(-maxim,maxim)
						graph[i][j]= c
						if c!=0: #si hay arista...
							#Se agrega a la lista de aristas
							edges.append((i,j,c))
						else:
							graph[i][j]=0#si no hay arista, el valor es 0
					else:
						graph[j][i]=graph[i][j]*(-1)
		print('ORIGINAL')
		for i in range(tam):
			print(graph[i])
		self.graphRes = graph # grafica residual
		self.order = tam
		self.edges=edges
		self.distance=distance
		
	'''
	Devuelve una lista con los nodos de la grafica.
	'''
	def getNodes(self):
		nodes=[]
		for i in range(self.order-1):
			if i==0:
				nodes.append('S')
			elif i==(self.order-1):
				nodes.append('T')
			else:
				nodes.append(i)
		return nodes
	'''
	Devuelve una lista de las aristas de la grafica en forma de
	tuplas muestran de la siguiente forma:
		(nodo_ini, nodo_fin, capacidad)
	'''
	def getEdges(self):
		edges=[]
		for i in range(0,len(self.edges)):
			val=self.edges[i]
			n1=val[0]
			n2=val[1]
			if val[0]==0:
				n1='S'
			if val[1]==0:
				n2='S'
			if val[0]==(self.order-1):
				n1='T'
			if val[1]==(self.order-1):
				n2='T'
			#Se distingue el nodo de entrada y de salida por arista
			if val[2]>0: 
				edges.append((n1,n2, val[2]))
			if val[2]<0:
				edges.append((n2,n1, val[2]*(-1)))
		return edges
	'''
	Funcion que implementa el etiquetado de una red
	calculando las distancias.
	t: El nodo final (pozo) de la red.
	'''
	def etiqueta(self, t):
		mod=self.graphRes
		self.distance[t]=0 #La distancia de t=0
		dist=self.distance.copy() #Se obtienen las distancias de la red que inicialmente estan en -1
		nodos=[t]#Se guardan los nodos a visitar en una lista
		val=1
		copy=nodos.copy()
		while len(nodos)>0:#Se comienzan a recorrer los nodos a visitar
			fin=nodos[-1]#guardo el ultimo nodo que va a tener la distancia actual
			actual=nodos.pop(0)#Nodo visitado
			aux=[]
			for i in range(len(mod[actual])): #por cada elemento en la fila
				if mod[actual][i]<0 and actual!=i: #si hay arista al nodo actual desde ese elemento
					if dist[i]==-1:#si el valor es -1
						dist[i]=val#se le asigna la nueva distancia al elemento
						if copy.count(i)==0:#Si ese elemento no existe actualmente
							nodos.append(i)#lo agregamos a la lista de nodo
							copy.append(i)
			if actual == fin:#Si llego al ultimo nodo que debe tener esa distancia, aumento el valor
				val+=1
		self.distance=dist.copy()#Al terminar actualizo las distancias de la red
	
	'''
	Funcion que implementa la subrutina 'avanza(i)' del
	algoritmo de etiquetamiento
	i: nodo activo
	j: nodo siguiente
	path: ruta que se lleva hasta el momento y reemplaza
		  la funcion pred(i)
	'''
	def avanza(self,i,j,path):
		path.append(j)
		return j
	
	'''
	Funcion que implementa la subrutina 'retrocede(i)' del
	algoritmo de etiquetamiento
	i: nodo activo
	j: nodo siguiente(para saber si se puede seguir por ese camino despues)
	path: ruta que se lleva hasta el momento y reemplaza
		  la funcion pred(i)
	'''
	def retrocede(self, i,j):
		dist_minx=self.distance[i]
		#Revisamos el minimo de las distancias
		dist_minx= self.distance[j] if self.distance[j] < dist_minx else dist_minx
		self.distance[i]=dist_minx+1#reemplazamos la distancia de i

	'''
	Implementacion del algoritmo de etiquetamiento
	s: Nodo inicial
	t: Nodo final
	'''
	def laveling_algorithm(self,s, t):
		self.etiqueta(t)# Etiquetamos los nodos obteniendo las distancias
		print("\nLas distancias iniciales \'nodo: distancia\'\n")
		print(self.distance)
		i=s
		path=[s]
		paro=t+1
		maxflow=0 #Para guardar el flujo maximo
		deltaMx=0
		
		while (self.distance[s]<paro or deltaMx==maxflow) and self.distance[s]>0: #while d(s)<n do
			flow_rest=0 #Calculamos si aun se puede enviar flujo desde ese nodo
			for j in self.graphRes[i]:
				flow_rest+=j if j>0 else 0
			if flow_rest<=0:
				print('\n* Se detiene porque ya no se puede enviar mas flujo por Node(%d)'%i)
				print('y no hay mas caminos*\n')
				break
			dist_i=self.distance[i]
			dist_x=0
			for j in range(len(self.graphRes[i])):#Recorremos los posibles vecinos del nodo i
				if self.graphRes[i][j]>0: #Si hay arista que sale de i -> j
					dist_x=self.distance[j]		# Si
					if dist_i==(dist_x+1):   	# Tiene un arco admisible
						i=self.avanza(i,j,path)	# avanza(i)
						if i==t: 				#if i=t then
							print('La ruta elegida es: ')
							print(path)
							
							#---------inicia aumenta(i)--------------
							cap=[]
							# Obtengo las capacidades de las aristas entre
							# los elementos de la ruta
							for i in range(len(path)-1): 
								cap.append(self.graphRes[path[i]][path[i+1]])
							flow=min(cap) # obtengo delta
							# Cambio las capacidades en la residual
							for elem in range(len(path)-1):
								cant=self.graphRes[path[elem]][path[elem+1]]
								self.graphRes[path[elem]][path[elem+1]]=cant-flow
								self.graphRes[path[elem+1]][path[elem]]=(cant*-1)+flow
							print('\nResidual Actual')
							for index in range(len(self.graphRes)):
								print(self.graphRes[index])
							path=[s]
							#----------acaba aumenta(i)---------------
							maxflow+=flow
							i=s
						else:
							break
					else:
						self.retrocede(i,j)#retrocede(i)
			for j in self.graphRes[s]:
				deltaMx+=j if j>0 else 0
						
		print('\n===RESIDUAL FINAL====')
		for elem in self.graphRes:
			print(elem)
		print('\nFlujo Maximo: %d'%maxflow)
	
'''
Funcion que dibuja la grafica dirigida con atributos
que se le pase como argumento
'''
#*******Si no se desea mostrar Grafica, se borra*******
def drawGraphic(graph):
	G = nx.DiGraph()

	for item in graph.getNodes():
		G.add_node(item, color='blue')
	for item in graph.getEdges():
		G.add_edge(item[0], item[1], c=item[2])
	pos=nx.spring_layout(G)
	nx.draw_networkx_nodes(G,pos,
						nodelist=G.nodes,
						node_color='#ffa555',
						node_size=500,
						alpha=0.8)

	nx.draw_networkx_edges(G,pos,width=1.0,alpha=0.5)     
	edge_labels=nx.get_edge_attributes(G,'c')
	nx.draw_networkx_edge_labels(G,pos,
                       labels=edge_labels,
                       width=3,alpha=0.5,edge_color='#444140') 
	nx.draw_networkx_labels(G,pos,font_size=16)
	plt.axis('off')
	plt.show()		

print('\n------------------------------------------------------------------\n')
print('			ALGORITMO DE ETIQUETADO')
print('\n------------------------------------------------------------------\n')
nodes=int(input('Ingrese la cantidad de nodos: '))
maxim=int(input('Ingresela cangtidad maxima de capacidad para las aristas: '))
grafica=str(input('Desea mostrar la red de forma gr[afica?[S/N] (Default N)'))#****Si no se desea mostrar grafica, se borra
print('\n*--Representacion--*\n')
g = GraphMatrix(nodes,maxim) 
s = 0; t=g.order-1
g.laveling_algorithm(s,t)
#********Si no se desea mostrar Grafica, se borra********
if grafica=='S':
	drawGraphic(g)
