import math

for n in [50,100,200,500,1000]:
    for I in [2,3,5,7,10,15,20,30]:
        l = int(math.ceil(math.sqrt(2*n*I+I*I/4.0) - I/2.0))
        print l
    print 
