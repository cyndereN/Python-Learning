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


# Returns the polar angle (radians) from p0 to p1.
# If p1 is None, defaults to replacing it with the
# global variable 'anchor', normally set in the
# 'graham_scan' function.
def polar_angle(p0,p1=None):
   if p1==None: p1=anchor
   y_span=p0[1]-p1[1]
   x_span=p0[0]-p1[0]
   return atan2(y_span,x_span)


# Returns the euclidean distance from p0 to p1,
# square root is not applied for sake of speed.
# If p1 is None, defaults to replacing it with the
def distance(p0,p1=None):
   if p1==None: p1=anchor
   y_span=p0[1]-p1[1]
   x_span=p0[0]-p1[0]
   return y_span**2 + x_span**2


# Returns the determinant of the 3x3 matrix...
#  [p1(x) p1(y) 1]
#  [p2(x) p2(y) 1]
#  [p3(x) p3(y) 1]
# If >0 then counter-clockwise
# If <0 then clockwise
# If =0 then collinear
def det(p1,p2,p3):
   return   (p2[0]-p1[0])*(p3[1]-p1[1]) \
         -(p2[1]-p1[1])*(p3[0]-p1[0])


# Sorts in order of increasing polar angle from 'anchor' point.
# 'anchor' variable is assumed to be global, set from within 'graham_scan'.
# For any values with equal polar angles, a second sort is applied to
# ensure increasing distance from the 'anchor' point.
def quicksort(a):
   if len(a)<=1: return a
   smaller,equal,larger=[],[],[]
   pivot_ang=polar_angle(a[randint(0,len(a)-1)]) # select random pivot
   for pt in a:
      point_ang=polar_angle(pt) # calculate current point angle
      if   point_ang<pivot_ang:  smaller.append(pt)
      elif point_ang==pivot_ang: equal.append(pt)
      else: larger.append(pt)
   return quicksort(smaller) \
         +sorted(equal,key=distance) \
         +quicksort(larger)


def graham_scan_extended(points):
   global anchor1

   xmin = None
   ymin = None
   xmax = None
   ymax = None

   for i,(x,y) in enumerate(points):
      if ymin==None or y<points[ymin][1]:
         ymin=i
      if y==points[ymin][1] and x<points[ymin][0]:
         ymin=i

   for i,(x,y) in enumerate(points):
      if ymax==None or y>points[ymax][1]:
         ymax=i
      if y==points[ymax][1] and x>points[ymax][0]:
         ymax=i

   for i,(x,y) in enumerate(points):
      if xmin==None or x<points[xmin][0]:
         xmin=i
      if x==points[xmin][0] and y<points[xmin][1]:
         xmin=i

   for i,(x,y) in enumerate(points):
      if xmax==None or x>points[xmax][0]:
         xmax=i
      if x==points[xmax][0] and y>points[xmax][1]:
         xmax=i


   anchor1 = points[xmin]

   sorted_pts1 = quicksort(points)
   del sorted_pts1[sorted_pts.index(anchor1)]

   anchor1 = points[xmax]

   sorted_pts2 = quicksort(points)
   del sorted_pts2[sorted_pts.index(anchor1)]

   anchor1 = points[ymax]

   sorted_pts3 = quicksort(points)
   del sorted_pts3[sorted_pts.index(anchor1)]

   anchor1 = points[ymin]

   sorted_pts4 = quicksort(points)
   del sorted_pts4[sorted_pts.index(anchor1)]

   hull = [points[xmin], points[ymin], points[xmax], points[ymax]]

   max = points.size()-2

   hull.append(sorted_pts3.index(max))
   hull.append(sorted_pts4.index(0))
   hull.append(sorted_pts2.index(max))
