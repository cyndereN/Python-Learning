# W1 Intro to AI
## 1.1 What is AI?

The science of making machines that: Think rationally, Think like people, Act like people, Act rationally(optimally)

Better called Computational Rationality - Maximize Your Expected Utility

## 1.2 What about Brain?
Lessons learned: memory(data) and simulation(computation) are key to decision making

Brains are to intelligence as wings are to flight

## 1.3 Course Topics
- __Intelligence from Computation__:  
About algorithms that through computation, take a situation and figure out something smart to do

- __Intelligence form Data__:  
ML

- __Throughout Applications__:  
NLP, Games

## 1.4 Design Rational Agent
An agent is an entity that perceives and acts.  
A rational agent selects actions that maximize its (expected) utility.  
Characteristics of the percepts, environment, and action space dictate techniques for selecting rational actions


# W2 Searches


## 2.1 Uninformed Searches
### 2.1.1 Agents that plan
#### 2.1.1.1 Reflex Agents

- choose action based on current percept(and maybe memory)
- May have memory or a model of the world's current state
- Do not consider the future consequences of their actions
- Consider how the world ***IS***
(could be rational)

#### 2.1.1.2 Plaaning Agents

- Ask "what if"
- Decision based on (hypothesized) consequences of actions
- Must have a model of how the world evolves in response to actions
- Must formulate a goal(test)
- Consider how the world ***WOULD BE***

### 2.1.2 Search Problems

A ***Search Problem*** consists of:  
- A state space
- A successor function (with actions, costs)
- A start state amd a goal test

A ***solution*** is a sequence of actions which transforms the start state to a goal state

***World State*** includes every last detail of the environment.  

***Search State*** keeps only the details needed for planning.

***State Space Graphs***  
Nodes are abstracted world configurations;  
Arcs represent successors(action results);  
The goal test is a set of goal nodes (maybe only one);
Each state occurs only once;  

#### 2.1.2.1 DFS v.s. BFS

***Iterative Deepening***:   
Run DFS with deep limit 1: if not ...  
Run DFS with deep limit 2: if not ...  
...  

#### 2.1.2.2 Uniform Search v.s. Dijkstra
单源至单点（贪心找路径，找到一条之后继续找比当前cost小的路径搜索直到都比当前solution大） 单源至所有  
都是Complete且Optimal

## 2.2 A* Search and Heuristics
### 2.2.1 Heuristics

A heuristic is is a function that estimates how close state is to a goal. Designed for a particular search problem


### 2.2.2 A* Search

we only stop when dequeue a goal, not enqueue a goal

A* is not optimal(because heuristic is not always correct? (inadmissible, pessimistic))

***Admissibility***:
h is admissible if 0 <= h(n) <= h*(n), where h*(n) is the true cost to a nearest goal. e.g. Manhattan Distance

***Dominance***: ha >= hc if for any n, ha(n) >= hc(n)
Max ofd admissible heuristics is admissible: h(n) = max(ha(n), hb(n))

#### 2.2.3 Graph Search

Idea: Never expand a state twice
- Tree search + "closed set"
- Expand the search tree node-by-node, but...
- Before expanding a node, check to make sure its state has never been expanded before
- If not new, skip it, if new add to closed set

***Consistency***: h(A) - h(C) <= cost(A to C)
If hh is consistent, then A* graph search finds an optimal solution.


# W3 Constraint Satisfaction Problems（约束满足问题）

## 3.1 CSP 1

"What is search for?"
- Assumptions about a world: a single agent, deterministic actions, fully observed state, discrete state space. Deterministic  
- Planning: sequences of actions
    - The path to the goal is the important thing
    - Paths have various costs, depths
    - Heuristics give problem-specific guidance
- Identification: assignments to variables
    - The goal it self is important, not the path
    - All paths at the same depth (for some formulations)
    - CSPs are a specialized class of identification problems
(Planning像是小偷确定如何偷东西的步骤，Identification像是侦探根据线索倒推如何失窃的过程)

## 3.2 CSP 2