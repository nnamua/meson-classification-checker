# Classification of meson objects and Tool for automatic checking

## Classification

Meson objects are classified in the file `objects.py`, and functions in the file `functions.py`.

## Tool

positional arguments:

* `explicit` A list of objects and functions that should be checked. If left empty, entire classification will be checked.

optional arguments:

* `-h, --help` Displays a help message.
* `--check-type-usages` When checking a type, also try every function and method that expects an argument of this type.
* `--check-returnval-usages` When checking a return value, also try every function and method that expects an argument of the return type.
* `--verbose` On error, output the meson.build and stdout contents aswell.
* `--warnings` Treat meson warnings as errors (not recommended, will result in many errors on cross-compilation).
* `--only-function-name` Only displays the function (or method) name in a check, without the parameter types.
* `--summarize` Print a summary (how many failures, how many successes).
