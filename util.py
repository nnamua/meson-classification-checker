# SPDX-FileCopyrightText: 2021 Paul Aumann
#
# SPDX-License-Identifier: Apache-2.0

import multimethod, objects, functions, random, inspect, string, typing, re

def ismultimethod(obj) -> bool:
    """Returns whether the given object is a multimethod"""
    return isinstance(obj, multimethod.multimethod)

def iskwarg(param: inspect.Parameter) -> bool:
    """Returns whether the given parameter is to be supplied via keyword"""
    return param.default != inspect.Parameter.empty or param.kind == inspect.Parameter.KEYWORD_ONLY 

def isposonly(param: inspect.Parameter) -> bool:
    """Returns whether the given parameter is a *param parameter"""
    return param.kind == inspect.Parameter.VAR_POSITIONAL

def isarray(T) -> bool:
    """Returns whether the given type is a generic array"""
    return typing.get_origin(T) == objects.Array

def isunion(T) -> bool:
    """Returns whether the given type is a generic union"""
    return typing.get_origin(T) == typing.Union

def get_methods(obj: multimethod.multimethod):
    """Returns all methods of the multimethod"""
    if isinstance(obj, multimethod.multimethod):
        return list(obj.values())
    else:
        raise ValueError(f"Can only retriebe methods of multimethod, not {type(obj)}.")

def is_subclass(S, T) -> bool:
    """Custom issubclass() function, accepts generics"""
    s_origin = typing.get_origin(S)
    t_origin = typing.get_origin(T)
    if s_origin== None and t_origin == None:
        return issubclass(S, T)
    elif s_origin != None and t_origin != None:
        for s_arg in typing.get_args(S):
            found = False
            for t_arg in typing.get_args(T):
                if is_subclass(s_arg, t_arg):
                    found = True
            if not found:
                return False
        return is_subclass(s_origin, t_origin)
    elif s_origin != None and t_origin == None:
        return issubclass(s_origin, T)
    elif s_origin == None and t_origin != None:
        return issubclass(S, t_origin)

def is_array_type(A, T) -> bool:
    """Return whether the type T is a generic type of array type A"""
    if not isarray(A):
        return False
    else:
        # check if T is arg or in arg
        for arg in typing.get_args(A):
            if isunion(arg):
                for union_arg in typing.get_args(arg):
                    if is_subclass(T, union_arg):
                        return True
            elif isarray(arg):
                return is_array_type(arg, T)
            elif is_subclass(T, arg):
                return True
        return False

def in_generic_types(G, T) -> bool:
    """Returns whether the given type T is a generic type of type G"""
    if isarray(G):
        return is_array_type(G, T)
    elif isunion(G):
        for arg in typing.get_args(G):
            if is_subclass(T, arg):
                return True
        return False
    else:
        return False

def get_objects():
    """Returns all objects from the objects module"""
    predicate = lambda m : inspect.isclass(m) and m.__module__ == "objects"
    return [obj for name, obj in inspect.getmembers(objects, predicate=predicate)]
        
def get_functions():
    """Returns all functions from the functions module"""
    predicate = lambda m: callable(m) and m.__module__ == "functions"
    return [obj for name, obj in inspect.getmembers(functions, predicate=predicate)]

def get_type(type_name: str):
    """Evaluates and returns the class object of the given type string. """
    T = eval(type_name, objects.__dict__) if isinstance(type_name, str) else type_name
    return type(None) if T == None else T

def get_name(func) -> str:
    """Returns the name of the given function or multimethod"""
    # Remove a trailing _ from the function name, but only if there is exactly one trailing _
    name = get_methods(func)[0].__name__ if isinstance(func, multimethod.multimethod) else func.__name__
    return name.rstrip("_") if re.match(r".*[^_]_", name) else name

def pretty_print_func(func_name, params) -> str:
    """Returns a string representation of a function including a parameter combination"""
    param_strings = []
    for param in params:
        param_string = ""
        if iskwarg(param):
            param_string += param.name + " : "
        param_string += pretty_print_type(param.annotation)
        param_strings.append(param_string)
    return f"{func_name}({', '.join(param_strings)})"

def pretty_print_type(T) -> str:
    """Returns a string representation of a Type. Required, because names of generic types are not trivial."""
    if isinstance(T, typing._GenericAlias):
        string = "Union" if typing.get_origin(T) == typing.Union else typing.get_origin(T).__name__
        arg_names = [pretty_print_type(arg) for arg in typing.get_args(T)]
        return string + f"[{','.join(arg_names)}]"
    else:
        return T.__name__

def varname() -> str:
    """Returns a random string with length 10. Can be used as a variable name inside Meson."""
    return "".join(random.choices(string.ascii_lowercase + string.ascii_uppercase, k=10))

def get_parameter_combinations(method):
    """Returns all combinations of parameters of the given method."""
    # Store each combination of parameter types
    # Each parameter consists of (type of parameter, kind of parameter {keyword, positional, ...})
    combinations = [[]]

    for param in inspect.signature(method).parameters.values():
        param_type = get_type(param.annotation)
            
        """
        Some methods have Union[...] or Optional[...] as
        type annotation (Optional[T] -> Union[T, None]).
        In this case, we need to check every possible
        combination of parameter types.
        """
        if typing.get_origin(param_type) is typing.Union:
            """
            For each current parameter variant create
            a new variant for each type in the union.
            If NoneType is already in the variant, only
            add keyword-arguments
            """
            new_combinations = []
            for combination in combinations:
                for arg in typing.get_args(param_type):
                    # If arg is 'Any', just use a parameter
                    # of type Number (no check is required here)
                    new_param = param.replace(annotation=objects.Number) if arg is typing.Any else param.replace(annotation=arg)
                    new_combinations.append(combination + [new_param])
            combinations = new_combinations

        # Otherwise, just append the parameter to all variants
        else:
            for combination in combinations:
                # If param_type is 'Any', just use a parameter
                # of type Number (no check is required here)
                if param_type is typing.Any:
                    param_type = objects.Number
                new_param = param.replace(annotation=param_type)
                combination.append(new_param)

    return combinations

def red(string: str) -> str:
    """Wraps the given string in terminal color code red"""
    return "\033[91m" + string + "\033[0m"

def green(string: str) -> str:
    """Wraps the given string in terminal color code green"""
    return "\033[92m" + string + "\033[0m"

def yellow(string: str) -> str:
    """Wraps the given string in terminal color code yellow"""
    return "\033[93m" + string + "\033[0m"