# coding=utf-8
ST = "1"	#STANDART WINDOW -> first digit
I = "1"		#(ST) PARTITION IS NURSES -> second digit
W = "2"		#(ST) PARTITION IS WEEKS -> second digit
NUMBER = "1"	#IF THE VALUE IS GIVEN BY A NUMBER
PERCENT = "2"	#IF THE VALUE IS GIVEN BY A PERCENT

#-FOR ST:
#third digit -> IF WINDOW IS PERCENT OR NUMBER
#fourth digit -> IF STEP IS PERCENT OR NUMBER
## WINDOW SIZE
BRAKE = "|"
## STEP SIZE

ST_I_P_P = ST+I+PERCENT+PERCENT
ST_I_P_N = ST+I+PERCENT+NUMBER
ST_I_N_P = ST+I+NUMBER+PERCENT
ST_I_N_N = ST+I+NUMBER+NUMBER

ST_W_P_P = ST+W+PERCENT+PERCENT
ST_W_P_N = ST+W+PERCENT+NUMBER
ST_W_N_P = ST+W+NUMBER+PERCENT
ST_W_N_N = ST+W+NUMBER+NUMBER