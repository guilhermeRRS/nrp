# coding=utf-8
from dad_nurseMethods import Dad_NurseMethods
import nurseMethod_relaxAndFix.constants as NM_RF
import math

class NurseMethod_RelaxAndFix(Dad_NurseMethods):

    from ._st_window import _st_window_config, _st_window_run
    
    def run(self, variables, sets, parameters, arguments):
        solution = {"status": False}
        actionsTaken = []
        
        if len(arguments) == 3:
        
            sucess = True
            errors = []
            
            time = arguments[0]
            valid, fixApproach, partition, iw_size, fw_size, rollback = self._st_window_config(arguments[1])
            pathFile = arguments[2]
            
            if valid:
                
                if partition == int(NM_RF.I):
                    if iw_size[0] == int(NM_RF.NUMBER):
                        iw_size = min(iw_size[1], len(sets["I"]))
                    elif iw_size[0] == int(NM_RF.PERCENT):
                        iw_size = math.ceil(0.01*iw_size[1]*len(sets["I"]))
                        
                    if fw_size[0] == int(NM_RF.NUMBER):
                        fw_size = min(fw_size[1], len(sets["I"]))
                    elif fw_size[0] == int(NM_RF.PERCENT):
                        fw_size = math.ceil(0.01*fw_size[1]*len(sets["I"]))
                        
                elif partition == int(NM_RF.W):
                
                    if iw_size[0] == int(NM_RF.NUMBER):
                        iw_size = min(iw_size[1], len(sets["W"]))
                    elif iw_size[0] == int(NM_RF.PERCENT):
                        iw_size = math.ceil(0.01*iw_size[1]*len(sets["W"]))
                        
                    if fw_size[0] == int(NM_RF.NUMBER):
                        fw_size = min(fw_size[1], len(sets["W"]))
                    elif fw_size[0] == int(NM_RF.PERCENT):
                        fw_size = math.ceil(0.01*fw_size[1]*len(sets["W"]))
                
                if iw_size < fw_size:
                    sucess = False
                    errors.append("Error: The integer window must by equal or bigger than the fixed window")
                    
                else:
                    sucess, errors, solution, actionsTaken = self._st_window_run(variables, sets, parameters, fixApproach, partition, iw_size, fw_size, rollback, time, pathFile)
                
            else:
                sucess = False
                errors.append("Error: The parameter windowConfig was not recognized, check the file 'constants'")
                
            return sucess, errors, solution, actionsTaken
            
        else:
            return False, ["Error: Approach_Solver requires two parameters when run ('time', 'windowConfig')"], solution, actionsTaken