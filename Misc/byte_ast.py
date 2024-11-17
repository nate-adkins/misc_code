# By Nathan Adkins 
# 07/02/2023

import dis

def short_add():
    return 9 + 9

def long_add():
    variable_nine = 9 
    return 9 * variable_nine

def see_python_internals(func):
    print("__code__: " + str(func.__code__))
    print("co_consts: " + str(func.__code__.co_consts))
    print("co_varnames: " + str(func.__code__.co_varnames))
    print("co_code: " + str(func.__code__.co_code))
    print("dis.dis: " + str(dis.dis(func)))
    print("\n")

see_python_internals(short_add)
see_python_internals(long_add)