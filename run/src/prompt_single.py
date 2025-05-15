
subproblem_description_depend = """
## Subproblem {name} 
# Description:
You need to complete {name} function.
{statement} 
To solve the problem, you need to utilize your pre-implemented function {dependencies}.
"""


subproblem_description = """
## Subproblem {name} 
# Description:
You need to complete {name} function.
{statement} 
"""

#combined_subproblem_description is to concatenate all the Subproblem_descriptions

PROMPT="""You are a Programming Expert. You always provide correct and reliable code solutions. You are required to solve a problem which consists of multiple subproblems, each with its own requirements. 
You will be provided with the background of the problem and description of all subproblems. You need to generate the complete implementations for all subproblems in a single response.  
The response for the final subproblem will be tested using stdin and stdout. Ensure the corresponding code meet this requirement.

## Background of the whole problem:
{problem_description}

## Problem Description:
{combined_subproblem_description}
## Subproblem {name} 
# Description:
You need to complete {name} function.
{statement} 

## Guidelines:
- Ensure that all functions are executable and meet their respective requirements.
- For each subproblem, correctly handle any dependency information.
- Provide clear and concise comments explaining the key parts of the code.
- For the last subproblem {name}, please use 'import sys\ndef {name}():\n    input = sys.stdin.read().split()\n" as the beginning.

Return your response by generating all functions in a single code block. 
```python
"""


PROMPT_depend="""You are a Programming Expert. You always provide correct and reliable code solutions. You are required to solve a problem which consists of multiple subproblems, each with its own requirements. 
You will be provided with the background of the problem and description of all subproblems. You need to generate the complete implementations for all subproblems in a single response.  
The response for the final subproblem will be tested using stdin and stdout. Ensure the corresponding code meet this requirement.

## Background of the whole problem:
{problem_description}

## Problem Description:
{combined_subproblem_description}
## Subproblem {name} 
# Description:
You need to complete {name} function.
{statement} 
To solve the problem, you need to utilize your pre-implemented function {dependencies}.

## Guidelines:
- Ensure that all functions are executable and meet their respective requirements.
- For each subproblem, correctly handle any dependency information.
- Provide clear and concise comments explaining the key parts of the code.
- For the last subproblem {name}, please use 'import sys\ndef {name}():\n    input = sys.stdin.read().split()\n" as the beginning.

Return your response by generating all functions in a single code block. 
```python
"""