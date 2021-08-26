# coding=utf-8
import gurobipy as gp
from gurobipy import GRB
import io, os, sys
import nurseMethod_relaxAndFix.constants as NM_RF

def _st_window_config(self, windowConfig):

	windowConfig = str(windowConfig)
	
	valid, fixApproach, partition, iw_size, fw_size, rollback = True, -1, -1, -1, -1, -1
	
	if windowConfig[0] == NM_RF.ST:
	
		fixApproach = windowConfig[1]
		partition = windowConfig[2]
		rollback = windowConfig[3]
		kind_iw = windowConfig[4]
		kind_fw = windowConfig[5]
		
		if not (fixApproach in (NM_RF.BOTH, NM_RF.ONE)):
			valid = False
		if not (partition in (NM_RF.I, NM_RF.W)):
			valid = False
		if not (rollback in (NM_RF.NO_R, NM_RF.DO_R1)):
			valid = False
		if not (kind_iw in (NM_RF.PERCENT, NM_RF.NUMBER)):
			valid = False
		if not (kind_fw in (NM_RF.PERCENT, NM_RF.NUMBER)):
			valid = False
			
		if valid:
			
			windowConfig = windowConfig[6:].split("|")
			iw_size = [int(kind_iw), int(windowConfig[0])]
			fw_size = [int(kind_fw), int(windowConfig[1])]
	else:
		valid = False
		
	return valid, int(fixApproach), int(partition), iw_size, fw_size, int(rollback)

