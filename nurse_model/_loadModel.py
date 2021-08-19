# coding=utf-8
import gurobipy as gp
from gurobipy import GRB

'''
This function is responsable for collecting the model since it is in an stardad format in which the vars have the following name structure
unidimesional: b[i] -> b is the var and i the dimension
bidimesional: b[i][j] -> b is the var and i the first dimension and j the second
and so on
'''
def _get_model(self, path, I, D, T, W):
	
	'''
	m -> model
	x, k, y, z, v -> variables of the model
	'''
	
	m = gp.read(path) #we assume that there is the file and no error will occur
	
	x = []
	k = []
	y = []
	z = []
	v = []
	for i in range(I):
		x.append([])
		v.append([])
		for d in range(D):
			x[-1].append([])
			v[-1].append([])
			for t in range(T):
				x[-1][-1].append(m.getVarByName("x["+str(i)+"]["+str(d)+"]["+str(t)+"]"))
				v[-1][-1].append(m.getVarByName("v["+str(i)+"]["+str(d)+"]["+str(t)+"]"))
				
		k.append([])
		for w in range(W):
			k[-1].append(m.getVarByName("k["+str(i)+"]["+str(w)+"]"))
	
	for d in range(D):
		y.append([])
		z.append([])
		for t in range(T):
			y[-1].append(m.getVarByName("y["+str(d)+"]["+str(t)+"]"))
			z[-1].append(m.getVarByName("z["+str(d)+"]["+str(t)+"]"))
	
	return m, x, k, y, z, v