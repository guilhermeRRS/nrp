from nurse_model import Nurse_Model
from nurseMethod_solver import NurseMethod_Solver
from nurseMethod_relaxAndFix import NurseMethod_RelaxAndFix
import nurseMethod_relaxAndFix.constants as NM_RF

model = Nurse_Model()
model.collectData("instance04.txt")
model.loadModel("model04.lp")
model.setConstructMethod(NurseMethod_Solver())
model.run_construct(30, "solution04")
print(model.sucess, model.errors)
input(model.actionsTaken)