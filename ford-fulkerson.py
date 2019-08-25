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
		for t in range(tam):
			row= [-1 for i in range(tam)]
			graph.append(row)
		# Se rellena la matriz con valores aleatorios de capacidad
		# para representar la direccion de las aristas, si la 
		# capacidad es positiva, la arista sale desde el nodo (fila) en
		# el que se enucntre el valor positivo, si la capacidad es,
		# negativa, la arista entra hacia el nodo (fila) en donde esta
		# el valor negativo.
		for i in range(tam):
			for j in range(tam):
				if graph[i][j] == -1:
					if i!=j:#para evitar loops
						c= random.randint(-maxim,maxim)
						graph[i][j]= c
						if c!=0: #si hay arista...
							#Se agrega a la lista de aristas
							edges.append((i,j,c))
						else:
							graph[i][j]=0 #si no hay arista, el valor es 0
					#else:
						graph[j][i]=graph[i][j]*(-1)
		print('ORIGINAL')
		for i in range(tam):
			print(graph[i])
		self.graphRes = graph # grafica residual
		self. order = tam
		self.edges=edges
		
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
	Funcion que regresa 'True' si hay un camino de S a T y falso
	en caso contrario. A su vez, llena una lista de nodos con el
	camino encontrado.
	'''
	def BFS(self,s, t, path): 
		#Se inicializan todos los nodos como 'no visitados'
		visited =[False]*(self.order) 
		queue=[] 
		
		#Para iniciar con 'S'
		queue.append(s) 
		visited[s] = True
		
		while queue: 
			u = queue.pop(0) 
			# Se obtienen todos los nodos adyacentes al actual y
			# se meten a la pila. Se marcan como 'visitados'
			for i, val in enumerate(self.graphRes[u]): 
				if visited[i] == False and val > 0 : 
					queue.append(i) 
					visited[i] = True
					path[i] = u 
		return True if visited[t] else False
			
	
	'''
	Funcion que implementa el algoritmo Ford-Fulkerson para 
	obtener el flujo maximo.
	Regresa el flujo maximo de una digrafica con capacidad (red)
	s: nodo inicial o de entrada
	'''
	def FordFulkerson(self, s, t): 
		#Creo un camino relleno de -1
		path = [-1]*(self.order) 
		max_flow = 0 

		#Se repite hasta que ya no existan caminos
		while self.BFS(s,t,path): #Devuelve si hay camino S->...->T , 'path' es el camino
			delta = float("Inf") 
			current = t 
			while(current!=s): #mientras no se llegue al inicial
				# Se va a elegir el menor valor de flujo de todo el camino
				delta = min (delta, self.graphRes[path[current]][current]) 
				# Se avanza una posicion  de regreso a s en el camino
				# si antes se tenia S->...->k->k+1->...->T y current=k+1
				# entonces se reasigna current=k y contin[ua la iteracion
				current = path[current] 
				
			max_flow += delta #se suma el delta encontrado
			k1 = t
			while(k1 != s): 
				# Se actualizan los valores de flujo enviado por la arista entre k y k+1
				# dentro del camino S->...->k->k+1->...->T
				k = path[k1] 
				self.graphRes[k][k1] -= delta
				self.graphRes[k1][k] += delta
				k1 = path[k1] 
		print('RESIDUAL')
		for item in self.graphRes:
			print(item)
		return max_flow 

'''
Clase que reprresenta una Grafica dirigida con atributo
de capacidad, en forma de listas
''' 
class GraphLists:
	def __init__(self, tam, maxim):
		nodes=[i for i in range(tam)]
		edges=[]
		for i in range(tam):
			for j in range(i+1,tam):
				res= random.randint(-1,1)
				if res==1:
					edge=(i,j,random.randrange(maxim))
					edges.append(edge)
				if res==-1:
					edge=(j,i,random.randrange(maxim))
					edges.append(edge)
		self.order=tam
		self.nodes=nodes
		self.edges=edges
		
	'''
	Devuelve una lista con los nodos de la grafica
	'''
	def getNodes(self):
		nodes=[]
		for i in self.nodes:
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
		for i in self.edges:
			n1=i[0]
			n2=i[1]
			if i[0]==0:
				n1='S'
			if i[1]==0:
				n2='S'
			if i[0]==(self.order-1):
				n1='T'
			if i[1]==(self.order-1):
				n2='T'
			edges.append((n1,n2, i[2]))
		print(edges)
		return edges
		
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
rep=int(input('\n1.Matriz\n2.Listas\n'))
if rep ==1:
	print('\n*--Representacion--*\n')
	g = GraphMatrix(nodes,maxim) 
	s = 0; t=g.order-1
	print ("El flujo maximo es %d " % g.FordFulkerson(s, t)) 
	drawGraphic(g)
elif rep ==2:
	print('\n*--Representacion--*\n')
	g=GraphLists(nodes,maxim)
	drawGraphic(g)
