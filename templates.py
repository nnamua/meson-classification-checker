# SPDX-FileCopyrightText: 2021 Paul Aumann
#
# SPDX-License-Identifier: Apache-2.0

from buildfile import IGNORE_STRING, BuildFile
from typing import Union
from util import varname
import objects, functions, os

"""
This file specifies templates for each type. The dictionary 'templates' contains
all regular templates, while the dictionary 'special' contains further template
dictionaries for functions and methods. In such a special template dictionary
the user can define templates for:
    (1) the object of the method
    (2) a certain parameter
    (3) a certain parameter and a type, using key (param_name, T)
    
The variable 'OBJECT' can be used to reference, that a method requires a special
object to operate on.
The variables 'RANDOM_STRING' and 'BUILDFILE_DIR' by a respective string on usage.
'RANDOM_STRING' is required for target names, because multiple target must not share
the name.
"""

class TemplateNotFoundException(Exception):
    pass

OBJECT = "_obj" # If a method requires a specific object, use this key in special templates
RANDOM_STRING = "$RANDOM_STRING$" # This substring will be replaced by a random string when fetching a template
BUILDFILE_DIR = "$BUILDFILE_DIR$" # This substring will be replaced by the working directory of the buildfile

def get_template(T, name=None, special_templates_key=None):
    """Returns the (special) template for a given type."""
    # Without a special templates key (or a non-existing one), return regular template
    if special_templates_key == None or special_templates_key not in special:
        try:
            tmpl = templates[T]
            return tmpl.replace(RANDOM_STRING, f"'{varname()}'")
        except KeyError:
            raise TemplateNotFoundException(f"No template found for type {T}")

    # Otherwise, return special template
    special_templates = special[special_templates_key]
    try:
        if (name, T) in special_templates:
            tmpl = special_templates[(name, T)]
        elif name in special_templates:
            tmpl = special_templates[name]
        elif T in special_templates:
            tmpl = special_templates[T]
        else:
            tmpl = templates[T]
    except KeyError:
        raise TemplateNotFoundException(f"No template found for type {T}")
    return tmpl.replace(RANDOM_STRING, f"'{varname()}'")

def has_special_template(T, name, special_templates_key):
    """Returns whether a special template exists for the given combination."""
    if special_templates_key not in special:
        return False
    special_templates = special[special_templates_key]
    return (name, T) in special_templates or name in special_templates

