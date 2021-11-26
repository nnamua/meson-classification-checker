# SPDX-FileCopyrightText: 2021 Paul Aumann
#
# SPDX-License-Identifier: Apache-2.0

from typing import List, Union
import templates, inspect
from util import iskwarg, varname, get_parameter_combinations, ismultimethod, get_methods

"""
    The following generator are used to generate lines for different checks.
    They will only create the required lines, but will append them to a buildfile or
    check in any other way.
"""

# Defines how many parameters a magic method takes
magic_methods = { "__add__" : 1, "__sub__" : 1, "__mult__" : 1, "__div__" : 1,
                  "__mod__" : 1, "__getitem__" : 1, "__setitem__" : 2, "__contains__" : 1 }

class FunctionGenerator:
    """This class provides methods to generate lines for a function call"""

    def __init__(self, func_name: str, parameters, special_templates_key=None, existing_objects=None):
        self.func_name = func_name
        self.parameters = parameters
        self.special_templates_key = special_templates_key
        self.existing_objects = dict() if existing_objects == None else existing_objects

    def _generate_call_line(self, param_strings: List[str], return_var: str) -> str:
        """Generates the line of the function invocation"""
        call = f"{self.func_name}({','.join(param_strings)})"
        return f"{return_var} = {call}" if return_var != None else call

    def _generate_parameter_lines(self, inline: bool = False) -> Union[List[str], List[str]]:
        """ Generates lines with an object creation for each parameter"""
        
        """
        For each parameter:
            (1) Add a variable to the lines list that will be supplied as a parameter
            (2) Build a string of variable names that the method will receive (-> "a, b, c, kw : d" )
        After a parameter of NoneType is encountered, only allow keyword arguments.
        Eventually, append a call to the method to the lines list.
        """
        lines = []
        param_strings = [] # Strings of variable names
        kwargs_only = False
        for param in self.parameters:
            param_type = param.annotation

            # Check if only keyword arguments should be allowed afterwards
            if param_type == type(None):
                kwargs_only = True
                continue

            # If only keyword arguments are allowed, check if current parameter is kwarg
            if kwargs_only and not iskwarg(param):
                continue

            param_template = templates.get_template(param_type, name=param.name,
                                special_templates_key=self.special_templates_key)

            # If 'inline' is set to false, generate variables for each argument
            # Otherwise, create objects in the method call
            # (Required for project()-call, because it must be first statement in file)
            if not inline:
                # Also, if an object already exists for the parameter (-> entry in existing_objects),
                # use the variable name specified there.
                if param.name in self.existing_objects:
                    param_var = self.existing_objects[param.name]
                else:
                    param_var = varname()
                    lines.append(f"{param_var} = {param_template}")

                # Add parameter as keyword argument after kwargs has been set to True
                if iskwarg(param):
                    param_strings.append(f"{param.name} : {param_var}")
                else:
                    param_strings.append(param_var)
            else:
                # Check if object already exists too
                param_var = self.existing_objects[param.name] if param.name in self.existing_objects else param_template
                if iskwarg(param):
                    param_strings.append(f"{param.name} : {param_var}")
                else:
                    param_strings.append(param_var)
        
        return (lines, param_strings)

    def generate_lines(self, return_var: str, inline: bool = False) -> List[str]:
        """Returns all lines required for a function call."""
        lines, param_strings = self._generate_parameter_lines(inline=inline)
        call = self._generate_call_line(param_strings, return_var=return_var)
        lines.append(call)
        return lines

class MethodGenerator(FunctionGenerator):
    """This class provides methods to generate lines for a method call"""

    def __init__(self, method_name: str, obj_name: str, parameters, special_templates_key=None, existing_objects=None):
        super().__init__(method_name, parameters, special_templates_key=special_templates_key, existing_objects=existing_objects)
        self.obj_name = obj_name

    def _generate_call_line(self, param_strings, return_var: str) -> str:
        """Generates a line for the function invocation. Resolves special method names."""
        # Check if enough arguments are supplied for magic method
        if self.func_name in magic_methods and len(param_strings) != magic_methods[self.func_name]:
            raise ValueError(f"{self.func_name} must be called with exactly 1 argument (not {len(param_strings)}).")

        # TODO: Could be replaced with match statement in py 3.10
        # Handle magic methods
        if self.func_name == "__add__":
            call = f"{self.obj_name} + {param_strings[0]}"

        elif self.func_name == "__sub__":
            call = f"{self.obj_name} - {param_strings[0]}"

        elif self.func_name == "__mult__":
            call = f"{self.obj_name} * {param_strings[0]}"

        elif self.func_name == "__div__":
            call = f"{self.obj_name} / {param_strings[0]}"

        elif self.func_name == "__mod__":
            call = f"{self.obj_name} % {param_strings[0]}"

        elif self.func_name == "__getitem__":
            call = f"{self.obj_name}[{param_strings[0]}]"

        elif self.func_name == "__setitem__":
            call = f"{self.obj_name}[{param_strings[0]}] = {param_strings[1]}"

        elif self.func_name == "__contains__":
            call = f"{param_strings[0]} in {self.obj_name}"

        else:
            call = f"{self.obj_name}.{self.func_name}({','.join(param_strings)})"

        return f"{return_var} = {call}" if return_var != None else call


class ReturnTypeGenerator():
    """This class provides methods to generate lines for a returnvalue type check"""

    def __init__(self, T, obj_name: str):
        self.T = T
        self.obj_name = obj_name

    def generate_lines(self) -> List[str]:
        """Generates lines required for a returnvalue type check"""
        lines = []
        # Iterate over methods
        for name, mm in inspect.getmembers(self.T, predicate=ismultimethod):

            # Check if multimethod has special templates
            special_templates = templates.special[mm] if mm in templates.special else None

            # TODO: Right now, if this method requires a special object of its type, skip it
            if special_templates != None and templates.OBJECT in special_templates:
                continue

            # Generate lines for each method, dont check return type
            for method in get_methods(mm):
                """
                Since parameters can be optional, there are multiple combinations of parameters that
                need to be tested.
                """
                for parameter_combination in get_parameter_combinations(method):
                    check = MethodGenerator(name, self.obj_name, parameter_combination, special_templates_key=mm)
                    lines += check.generate_lines(None)
        return lines
