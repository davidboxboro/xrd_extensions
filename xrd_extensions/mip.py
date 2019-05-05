# mixed int programming

from mip.model import *

N_USER = 3
N_SERV = 5
N_PAIR = N_USER * (N_USER - 1) / 2

M = 99999

#model
m = Model()
#vars
edges = [m.add_var(var_type=CONTINUOUS, lb=0, ub=1) for i in range(N_SERV*N_USER)]
intersections = [m.add_var(var_type=BINARY) for i in range(N_SERV*N_PAIR)]
#constraints
intersections_index = 0 
for i in range(N_USER):
    for j in range(i):
        for s in range(N_SERV):
            intersections_index += 1
            m += edges[i*N_SERV+s] + edges[j*N_SERV+s] >= 2 - M * (1 - intersections[intersections_index])
            m += edges[i*N_SERV+s] + edges[j*N_SERV+s] <= 2 + M * intersections[intersections_index] - 0.001
#objective function
m.objective = xsum(intersections[i] for i in range(N_SERV*N_PAIR))


m.max_gap = 0.05
status = m.optimize(max_seconds=300)
if status==OPTIMAL:
    print('optimal solution cost {} found'.format(m.objective_value))
elif status==FEASIBLE:
    print('sol.cost {} found, best possible: {}'.format(m.objective_value, m.objective_bound))
elif status==NO_SOLUTION_FOUND:
    print('no feasible solution found, lower bound is: {}'.format(m.objective_bound))
if status==OPTIMAL or status==FEASIBLE:
    print('solution:')
    for v in m.vars:
       if abs(v.x)<=1e-7:
           continue
       print('{} : {}'.format(v.name, v.x))