templates = {

    # Built-in objects
    objects.Boolean : "true",
    objects.Number : "42",
    objects.String : "'String'",
    objects.Dict : "{ 'foo' : 1, 'bar' : 2 }",
    objects.Array : "[ 'str', 1, true ]",
    objects.Meson : "meson",
    objects.BuildMachine : "build_machine",
    objects.HostMachine : "host_machine",
    objects.TargetMachine: "target_machine",

    # Returned objects
    objects.File : "files('foo.c')[0]",
    objects.ExternalFile : "files('foo.c')[0]",
    objects.Compiler : "meson.get_compiler('c')",
    objects.Dependency : "declare_dependency()",
    objects.Environment : "environment()",
    objects.ExternalProgram : "find_program('python3')",
    objects.ConfiguredFile : "configure_file(input : 'config.h.in', output: 'config.h', configuration: configuration_data())",
    objects.Executable : f"executable({RANDOM_STRING}, sources : ['foo.c'])",
    objects.BuildTarget : f"build_target({RANDOM_STRING}, sources : ['foo.c'], target_type : 'executable')",
    objects.Target : f"build_target({RANDOM_STRING}, sources : ['foo.c'], target_type : 'executable')",
    objects.Jar : f"jar({RANDOM_STRING}, sources: 'foo.java')",
    objects.ConfigurationData : "configuration_data({ 'foo' : 1, 'bar' : false })",
    objects.CustomTarget : f"custom_target({RANDOM_STRING}, output : 'bar.c', input : 'bar.txt', command : [ find_program('script.py'), '@INPUT@', '@OUTPUT@'])",
    objects.CustomTargetIndex : f"custom_target({RANDOM_STRING}, output : 'bar.c', input : 'bar.txt', command : [ find_program('script.py'), '@INPUT@', '@OUTPUT@'])[0]",
    objects.Disabler : "disabler()",
    objects.ExternalLibrary : "meson.get_compiler('c').find_library('m', required : false)",
    objects.FeatureOption : "get_option('ft')",
    objects.Generator : f"generator(executable({RANDOM_STRING}, sources: 'foo.c'), arguments : [ 'foo', '@EXTRA_ARGS@' ], output : '@BASENAME@')",
    objects.Subproject : "subproject('foo_project')",
    objects.RunResult : f"run_command(find_program('script.py'), [])",
    objects.CompilationRunResult : f"meson.get_compiler('c').run('foo.c')",
    objects.Module : "import('keyval')",
    objects.IncludeDirectory : "include_directories('include')",
    objects.BothLibraries : f"both_libraries({RANDOM_STRING}, sources : 'foo.c')",
    objects.Library : f"library({RANDOM_STRING}, sources : 'foo.c')",
    objects.SharedLibrary : f"shared_library({RANDOM_STRING}, sources : 'foo.c')",
    objects.StaticLibrary : f"static_library({RANDOM_STRING}, sources : 'foo.c')",
    objects.Range : "range(0,10,1)",
    objects.SharedModule : f"shared_module({RANDOM_STRING}, sources : 'foo.c')",
    objects.GeneratorTarget : "generator(find_program('script.py'), output : '@BASENAME@.c', arguments : [ '@INPUT@' ]).process('foo.c')",
    objects.RunTarget : f"run_target({RANDOM_STRING}, command : ['meson'])",

    # Arrays with specified type
    objects.Array[objects.Boolean] : "[ true, false ]",
    objects.Array[objects.Number] : "[ 1, 2, 3 ]",
    objects.Array[objects.String] : "[ 'foo', 'bar' ]",
    objects.Array[objects.File] : "files('foo.c', 'bar.c')",
    objects.Array[objects.ExternalFile] : "files('foo.c', 'bar.c')",
    objects.Array[objects.Dependency] : "[ declare_dependency(), declare_dependency() ]",
    objects.Array[objects.Target] : f"[ build_target({RANDOM_STRING}, sources : ['foo.c'], target_type : 'executable') ]",
    objects.Array[objects.IncludeDirectory] : "include_directories('include')",
    objects.Array[objects.Library] : f"[ library({RANDOM_STRING}, 'foo.c') ]",
    objects.Array[objects.CustomTarget] : f"[custom_target({RANDOM_STRING}, output : 'bar.c', input : 'bar.txt', command : [ find_program('script.py'), '@INPUT@', '@OUTPUT@'])]",
    objects.Array[Union[objects.String, objects.Number]] : "[ 'str', 2 ]",
    objects.Array[Union[objects.String, objects.File]] : "[ files('foo.c')[0], 'bar.c' ]",
    objects.Array[Union[objects.String, objects.Target]] : f"[ 'bar.c', build_target({RANDOM_STRING}, sources : ['foo.c'], target_type : 'executable') ]",
    objects.Array[Union[objects.String, objects.File, objects.Target]] : f"[ files('foo.c')[0], 'bar.c', build_target({RANDOM_STRING}, sources : ['foo.c'], target_type : 'executable') ]", 
    objects.Array[Union[objects.Library, objects.CustomTarget]] : f"[ library({RANDOM_STRING}, 'foo.c') ]",
    objects.Array[Union[objects.ExternalLibrary, objects.CustomTarget]] : "[ meson.get_compiler('c').find_library('m', required : false) ]",
    objects.Array[Union[objects.IncludeDirectory, objects.String]] : "[ include_directories('include'), 'include' ]"
}

