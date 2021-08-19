from nurse_model import Nurse_Model
from nurseMethod_solver import NurseMethod_Solver
from nurseMethod_relaxAndFix import NurseMethod_RelaxAndFix
import nurseMethod_relaxAndFix.constants as NM_RF

model = Nurse_Model()
model.collectData("instance04.txt")
model.loadModel("model04.lp")
model.setInitialSolution("solution04")
if model.sucess:
	model.setImproveMethod(NurseMethod_FixAndOptimize())
	model.run_improve(60, options_fo[j], "solution_fo04")
	print(model.sucess,model.errors)
	print(model.actionsTaken)
else:
	print("!",model.sucess,model.errors)