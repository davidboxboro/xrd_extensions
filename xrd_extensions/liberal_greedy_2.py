# start with all connections; remove one by one

N_USR = 10
N_SVR = 50
N_INT = 9

# binary 2d array; says which users are connected to which servers 
edges = []
for i in range(N_USR):
    edges.append([])
    for j in range(N_SVR):
        edges[i].append(1)

print edges

## number of intersections for each user pair
#n_ints = []
#for i in range(N_USR):
#    n_ints.append([])
#    for j in range(N_USR):
#        n_ints[i].append(N_SVR)
#    n_ints[i][i] = -1
#
#print n_ints

# num of servers each user connected to
n_lost = []
for i in range(N_USR):
    n_lost.append(0) 


def is_removable(usr, srv):
    if edges[usr][srv] == 0:
        return False

    for i in range(N_USR):
        if i == usr:
            continue
        svr_in_com = 0
        for j in range(N_SVR):
            if j != srv and edges[usr][j] == 1 and edges[i][j] == 1:
                svr_in_com += 1
        #print "svr in com", svr_in_com
        if svr_in_com < N_INT:    
            return False
    return True   

def edges_broken(usr, srv):
    edges_broken = 0
    for i in range(N_USR):
        if i == usr:
            continue
        edges_broken += edges[i][srv]
    return edges_broken
            

def remove_edge(edges, srv):
    min_val = 999999999
    usr_to_rem = -1
    for i in range(0, N_USR): # check each user connected to that server
        ed_broken = edges_broken(i, srv)
        curr_val = ed_broken * 1000 + n_lost[i]
        #print i, is_removable(i,srv), curr_val
        if is_removable(i, srv) and curr_val < min_val:
            usr_to_rem = i
            min_val = curr_val
            #print "ed broken", ed_broken
    if usr_to_rem != -1:
        edges[usr_to_rem][srv] = 0
        n_lost[usr_to_rem] += 1

    return usr_to_rem, edges

# run alg
usr_to_rem = 99999999999 
svr = 0
loop_count = 0
#print edges
fails = 0
while fails <= N_SVR*0.1:
    usr_to_rem, edges = remove_edge(edges, svr)
    if usr_to_rem == -1:
        fails += 1

    svr = (svr + 1) % N_SVR
    loop_count += 1
    print loop_count

# print result
for row in edges:
    print row



# check
for i in range(N_USR):
    for j in range(i):
        svr_in_com = 0
        for s in range(N_SVR):
            if edges[i][s] == 1 and edges[j][s] == 1:
                svr_in_com += 1
        #print svr_in_com
        if svr_in_com < N_INT:    
            print "FAILED" 
print 

# stat calcs
for a in edges:
    count = 0
    for b in a:
        count += b
    print count
    
       
 
