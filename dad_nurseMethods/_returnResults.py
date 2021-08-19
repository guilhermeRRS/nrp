import io

def printContent(data, pathFile):
	
	errors = []
	sucess = True
		
	try:
		file = io.open(pathFile, "w+", encoding = "utf8")
		file.write(data)
				
	except Exception as e:
		errors.append("Error: Not able to add file in "+pathFile)
		sucess = False
			
	return errors, sucess

def readableSolution_to_string(solution):
	
	stringSolution = str(solution["timeLeft"])+"\n"
	solution = solution["readable"]
	
	for i in range(len(solution)):
		for d in range(len(solution[i])):
			stringSolution = stringSolution+solution[i][d]
			if d < len(solution[i]):
				stringSolution = stringSolution + "\t"
		if i < len(solution):
			stringSolution = stringSolution + "\n"
			
	return stringSolution

def variables_to_string(solution):
	
	bestObjectives, bestBounds, actionsTaken, timeTaken = solution["bestObjectives"], solution["bestBounds"], solution["actionsTaken"], solution["timeTaken"]
	
	stringBestObjectives = "Best Objectives: "
	if len(bestObjectives) == 0:
		bestObjectives = stringBestObjectives + "None"
	else:
		len_bestObjectives = len(bestObjectives)
		for i in range(len_bestObjectives):
			stringBestObjectives = stringBestObjectives+str(bestObjectives[i])
			if i < len_bestObjectives - 1:
				stringBestObjectives = stringBestObjectives+"; "
	
	stringBestBounds = "Best Bounds: "
	if len(bestBounds) == 0:
		stringBestBounds = stringBestBounds + "None"
	else:
		len_bestBounds = len(bestBounds)
		for i in range(len_bestBounds):
			stringBestBounds = stringBestBounds+str(bestBounds[i])
			if i < len_bestBounds - 1:
				stringBestBounds = stringBestBounds+"; "
				
	stringActionsTaken = "Actions Taken: "
	if len(actionsTaken) == 0:
		stringActionsTaken = stringActionsTaken + "None"
	else:
		len_actionsTaken = len(actionsTaken)
		for i in range(len_actionsTaken):
			stringActionsTaken = stringActionsTaken+str(actionsTaken[i])
			if i < len_actionsTaken - 1:
				stringActionsTaken = stringActionsTaken+"; "
	
	stringTimeTaken = "Time Taken: "
	if len(timeTaken) == 0:
		stringTimeTaken = stringTimeTaken + "None"
	else:
		len_timeTaken = len(timeTaken)
		for i in range(len_timeTaken):
			stringTimeTaken = stringTimeTaken+str(timeTaken[i])
			if i < len_timeTaken - 1:
				stringTimeTaken = stringTimeTaken+"; "
	
	return stringBestObjectives+"\n"+stringBestBounds+"\n"+stringActionsTaken+"\n"+stringTimeTaken
	
def returnResults_solutionAndVariables(self, solution, pathFile, partial = False):
	sucess = False
	errors = []
	
	if not partial:
		stringSolution = readableSolution_to_string(solution)
		errors1, sucess1 = printContent(stringSolution, pathFile+".s.txt")
	else:
		stringSolution = str(solution["timeLeft"])+"\n"+str(solution["solution"])
		errors1, sucess1 = printContent(stringSolution, pathFile+".sf.txt")
		
	stringVariables = variables_to_string(solution)
	if not partial:
		errors2, sucess2 = printContent(stringVariables, pathFile+".v.txt")
	else:
		errors2, sucess2 = printContent(stringVariables, pathFile+".vf.txt")
		
	sucess = sucess1 and sucess2
	errors = errors1 + errors2
		
	if sucess1 != sucess2:
		errors = ["UNEXPECTED", "It "+("was" if sucess1 else "wasn't")+" possible to save the solution but we "+("did" if sucess2 else "didn't")+" save the variables"] + errors
	
	return sucess, errors
	
def returnPartialResults_solutionAndVariables(self, solution, pathFile):
	return self.returnResults_solutionAndVariables(solution, pathFile, True)