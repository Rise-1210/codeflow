import os
import ast
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




#First round of answers
PROMPT1="""You are a Programming Expert. You always provide correct and reliable code solutions. You will be provided with the Background of the whole problem, a programming problem and may also some pre-implemented functions.If pre-implemented functions provided, you need to call the pre-implemented functions and write a new function to solve the problem.

## Background of the whole problem:
{problem_description}

## Problem Discription:
You need to complete {name} function.
{statement}

## Guidelines:
- Ensure the function is executable and meets the requirement.
- Provide clear and concise comments to explain key parts of the code.

Return your response by filling the function following the function signature provided. Just generate the function itself and don't output anything else.
```python
"""

#Intermediate answer, dependent
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

Return your response by filling the function body following the function signature provided. Just generate the function itself and don't output any examples.
```python
"""

#The last round of answers, there are dependencies
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

Return your response by filling the function body following the function signature provided. Just generate the function itself and don't output any examples.
```python
import sys
def {name}():
    input = sys.stdin.read().split()
"""

#Last round of answers (but no dependencies)
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

Return your response by filling the function body following the function signature provided. Just generate the function itself and don't output any examples.

```python
import sys
def {name}():
    input = sys.stdin.read().split()
"""

#Intermediate answer without dependencies
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

Return your response by filling the function body following the function signature provided. Just generate the function itself and don't output any examples. 
```python
"""
def get_filenames_without_extension(folder_path):
    # Initialize an empty list to store filenames without extensions
    filenames = []

    # Iterate over all files in the folder
    for filename in os.listdir(folder_path):
        # Check if the current item is a file (exclude directories)
        if os.path.isfile(os.path.join(folder_path, filename)):
            # Remove the file extension
            name_without_extension = os.path.splitext(filename)[0]
            # Add the filename without extension to the list
            filenames.append(name_without_extension)

    return filenames



import re

def replace_spaces_with_commas(text):
    # Use a regular expression to replace spaces with commas
    # Explanation of the regex:
    # (?<!,) means the preceding character is NOT a comma
    # \s matches any whitespace character
    # (?!,) means the following character is NOT a comma
    result = re.sub(r'(?<!,)\s(?!,)', ',', text)
    return result


def get_uuid(dir):    
    files = os.listdir(dir)
    uuids_in_files = set()
    for file_name in files:
        if file_name.endswith(".json"):  # Process only .json files
            try:
                # Remove the .json suffix (last 5 characters)
                file_uuid = file_name[:-5]
                uuids_in_files.add(file_uuid)
            except ValueError:
                # Ignore files where the filename is not a number
                continue
    return uuids_in_files




def extract_code(pred):
    """
    Extract the last complete Python code block from the given string pred.
    Priority is given to matching the following formats in order:
    1. ```python ... ```
    2. `python ... `
    3. ----- ... ----- (blocks wrapped with at least 4 hyphens)
    """
    patterns = [
        # Strictly match complete code blocks in the format ```python ... ```
        r'```python\s*?\n(.*?)\n```',
        # Match code blocks in the format `python ... `
        r'`python\s*(.*?)\s*`',
        # Match blocks wrapped with at least 4 hyphens ----- ... -----
        r'-{4,}\s*\n(.*?)\n\s*-{4,}',
    ]
    
    last_match = None
    for pattern in patterns:
        matches = list(re.finditer(pattern, pred, re.DOTALL))
        if matches:
            # Consider only matches with non-empty content
            valid_matches = [m for m in matches if m.group(1).strip()]
            if valid_matches:
                last_match = valid_matches[-1].group(1)
    
    code = last_match.strip() if last_match is not None else pred.strip()
    
    # Remove shebang line if it exists as the first line
    lines = code.splitlines()
    if lines and lines[0].startswith('#!'):
        lines = lines[1:]
    return '\n'.join(lines).strip()


def get_input(subproblem,turn_number,overall_turns,problem_description_now,history):
    if history:
        history_all="\n\n".join(f'```python\n{item}\n```' for item in history)
    else:
        history_all=""
    
    #First round of input
    if turn_number==1 and turn_number!=overall_turns:
        input=PROMPT1.format(
                problem_description=problem_description_now,
                name=subproblem["name"],
                statement=subproblem["statement"],
                )

    #Last round of input
    elif turn_number==overall_turns:
        if "dependencies" in subproblem and isinstance(subproblem["dependencies"], list) and subproblem["dependencies"]:#Dependency exists and is not empty
            input=PROMPT3.format(
                problem_description=problem_description_now,
                name=subproblem["name"],
                statement=subproblem["statement"],
                dependencies=subproblem["dependencies"],
                history=history_all
                    )
        else:
            input=PROMPT4.format(
                    problem_description=problem_description_now,
                    name=subproblem["name"],
                    statement=subproblem["statement"],
                    history=history_all
                    )
    #Intermediate input, with dependencies
    elif "dependencies" in subproblem and isinstance(subproblem["dependencies"], list) and subproblem["dependencies"]:#Dependency exists and is not empty
        input=PROMPT2.format(
                problem_description=problem_description_now,
                name=subproblem["name"],
                statement=subproblem["statement"],
                dependencies=subproblem["dependencies"],
                history=history_all
                )
                
    #Intermediate input, no dependencies  
    else:
        input=PROMPT5.format(
                problem_description=problem_description_now,
                name=subproblem["name"],
                statement=subproblem["statement"],
                history=history_all
                )
    return input

def ensure_python_code_block(s):
    prefix = "```python\n"
    if not s.startswith("```python"):
        return prefix + s
    if not s.endswith("```"):
        s += "```"
    return s

