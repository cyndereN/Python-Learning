# W1
## 1. Intro
### 1.1 An introduction to Computer Science
#### 1.1.1 What is CS?
The study of: 
1. what probblems can be solved using computation 
2. how to solve those problems 
3. what technique lead to effective solutions

#### 1.1.2 编程
控制逻辑+业务逻辑

## 2. Function
### 2.1 Assignments
#### 2.1.1Environment Diagrams

code + frame

#### 2.1.2 Execution Rule for Assignment Statements

1. Evaluate all expressions to the right of = from left to right 
2. Bind all names to the left of = to the resulting values in the current frame

### 2.1.3 Defining Functions

Assignment is a simple means of abstraction: binds names to values

Function definition: binds names to expressions 

- An environment is a sequence of frames.
- A name evalutates to the value bound to that name in the earliest frame of the current environment in which that name is found

e.g., To look up some name in the body of the square funciton: 
Look for that name in the local frame. If not found, go to global

## 3. Control
### 3.1 Print and None

#### 3.1.1 Pure & Non-Pure Functions

Pure: just return values
Non-Pure: have side effects

### 3.2 Statements

A statenment is executed by the interpreter to perform an action 

The first header determines a statement's type; The header of a clause "controls" the suite that follows; def statements are compound statements

#### 3.2.1 Compoud statements

A suite is a sequence of statements; To "execute" a suite means to execute its sequence of statements, in order. 

### 3.3 Designing functions

- Give each function exactly one job
- Don't repeat yourself (DRY)
- Define functions generally

## 4. Higher-Order Functions

### 4.1 Purpose
Functions are first-class: Functions can be manipulated as values in our programming language. 

Higher-order function: A function that takes a function as an argument value or returns a function as a return value

- Express general methods of computation
- Remove repetition from prgorams
-Separate concerns among funcitons

### 4.2 Currying
Transforming a multi-argument function into a single-argument, high-order funciton 


---

# W2
## 1. Recursion
### 1.1 Recursive Functions
The body of that function calss itself, either directly or indirectly.

## 2. Tree Recursion
Tree-shaped processes arise whenever executing the body of a recursive function makes more than one call to that function. e.g., Fibonacci

---

# W3

## 1. Sequences & Data Abstraction

### 1.1 Sequences

### 1.2 Data Abstraction
Compound objects combine objects together

### 1.3 Abstraction barriers

e.g. violation of barriers:
```python
add_rational([1,2], [1,4]) # Does not use constructors

def divide_rational(x,y):
    return [x[0]*y[1], x[1]*y[0]]  # no selectors, no constructor
```

### 1.4 List in Envionment Diagrams

| s = [2,3] | t = [5,6] |
| ----:| ----: |
| append: |  result:  |
| s.append(t)   |  s ->  [2,3,[5,6]] |
|        t = 0          |     t -> 0 |
| --------------------- | ---------------------- |
| extend: s.extend(t)   |   result: s = [2,3,5,6] |
|      t[1] = 0         |    t = [5,0]  |
| --------------------- | ---------------------- |
| addition & slicing:   |  result: s->[2,3] |
| a = s+[t] | t->[5,0] |
| b = a[1:] | a->[2,9,[5,0]] |
| b[1][1] = 0 | b->[3,[5,0]] |
| a[1]=9 | |
| --------------------- | ---------------------- |
| list funciton: | result: |
| t = list(s) | s-> [2,0] |
| s[1] = 0 | t->[2,3] |
| --------------------- | ---------------------- |
| slice assignment | result: |
| s[0:0] = t | s->[5,6,2,5,6] | 
| s[3:] = t | t->[5,0] |
| t[1] = 0 |           |
| --------------------- | ---------------------- |

## 2. Functional Decomposition & Debugging


### 2.1 Assert
- require invariants
- assertions check that code meets an existing understanding

### 2.2 Testing
- Detect errors in code
- Have confidence in the correctness of subcomponents
- Narrow down the scope of debugging
- Document how your code works

Python provides ***doctest***  ```python3 -m doctest file.py```
***REPL test*** ```python3 -i file.py```and ***OK integration*** ```python3 ok -q whatever -i```

### 2.3 Handing Errors
- assertion
- raise statement
- try statement

## 3. Trees

### 3.1 Slicing list
Always creating new list

### 3.2 Tree Abstraction
- A tree has a root label and a list of branches
- Each branch is a tree 


## 4. Mutable Sequences

### 4.1 Object
### 4.2 Mutable Operations
### 4.3 Tuples
### 4.4 Mutation
sameness : is
equality : ==

a default argument value is part of a function value, not generated b a call