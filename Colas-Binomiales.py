'''
Este programa implementa las colas binomiales a traves de heaps
y una lista de las raices de estas.

Autor: Diana Tadeo G.
'''
import math

"""
Clase que implementa la estructura de un heap
"""
class Heap:

	def __init__(self,llave): 
		self.padre= None
		self.llave= llave
		self.grado=	0
		self.hijos= []
		self.shermano= None
		

"""
Clase que implementa la estructura de colas binomiales
"""
class ColaBinomial:
	
	def __init__(self):
		self.heaps={}
		self.bk=[]
	
	"""
	Funcion que permite insertar un heap dentro de la
	cola binomial.
	new_heap: es el heap que se desea insertar a la cola binomial
	"""
	def insertar(self,new_heap):
		if new_heap.llave in self.bk: #Para no repetir raices
			return False
		por_acomodar=new_heap
		if len(self.bk)==0: #Si la cola es nueva
			self.bk.append(new_heap.llave)
			self.heaps[new_heap.llave]=new_heap
		else:
			k=new_heap.grado
			while(True): #para acomodar bk's
				if len(self.bk)-1>=k: #Si existe el espacio en la cola
					if self.bk[k]==0:#Si el espacio no esta ocupado (No existe un heap bk)
						self.bk[k]=por_acomodar.llave
						self.heaps[por_acomodar.llave]= por_acomodar
						for n in range(k,len(self.bk)):
							por_acomodar.shermano= n if n!=0 else None
						break
					else:#Si el espacio ya esta ocupado (Ya existe un heap bk)
						aux_heap=self.heaps[self.bk[k]]
						del self.heaps[self.bk[k]]
						res_heap=self.fundir(aux_heap,por_acomodar)
						self.bk[k]=0
						self.bk.append(0)
						for n in range(k,len(self.bk)):
							res_heap.shermano= n if n!=0 else None
						por_acomodar=res_heap
						k+=1
				else: #si no existe, se agrega
					self.bk.append(new_heap.llave)
					self.heaps[new_heap.llave]=por_acomodar
		return True
					
	"""
	Funcion que une dos heaps independientemente de su tamanio
	heapT: un heap a unir
	heapQ: un heap a unir
	"""
	def fundir(self, heapT, heapQ):
		if heapT.llave < heapQ.llave:
			heapQ.padre=heapT
			heapQ.shermano=None
			heapT.hijos.append(heapQ)
			heapT.grado+=1
			return heapT
		else:
			heapT.padre= heapQ
			heapT.shermano=None
			heapQ.hijos.append(heapT)
			heapQ.grado+=1
			return heapQ
	
	"""
	Funcion que permite eliminar el minimo global dentro de 
	la cola binaria.
	"""
	def eliminar_minimo(self):
		# Primero buscamos el minimo que, por las condiciones de la cola binomial
		# debe de estar hasta arriba de alg[un heap.
		minimo= float("Inf") 
		if len(self.bk)>0:
			for n in self.bk:
				if n!=0:
					minimo=n if n<minimo else minimo
		print("El minimo es: %d" %minimo)
		por_eliminar=self.heaps[minimo]
		del self.heaps[minimo]
		pos=self.bk.index(minimo)
		self.bk[pos]=0
		hijos=por_eliminar.hijos
		#Se insertan los hijos
		for h in hijos:
			print(self.insertar(h))

"""
Funcion que devuelve el formato de un heap local, es
decir, la llave del heap actual y sus hijos.
heap: heap que se mostrara en formato.
"""
def formato(heap):
	hijos=""
	for h in heap.hijos:
		hijos+=str(h.llave)+" "
	print(str(heap.llave)+" hijos["+hijos+"]")
	for n in heap.hijos:
		formato(n)
		
	
print('\n------------------------------------------------------------------\n')
print('			Colas Binomiales')
print('\n------------------------------------------------------------------\n')
elementos=raw_input('Ingrese los elementos de inicio en la cola binomial separados por comas:\n ')
Cb= ColaBinomial()
try:
	elems=elementos.split(',')
	for n in elems:
		nuevo= Heap(int(n))
		Cb.insertar(nuevo)
	h1=Cb.heaps.values()
	print("El resultado es...")
	print("Lista de bk's")
	print(Cb.bk)
	print("heaps")
	for bk in Cb.bk:
		if bk!=0:
			formato(Cb.heaps[bk])
	while(True):
		respuesta=raw_input('Desea eliminar el elemento minimo?[S/N]: ').upper()
		if respuesta=="S":
			Cb.eliminar_minimo()
			print("El resultado es...")
			print("Lista de bk's")
			print(Cb.bk)
			print("heaps")
			for bk in Cb.bk:
				if bk!=0:
					formato(Cb.heaps[bk])
		elif respuesta=="N":
			print "Terminando"
			break
		else:
			print("La entrada no es valida")
except:
	print("La entrada de datos fue incorrecta")
	
	
