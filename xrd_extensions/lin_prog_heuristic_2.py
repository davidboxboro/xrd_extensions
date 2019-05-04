# linear programming heuristic 2 - variable is in form xij

import random
import numpy as np
from scipy.optimize import linprog

g = 3
num_users = 3
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

        A_ele = [0 for a in range(num_var)]
        for k in range(num_serv):
            A_ele[i*num_serv+k] = -1
        A.append(A_ele) 

        A_ele = [0 for a in range(num_var)]
        for k in range(num_serv):
            A_ele[j*num_serv+k] = -1
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

b = [(-g+1) for i in range(3*num_pairs)]
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

#print(b)
b2 = []
for row in A:
    s = 0
    for term in row:
        s += term
    b2.append(s)
#print(b2)

for i in range(len(b)):
    if  (b[i]) < (b2[i]):
        print "FAILED"
#    if b[i] > b2[i]:
#        print "LESS"
#    if b[i] == b2[i]:
#        print "EQUAL"

#res = linprog(fnc, A_ub=A, b_ub=b, bounds=(0, 1), options={"disp": True, "bland": True})
res = linprog(fnc, method="simplex", A_ub=A, b_ub=b, bounds=(0, 1), options={"disp": True, "bland": True, "tol": 1e-12})
print(res.x)

res.x = (res.x[0:num_users*num_serv]).tolist()

C_all = [[] for i in range(num_users)]

## Function to collect next highest cell
def collect_next_highest(C_all):
    max_index = (res.x).index(max(res.x))
    res.x[max_index] = -1
    C_all[max_index / num_serv].append(max_index % num_serv)

    print C_all
    return C_all

## Function to check if random group chat is possible
def works(C_all):
    for i in range(num_users):
        for j in range(i+1, num_users):
            if len(set(C_all[i]).intersection(set(C_all[j]))) <= g-1:
                return False
    return True

arr = collect_next_highest(C_all)

while not works(C_all):
    collect_next_highest(C_all)

# calc average num msg per usr
tot = 0
for row in C_all:
    tot += len(row) 

print "Num msg per user:", float(tot)/len(C_all)
print "Num serv:", num_serv


