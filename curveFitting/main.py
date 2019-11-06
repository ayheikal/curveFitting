import random

import numpy as np
from curveFitting.curvematch import Curve
obj=Curve()
obj.points=[(1,5) , (2, 8), (3 ,13), (4 ,20)]
obj.numberOfGenes = 3
x = obj.estimateFitness([1 , 0 , 4 ])
print(x)

# path='/media/ayman/8497-FE2D/genetic algorithms tutorials points/Assignment 2/input-2.txt'
# with open(path,'r') as file:
#     line=int(file.readline())
#     staticLine=line
#     while(int(line)>0):
#         pairs=[]
#         li=file.readline()
#         li= li.strip().split()
#         num1=int(li[0])
#         num2=int(li[1])
#         for _ in range(num1):
#             li=file.readline()
#             li=li.strip().split()
#             x=float(li[0])
#             y=float(li[1])
#             pairs.append((x,y))
#         #print('pairs: ',pairs)
#         print('case id: ',staticLine-line+1)
#         obj=Curve()
#         obj.points=pairs
#         obj.numberOfGenes=num2+1
#         print('run: ',obj.run(100,100))
#         line-=1


