# nrp
An approach to deal with a mathematical model for the Nurse Roastering Problem

This code intends to help the study of the Nurse Rostering Problem. Here it is possible to collect the data avaiable in [http://www.schedulingbenchmarks.org/nrp/] and is implemented the model proposed by Tim Curtois, Rong Qu [http://www.schedulingbenchmarks.org/papers/computational_results_on_new_staff_scheduling_benchmark_instances.pdf], rewritten by Erfan Rahimian, Kerem Akartunah, John Levine [https://www.sciencedirect.com/science/article/abs/pii/S0377221716307822].

Some mistakes might have been made (english comments/vars), they do not harm the algorithms that were implemented (relax-and-fix, fix-and-optimize). Also, some validators were not implemented, this may cause unexpected behavior, so, pay attention when using the code as it is!

Feel free to reuse the code and improve it, correcting unecessary imports, variables and change the solver (we depend on gurobi [https://www.gurobi.com/]). If possible, share the improvements made so it may help other people who are also studying the problem :)
