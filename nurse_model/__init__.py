# coding=utf-8
import io, sys, os

class Nurse_Model:

	dataInserted = False
	modelLoaded = False
	constructMethodSet = False
	improveMethodSet = False
	solutionSaved = False
	
	errors = []
	sucess = False
	actionsTaken = []
	
	sets = {}
	parameters = {}
	variables = {}
	construct_method = False #construct method: solver, relax-and-fix...
	improve_method = False #improve solution method: fix-and-optimize...
	solution = {"status": False} #directly loaded or from construct method
	
	from ._collectData import _get_data
	
	#this function is responsable for collecting the sets and parameters of the model and its data
	def collectData(self, path):
		
		self.errors = []
		self.sucess = True
	
		sucess, sets, parameters = self._get_data(path)
		
		if sucess == False:
		
			self.errors = sets #when there is no sucess, 'sets' return will be 'errors'
			self.sucess = False
			
		else:
		
			self.dataInserted = True
			self.sets = sets
			self.parameters = parameters
			
	from ._loadModel import _get_model
	
	def loadModel(self, path):
		
		self.errors = []
		self.sucess = True
		
		if self.dataInserted == True:
		
			m, x, k, y, z, v = self._get_model(path, len(self.sets["I"]), len(self.sets["D"]), len(self.sets["T"]), len(self.sets["W"]))
			self.variables = {"m": m, "x": x, "k": k, "y": y, "z": z, "v": v}
			self.modelLoaded = True
			
		else:
		
			self.sucess = False
			self.errors.append("Error: The data was not collected, call function 'collectData'")
			
	def setConstructMethod(self, construct_method):
		self.errors = []
		self.sucess = True
		self.construct_method = construct_method
		self.constructMethodSet = True
		
	def run_construct(self, *argv):
		self.actionsTaken = []
		self.errors = []
		self.sucess = False
			
		if not self.dataInserted:
			self.errors.append("Error: The data must be collected before run (call 'collectData')")
			
		if not self.modelLoaded:
			self.errors.append("Error: An model must be loaded before run (call 'loadModel')")
		
		if not self.constructMethodSet:
			self.errors.append("Error: An construct method must be added before run (call 'setConstructMethod')")
			
		if self.constructMethodSet and self.dataInserted and self.modelLoaded:
		
			try:
				sucess, errors, solution, actionsTaken = self.construct_method.run(self.variables, self.sets, self.parameters, argv)
				self.sucess = sucess
				self.errors = errors
				self.actionsTaken = actionsTaken
				
				if sucess:
					self.solutionSaved = True
					self.solution = solution
					
			except:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				self.errors = ["An exception happened while running the construct method", exc_type, fname, exc_tb.tb_lineno]
	
	from ._collectSolution import _get_initialSolution
	
	def setInitialSolution(self, path):
		
		self.errors = []
		self.sucess = True
		
		if self.dataInserted:
	
			sucess, errors, solution = self._get_initialSolution(path, self.sets)
		
			if sucess == False:
		
				self.errors = errors
				self.sucess = False
			
			else:
		
				self.solutionSaved = True
				self.solution = solution
				
		else:
			self.errors.append("Error: The data must be collected before collect an initial solution (call 'collectData')")
	
	def setImproveMethod(self, improve_method):
		self.errors = []
		self.sucess = True
		self.improve_method = improve_method
		self.improveMethodSet = True
		
	def run_improve(self, *argv):
		self.actionsTaken = []
		self.errors = []
		self.sucess = False
			
		if not self.dataInserted:
			self.errors.append("Error: The data must be collected before run (call 'collectData')")
			
		if not self.modelLoaded:
			self.errors.append("Error: An model must be loaded before run (call 'loadModel')")
		
		if not self.improveMethodSet:
			self.errors.append("Error: An improve method must be added before run (call 'setImproveMethod')")
		
		if not self.solutionSaved:
			self.errors.append("Error: An initial solution must be added before run (call 'setInitialSolution')")
			
		if self.improveMethodSet and self.dataInserted and self.modelLoaded and self.solutionSaved:
		
			try:
				sucess, errors, solution, actionsTaken = self.improve_method.run(self.variables, self.sets, self.parameters, self.solution, argv)
				self.sucess = sucess
				self.errors = errors
				self.actionsTaken = actionsTaken
				
				if sucess:
					self.solutionSaved = True
					self.solution = solution
					
			except:
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				self.errors = ["An exception happened while running the improve method", exc_type, fname, exc_tb.tb_lineno]