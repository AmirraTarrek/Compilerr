import ast
import astor

# Optimization

input_code = """
x = 7
y = 5
z = y + 3 + x
"""

##############################################################################

def constant(r, dictionary):  # x=5 =>> 5=5
    if isinstance(r, ast.Name) and r.id in dictionary:
        return ast.Constant(value=dictionary[r.id])
    return r

##############################################################################

def assignment(s, dictionary):   #x=5 , y=x+1 =>> y=5+1
    if isinstance(s, ast.Assign):
        for i in s.targets:
            if isinstance(i, ast.Name) and isinstance(s.value, ast.Constant):
                dictionary[i.id] = s.value.value
    return s

##############################################################################

def apply_constant_propagation(q, dictionary):
    q = constant(q, dictionary)
    q = assignment(q, dictionary)
    
    for field, val in ast.iter_fields(q):
        if isinstance(val, list):
            new_A = [apply_constant_propagation(i, dictionary) if isinstance(i, ast.AST) else i for i in val]
            setattr(q, field, new_A)
        elif isinstance(val, ast.AST):
            new_B = apply_constant_propagation(val, dictionary)
            setattr(q, field, new_B)

    return q

##############################################################################

def parse_optimize(code):
    dictionary = {}
    parsed_code = ast.parse(code)
    applied_code = apply_constant_propagation(parsed_code, dictionary)
    optimized_code = astor.to_source(applied_code)
    return optimized_code

##############################################################################

output_code = parse_optimize(input_code)
print("\nBefore Optimization", input_code)
print("After Optimization\n", output_code)
