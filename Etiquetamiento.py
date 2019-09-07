'''
Este programa implementa 2 tipos de representacion de una grafica:
	-Matricial
	-En Listas
Tambien implementa el algoritmo de ford-fulkerson para obtener el
flujo maximo de una red.

Autor: Diana Tadeo G.
'''
import random
import networkx as nx
import matplotlib.pyplot as plt

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

	def etiqueta(self, t):
		mod=self.graphRes
		self.distance[t]=0
		dist=self.distance.copy()
		totnodos=self.getNodes()
		nodos=[t]
		val=1
		copy=nodos.copy()
		while len(nodos)>0:
			fin=nodos[-1]
			actual=nodos.pop(0)
			aux=[]
			for i in range(len(mod[actual])): #por cada elemento en la fila
				if mod[actual][i]<0 and actual!=i: #si hay arista al nodo actual desde ese elemento
					if dist[i]==-1:#si el valor es -1
						dist[i]=val#se le asigna la nueva distancia al elemento
						if copy.count(i)==0:#Si ese elemento no existe actualmente
							nodos.append(i)#lo agregamos a la lista de nodo
							copy.append(i)

			if actual == fin:
				val+=1

		self.distance=dist.copy()
	
	def avanza(self,i,j,path):
		path.append(j)
		return j

	def retrocede(self, i,j, path):
		dist_i=0
		dist_minx=self.distance[i]
		dist_minx= self.distance[j] if self.distance[j] < dist_minx else dist_minx
		self.distance[i]=dist_minx+1


	def laveling_algorithm(self,s, t):
		self.etiqueta(t)
		print("\nLas distancias iniciales \'nodo: distancia\'\n")
		print(self.distance)
		i=s
		path=[s]
		paro=t+1
		maxflow=0
		
			
		deltaMx=0
		
		while (self.distance[s]<paro or deltaMx==maxflow) and self.distance[s]>0: #while d(s)<n do
			maxflow=0
			for j in self.graphRes[i]:
				maxflow+=j if j>0 else 0
			if maxflow<=0:
				print('\n* Se detiene porque ya no se puede enviar mas flujo por Node(%d)'%i)
				print('y no hay mas caminos*\n')
				break
			#print('Entra al while con i: %d'%i)
			#print('path salida')
			#print(path)
			#print('Val d= %d  val paro= %d distance[i]: %d'%(self.distance[s],paro, self.distance[i]))
			dist_i=self.distance[i]
			dist_x=0
			for j in range(len(self.graphRes[i])):
				#print('j es: %d' %j)
				if self.graphRes[i][j]>0:
					dist_x=self.distance[j]# Si
					#print('El val es %d - distance[j]: %d' %(self.graphRes[i][j], dist_x))
					if dist_i==(dist_x+1):   # Tiene un arco admisible
						#print('dist_i= %d - dist_x=%d -  self.graphRes[i][j]= %d'%(dist_i,dist_x, self.graphRes[i][j]))
						i=self.avanza(i,j,path)# avanza(i)
						#print('Tengo mi i= %d'%i)
						if i==t: #if i=t then
							print('La ruta elegida es: ')
							print(path)
							#print('Llego al fin')
							#////inicia aumenta(i)
							cap=[]
							#print('Calculo delta...')
							for i in range(len(path)-1):
								#print('delta_actual[%d][%d]=%d'%(path[i],path[i+1],self.graphRes[i][i+1]))
								cap.append(self.graphRes[path[i]][path[i+1]])
							#print(cap)
							flow=min(cap) #delta
							for elem in range(len(path)-1):
								cant=self.graphRes[path[elem]][path[elem+1]]
								self.graphRes[path[elem]][path[elem+1]]=cant-flow
								self.graphRes[path[elem+1]][path[elem]]=(cant*-1)+flow
								#print('CANT: %d, delta: %d, ij: %d, ji:%d'%(cant,flow,self.graphRes[path[elem]][path[elem+1]],self.graphRes[path[elem+1]][path[elem]]))
							print('\nResidual Actual')
							for index in range(len(self.graphRes)):
								print(self.graphRes[index])
							path=[s]
							#//////acaba aumenta(i)
							i=s
						else:
							break
					else:
						self.retrocede(i,j, path)#retrocede(i)
			for j in self.graphRes[s]:
				deltaMx+=j if j>0 else 0
						
		print('\n===RESIDUAL FINAL====')
		for elem in self.graphRes:
			print(elem)
	
'''
Funcion que dibuja la grafica dirigida con atributos
que se le pase como argumento
'''
def drawGraphic(graph):
	G = nx.DiGraph()

	for item in graph.getNodes():
		G.add_node(item, color='blue')
	for item in graph.getEdges():
		G.add_edge(item[0], item[1], c=item[2])
	pos=nx.spring_layout(G)
	nx.draw_networkx_nodes(G,pos,
						nodelist=G.nodes,
						node_color='#ffa987',
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
print('Obtener el maximo valor de flujo solo esta disponible para la')
print('representacion de matriz, pero se pueden visualizar ambas')
print('representaciones.')
print('\n------------------------------------------------------------------\n')
nodes=int(input('Ingrese la cantidad de nodos: '))
maxim=int(input('Ingresela cangtidad maxima de capacidad para las aristas: '))
print('Ingrese la representacion que desea visualizar.')
print('\n*--Representacion--*\n')
g = GraphMatrix(nodes,maxim) 
s = 0; t=g.order-1
g.laveling_algorithm(s,t)
#drawGraphic(g)
#print ("El flujo maximo es %d " % g.FordFulkerson(s, t)) 
