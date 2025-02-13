# import dis, ast, inspect

# def short_add(): 
#     return 9 + 9

# def long_add(): 
#     nine = 9; 
#     return 9 + nine

# def see_python_internals(func):
#     print("co_code: " + str(func.__code__.co_code))
#     print("dis.dis: ")
#     dis.dis(func)
#     ast.dump(ast.parse(func))
    
# see_python_internals(short_add)
# see_python_internals(long_add)


import ast  
 
# Creating AST
code = ast.parse("print(10+12)")  
# Printing AST
print(ast.dump(code))