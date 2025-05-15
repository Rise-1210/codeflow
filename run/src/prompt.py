#First round of answers
PROMPT1="""You are a Programming Expert. You always provide correct and reliable code solutions. You will be provided with the background of the whole problem, a programming problem and may also some pre-implemented functions.If pre-implemented functions provided, you need to call the pre-implemented functions and write a new function to solve the problem.

## Background of the whole problem:
{problem_description}

## Problem Description:
You need to complete {name} function.
{statement}

## Guidelines:
- Ensure the function is executable and meets the requirement.
- Provide clear and concise comments to explain key parts of the code.

Return your response by filling the function body following the function signature provided. Just generate the function and don't output any examples.
```python
"""

#Intermediate answer, dependent
PROMPT2="""You are a Programming Expert. You always provide correct and reliable code solutions. You will be provided with the background of the whole problem, a programming problem and may also some pre-implemented functions.If pre-implemented functions provided, you need to call the pre-implemented functions and write a new function to solve the problem.

## Background of the whole problem:
{problem_description}

## Problem Description:
You need to complete {name} function.
{statement}

## Dependency information:
To solve the problem, you need to utilize the ## Pre-implemented functions {dependencies} provided.

## Pre-implemented functions:
{history}

## Guidelines:
- Ensure the function is executable and meets the requirement.
- Handle ## Dependency information correctly.
- Provide clear and concise comments to explain key parts of the code.

Return your response by filling the function body following the function signature provided. Just generate the function and don't output any examples.
```python
"""

#The last round of answers, there are dependencies
PROMPT3="""You are a Programming Expert. You always provide correct and reliable code solutions. You will be provided with the background of the whole problem, a programming problem and may also some pre-implemented functions.If pre-implemented functions provided, you need to call the pre-implemented functions and write a new function to solve the problem.

## Background of the whole problem:
{problem_description}

## Problem Description:
You need to complete {name} function.
{statement}

## Dependency information:
To solve the problem, you need to utilize the ## Pre-implemented functions {dependencies} provided.

## Pre-implemented functions:
{history}

## Guidelines:
- Ensure the function is executable and meets the requirement.
- Handle ## Dependency information correctly.
- Provide clear and concise comments to explain key parts of the code. 

Return your response by filling the function body following the function signature provided. Just generate the function and don't output any examples.
```python
import sys
def {name}():
    input = sys.stdin.read().split()
"""

#Last round of answers (but no dependencies)
PROMPT4="""You are a Programming Expert. You always provide correct and reliable code solutions. You will be provided with the background of the whole problem, a programming problem and may also some pre-implemented functions.If pre-implemented functions provided, you need to call the pre-implemented functions and write a new function to solve the problem.

## Background of the whole problem:
{problem_description}

## Problem Description:
You need to complete {name} function.
{statement}

## Pre-implemented functions:
{history}

## Guidelines:
- Ensure the function is executable and meets the requirement.
- Provide clear and concise comments to explain key parts of the code. 

Return your response by filling the function body following the function signature provided. Just generate the function and don't output any examples.
```python
import sys
def {name}():
    input = sys.stdin.read().split()
"""

#Intermediate answer without dependencies
PROMPT5="""You are a Programming Expert. You always provide correct and reliable code solutions. You will be provided with the background of the whole problem, a programming problem and may also some pre-implemented functions.If pre-implemented functions provided, you need to call the pre-implemented functions and write a new function to solve the problem.

## Background of the whole problem:
{problem_description}

## Problem Description:
You need to complete {name} function.
{statement}

## Pre-implemented functions:
{history}

## Guidelines:
- Ensure the function is executable and meets the requirement.
- Provide clear and concise comments to explain key parts of the code.

Return your response by filling the function body following the function signature provided. Just generate the function and don't output any examples.
```python
"""