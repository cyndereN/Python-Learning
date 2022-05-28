# Assignments

## Environment Diagrams

code + frame

## Execution Rule for Assignment Statements

1. Evaluate all expressions to the right of = from left to right 
2. Bind all names to the left of = to the resulting values in the current frame

## Defining Functions

Assignment is a simple means of abstraction: binds names to values

Function definition: binds names to expressions 

- An environment is a sequence of frames.
- A name evalutates to the value bound to that name in the earliest frame of the current environment in which that name is found

e.g., To look up some name in the body of the square funciton: 
Look for that name in the local frame. If not found, go to global