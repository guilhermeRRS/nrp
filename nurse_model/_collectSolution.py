# coding=utf-8
import io

def readFile(path):
	sucess = 1
	errors = []
	fileConteds = []	
	try:	
		with io.open(path, "r", encoding = "utf8") as file:		
			fileConteds = file.read()
	except:
		sucess = 0
		errors.append("Error: Not able to open file ["+path+"]")
		
	return sucess, errors, fileConteds
	
def _get_initialSolution(self, path, sets):	#we assume that it is always inserted a valid solution
	solution = []
	timeLeft = 0
	
	sucess, errors, fileConteds	= readFile(path)
	if(sucess):
	
		fileConteds = fileConteds.split("\n")
		
		if len(fileConteds) == 1:
			if fileConteds[1] == "":
				sucess = False
		
		if sucess:
		
			timeLeft = fileConteds[0]
			fileConteds = fileConteds[1:]
			
			I = len(sets["I"])
			D = len(sets["D"])
			T = len(sets["T"])
			
			for i in range(I):
				solution.append([])
				line = fileConteds[i].split("\t")
				for d in range(D):
					solution[-1].append([])
					for t in range(T):
						solution[-1][-1].append(0)
					if line[d] != "":
						solution[-1][-1][sets["T"].index(line[d])] = 1
		
	return sucess, errors, {"status": sucess, "solution": solution, "readable": [], "timeLeft": timeLeft, "bestObjectives": [], "actionsTaken": [], "timeTaken": [], "bestBounds": []}