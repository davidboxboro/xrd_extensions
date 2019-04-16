# linear programming heuristic

from scipy.optimize import linprog

g = 3
num_users = 10
num_serv = 10
num_pairs = num_users * (num_users-1) / 2
num_var = num_pairs * num_serv

fnc = [1 for i in range(num_var)]

A = []

for i in range(num_pairs):
    A_ele = [0 for j in range(num_var)]
    for k in range(num_serv):
        A_ele[i*num_serv+k] = -1
    A.append(A_ele) 

for i in range(1, num_serv):
    A_ele = [0 for k in range(num_var)]
    for j in range(num_pairs):
        A_ele[j*num_serv] = -1
        A_ele[j*num_serv+i] = 1
    A.append(A_ele)

for i in range(1, num_serv):
    A_ele = [0 for k in range(num_var)]
    for j in range(num_pairs):
        A_ele[j*num_serv] = 1
        A_ele[j*num_serv+i] = -1
    A.append(A_ele)

for i in range(num_pairs):
    for j in range(i+1, num_pairs):
        for k in range(j+1, num_pairs):
            for s in range(num_serv):
                A_ele = [0 for a in range(num_var)]
                A_ele[i*num_serv+s] = 1
                A_ele[j*num_serv+s] = 1
                A_ele[k*num_serv+s] = -1
                A.append(A_ele)
            for s in range(num_serv):
                A_ele = [0 for a in range(num_var)]
                A_ele[i*num_serv+s] = 1
                A_ele[j*num_serv+s] = -1
                A_ele[k*num_serv+s] = 1
                A.append(A_ele)
            for s in range(num_serv):
                A_ele = [0 for a in range(num_var)]
                A_ele[i*num_serv+s] = 1
                A_ele[j*num_serv+s] = -1
                A_ele[k*num_serv+s] = 1
                A.append(A_ele)

b = [-g+1 for i in range(num_pairs)]
for i in range(1, num_serv):
    b.append(0)
for i in range(1, num_serv):
    b.append(0)
for i in range(num_pairs):
    for j in range(i+1, num_pairs):
        for k in range(j+1, num_pairs):
            for s in range(3*num_serv):
                b.append(1)

print len(A)
print len(b)

res = linprog(fnc, A_ub=A, b_ub=b, bounds=(0, 1), options={"disp": True})

# collect results
conv_arr = []
for i in range(num_users):
    for j in range(i+1, num_users):
        conv_arr.append([i,j])

#print conv_arr

C_all = []
for i in range(num_users):
    C_all.append([])

print res.x
#print len(res.x)

for i in range(num_pairs):
    print
    for j in range(num_serv):
        print res.x[i*num_serv+j]
        if round(res.x[i*num_serv+j]) == 1:
            a = conv_arr[i][0]
            b = conv_arr[i][1]
            C_all[a].append(j)
            C_all[b].append(j)

for i in range(num_users):
    C_all[i] = list(set(C_all[i]))

print C_all

