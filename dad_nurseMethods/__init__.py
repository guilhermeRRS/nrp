# coding=utf-8
import gurobipy as gp
from gurobipy import GRB
import io, sys, os
'''
actionsTaken

append([*])
* -> Digit 1, Digit 2, List

Digit 1:
0 -> config
1 -> related to algoritm (happened in method)
2 -> related to code (happened while saving or computing something)

Digit 2:
True if sucess or neutral
False if error

List -> more data
'''

class Dad_NurseMethods:

	def getSetsLen(self, sets):
		#I, D, T, W
		return len(sets["I"]), len(sets["D"]), len(sets["T"]), len(sets["W"])
		
	def getVariables(self, variables):
		#m, x, k, y, z, v
		return variables["m"], variables["x"], variables["k"], variables["y"], variables["z"], variables["v"]
		
	def _readableSolution(self, solution, I, D, T_set, partial = False):
		readable = []
		if not partial:
			T = len(T_set)
			
			readable = []
			for i in range(I):
				readable.append([])
				for d in range(D):
					shift = ""
					for t in range(T):
						if solution[i][d][t] >= 0.5:
							shift = T_set[t]
					readable[-1].append(shift)
						
		return readable
		
	def getSolution(self, x, I, D, T_set, timeLeft, bestObjectives = [], actionsTaken = [], timeTaken = [], bestBounds = [], partial = False):
		T = len(T_set)
		sucess = True
		errors = []
		solution = []
		
		if not partial:
		
			try:
				for i in range(I):
					solution.append([])
					for d in range(D):
						solution[-1].append([])
						for t in range(T):
							solution[-1][-1].append(x[i][d][t].x)
			except:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				self.errors = ["While getting the solution",partial, exc_type, fname, exc_tb.tb_lineno]
				sucess = False
				solution = []
				
		else:
		
			try:
				for i in range(I):
					solution.append([])
					for d in range(D):
						solution[-1].append([])
						for t in range(T):
							solution[-1][-1].append(x[i][d][t]) #notice here x is a matrix, not a var from the problem!!!
			except:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				self.errors = ["While getting the solution",partial, exc_type, fname, exc_tb.tb_lineno]
				sucess = False
				solution = []
			
		solution = {"status": sucess, "solution": solution, "readable": self._readableSolution(solution, I, D, T_set, partial), "timeLeft": timeLeft, "bestObjectives": bestObjectives, "actionsTaken": actionsTaken, "timeTaken": timeTaken, "bestBounds": bestBounds}
		
		return sucess, errors, solution
	
	def getPartialSolution(self, x, I, D, T_set, timeLeft, bestObjectives = [], actionsTaken = [], timeTaken = [], bestBounds = []):
		return self.getSolution(x, I, D, T_set, timeLeft, bestObjectives, actionsTaken, timeTaken, bestBounds, True)
		
	def fillSolution(self, solution, I, D, T_set, timeLeft, bestObjectives = [], actionsTaken = [], timeTaken = [], bestBounds = [], partial = False):
		T = len(T_set)
		sucess = True
		errors = []
		solution = solution["solution"]
		
		solution = {"status": sucess, "solution": solution, "readable": self._readableSolution(solution, I, D, T_set, partial), "timeLeft": timeLeft, "bestObjectives": bestObjectives, "actionsTaken": actionsTaken, "timeTaken": timeTaken, "bestBounds": bestBounds}
		
		return sucess, errors, solution
	
	from ._returnResults import returnResults_solutionAndVariables, returnPartialResults_solutionAndVariables