#首轮回答
PROMPT1="""You are a Programming Expert. You always provide correct and reliable code solutions. You will be provided with the Background of the whole problem, a programming problem and may also some pre-implemented functions.If pre-implemented functions provided, you need to call the pre-implemented functions and write a new function to solve the problem.

## Background of the whole problem:
{problem_description}

## Problem Discription:
You need to complete {name} function.
{statement}

## Guidelines:
- Ensure the function is executable and meets the requirement.
- Provide clear and concise comments to explain key parts of the code.

Return your response by filling the function body following the function signature provided. Just generate the function and don't output any examples.
```python
"""

#中间回答，有依赖
PROMPT2="""You are a Programming Expert. You always provide correct and reliable code solutions. You will be provided with the Background of the whole problem, a programming problem and may also some pre-implemented functions.If pre-implemented functions provided, you need to call the pre-implemented functions and write a new function to solve the problem.

## Background of the whole problem:
{problem_description}

## Problem Discription:
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

#最后一轮回答，有依赖
PROMPT3="""You are a Programming Expert. You always provide correct and reliable code solutions. You will be provided with the Background of the whole problem, a programming problem and may also some pre-implemented functions.If pre-implemented functions provided, you need to call the pre-implemented functions and write a new function to solve the problem.

## Background of the whole problem:
{problem_description}

## Problem Discription:
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

#最后一轮回答（但没有依赖）
PROMPT4="""You are a Programming Expert. You always provide correct and reliable code solutions. You will be provided with the Background of the whole problem, a programming problem and may also some pre-implemented functions.If pre-implemented functions provided, you need to call the pre-implemented functions and write a new function to solve the problem.

## Background of the whole problem:
{problem_description}

## Problem Discription:
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

#没有依赖项的中间回答
PROMPT5="""You are a Programming Expert. You always provide correct and reliable code solutions. You will be provided with the Background of the whole problem, a programming problem and may also some pre-implemented functions.If pre-implemented functions provided, you need to call the pre-implemented functions and write a new function to solve the problem.

## Background of the whole problem:
{problem_description}

## Problem Discription:
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