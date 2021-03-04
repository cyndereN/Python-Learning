from matplotlib import pyplot as plt
from random import randint
from math import atan2
import time

def create_points(ct,min=0,max=10000):
   return [[randint(min,max),randint(min,max)] \
         for _ in range(ct)]

def scatter_plot(coords,convex_hull=None):
   xs,ys=zip(*coords) # unzip into x and y coord lists
   plt.scatter(xs,ys) # plot the data points

   if convex_hull!=None:
      # plot the convex hull boundary, extra iteration at
      # the end so that the bounding line wraps around
      for i in range(1,len(convex_hull)+1):
         if i==len(convex_hull): i=0 # wrap
         c0=convex_hull[i-1]
         c1=convex_hull[i]
         plt.plot((c0[0],c1[0]),(c0[1],c1[1]),'r')
   plt.show()


def get_region(points):
    min_y = 0
    min_x = 0
    max_y = 0
    max_x = 0

    n = len(points)
    for i in range(0, n):
        if points[i][1] < points[min_y][1]:
            min_y = i
        if points[i][0] < points[min_x][0]:
            min_x = i
        if points[i][1] > points[max_y][1]:
            max_y = i
        if points[i][0] > points[max_x][0]:
            max_x = i

    a = points[max_y]  # top
    b = points[min_x]  # left
    c = points[min_y]  # bottom
    d = points[max_x]  # right

    print(a, b, c, d)

    region_1 = [a, b, d]
    region_2 = [b, c, d]

    for p in points:
        if p[0] < a[0] and p[1] > b[1] and det2(b, a, p) >= 0 or p[0] > a[0] and p[1] > d[1] and det2(a, d, p) >= 0:
            region_1.append(p)
        if p[0] < c[0] and p[1] < b[1] and det2(b, c, p) <= 0 or p[0] > c[0] and p[1] < d[1] and det2(c, d, p) <= 0:
            region_2.append(p)


    #print("region1 and 2",[region_1, region_2])

    region_1_sorted = sorted(region_1, key=lambda x: x[0])
    region_2_sorted = sorted(region_2, key=lambda x: -x[0])

    return ([region_1_sorted, region_2_sorted])

import matplotlib.pyplot as plt

def det2(p1,p2,p3):
   return (p2[0] - p1[0]) * (p3[1] - p1[1]) \
          - (p2[1] - p1[1]) * (p3[0] - p1[0])


def det(p1, p2, p3):
    S = ((p2[1] - p1[1]) * (p3[0] - p2[0])) + ((p1[0] - p2[0]) * (p3[1] - p2[1]))
    return S


def extendedgrahamscan(inputSet):
    sorted_points = get_region(inputSet)

    #scatter_plot(inputSet, sorted_points)
    outputSet_1 = []
    outputSet_1.append(sorted_points[0].pop(0))
    outputSet_1.append(sorted_points[0][0])
    for point in sorted_points[0][1:]:
        while det(outputSet_1[-2], outputSet_1[-1], point) < 0:
            if len(outputSet_1) >2:
               outputSet_1.pop()
        outputSet_1.append(point)

    outputSet_2 = []
    outputSet_2.append(sorted_points[1].pop(0))
    outputSet_2.append(sorted_points[1][0])
    for point in sorted_points[1][1:]:
        while det(outputSet_2[-2], outputSet_2[-1],point) < 0:
            if len(outputSet_2) > 2:
               outputSet_2.pop()
        outputSet_2.append(point)

    hull = outputSet_1 + outputSet_2
    #list(set(outputSet_1 + outputSet_2))
    return hull




# inputSet and outputSet should have been defined above.
# uncomment the next two lines only if you wish to test the plotting code before coding your algorithm

#inputSet = [[1.5,2], [2,2] , [3, 3], [4,4], [1,4], [3,1], [1.5, 4.5], [2, 4], [3, 5], [3.5,1.5],[3.5,5], [5,3], [1.4,6], [3,2]]
#print("sorted list",get_region(inputSet))
inputSet = create_points(2000)
outputSet = extendedgrahamscan(inputSet)


plt.figure()

#first do a scatter plot of the inputSet
input_xs, input_ys = zip(*inputSet)
plt.scatter(input_xs, input_ys)

#then do a polygon plot of the computed covex hull
outputSet.append(outputSet[0]) #first create a 'closed loop' by adding the first point at the end of the list
output_xs, output_ys = zip(*outputSet)
plt.plot(output_xs, output_ys)

plt.show()