def ensure_python_code_block_main(s, subproblem):
    # Define a prefix to prepend when a Python code block is missing
    prefix = f"""```python
import sys
def {subproblem["name"]}():
    input = sys.stdin.read().split()
"""
    # If multiple ```python markers exist, keep only the last one and the content after it
    if s.count("```python") > 1:
        s = "```python" + s.split("```python")[-1]
    # If the cleaned string does not start with ```python, prepend the prefix
    if not s.startswith("```python"):
        s = prefix + s
    return s


def clean_code_block(s):
    # Remove everything before the first occurrence of "from", "import", or "def"
    pos_from = s.find("from")
    pos_import = s.find("import")
    pos_def = s.find("def")
    # Select the smallest index among those found (ignore -1)
    pos_candidates = [pos for pos in [pos_from, pos_import, pos_def] if pos != -1]
    if pos_candidates:
        pos = min(pos_candidates)
        s = s[pos:]
    # If there are multiple ```python markers, keep only the last one and content after it
    if s.count("```python") > 1:
        s = "```python" + s.split("```python")[-1]
    # If the string ends with ```, remove it and everything after it (avoid removing last char unintentionally)
    if s.strip().endswith("```"):
        s = s[:s.rfind("```")]
    return s

    

def get_input_single(subproblem,turn_number,overall_turns,problem_description_now,history):
    if turn_number!=overall_turns:
        if "dependencies" in subproblem and isinstance(subproblem["dependencies"], list) and subproblem["dependencies"]:#Dependency exists and is not empty
            sub_description=subproblem_description_depend.format(
                name=subproblem["name"],
                statement=subproblem["statement"],
                dependencies=subproblem["dependencies"],
                    )
        else:
            sub_description=subproblem_description.format(
                name=subproblem["name"],
                statement=subproblem["statement"],
                )
        return sub_description
    else:
        if "dependencies" in subproblem and isinstance(subproblem["dependencies"], list) and subproblem["dependencies"]:#Dependency exists and is not empty
            input=PROMPT_depend.format(
                    name=subproblem["name"],
                    statement=subproblem["statement"],
                    problem_description=problem_description_now,
                    combined_subproblem_description=history,
                    dependencies=subproblem["dependencies"],
                        )
        else:
            input=PROMPT.format(
                    name=subproblem["name"],
                    statement=subproblem["statement"],
                    problem_description=problem_description_now,
                    combined_subproblem_description=history,
                        )
        return input



def has_print(code_str):
    """
    Use AST to check if the code contains a print call or sys.stdout.write / stdout.write call.
    """
    try:
        tree = ast.parse(code_str)
    except Exception:
        return False  # If parsing fails, assume no output calls are present

    for node in ast.walk(tree):
        # Check for print(...)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'print':
            return True

        # Check for sys.stdout.write(...) or stdout.write(...)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            func_val = node.func.value
            if isinstance(func_val, ast.Attribute):
                # Pattern like sys.stdout.write
                if (isinstance(func_val.value, ast.Name)
                        and func_val.value.id == 'sys'
                        and func_val.attr == 'stdout'
                        and node.func.attr == 'write'):
                    return True
            # Pattern like stdout.write
            if isinstance(func_val, ast.Name) and func_val.id == 'stdout' and node.func.attr == 'write':
                return True

    return False
