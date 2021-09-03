# coding=utf-8
ST = "1"	#STANDART WINDOW -> first digit
BOTH = "1"	#FIX ZEROS AND ONES -> second digit
ONE = "2"		#FIX ONLY ONES -> second digit
I = "1"		#PARTITION IS NURSES -> third digit
W = "2"		#PARTITION IS WEEKS -> third digit
NO_R = "0"	#IF THERE IS NO ROLLBACK -> fourth digit
DO_R1 = "1"	#IF THERE WE USE THE ROLLBACK APPROACH 1 -> fourth digit
NUMBER = "1"	#IF THE WINDOW SIZE IS GIVEN BY A NUMBER
PERCENT = "2"	#IF THE WINDOW SIZE IS GIVEN BY A PERCENT
#fifth digit -> IF INTEGER WINDOW IS PERCENT OR NUMBER
#sixth digit -> IF FIXED WINDOW IS PERCENT OR NUMBER
## INTEGER WINDOW SIZE
BRAKE = "|"
## FIXED WINDOW SIZE

ST_BOTH_I_NO_P_P = ST+BOTH+I+NO_R	+PERCENT+PERCENT
ST_BOTH_I_R1_P_P = ST+BOTH+I+DO_R1	+PERCENT+PERCENT
ST_BOTH_W_NO_P_P = ST+BOTH+W+NO_R	+PERCENT+PERCENT
ST_BOTH_W_R1_P_P = ST+BOTH+W+DO_R1	+PERCENT+PERCENT
ST_ONE_I_NO_P_P = ST+ONE+I+NO_R		+PERCENT+PERCENT
ST_ONE_I_R1_P_P = ST+ONE+I+DO_R1	+PERCENT+PERCENT
ST_ONE_W_NO_P_P = ST+ONE+W+NO_R		+PERCENT+PERCENT
ST_ONE_W_R1_P_P = ST+ONE+W+DO_R1	+PERCENT+PERCENT

ST_BOTH_I_NO_P_N = ST+BOTH+I+NO_R	+PERCENT+NUMBER
ST_BOTH_I_R1_P_N = ST+BOTH+I+DO_R1	+PERCENT+NUMBER
ST_BOTH_W_NO_P_N = ST+BOTH+W+NO_R	+PERCENT+NUMBER
ST_BOTH_W_R1_P_N = ST+BOTH+W+DO_R1	+PERCENT+NUMBER
ST_ONE_I_NO_P_N = ST+ONE+I+NO_R		+PERCENT+NUMBER
ST_ONE_I_R1_P_N = ST+ONE+I+DO_R1	+PERCENT+NUMBER
ST_ONE_W_NO_P_N = ST+ONE+W+NO_R		+PERCENT+NUMBER
ST_ONE_W_R1_P_N = ST+ONE+W+DO_R1	+PERCENT+NUMBER

ST_BOTH_I_NO_N_P = ST+BOTH+I+NO_R	+NUMBER+PERCENT
ST_BOTH_I_R1_N_P = ST+BOTH+I+DO_R1	+NUMBER+PERCENT
ST_BOTH_W_NO_N_P = ST+BOTH+W+NO_R	+NUMBER+PERCENT
ST_BOTH_W_R1_N_P = ST+BOTH+W+DO_R1	+NUMBER+PERCENT
ST_ONE_I_NO_N_P = ST+ONE+I+NO_R		+NUMBER+PERCENT
ST_ONE_I_R1_N_P = ST+ONE+I+DO_R1	+NUMBER+PERCENT
ST_ONE_W_NO_N_P = ST+ONE+W+NO_R		+NUMBER+PERCENT
ST_ONE_W_R1_N_P = ST+ONE+W+DO_R1	+NUMBER+PERCENT

ST_BOTH_I_NO_N_N = ST+BOTH+I+NO_R	+NUMBER+NUMBER
ST_BOTH_I_R1_N_N = ST+BOTH+I+DO_R1	+NUMBER+NUMBER
ST_BOTH_W_NO_N_N = ST+BOTH+W+NO_R	+NUMBER+NUMBER
ST_BOTH_W_R1_N_N = ST+BOTH+W+DO_R1	+NUMBER+NUMBER
ST_ONE_I_NO_N_N = ST+ONE+I+NO_R		+NUMBER+NUMBER
ST_ONE_I_R1_N_N = ST+ONE+I+DO_R1	+NUMBER+NUMBER
ST_ONE_W_NO_N_N = ST+ONE+W+NO_R		+NUMBER+NUMBER
ST_ONE_W_R1_N_N = ST+ONE+W+DO_R1	+NUMBER+NUMBER