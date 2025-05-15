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

## Sample Test Case:
{sample_test_case}

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

## Sample Test Case:
{sample_test_case}

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

## Sample Test Case:
{sample_test_case}

## Guidelines:
- Ensure the function is executable and meets the requirement.
- Provide clear and concise comments to explain key parts of the code.

Return your response by filling the function body following the function signature provided. Just generate the function itself and don't output any examples. 
```python
"""
def get_filenames_without_extension(folder_path):
    # Initialize an empty list to store filenames without extensions
    filenames = []

    # Iterate over all entries in the folder
    for filename in os.listdir(folder_path):
        # Check if the entry is a file (exclude directories)
        if os.path.isfile(os.path.join(folder_path, filename)):
            # Remove the file extension from the filename
            name_without_extension = os.path.splitext(filename)[0]
            # Add the filename without extension to the list
            filenames.append(name_without_extension)

    return filenames




import re

def replace_spaces_with_commas(text):
    # Use regular expression to replace spaces with commas
    # Regex explanation:
    # (?<!,) means the preceding character is not a comma
    # \s matches any whitespace character
    # (?!,) means the following character is not a comma
    result = re.sub(r'(?<!,)\s(?!,)', ',', text)
    return result



def get_uuid(dir):
    files = os.listdir(dir)
    uuids_in_files = set()
    for file_name in files:
        if file_name.endswith(".json"):  # Process only .json files
            try:
                # Remove the .json suffix to get the UUID (as string)
                file_uuid = file_name[:-5]
                uuids_in_files.add(file_uuid)
            except ValueError:
                # Ignore if the filename is not a valid UUID (if conversion needed)
                continue
    return uuids_in_files



def extract_code(pred):
    """
    Extract the content of the last Python code block from the given string pred.
    If multiple code blocks exist, return the content of the last one;
    if no code block is found, return the original string with leading and trailing whitespace removed.
    """
    # Define regex patterns to match content between ```python and ```
    # \s* is used to trim surrounding whitespace
    patterns = [
        r'```python\s*(.*?)\s*```',  # Match ```python\n...content...\n```
    ]

    last_match = None
    # Iterate over all patterns
    for pattern in patterns:
        # Find all matches using re.finditer and convert to list
        matches = list(re.finditer(pattern, pred, re.DOTALL))
        if matches:
            # Take the last match found
            last_match = matches[-1].group(1)
    
    # If no matches found, return original string stripped of whitespace
    if last_match is None:
        return pred.strip()

    # Remove any trailing ``` or similar delimiters from the extracted content
    code = re.sub(r'(`{3,}.*)$', '', last_match.strip(), flags=re.IGNORECASE).strip()

    return code



def get_input(subproblem, turn_number, overall_turns, problem_description_now, history):
    # 1. Piecing together history
    if history:
        history_all = "\n\n".join(f'```python\n{item}\n```' for item in history)
    else:
        history_all = ""

    # 2. Extract sample_test_case (set to "" if not present)
    test_cases = subproblem.get("test_code")
    if isinstance(test_cases, list) and test_cases:
        sample_test_case = test_cases[0]
    else:
        sample_test_case = ""

    # 3. Choose different PROMPTs according to rounds and dependencies
    if turn_number == 1 and turn_number != overall_turns:
        # First round of input
        input_text = PROMPT1.format(
            problem_description=problem_description_now,
            name=subproblem["name"],
            statement=subproblem["statement"],
            sample_test_case=sample_test_case
        )

    elif turn_number == overall_turns:
        # Final round of input
        if subproblem.get("dependencies"):
            input_text = PROMPT3.format(
                problem_description=problem_description_now,
                name=subproblem["name"],
                statement=subproblem["statement"],
                dependencies=subproblem["dependencies"],
                history=history_all
            )
        else:
            input_text = PROMPT4.format(
                problem_description=problem_description_now,
                name=subproblem["name"],
                statement=subproblem["statement"],
                history=history_all
            )

    elif subproblem.get("dependencies"):
       # Intermediate turn, with dependencies
        input_text = PROMPT2.format(
            problem_description=problem_description_now,
            name=subproblem["name"],
            statement=subproblem["statement"],
            dependencies=subproblem["dependencies"],
            history=history_all,
            sample_test_case=sample_test_case
        )

    else:
        # Intermediate turn, no dependencies
        input_text = PROMPT5.format(
            problem_description=problem_description_now,
            name=subproblem["name"],
            statement=subproblem["statement"],
            history=history_all,
            sample_test_case=sample_test_case
        )

    return input_text
def ensure_python_code_block(s):
    prefix = "```python\n"
    if not s.startswith("```python"):
        return prefix + s
    return s

def ensure_python_code_block_main(s, subproblem):
    # Define a prefix to add when a Python code block does not exist
    prefix = f"""```python
import sys
def {subproblem["name"]}():
    input = sys.stdin.read().split()
"""
    # If there are multiple ```python markers, keep only the last one and the content after it
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
    # If there is a closing ```, remove it and everything after it
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
    Use AST to check if the code contains a print function call.
    """
    try:
        tree = ast.parse(code_str)
    except Exception:
        return False  # If parsing fails, assume there is no print call
    for node in ast.walk(tree):
        # Check if the node is a function call and the function name is 'print'
        if isinstance(node, ast.Call) and getattr(node.func, 'id', None) == 'print':
            return True
    return False
