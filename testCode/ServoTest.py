# Trey's function for testing servos

import sys
from math import sqrt


def F(n):
    return ((1+sqrt(5))**n-(1-sqrt(5))**n)/(2**n*sqrt(5))

startPointS = sys.argv[1]
endPointS = sys.argv[2]

startPoint = int(startPointS)
endPoint = int(endPointS)
temp = startPoint
n = 2
halfway = endPoint / 2
while temp < halfway:
  print(temp)
  temp += F(n)
  n+=1

while temp < endPoint:
  print(temp)
  temp += F(n)
  n-=1

print(temp)

