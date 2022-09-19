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


### 3.1.1 Difference between Standard Search Problems

- Standard Search Problems:
    - State is a "black" box: arbitary data structure (can only call GetSuccessor(), isGoal())
    - Goal test can be any function over states
    - Successor functgion can also be anything

- CSP(e.g., Color Mapping, N-Queens, Sudoku)
    - A special subset of search proiblems
    - State is defined by variables Xi with values from a domain D (sometimes D depends on i)
    - Goal test is a set of constraints specifying allowable combinations of values for subsets of variables

### 3.1.2 Standard Search Formulations
States defined by the values assigned so far (partial assignments)
- Initial state: {}
- Successor function: assign a value to an unassigned variable
- Goal test: the current assignment is complete and satisfies all constraints

#### 3.1.2.1 Search Methods
For example, color mapping problem.
DFS. Naive way. Better idea?
Backtracking Search.

#### 3.1.2.2 Backtracking Search
- One variable at a time
    - variable assignments are commutative, so fix ordering. i.e., [WA = red then NT = green] same as [NT = green then WA = red]
    - only need to consider assignments to a single variable at each step
- Check constraints as you go

Backtracking = DFS + variable-ordering + fail-on-violation

#### 3.1.2.3 Filtering
***Filtering***: Keep track of domains for unassigned variables and cross off bad options.
***Forward Checking***: Cross off values that violates a constraint when added to the existing assignment

***Constraint Propagation***: Reason from constraint to constraint

### 3.1.3 Arc Consistency
An arc X->Y is consistent iff for every x in the tail there is some y in the head which could be assigned without violating a constraint

***Forward Checking***: Enforcing consistency of arcs pointing to each new assignment

### 3.1.4 Ordering
Variable Ordering: Minimum remaiuning values(MRV)
Choose the variable with the fewest legal left values in its domain

## 3.2 CSP 2
NP-Hard 

Arc consistency detects failure earlier than forward checking 

filter - assign - fileter - assign ...

### 3.2.1 K-Consistency

"Instead of checking all arcs are following the rule, check all triples or quads"

1-Consistency (Node Consistency): Every node domain has a value which meets that nodes's unary constraints

2-Consistency (Arc Consistency): For each pair of nodes, any consistent assignment to one can be extended to the other

K-Consistency: For each k nodes, any consistent assignment to k-1 ca be extended to the kth node.

Strong n-consistency means we can solve without backtracking

### 3.2.2 Tree-Structured CSPs

(Only need Arc-consistency)

If the constraint graph has no loops, the CSP can be solved in O(nd^2), compare to General CSPs where worst-case time is O(d^n)


### 3.2.3 Iterative Algorithms for CSPs

### 3.2.4 Simulated Annealing

"Solve" the hill climbing problem by allowing some "downhill" moves