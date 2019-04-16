# linear programming heuristic 2 - variable is in form xij

import random
from scipy.optimize import linprog

g = 3
num_users = 10
num_serv = 5
num_pairs = num_users * (num_users-1) / 2
num_var = num_users * num_serv + num_pairs * num_serv
num_var_1 = num_users * num_serv

fnc = [0 for i in range(num_var)]
for i in range(num_var_1):
    fnc[i] = 1

A = []

pair_index = -1
for i in range(0, num_users):
    for j in range(i+1, num_users):
        pair_index += 1

        A_ele = [0 for a in range(num_var)]
        for k in range(num_serv):
            A_ele[num_var_1 + pair_index*num_serv+k] = -1
        A.append(A_ele) 

for i in range(1, num_serv):
    A_ele = [0 for k in range(num_var)]
    for j in range(num_users):
        A_ele[j*num_serv] = -1
        A_ele[j*num_serv+i] = 1
    A.append(A_ele)

for i in range(1, num_serv):
    A_ele = [0 for k in range(num_var)]
    for j in range(num_users):
        A_ele[j*num_serv] = 1
        A_ele[j*num_serv+i] = -1
    A.append(A_ele)

pair_index = -1
for i in range(0, num_users):
    for j in range(i+1, num_users):
        pair_index += 1

        for s in range(0, num_serv):
            A_ele = [0 for k in range(num_var)]
            A_ele[num_var_1 + pair_index*num_serv+s] = 1
            A_ele[i*num_serv+s] = -1
            A.append(A_ele)

        for s in range(0, num_serv):
            A_ele = [0 for k in range(num_var)]
            A_ele[num_var_1 + pair_index*num_serv+s] = 1
            A_ele[j*num_serv+s] = -1
            A.append(A_ele)

        for s in range(0, num_serv):
            A_ele = [0 for k in range(num_var)]
            A_ele[num_var_1 + pair_index*num_serv+s] = -1
            A_ele[i*num_serv+s] = 1
            A_ele[j*num_serv+s] = 1
            A.append(A_ele)

b = [(-g+1) for i in range(num_pairs)]
for i in range(1, num_serv):
    b.append(0)
for i in range(1, num_serv):
    b.append(0)

for i in range(num_pairs):
    for j in range(num_serv):
        b.append(0)
    for j in range(num_serv):
        b.append(0)
    for j in range(num_serv):
        b.append(1)

res = linprog(fnc, A_ub=A, b_ub=b, bounds=(0, 1), options={"disp": True})
print(res.x)

## Function to collect results
C_all = [[] for i in range(num_users)]
def collect():
    C_all = [[] for i in range(num_users)]
    for i in range(num_users):
#        print
        for j in range(num_serv):
#            print res.x[i*num_serv+j]
            if round(res.x[i*num_serv+j]) == 1:
                C_all[i].append(j)

    print C_all
    return C_all


## Function to check if random group chat is possible
def works(C_all):
    for i in range(num_users):
        for j in range(i+1, num_users):
            if len(set(C_all[i]).intersection(set(C_all[j]))) <= g-1:
                return False
    return True

arr = collect()
while not works(arr):
    added_term = False
    while not added_term:
        i = random.randint(0, num_var-1)
        if round(res.x[i]) != 1:
            res.x[i] = 1
            added_term = True 

    arr = collect()

# calc average num msg per usr
arr = collect()
tot = 0
for row in arr:
    tot += len(row) 

print float(tot)/len(arr)