'''
####### integer to real
####### resetting integer window
####### setting parameters: real to integer
####### real to integer
####### saving solution in alternative_x
####### setting parameters: fix
####### fix

####### setting parameters: unfix infactibility (rollback 1)
####### unfix infactibility (rollback 1)

'''
def _st_window_run(self, variables, sets, parameters, fixApproach, partition, iw_size, fw_size, rollback, maxTime, pathFile):
	solution = {"status": False}
	
	I, D, T, W = self.getSetsLen(sets)
	limit = 0
	if partition == int(NM_RF.I):
		limit = I
	elif partition == int(NM_RF.W):
		limit = W
	alternative_x = []
	for i in range(I):
		alternative_x.append([])
		for d in range(D):
			alternative_x[-1].append([])
			for t in range(T):
				alternative_x[-1][-1].append(-1)
	m, x, k, y, z, v = self.getVariables(variables)
			
	timeLeft = maxTime
	maxTimeIteration = maxTime*fw_size/limit
	m.setParam('Timelimit', maxTimeIteration)
			
	sucess = False
	errors = []
				
	bestObjectives = []
	actionsTaken = []
	actionsTaken.append([0, True, ["RELAX-AND-FIX", "ST_WINDOW", fixApproach, partition, iw_size, fw_size, rollback, maxTimeIteration, timeLeft]])
	timeTaken = []
	bestBounds = []
				
	####### integer to real
	for d in range(D):
		for t in range(T):
			y[d][t].vtype = GRB.CONTINUOUS
			y[d][t].lb = 0
			z[d][t].vtype = GRB.CONTINUOUS
			z[d][t].lb = 0
			for i in range(I):
				x[i][d][t].vtype = GRB.CONTINUOUS
				x[i][d][t].lb = 0
				x[i][d][t].ub = 1
				v[i][d][t].vtype = GRB.CONTINUOUS
				v[i][d][t].lb = 0
	for i in range(I):
		for w in range(W):
			k[i][w].vtype = GRB.CONTINUOUS
			k[i][w].lb = 0
			k[i][w].ub = 1
		
	If = 0
	Il = I
	Df = 0
	Dl = D
	Wf = 0
	Wl = W
	Tf = 0
	Tl = T
			
	pos = 0
	ipos = 0
	running = True
	rollbackMode = 0
	timesInfactibility = 0
	timesInfactibilityAll = 0
	while running and (pos <= (limit - fw_size) or (rollbackMode != 0 and timeLeft > 0)): #if no problem happened + (if we reached the last partition or we are in (rollback mode and time is left))
			
		####### setting parameters: real to integer
		if partition == int(NM_RF.I):
			If = min(ipos, I)
			Il = min(pos+iw_size, I)
		elif partition == int(NM_RF.W):
			Df = min(7*ipos, D)
			Dl = min(7*pos+7*iw_size, D)
			Wf = min(ipos, W)
			Wl = min(pos+iw_size, W)
			
		####### resetting integer window
		ipos = min(pos+iw_size, limit)
			
		####### real to integer
		#print(If,Il,Df,Dl)
		#input("!")
		for d in range(Df, Dl):
			for t in range(Tf, Tl):
				y[d][t].vtype = GRB.INTEGER
				z[d][t].vtype = GRB.INTEGER
				for i in range(If, Il):
					x[i][d][t].vtype = GRB.BINARY
					v[i][d][t].vtype = GRB.INTEGER
		for i in range(If, Il):
			for w in range(Wf, Wl):
				k[i][w].vtype = GRB.BINARY
					
		#notice that if we are in rollback mode and there is time left, then if we extrapolate the limit all variables are integer already
					
		m.update()
		m.optimize()
			
		status = m.Status
		timeTakenIteration = min(maxTimeIteration, m.Runtime)
		timeLeft -= timeTakenIteration
		timeTaken.append(timeTakenIteration)
				
		if not (status in (GRB.OPTIMAL, GRB.TIME_LIMIT)) or m.SolCount == 0:
					
			actionsTaken.append([1, False, ["IF", status, m.SolCount, pos, ipos]])
						
			if status == GRB.INFEASIBLE:
						
				timesInfactibilityAll += 1
						
				try:
					m.computeIIS()
					m.write(pathFile+"."+str(timesInfactibilityAll)+".i.ilp")
					actionsTaken.append([2, True, ["INFACTIBILITY_REPORT", timesInfactibilityAll]])
				except:
					actionsTaken.append([2, False, ["INFACTIBILITY_REPORT", timesInfactibilityAll]])
					
				rollbackMode = rollback
				#if rollback == 0: #-> covered by 'else'
				if rollback == 1:

					timesInfactibility += 1
						
					if pos == 0:
						actionsTaken.append([1, False, ["IMPOSSIBLE_ROLLBACK"]])
						running = False
					else:
						if (limit - pos) > 0:
							if timeLeft*iw_size/(limit - pos) > maxTimeIteration: #here we try to expand the computing time for the nex windows if possible
								maxTimeIteration = timeLeft*iw_size/(limit - pos)
								m.setParam('Timelimit', maxTimeIteration)
						else:
							maxTimeIteration = timeLeft
							m.setParam('Timelimit', maxTimeIteration)
								
						actionsTaken.append([1, True, ["ROLLBACK", timesInfactibility]])
							
						####### setting parameters: unfix infactibility (rollback 1)
						pos -= fw_size*(2*(timesInfactibility - 1) + 1) #we go back a step while pos keeps movingo forward, this is why we do it times two
							
						if partition == int(NM_RF.I):
							If = min(pos, I)
							Il = min(pos+fw_size, I)
						elif partition == int(NM_RF.W):
							Df = min(7*pos, D)
							Dl = min(7*pos+7*fw_size, D)
							Wf = min(pos, W)
							Wl = min(pos+fw_size, W)
							
						####### unfix infactibility (rollback 1)
						#print(If,Il,Df,Dl,timesInfactibility)
						#input("@")
						for i in range(If, Il):
							for d in range(Df, Dl):
								for t in range(Tf, Tl):
									x[i][d][t].lb = 0
									x[i][d][t].ub = 1
							
						pos += fw_size*(2*(timesInfactibility - 1) + 1)
						#as if it where solved we go to the next window
							
				else:
					running = False
						
			else:
				running = False
							
		else:
					
			bestObjectives.append(m.objVal)
			try:
				bestBounds.append(m.objBound)
			except:
				bestBounds.append("-")
					
			####### saving solution in alternative_x
			for i in range(I):
				for d in range(D):
					for t in range(T):
						alternative_x[i][d][t] = x[i][d][t].x
			
			####### setting parameters: fix
			if timesInfactibility > 0:
				pos -= fw_size*(2*(timesInfactibility - 1) + 2) #we go back a step while pos keeps movingo forward, this is why we do it times two
			if partition == int(NM_RF.I):
				If = min(pos, I)
			elif partition == int(NM_RF.W):
				Df = min(7*pos, D)
			if timesInfactibility > 0:
				pos += fw_size*(2*(timesInfactibility - 1) + 2)
			if partition == int(NM_RF.I):
				Il = min(pos+fw_size, I)
			elif partition == int(NM_RF.W):
				Dl = min(7*pos+7*fw_size, D)
			timesInfactibility = 0
			rollbackMode = 0
				
			####### fix
			#print(If,Il,Df,Dl)
			#input("#")
			for i in range(If, Il):
				for d in range(Df, Dl):
					for t in range(Tf, Tl):
						value = 1 if x[i][d][t].x >= 0.5 else 0
						if fixApproach == 1:
							x[i][d][t].lb = value
							x[i][d][t].ub = value
						elif fixApproach == 2 and value == 1:
							x[i][d][t].lb = 1
							x[i][d][t].ub = 1
					
			actionsTaken.append([1, True, ["ITERATION_DONE", pos, ipos, rollbackMode, timesInfactibility]])
					
		pos += fw_size
		
	timeLeft = max(0, timeLeft)
	if running == True:
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
		sucess, errors, solution = self.getPartialSolution(alternative_x, I, D, sets["T"], timeLeft, bestObjectives, actionsTaken, timeTaken, bestBounds)	#will return nothing due to the fact that there is no solution when it happens, if you want to better study the infactibility: add a variable that has the same size of x, than add the solution found always, so, when there is a error, return it here
			
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