from nurse_model import Nurse_Model
from nurseMethod_solver import NurseMethod_Solver
from nurseMethod_relaxAndFix import NurseMethod_RelaxAndFix
import nurseMethod_relaxAndFix.constants as NM_RF

model = Nurse_Model()
model.collectData("instance04.txt")	#path of the instance
model.loadModel("model04.lp")	#path of the model
model.setConstructMethod(NurseMethod_RelaxAndFix())
model.run_construct(60, (NM_RF.ST_BOTH_W_NO_N_N+"%d"+NM_RF.BRAKE+"%d") % (1, 1), "solution04")
print(model.sucess,model.errors)
input(model.actionsTaken)