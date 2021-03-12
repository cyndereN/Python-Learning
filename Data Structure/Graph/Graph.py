from queue import *

class Vertex:
    def __init__(self, key):
        self.id = key
        self.connectedTo = {}

    def addNeighbor(self, nbr, weight = 0):
        self.connectedTo[nbr] = weight

    def __repr__(self):
        return str(self.id) + " connectedTo: "\
            + str([x.id for x in self.connectedTo])

    def getConnections(self):
        return self.connectedTo.keys()
    
    def getId(self):
        return self.id

    def getWeight(self, nbr):
        return self.connectedTo[nbr]

class Graph:
    def __init__(self):
        self.vertList = {}
        self.numVertices = 0

    def addVertex(self, key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertList[key] = newVertex
        return newVertex

    def getVertex(self, n):
        if n in self.vertList:
            return self.vertList[n]
        else:
            return None
    
    def __contains__(self, n):
        return n in self.vertList

    def addEdge(self, f, t, cost=0):
        if f not in self.vertList:
            nv = self.addVertex(f)
        if t not in self.vertList:
            nv = self.addVertex(t)
        self.vertList[f].addNeighbor(self.vertList[t], cost)
    
    def getVertices(self):
        return self.vertList.keys()

    def  __iter__(self):
        return iter(self.getVertices)

    def printEdges(self):
        for v in self.vertList.values():
            for w in v.getConnections():
                print("(%s, %s, %s)"%(v.getId(), w.getId(), v.connectedTo[w]))

    def bfs(self, s):
        distToSource = {v:-1 for v in self.getVertices()}
        edgeTo = {v:-1 for v in self.getVertices()}
        q = Queue()
        q.put(s)
        distToSource[s] = 0
        while not q.empty():
            v = q.get()
            for w in self.vertList[v].getConnections():
                if (distToSource[w.getId()] == -1):
                    q.put(w.getId())
                    distToSource[w.getId()] = distToSource[v]+1
                    edgeTo[w.getId()] = v
        print(distToSource)

    
            
    def dfs(self, s):
        def dfsHelper(self, v):
            marked[v] = True
            for w in self.vertList[v].getConnections():
                if (marked[w.getId()] == False):
                    dfsHelper(self, w.getId())
                    edgeTo[w.getId()] = v

        marked = {v:False for v in self.getVertices()}
        edgeTo = {v:-1 for v in self.getVertices()}
        dfsHelper(self, s)
        print(edgeTo)

    def isDAG(self):
        def dfsHelper(self, v):
            nonlocal cycleDetected
            marked[v] = True
            onCallStack[v] = True
            for w in self.vertList[v].getConnections():
                if cycleDetected == True:
                    return 
                elif (not marked[w.getId()]): 
                    dfsHelper(self, w.getId())
                elif onCallStack[w.getId()]:
                    cycleDetected = True
            onCallStack[v] = False

        marked = {v:False for v in self.getVertices()}
        onCallStack = {v:False for v in self.getVertices()}
        cycleDetected = False
        for v in self.vertList.values():
            if (not marked[v.getId()]):
                dfsHelper(self, v.getId())
        return not cycleDetected


g = Graph()
for i in range(6):
	g.addVertex(i)
print(g.getVertices())
print(g.vertList)
g.addEdge(0,1,5)
g.addEdge(0,5,2)
g.addEdge(1,2,4)
g.addEdge(2,3,9)
g.addEdge(3,4,7)
g.addEdge(3,5,3)
g.addEdge(4,0,1)
g.addEdge(5,4,8)
g.addEdge(5,2,1)
print(g.vertList[3].getConnections())
g.printEdges()
g.bfs(1)
g.dfs(1)
print(g.isDAG())

d = Graph()
d.addEdge('v', 'q')
d.addEdge('q', 'w')
d.addEdge('w', 'z')
d.addEdge('v', 'r')
print(d.vertList)
print(d.isDAG())