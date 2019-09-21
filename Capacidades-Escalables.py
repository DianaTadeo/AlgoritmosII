'''
Este programa implementa la representacion de una grafica en forma Matricial
Tambien implementa el algoritmo de Capacidades escalables para obtener el
flujo maximo de una red.

Autor: Diana Tadeo G.
'''
import random
import math
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
					if j==(i+1):
						#print ('entra')
						graph[i][j]= random.randint(1,maxim)
						graph[j][i]=random.randint(-maxim,-1)
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
					else:
						graph[i][j]=0
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
	def BFS(self,s, t, path, graph): 
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
			for i, val in enumerate(graph[u]): 
				if visited[i] == False and val > 0 : 
					queue.append(i) 
					visited[i] = True
					path[i] = u
		return True if visited[t] else False

	'''
	Funcion que implementa el algoritmo de Capacidades Escalables para 
	obtener el flujo maximo.
	Regresa el flujo maximo de una digrafica con capacidad
	
	s: nodo inicial o de entrada
	t: nodo final o de salida
	'''
	def capacidades_escalables(self, s, t): 
		actual=self.graphRes
		u=0
		for n in actual:
			val=max(n)
			u=val if val>u else u #Calculo el valor mayor de flujo
		if u>0:
			delta=math.pow(2,math.floor(math.log(u,2))) #calculo Delta
		else:
			print("Se genero una red sin valores aceptables")
			exit(1)
		
		
		#Creo un camino relleno de -1
		path = [-1]*(self.order) 
		max_flow = 0 
		graph=self.graphRes
		while delta >=1: #Mientras delta sea mayor o igual a 1
			print("Delta actual= %d"%delta)
			residual_actual= self.delta_Residual(delta) #genero la delta residual
			print("%d-Residual"%delta)
			for n in residual_actual:
				print(n)
			#Se repite hasta que ya no existan caminos en la delta residual
			if self.BFS(s,t,path,residual_actual): #Devuelve si hay camino S->...->T , 'path' es el camino
				print(path)
				mincam = float("Inf") 
				current = t 
				while(current!=s): #mientras no se llegue al inicial
					# Se va a elegir el menor valor de flujo de todo el camino
					mincam = min (mincam, self.graphRes[path[current]][current]) 
					# Se avanza una posicion  de regreso a s en el camino
					# si antes se tenia S->...->k->k+1->...->T y current=k+1
					# entonces se reasigna current=k y contin[ua la iteracion
					current = path[current] 
				
				max_flow += mincam #se suma el delta encontrado
				k1 = t
				while(k1 != s): 
					# Se actualizan los valores de flujo enviado por la arista entre k y k+1
					# dentro del camino S->...->k->k+1->...->T
					k = path[k1] 
					self.graphRes[k][k1] -=mincam
					self.graphRes[k1][k] += self.graphRes[k][k1]+mincam
					
					k1 = path[k1] 
			else:
				#Si ya no hay caminos, se obtiene un nuevo delta y a partir de ahi una 
				#nueva delta=residual
				delta=delta/2 
				
		print('\nRESIDUAL FINAL')
		for item in self.graphRes:
				print(item)
		return max_flow 

	"""
	Funcion auxiliar que genera una grafica delta-residual
	a partir de una grafica residual original y una delta dada
	La grafica delta-residual contiene todos los valores de la
	grafica residual original que sean mayores a la delta dada.
	"""
	def delta_Residual(self,delta):
		actual=[]
		#se realiza una copia de la residual original
		for t in range(self.order):
			row= [-1 for i in range(self.order)]
			actual.append(row)
		#Se incluyen los valores que sean mayores a la delta
		for i in range(len(actual)):
			for j in range(len(actual[i])):
				val=self.graphRes[i][j]
				#Si la capacidad en el arco de ida es mayor a la delta, se agrega
				# al igual que los valores negativos de este pues son los arcos que
				#apuntan a este nodo
				actual[i][j]= val if (val>=delta or val<=(-1*delta)) else 0
				
		return actual

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
maxflow=g.capacidades_escalables(s,t)
print("Max Flow= %d"%maxflow)
#********Si no se desea mostrar Grafica, se borra********
if grafica=='S':
	drawGraphic(g)
