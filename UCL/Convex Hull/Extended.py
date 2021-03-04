from matplotlib import pyplot as plt
from random import randint
from math import atan2
import time


def create_points(ct,min=0,max=10000):
   return [[randint(min,max),randint(min,max)] \
         for _ in range(ct)]


def scatter_plot(coords,convex_hull=None):
   xs,ys=zip(*coords)
   plt.scatter(xs,ys)

   if convex_hull!=None:
      for i in range(1,len(convex_hull)+1):
         if i==len(convex_hull): i=0 # wrap
         c0=convex_hull[i-1]
         c1=convex_hull[i]
         plt.plot((c0[0],c1[0]),(c0[1],c1[1]),'r')
   plt.show()


def det(p1,p2,p3):
   return   (p2[0]-p1[0])*(p3[1]-p1[1]) \
         -(p2[1]-p1[1])*(p3[0]-p1[0])


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

    a = points[max_y]  #top
    b = points[min_x]  #left
    c = points[min_y]  #bottom
    d = points[max_x]  #right

    print(a, b,c,d)

    region_1 = [a, b]
    region_2 = [b, c]
    region_3 = [c, d]
    region_4 = [d, a]

    for p in points:
        if p[0]<a[0] and p[1]>b[1] and det(b, a, p) >= 0 :
            region_1.append(p)
        if p[0]<c[0] and p[1]<b[1] and det(b, c, p) <= 0 :
            region_2.append(p)
        if p[0] > a[0] and p[1] > d[1] and det(a, d, p) >= 0:
            region_4.append(p)
        if p[0] > c[0] and p[1] < d[1] and det(c, d, p) <= 0:
            region_3.append(p)


    region_1_sorted = sorted(region_1, key = lambda x: x[0])
    region_2_sorted = sorted(region_2, key = lambda x: -x[0])
    region_3_sorted = sorted(region_3, key = lambda x: -x[0])
    region_4_sorted = sorted(region_4, key = lambda x: x[0])
    print(region_1_sorted, region_2_sorted, region_3_sorted, region_4_sorted)
    return [region_1_sorted, region_2_sorted, region_3_sorted, region_4_sorted]


def determine(p1,p2,p3):
    S = ((p2[1] - p1[1]) * (p3[0] - p2[0])) + ((p1[0] - p2[0]) * (p3[1]-p2[1]))
    return S




def Extended(points):
    xmin = None
    ymin = None
    xmax = None
    ymax = None

    for i, (x, y) in enumerate(points):
        if ymin == None or y < points[ymin][1]:
            ymin = i
        if y == points[ymin][1] and x < points[ymin][0]:
            ymin = i

    for i, (x, y) in enumerate(points):
        if ymax == None or y > points[ymax][1]:
            ymax = i
        if y == points[ymax][1] and x > points[ymax][0]:
            ymax = i

    for i, (x, y) in enumerate(points):
        if xmin == None or x < points[xmin][0]:
            xmin = i
        if x == points[xmin][0] and y < points[xmin][1]:
            xmin = i

    for i, (x, y) in enumerate(points):
        if xmax == None or x > points[xmax][0]:
            xmax = i
        if x == points[xmax][0] and y > points[xmax][1]:
            xmax = i

    extreme = []

    if xmin != ymin != ymax != xmax:
        extreme = [xmax, xmin, ymin, ymax]
    elif xmin == ymin and xmax == ymax:
        extreme = [xmin, xmax]
    elif xmin == ymax and xmax == ymin:
        extreme = [xmax, xmin]
    elif xmin == ymin:
        extreme = [xmax, xmin, ymax]
    elif ymax == xmax:
        extreme = [xmax, xmin, ymin]
    elif xmin == ymax:
        extreme = [xmax, ymin, ymax]
    elif xmax == ymin:
        extreme = [xmin, ymin, ymax]

    hull = [points[xmin], points[ymin], points[xmax], points[ymax]]

    zones = get_region(points)

    for zone1 in zones:
        s = 0
        while s < len(zone1)-2:
            if determine(zone1[s], zone1[s+1], zone1[s+2]) >= 0:
                hull.append(zone1[s])
            else:
                del zone1[s+1]
            s = s+1
            #scatter_plot(points, hull)

    return hull


def extendedgrahamscan(inputSet):
    sorted_points = get_region(inputSet)
    outputSet_1 = []
    outputSet_1.append(sorted_points[0].pop(0))
    outputSet_1.append(sorted_points[0][0])
    for point in sorted_points[0][1:]:
        while det(outputSet_1[+2], outputSet_1[+1], point) <= 0:
            outputSet_1.pop()
        outputSet_1.append(point)

    outputSet_2 = []
    outputSet_2.append(sorted_points[1].pop(0))
    outputSet_2.append(sorted_points[1][0])
    for point in sorted_points[1][1:]:
        while det(outputSet_2[-2], outputSet_2[-1], point) <= 0:
            outputSet_2.pop()
        outputSet_2.append(point)

    return list(set(outputSet_1 + outputSet_2))

def benchmark(sizes=[10,100,1000,10000,100000]):
   for s in sizes:
      tot = 0.0
      for _ in range(3):
         pts = create_points(s,0,max(sizes)*10)
         t0 = time.time()
         hull = Extended(pts)
         tot += (time.time()-t0)
      print("size %d time: %0.5f"%(s,tot/3.0))



time.time()
pts=create_points(10)
#pts=[[0,0],[0,1],[0,2],[0,3],[0,4],[0,5],[3,3]]
print("Points:",pts)
hull=Extended(pts)
#hull = extendedgrahamscan(pts)
print("Hull:",hull)
scatter_plot(pts,hull)
#benchmark()