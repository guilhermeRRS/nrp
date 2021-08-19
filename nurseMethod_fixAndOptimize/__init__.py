# coding=utf-8
from dad_nurseMethods import Dad_NurseMethods
import nurseMethod_fixAndOptimize.constants as NM_FO
import math, io, os, sys

class NurseMethod_FixAndOptimize(Dad_NurseMethods):

    from ._st_window import _st_window_config, _st_window_run
    
    def run(self, variables, sets, parameters, initialSolution, arguments):
        solution = {"status": False}
        actionsTaken = []
        
        if len(arguments) == 3:
                
            sucess = True
            errors = []
                
            time = arguments[0]
            extraTime = float(initialSolution["timeLeft"])
            time += extraTime
            windowConfig = arguments[1]
            pathFile = arguments[2]
                
            valid, partition, w_size, s_size = self._st_window_config(windowConfig)
            if valid:
                
                if partition == int(NM_FO.I):
                        
                    if w_size[0] == int(NM_FO.NUMBER):
                        w_size = w_size[1]
                    elif w_size[0] == int(NM_FO.PERCENT):
                        w_size = math.ceil(0.01*w_size[1]*len(sets["I"]))
                        
                    if s_size[0] == int(NM_FO.NUMBER):
                        s_size = s_size[1]
                    elif s_size[0] == int(NM_FO.PERCENT):
                        s_size = math.ceil(0.01*s_size[1]*len(sets["I"]))
                                    
                elif partition == int(NM_FO.W):
                                    
                    if w_size[0] == int(NM_FO.NUMBER):
                        w_size = w_size[1]
                    elif w_size[0] == int(NM_FO.PERCENT):
                        w_size = math.ceil(0.01*w_size[1]*len(sets["W"]))
                                    
                    if s_size[0] == int(NM_FO.NUMBER):
                        s_size = s_size[1]
                    elif s_size[0] == int(NM_FO.PERCENT):
                        s_size = math.ceil(0.01*s_size[1]*len(sets["W"]))
                    
                sucess, errors, solution, actionsTaken = self._st_window_run(variables, sets, parameters, initialSolution, partition, w_size, s_size, time, pathFile)
                    
            else:
                sucess = False
                errors.append("Error: The parameter windowConfig was not recognized, check the file 'constants'")
                    
            return sucess, errors, solution, actionsTaken
                
        else:
            return False, ["Error: Approach_Solver requires two parameters when run ('time', 'windowConfig')"], solution, actionsTaken