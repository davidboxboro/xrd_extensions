# calculate the success rate of XRD group chats with original XRD algorithm
# n = number of chains
# l = number of chains each user sends messages to
# N = number of users
# C_all = chains each group of users is connected to, ith row for ith group of users; 2D array
# C_curr = chains current group of users is connected to; 1D array
# g = group size 

import math
import random 

n = 100
N = 5000000 # users are numbered 0 to N-1, inclusive; user u belongs to group u % (l+1)
l = int(math.ceil(math.sqrt(2*n+0.25) - 0.5))
g = 5 

print "\n%s users, %s chains, %s messages per user\n" % (N, n, l) 
print "Chains each group sends messages to:"

# Row 0 of C_all (base case)
C_all = []
C_curr = []
for i in range(0, l):
    C_curr.append(i)
C_all.append(C_curr) 

print " Group 0: %s" % (C_curr)

# Rows 1, 2, ..., l of C_all
for i in range(1, l+1): # i goes from 1 to l, inclusive
    C_curr = []

    for j in range(0, i): # j goes from 0 to i-1, inclusive
        C_curr.append(C_all[j][i-1] % n)

    for k in range(1, l-i+1):
        C_curr.append((C_all[i-1][l-1] + k) % n)

    print " Group %s: %s" % (i, C_curr)

    C_all.append(C_curr)

# Function to test if two sets intersect
def common_elm(a, b): 
    a_set = set(a) 
    b_set = set(b) 
    if (a_set & b_set): 
        return True 
    else: 
        return False

# Check if C_all indeed leads to all groups intersecting
for i in range(len(C_all)):
    for j in range(0, i):
        if not common_elm(C_all[i], C_all[j]):
            print "\nAlgorithm FAILED, %s and %s do not intersect!\n" % (i, j) 
            exit()



# Function to check if random group chat is possible
def group_chat_possible():

    # Find where each pair in group intersect
    G = []
    while len(G) < g:
        new_ele = random.randint(0, N-1)
        if not new_ele in G:
            G.append(new_ele)

#    print "\nGroup: %s" % G

    intersections = []
    for i in range(len(G)):
        for j in range(0, i):
            set1 = set(C_all[G[i] % (l+1)])
            set2 = set(C_all[G[j] % (l+1)])
            intersections.append(list(set1 & set2))

#    print "\nIntersections: %s" % intersections

    arr = [[]]
    for intersection in intersections:
        l_orig = len(arr)
        for i in range(len(intersection)-1):
            for j in range(l_orig):
                arr.append(arr[j][:])

        for i in range(len(intersection)):
            for j in range(l_orig):
                arr[i*l_orig+j].append(intersection[i])

#    print "\nIntersection combinations:"
#    for i in range(len(arr)):
#        print " %s: %s" % (i, arr[i])    

    print len(arr)

    for i in range(len(arr)):
        if len(arr[i]) == len(set(arr[i])):
            return True
    return False


successes = 0
total = 100
for i in range(total):
    if group_chat_possible():
        successes += 1

print "Success rate: %f" % (float(successes)/float(total)) 
    