special = {

    objects.String.join : {
        "list_of_strings" : "[ 'str1', 'str2' ]"
    },

    objects.String.to_int : {
        OBJECT : "'42'" 
    },

    objects.Dict.get : {
        "key" : "'foo'"
    },

    objects.Array.get : {
        OBJECT : "[ 1, 2, 3]",
        "index" : "0"
    },

    objects.Array.__getitem__ : {
        OBJECT : "[ 1, 2, 3]",
        "index" : "0"
    },

    objects.Compiler.alignment : {
        "type_name" : "'int'",
        "args" : "[]"
    },

    objects.Compiler.check_header : {
        "header_name" : "'stdio.h'",
        "dependencies" : "[]",
        "prefix" : "''",
        "required" : "false"
    },

    objects.Compiler.compute_int : {
        "expr" : "'1 + 2'"
    },

    objects.Compiler.get_supported_function_attributes : {
        "list_of_names" : "[ 'error' ]"
    },

    objects.Compiler.has_function_attribute : {
        "name" : "'error'"
    },

    objects.Compiler.has_header : {
        "header_name" : "'stdio.h'",
        "dependencies" : "[]",
        "prefix" : "''",
        "args" : "[ '-Werror' ]",
        ("required", objects.Boolean) : "false"
    },
    
    objects.Compiler.has_header_symbol : {
        "header_name" : "'stdio.h'",
        "symbol_name" : "'printf'",
        "dependencies" : "[]",
        "prefix" : "''",
        "args" : "[ '-Werror' ]",
        ("required", objects.Boolean) : "false"
    },

    objects.CustomTarget.__getitem__ : {
        "index" : "0",
    },

    objects.Meson.get_compiler : {
        "language" : "'c'"
    },

    objects.Meson.add_dist_script : {
        ("script_name", objects.String) : "'script.py'",
        ("script_name", objects.File) : "files('script.py')[0]"
    },

    objects.Meson.add_install_script : {
        ("script_name", objects.String) : "'script.py'",
        ("script_name", objects.File) : "files('script.py')[0]"
    },

    objects.Meson.add_postconf_script : {
        ("script_name", objects.String) : "'script.py'",
        ("script_name", objects.File) : "files('script.py')[0]"
    },

    objects.BuildTarget.extract_objects : {
        "sources" : "'foo.c'"
    },

    objects.ConfigurationData.get : {
        OBJECT : "configuration_data({ 'foo' : 1, 'bar' : false })",
        "var_name" : "'foo'"
    },

    objects.ConfigurationData.get_unquoted : {
        OBJECT : "configuration_data({ 'foo' : 1, 'bar' : false })",
        "var_name" : "'foo'"
    },

    objects.Dependency.as_system : {
        "value" : "'preserve'"
    },

    objects.Generator.process : {
        "extra_args" : "[ 'bar' ]",
        "preserve_path_from" : "'C:/'" if os.name == "nt" else "'/'"
    },

    objects.Range.__getitem__ : {
        "index" : "0"
    },

    objects.BothLibraries.extract_objects : {
        # https://mesonbuild.com/Build-targets.html#object-files
        # No sources can be extracted in this simple template example
        "sources" : "[]"
    },

    functions.add_global_arguments : {
        ("language", objects.String) : "'c'",
        ("language", objects.Array[objects.String]) : "['c', 'cpp']"
    },

    functions.add_global_link_arguments : {
        ("language", objects.String) : "'c'",
        ("language", objects.Array[objects.String]) : "['c', 'cpp']"
    },

    functions.add_languages : {
        ("langs", objects.String) : "'c'",
        ("langs", objects.Array[objects.String]) : "['c', 'cpp']"
    },

    functions.add_project_arguments : {
        ("language", objects.String) : "'c'",
        ("language", objects.Array[objects.String]) : "['c', 'cpp']"
    },

    functions.add_project_link_arguments : {
        ("language", objects.String) : "'c'",
        ("language", objects.Array[objects.String]) : "['c', 'cpp']"
    },
    
    functions.add_test_setup : {
        ("env", objects.Array[objects.String]) : "['key1=val1', 'key2=val2']",
        ("env", objects.Dict) : "{ 'key1' : 'value1', 'key2' : 'value2' }",
    },

    functions.benchmark : {
        "name" : RANDOM_STRING,
        ("executable", objects.ExternalFile) : "files('script.py')[0]",
        "workdir" : f"'{os.getcwd()}'",
        "protocol" : "'exitcode'",
        ("env", objects.Array[objects.String]) : "['key1=val1', 'key2=val2']",
        ("env", objects.Dict) : "{ 'key1' : 'value1', 'key2' : 'value2' }",
    },

    functions.both_libraries : {
        "library_name" : RANDOM_STRING,
        ("sources", objects.String) : "'foo.c'",
        "install_mode" : "'rwxr-xr-x'",
        "override_options" : "[ 'key1=value1', 'key2=value2' ]",
        "link_whole" : f"[ static_library({RANDOM_STRING}, 'foo.c') ]",
        "link_with": f"[ static_library({RANDOM_STRING}, 'foo.c') ]"
    },

    functions.build_target : {
        "name" : RANDOM_STRING,
        ("sources", objects.String) : "'foo.c'",
        "install_mode" : "'rwxr-xr-x'",
        "override_options" : "[ 'key1=value1', 'key2=value2' ]",
        "link_whole" : f"[ static_library({RANDOM_STRING}, 'foo.c') ]",
        "link_with": f"[ static_library({RANDOM_STRING}, 'foo.c') ]",
        "target_type" : "'executable'",
        "win_subsystem" : "'console'",
        "gnu_symbol_visibility" : "''",
        "link_language" : "'c'"
    },

    functions.configuration_data : {
        "dict" : "{ 'foo' : 1, 'bar' : false }"
    },

    functions.configure_file : {
        "format" : "'meson'",
        "output_format" : "'c'",
        ("depfile", objects.String) : "'foo.c'",
        ("input", objects.String) : "'bar.c'",
        "install_mode" : "'rwxr-xr-x'"
    },

    functions.custom_target : {
        "name" : RANDOM_STRING,
        "install_mode" : "'rwxr-xr-x'",
        ("env", objects.Array[objects.String]) : "['key1=val1', 'key2=val2']",
        ("env", objects.Dict) : "{ 'key1' : 'value1', 'key2' : 'value2' }",
    },

    functions.declare_dependency : {
        ("variables", objects.Dict) : "{ 'key1' : 'value1', 'key2' : 'value2' }",
        ("variables", objects.Array[objects.String]) : "[ 'key1=value1', 'key2=value2' ]",
        ("include_directories", objects.String) : "'include'"
    },
    
    functions.dependency : {
        "dependency_name" : "'netcdf'",
        "language" : "'c'",
        "method" : "'auto'",
        "default_options" : "[ 'key1=value1', 'key2=value2' ]",
        ("fallback", objects.String) : "'foo_project'",
        ("fallback", objects.Array[objects.String]) : "[ 'foo_project', 'foo_dep' ]",
        "required" : "false",
        "include_type" : "'preserve'"
    },

    functions.error : {
        "message" : f"'{IGNORE_STRING}'"
    },

    functions.environment : {
        "dict" : "{ 'key1' : 'value1', 'key2' : 'value2' }"
    },

    functions.executable : {
        "exe_name" : RANDOM_STRING,
        ("sources", objects.String) : "'foo.c'",
        "install_mode" : "'rwxr-xr-x'",
        "override_options" : "[ 'key1=value1', 'key2=value2' ]",
        "link_whole" : f"[ static_library({RANDOM_STRING}, 'foo.c') ]",
        "link_with": f"[ static_library({RANDOM_STRING}, 'foo.c') ]",
        "win_subsystem" : "'console'",
        "gnu_symbol_visibility" : "''",
        "link_language" : "'c'"
    },

    functions.find_program : {
        "program_names" : "'script.py'",
        "dirs" : f"'{os.getcwd()}'",
        "version" : "'1.0'"
    },

    functions.files : {
        "list_of_files" : "'foo.c'"
    },

    functions.generator : {
        "output" : "'@BASENAME@.c'"
    },

    functions.get_option : {
        "option_name" : "'ft'"
    },

    functions.import_ : {
        "name" : "'keyval'"
    },

    functions.include_directories : {
        "directory_names" : "'include'"
    },

    functions.install_data : {
        "install_mode" : "'rwxr-xr-x'"
    },

    functions.install_headers : {
        "install_mode" : "'rwxr-xr-x'"
    },

    functions.install_man : {
        ("list_of_manpages", objects.String) : "'manpage.6'",
        ("list_of_manpages", objects.ExternalFile) : "files('manpage.6')[0]",
        "install_mode" : "'rwxr-xr-x'"
    },

    functions.install_subdir : {
        "subdir_name" : "'subdir'",
        "install_mode" : "'rwxr-xr-x'"
    },

    functions.jar : {
        "jar_name" : RANDOM_STRING,
        ("sources", objects.String) : "'foo.java'",
        ("sources", objects.Array[Union[objects.String, objects.File]]) : "[ 'foo.java', files('foo.java')[0] ]",
        "install_mode" : "'rwxr-xr-x'",
        "override_options" : "[ 'key1=value1', 'key2=value2' ]",
        "link_whole" : f"[ static_library({RANDOM_STRING}, 'foo.c') ]",
        "link_with": f"[ static_library({RANDOM_STRING}, 'foo.c') ]",
        "gnu_symbol_visibility" : "''",
        "link_language" : "'c'"
    },

    functions.library : {
        "library_name" : RANDOM_STRING,
        ("sources", objects.String) : "'foo.c'",
        "install_mode" : "'rwxr-xr-x'",
        "override_options" : "[ 'key1=value1', 'key2=value2' ]",
        "link_whole" : f"[ static_library({RANDOM_STRING}, 'foo.c') ]",
        "link_with": f"[ static_library({RANDOM_STRING}, 'foo.c') ]",
        "gnu_symbol_visibility" : "''",
        "link_language" : "'c'"
    },

    functions.project : {
        "meson_version" : "'>=0.55.0'",
        "default_options" : "[ 'key1=value1', 'key2=value2' ]",
        "list_of_languages" : "'c'"
    },

    functions.run_command : {
        ("env", objects.Array[objects.String]) : "[ 'key1=value1', 'key2=value2' ]",
        ("env", objects.Dict) : "{ 'key1' : 'value1', 'key2' : 'value2' }",
        ("command", objects.String) : "'script.py'",
        ("command", objects.Array[objects.File]) : "files('script.py')",
        "check" : "false"
    },

    functions.run_target : {
        "target_name" : RANDOM_STRING,
        ("env", objects.Array[objects.String]) : "[ 'key1=value1', 'key2=value2' ]",
        ("env", objects.Dict) : "{ 'key1' : 'value1', 'key2' : 'value2' }",
        "command" : f"[ 'script.py', build_target({RANDOM_STRING}, sources : ['foo.c'], target_type : 'executable') ]",
    },

    functions.shared_library : {
        "library_name" : RANDOM_STRING,
        ("sources", objects.String) : "'foo.c'",
        "install_mode" : "'rwxr-xr-x'",
        "override_options" : "[ 'key1=value1', 'key2=value2' ]",
        "link_whole" : f"[ static_library({RANDOM_STRING}, 'foo.c') ]",
        "link_with": f"[ static_library({RANDOM_STRING}, 'foo.c') ]",
        "gnu_symbol_visibility" : "''",
        "link_language" : "'c'",
        "soversion" : "'0'",
        "version" : "'1.0.0'",
        ("darwin_versions", objects.Number) : "1",
        ("darwin_versions", objects.String) : "'1'",
        ("darwin_versions", objects.Array[objects.String]) : "[ '1' ]",
        ("vs_module_defs", objects.String) : "'bar.txt'"
    },

    functions.shared_module : {
        "module_name" : RANDOM_STRING,
        ("sources", objects.String) : "'foo.c'",
        "install_mode" : "'rwxr-xr-x'",
        "override_options" : "[ 'key1=value1', 'key2=value2' ]",
        "link_whole" : f"[ static_library({RANDOM_STRING}, 'foo.c') ]",
        "link_with": f"[ static_library({RANDOM_STRING}, 'foo.c') ]",
        "gnu_symbol_visibility" : "''",
        "link_language" : "'c'",
        ("vs_module_defs", objects.String) : "'bar.txt'"
    },

    functions.static_library : {
        "library_name" : RANDOM_STRING,
        ("sources", objects.String) : "'foo.c'",
        "install_mode" : "'rwxr-xr-x'",
        "override_options" : "[ 'key1=value1', 'key2=value2' ]",
        "link_whole" : f"[ static_library({RANDOM_STRING}, 'foo.c') ]",
        "link_with": f"[ static_library({RANDOM_STRING}, 'foo.c') ]",
        "gnu_symbol_visibility" : "''",
        "link_language" : "'c'"
    },

    functions.subdir : {
        "dir_name" : "'subdir'"
    },

    functions.subproject : {
        "subproject_name" : "'foo_project'",
        "default_options" : "[ 'key1=value1', 'key2=value2' ]",
        "version" : "'>=1.0'"
    },

    functions.test : {
        "name" : RANDOM_STRING,
        ("executable", objects.ExternalFile) : "files('script.py')[0]",
        "workdir" : f"'{os.getcwd()}'",
        "protocol" : "'exitcode'",
        ("env", objects.Array[objects.String]) : "['key1=val1', 'key2=val2']",
        ("env", objects.Dict) : "{ 'key1' : 'value1', 'key2' : 'value2' }",
        "should_fail" : "false"
    },

    functions.range : {
        "start" : "0",
        "stop" : "10",
        "step" : "1"
    }

}