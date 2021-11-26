#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2021 Paul Aumann
#
# SPDX-License-Identifier: Apache-2.0

from log import Log
from templates import TemplateNotFoundException
import objects, functions, os, argparse, inspect, sys, util
from buildfile import BuildFile
from shutil import copyfile
from checkers import FunctionChecker, TypeChecker
from util import yellow, get_functions, get_objects

# argparser
parser = argparse.ArgumentParser(description="Tool to check a meson classification") 
parser.add_argument("explicit", default=None, nargs="*",
                    help="Specify a function or a type that should be checked.")
parser.add_argument("--check-type-usages", dest="type_usages", const=True, default=False, nargs="?",
                    help="When checking a type, also try every function and method that expects an argument of this type.")
parser.add_argument("--check-returnval-usages", dest="return_usages", const=True, default=False, nargs="?",
                    help="When checking a return value, also try every function and method that expects an argument of the return type.")
parser.add_argument("--verbose", dest="verbose", const=True, default=False, nargs="?",
                    help="On error, output the meson.build and stdout contents aswell.")
parser.add_argument("--warnings", dest="warnings", const=True, default=False, nargs="?",
                    help="Treat meson warnings as errors (not recommended, will result in many errors on cross-compilation).")
parser.add_argument("--only-function-name", dest="only_func_name", const=False, default=True, nargs="?",
                    help="Only displays the function (or method) name in a check, without the parameter types.")
parser.add_argument("--summarize", const=True, default=False, nargs="?",
                    help="Print a summary (how many failures, how many successes)." )
args = parser.parse_args()

TEMPLATE_FILES_FOLDER = os.path.join(os.getcwd(), "template_files")

# main()
if __name__ == "__main__":
    try:
        bf = BuildFile(project_languages=["c", "java"],verbose=args.verbose, warnings=args.warnings)
    except RuntimeError as e:
        print(f"{yellow('INTERNAL')}:: {e}")
        sys.exit()

    bf.append_line() # Padding

    # Add template files to buildfile source dir
    for template_file in os.listdir(TEMPLATE_FILES_FOLDER):
        path = os.path.join(TEMPLATE_FILES_FOLDER, template_file)
        bf.add_file(template_file, path)
    
    funcs = get_functions()
    types = get_objects()

    explicit = args.explicit
    if explicit != None and len(explicit) != 0:
        funcs = [ f for f in funcs if util.get_name(f) in explicit ]
        types = [ t for t in types if util.get_name(t) in explicit ]
        if len(funcs) == 0 and len(types) == 0:
            print(f"No function or type found for the given name(s): '{explicit}'")

    # Run TypeChecker for each type
    for T in types:
        try:
            checker = TypeChecker(T, bf,
                        check_type_usages=args.type_usages,
                        check_return_usages=args.return_usages,
                        only_func_name=args.only_func_name)
            checker.run()
        except TemplateNotFoundException as e:
            print(f"{yellow('INTERNAL')}:: {e}")
        except KeyboardInterrupt as e:
            print(f"{yellow('INTERNAL')}:: KeyboardInterrupt {' '*10}")
            break

    # Run FunctionChecker for each function
    for func in funcs:
        try:
            checker = FunctionChecker(func, bf,
                        check_return_usages=args.return_usages,
                        only_func_name=args.only_func_name)
            checker.run()
        except TemplateNotFoundException as e:
            print(f"{yellow('INTERNAL')}:: {e}")
        except KeyboardInterrupt as e:
            print(f"{yellow('INTERNAL')}:: KeyboardInterrupt {' '*10}")
            break

    if args.summarize:
        successful, failures = Log.result()
        print(f"Out of {successful + failures} total checks, {successful} were successful and {failures} were failures.")

    del bf
