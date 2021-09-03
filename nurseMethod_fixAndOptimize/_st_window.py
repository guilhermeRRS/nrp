# coding=utf-8
import gurobipy as gp
from gurobipy import GRB
import math, io, os, sys
import nurseMethod_relaxAndFix.constants as NM_FO

def _st_window_config(self, windowConfig):

	windowConfig = str(windowConfig)
	valid, partition, w_size, s_size = True, -1, -1, -1
	
	if windowConfig[0] == NM_FO.ST:
	
		partition = windowConfig[1]
		kind_w = windowConfig[2]
		kind_s = windowConfig[3]
		
		if not (partition in (NM_FO.I, NM_FO.W)):
			valid = False
		if not (kind_w in (NM_FO.PERCENT, NM_FO.NUMBER)):
			valid = False
		if not (kind_s in (NM_FO.PERCENT, NM_FO.NUMBER)):
			valid = False
			
		if valid:
			
			windowConfig = windowConfig[4:].split("|")
			w_size = [int(kind_w), int(windowConfig[0])]
			s_size = [int(kind_s), int(windowConfig[1])]
	else:
		valid = False
		
	return valid, int(partition), w_size, s_size

'''
####### set initial solution
####### setting parameters: unset region
####### unset region
####### setting parameters: fix
####### fix

####### reset region

'''
def _st_window_run(self, variables, sets, parameters, initialSolution, partition, w_size, s_size, maxTime, pathFile):
	
	solution = initialSolution
			
	I, D, T, W = self.getSetsLen(sets)
	limit = 0
	if partition == int(NM_FO.I):
		limit = I
	elif partition == int(NM_FO.W):
		limit = W
	m, x, k, y, z, v = self.getVariables(variables)
				
	timeLeft = maxTime
	maxTimeIteration = maxTime*s_size/limit
				
	sucess = False
	errors = []
					
	bestObjectives = []
	actionsTaken = []
	actionsTaken.append([0, True, ["FIX-AND-OPTIMIZE", "ST_WINDOW", partition, w_size, s_size, maxTimeIteration, timeLeft]])
	timeTaken = []
	bestBounds = []
			
	If = 0
	Il = I
	Df = 0
	Dl = D
	Wf = 0
	Wl = W
	Tf = 0
	Tl = T
			
	####### set initial solution
	for i in range(I):
		for d in range(D):
			for t in range(T):
				x[i][d][t].lb = solution["solution"][i][d][t]
				x[i][d][t].ub = solution["solution"][i][d][t]
	m.update()
	m.optimize()
			
	running = True
	try:
		currentBestObjective = m.objVal
	except:
		currentBestObjective = -1
			
	if currentBestObjective == -1:
		running = False
		actionsTaken.append([2, False, ["INITIAL_SOLUTION_OBJECTIVE_NOT_FOUND", m.Status, m.SolCount]])
			
	if running:
			
		pos = 0
		timesUpdate = 0
		timesRepeate = 0
		limitTimesRepeate = math.ceil(2*limit/s_size)
		while running and timesRepeate < limitTimesRepeate:
				
			if pos >= limit:
				pos = 0
				
			####### setting parameters: unset region
			if partition == int(NM_FO.I):
				If = min(pos, I)
				Il = min(pos+w_size, I)
			elif partition == int(NM_FO.W):
				Df = min(7*pos, D)
				Dl = min(7*pos+7*w_size, D)
					
			####### unset region
			#print(If,Il,Df,Dl)
			#input("!")
			for i in range(If, Il):
				for d in range(Df, Dl):
					for t in range(Tf, Tl):
						x[i][d][t].lb = 0
						x[i][d][t].ub = 1
							
			m.setParam('Timelimit', maxTimeIteration)
			m.update()
			m.optimize()
			m.setParam('Timelimit', "default")
					
			status = m.Status
			timeTakenIteration = min(maxTimeIteration, m.Runtime)
			timeLeft -= timeTakenIteration
			timeTaken.append(timeTakenIteration)
						
			if not (status in (GRB.OPTIMAL, GRB.TIME_LIMIT)) or m.SolCount == 0:
					
				####### reset region
				for i in range(If, Il):
					for d in range(Df, Dl):
						for t in range(Tf, Tl):
							x[i][d][t].lb = solution["solution"][i][d][t]
							x[i][d][t].ub = solution["solution"][i][d][t]
								
				actionsTaken.append([1, False, ["IF", status, m.SolCount, pos]])
								
			else:
				
				bestObjectives.append(m.objVal)
				try:
					bestBounds.append(m.objBound)
				except:
					bestBounds.append("-")
				
				rollback = True
				if currentBestObjective > bestObjectives[-1]:
						
					####### setting parameters: fix
					if partition == int(NM_FO.I):
						If = min(pos, I)
						Il = min(pos+s_size, I)
					elif partition == int(NM_FO.W):
						Df = min(7*pos, D)
						Dl = min(7*pos+7*s_size, D)
							
					####### fix
					#print(If,Il,Df,Dl)
					#input("#")
					for i in range(If, Il):
						for d in range(Df, Dl):
							for t in range(Tf, Tl):
								value = 1 if x[i][d][t].x >= 0.5 else 0
								x[i][d][t].lb = value
								x[i][d][t].ub = value
						
					m.update()
					m.optimize()
					try:
						iterationObjective = m.objVal
					except:
						iterationObjective = -1
							
					if iterationObjective < currentBestObjective:
						rollback = False
						timesUpdate += 1
						timesRepeate = 0
						currentBestObjective = iterationObjective
						actionsTaken.append([1, True, ["ITERATION_NEW_OBJECTIVE", iterationObjective, currentBestObjective, pos, timesRepeate, timesUpdate, m.Status, m.SolCount]])
							
						for i in range(If, Il):
							for d in range(Df, Dl):
								for t in range(Tf, Tl):
									solution["solution"][i][d][t] = x[i][d][t].x
							
					else:
						timesRepeate += 1
						actionsTaken.append([1, False, ["ITERATION_ALMOST_NEW_OBJECTIVE", iterationObjective, currentBestObjective, pos, timesRepeate, timesUpdate, m.Status, m.SolCount]])
						
				else:
					timesRepeate += 1
					actionsTaken.append([1, True, ["ITERATION_SAME_OBJECTIVE", bestObjectives[-1], currentBestObjective, pos, timesRepeate, timesUpdate]])
					
				if rollback:
					####### reset region
					for i in range(If, Il):
						for d in range(Df, Dl):
							for t in range(Tf, Tl):
								x[i][d][t].lb = solution["solution"][i][d][t]
								x[i][d][t].ub = solution["solution"][i][d][t]
					
				actionsTaken.append([1, True, ["ITERATION_DONE", pos, timesRepeate, timesUpdate]])
							
			pos += s_size
				
	timeLeft = max(0, timeLeft)
	if running == True:
		sucess, errors, solution = self.fillSolution(solution, I, D, sets["T"], timeLeft, bestObjectives, actionsTaken, timeTaken, bestBounds)
							
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
		sucess, errors, solution = self.getPartialSolution(x, I, D, sets["T"], timeLeft, bestObjectives, actionsTaken, timeTaken, bestBounds)
					
		if sucess == True:
			actionsTaken.append([2, False, ["SUCESS_PARTIAL_GET"]])
		else:
			actionsTaken.append([2, False, ["FAILED_PARTIAL_GET"]])
					
		sucess, errors = self.returnPartialResults_solutionAndVariables(solution, pathFile)
		if sucess:
			actionsTaken.append([2, True, ["SUCESS_PARTIAL_SAVE"]])
		else:
			actionsTaken.append([2, False, ["FAILED_PARTIAL_SAVE"]])
				
		sucess = False
		
	return sucess, errors, solution, actionsTaken