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