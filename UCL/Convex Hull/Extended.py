from matplotlib import pyplot as plt
from random import randint
from math import atan2
import time
# Returns a list of (x,y) coordinates of length 'num_points',
# each x and y coordinate is chosen randomly from the range
# 'min' up to 'max'.
def create_points(ct,min=0,max=10000):
   return [[randint(min,max),randint(min,max)] \
         for _ in range(ct)]

# Creates a scatter plot, input is a list of (x,y) coordinates.
# The second input 'convex_hull' is another list of (x,y) coordinates
# consisting of those points in 'coords' which make up the convex hull,
# if not None, the elements of this list will be used to draw the outer
# boundary (the convex hull surrounding the data points).
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

def det(p1,p2,p3):
   return   (p2[0]-p1[0])*(p3[1]-p1[1]) \
         -(p2[1]-p1[1])*(p3[0]-p1[0])

def zones(pt1, pt2, points):
    for p in points:
        if

def determine(p1,p2,p3):
    S = (p2[1] - p1[1]) * (p3[0] - p2[0]) + (p1[0] - p2[0]) * (p3[1]-p2[1])
    return S

def quicksort(a):
   if len(a)<=1: return a
   smaller, equal, larger = [], [], []
   pivot = a[randint(0,len(a)-1)][0] # select random pivot
   for pt in a:
      if   pt[0]<pivot:  smaller.append(pt)
      elif pt[0]==pivot: equal.append(pt)
      else: larger.append(pt)
   return quicksort(smaller) \
         +sorted(equal,key=distance) \
         +quicksort(larger)

def Extended(pts):
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

    hull = extreme



    for s in zone1 :
        if determine(s, s+1, s+2) >= 0:
            hull.append(s)
        else:
            del hull[-1]
            del sorted_pts[s]

    return hull


