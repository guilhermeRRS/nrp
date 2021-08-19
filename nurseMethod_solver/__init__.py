# coding=utf-8
import gurobipy as gp
from gurobipy import GRB
from dad_nurseMethods import Dad_NurseMethods

class NurseMethod_Solver(Dad_NurseMethods):

	def run(self, variables, sets, parameters, arguments):
		solution = {"status": False}
		
		if len(arguments) == 2:
			
			sucess = True
			errors = []
			
			time = arguments[0]
			timeLeft = time
			pathFile = arguments[1]
			
			I, D, T, W = self.getSetsLen(sets)
			m, x, k, y, z, v = self.getVariables(variables)
			
			bestObjectives = []
			actionsTaken = []
			actionsTaken.append([0, True, ["SOLVER", time]])
			timeTaken = []
			bestBounds = []
			
			m.setParam('Timelimit', time)
			m.optimize()
			
			status = m.Status
			timeTaken.append(min(max(0, m.Runtime), time))
			timeLeft -= timeTaken[-1]
			
			if not (status in (GRB.OPTIMAL, GRB.TIME_LIMIT)) or m.SolCount == 0:
				sucess = False
				actionsTaken.append([1, False, ["IF", status, m.SolCount]])
				
			else:
				try:
					bestObjectives.append(m.objVal)
					
					try:
						bestBounds.append(m.objBound)
					except:
						bestBounds.append("-")
						
					actionsTaken.append([1, True, ["ITERATION_DONE"]])
				except:
					sucess = False
					actionsTaken.append([1, False, ["EXCEPT", status, m.SolCount]])
			
			if sucess == True:
				sucess, errors, solution = self.getSolution(x, I, D, sets["T"], timeLeft, bestObjectives, actionsTaken, timeTaken, bestBounds)
				
				if sucess == True:
					actionsTaken.append([2, True, ["SUCESS"]])
					sucess, errors = self.returnResults_solutionAndVariables(solution, pathFile)
					
					if sucess:
						actionsTaken.append([2, True, ["SUCESS_SAVE"]])
					else:
						actionsTaken.append([2, False, ["FAILED_SAVE"]])
					
				else:
					actionsTaken.append([2, False, ["FAILED_GET"]])
					
			else:
				actionsTaken.append([2, False, ["FAILED_RUN"]])
					
			return sucess, errors, solution, actionsTaken
			
		else:
			return False, ["Error: Approach_Solver requires two arguments when run ('time', 'pathFile')"], solution, []