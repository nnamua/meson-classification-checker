# Classification of meson objects and Tool for automatic checking

## Classification

Meson objects are classified in the file `objects.py`, and functions in the file `functions.py`.

## Tool

TL;DR: To execute the tool just run:
```
$ python3 main.py
```

Below follows the output of `python3 main.py -h`:
```
usage: main.py [-h] [--check-type-usages [TYPE_USAGES]]
               [--check-returnval-usages [RETURN_USAGES]]
               [--verbose [VERBOSE]] [--warnings [WARNINGS]]
               [--only-function-name [ONLY_FUNC_NAME]]
               [--summarize [SUMMARIZE]]
               [explicit [explicit ...]]

Tool to check a meson classification

positional arguments:
  explicit              Specify a function or a type that should be
                        checked.

optional arguments:
  -h, --help            show this help message and exit
  --check-type-usages [TYPE_USAGES]
                        When checking a type, also try every function and
                        method that expects an argument of this type.
  --check-returnval-usages [RETURN_USAGES]
                        When checking a return value, also try every
                        function and method that expects an argument of the
                        return type.
  --verbose [VERBOSE]   On error, output the meson.build and stdout
                        contents aswell.
  --warnings [WARNINGS]
                        Treat meson warnings as errors (not recommended,
                        will result in many errors on cross-compilation).
  --only-function-name [ONLY_FUNC_NAME]
                        Only displays the function (or method) name in a
                        check, without the parameter types.
  --summarize [SUMMARIZE]
                        Print a summary (how many failures, how many
                        successes).

```
