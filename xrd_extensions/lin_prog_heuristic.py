# linear programming heuristic


from scipy.optimize import linprog

num_users = 5
num_serv = 10
num_var = num_users * (num_users-1) / 2 * num_serv

fnc = [1 for i in range(num_var)]
A = []
b = []

res = linprog(fnc, A_ub=A, b_ub=b, bounds=(0, 1), options={"disp": True})

print(res)
