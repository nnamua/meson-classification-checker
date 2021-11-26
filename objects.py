# SPDX-FileCopyrightText: 2021 Paul Aumann
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
from typing import Union, Any, TypeVar, Optional, Generic
import multimethod

T = TypeVar("T")

# Basic types
class Boolean(metaclass=multimethod.multimeta):
    
    def to_int(
    ) -> Number:
        pass

    def to_string(
    ) -> String:
        ...

    def to_string(
        true_string: String,
        false_string: String
    ) -> String:
        ...

    #def fail() -> Number:
    #    ...

class Number(metaclass=multimethod.multimeta):

    def __add__(
        other: Number
    ) -> Number:
        ...

    def __mult__(
        other: Number
    ) -> Number:
        ...

    def __mod__(
        other: Number
    ) -> Number:
        ...
    
    def is_even(
    ) -> Boolean:
        ...
    
    def is_odd(
    ) -> Boolean:
        ...

    def to_string(
    ) -> String:
        ...

class String(metaclass=multimethod.multimeta):
    
    def __add__(
        other: String
    ) -> String:
        ...

    def __div__(
        other: String
    ) -> String:
        ...

    def contains(
        string: String
    ) -> Boolean:
        ...

    def endswith(
        string: String
    ) -> Boolean:
        ...

    def format(
        *args: Any
    ) -> String:
        ...

    def join(
        list_of_strings: Array[String]
    ) -> String:
        ...

    def replace(
        old_str: String,
        new_str: String
    ) -> String:
        ...

    def split(
        split_character: Optional[String]
    ) -> Array[String]:
        ...

    def startswith(
        string: String
    ) -> Boolean:
        ...

    def substring(
        start: Optional[Number],
        end: Optional[Number]
    ) -> String:
        ...

    def strip(
        string: Optional[String]
    ) -> String:
        ...

    def to_int(
    ) -> Number:
        ...

    def to_lower(
    ) -> String:
        ...

    def to_upper(
    ) -> String:
        ...

    def underscorify(
    ) -> String:
        ...

    def version_compare(
        comparison_string: String
    ) -> Boolean:
        ...

class Dict(metaclass=multimethod.multimeta):

    def __add__(
        other: Dict
    ) -> Dict:
        ...

    def __contains__(
        item: String
    ) -> Boolean:
        ...
    
    def has_key(
        key: String
    ) -> Boolean:
        ...

    def get(
        key: String,
        fallback: Optional[Any]
    ) -> Any:
        ...

    def keys(
    ) -> Array[String]:
        ...

class Array(Generic[T], metaclass=multimethod.multimeta):

    def __add__(
        other: Array
    ) -> Array:
        ...

    def __getitem__(
        index: Number
    ) -> Any:
        ...

    def __contains__(
        item: Any
    ) -> Boolean:
        ...

    def contains(
        item: Any
    ) -> Boolean:
        ...

    def get(
        index: Number,
        fallback: Optional[Any]
    ) -> Any:
        ...

    def length(
    ) -> Number:
        ...

class Meson(metaclass=multimethod.multimeta):

    def add_dist_script(
        script_name: Union[File, String],
        *args: Union[File, String]
    ) -> None:
        ...

    def add_install_script(
        script_name: Union[File, String],
        *args: Union[File, String],
        skip_if_destdir: Boolean = None
    ) -> None:
        ...

    def add_postconf_script(
        script_name: Union[File, String],
        *args: Union[File, String]
    ) -> None:
        ...

    def backend(
    ) -> String:
        ...

    # deprecated
    def build_root(
    ) -> String:
        ...

    # deprecated
    def source_root(
    ) -> String:
        ...

    def project_build_root(
    ) -> String:
        ...

    def global_build_root(
    ) -> String:
        ...

    def global_source_root(
    ) -> String:
        ...

    def current_build_dir(
    ) -> String:
        ...

    def current_source_dir(
    ) -> String:
        ...

    def get_compiler(
        language: String
    ) -> Compiler:
        ...

    # deprecated
    def get_cross_property(
        prop_name: String,
        fallback_value: Any
    ) -> Any:
        ...

    def get_external_property(
        prop_name: String,
        fallback_value: Any,
        native: Boolean = None
    ) -> Any:
        ...

    def has_external_property(
        prop_name: String,
        native: Boolean = None
    ) -> Boolean:
        ...

    def can_run_host_binaries(
    ) -> Boolean:
        ...

    # deprecated
    def has_exe_wrapper(
    ) -> Boolean:
        ...

    def install_dependency_manifest(
        output_name: Union[String, ExternalFile]
    ) -> None:
        ...

    def is_cross_build(
    ) -> Boolean:
        ...

    def is_subproject(
    ) -> Boolean:
        ...

    def is_unity(
    ) -> Boolean:
        ...

    def override_find_program(
        prog_name: String,
        program: Union[ExternalProgram, ConfiguredFile, Executable]
    ) -> None:
        ...

    def override_dependency(
        name: String,
        dep_object: Dependency,
        native: Boolean = None
    ) -> None:
        ...

    def project_version(
    ) -> String:
        ...

    def project_license(
    ) -> Array[String]:
        ...

    def project_name(
    ) -> String:
        ...

    def version(
    ) -> String:
        ...

    def add_devenv(
        env: Environment
    ) -> None:
        ...

class BuildMachine(metaclass=multimethod.multimeta):

    def cpu_family(
    ) -> String:
        ...

    def cpu(
    ) -> String:
        ...

    def system(
    ) -> String:
        ...

    def endian(
    ) -> String:
        ...

class HostMachine(metaclass=multimethod.multimeta):
    
    def cpu_family(
    ) -> String:
        ...

    def cpu(
    ) -> String:
        ...

    def system(
    ) -> String:
        ...

    def endian(
    ) -> String:
        ...

class TargetMachine(metaclass=multimethod.multimeta):

    def cpu_family(
    ) -> String:
        ...

    def cpu(
    ) -> String:
        ...

    def system(
    ) -> String:
        ...

    def endian(
    ) -> String:
        ...

# Function-generated types
class File(metaclass=multimethod.multimeta):

    def full_path(
    ) -> String:
        ...

class ExternalFile(File, metaclass=multimethod.multimeta):
    ...

class Target(File, metaclass=multimethod.multimeta):
    ...

class Compiler(File, metaclass=multimethod.multimeta):

    def alignment(
        type_name: String,
        dependencies: Array[Dependency] = None,
        args: Array[Union[String, File]] = None
    ) -> Number:
        ...

    def cmd_array(
    ) -> Array[String]:
        ...

    def compiles(
        code: Union[String, File],
        dependencies: Array[Dependency] = None,
        no_builtin_args: Boolean = None,
        name: String = None,
        args: Array[Union[String, File]] = None
    ) -> Boolean:
        ...

    def compute_int(
        expr: String,
        low: Number = None,
        high: Number = None,
        guess: Number = None,
        no_builtin_args: Boolean = None,
        args: Array[Union[String, File]] = None
    ) -> Number:
        ...

    def find_library(
        lib_name: String,
        required: Union[Boolean, FeatureOption] = None,
        dirs: Union[Array[String], String] = None,
        disabler: Boolean = None,
        has_headers: Array[Union[String, File]] = None,
        header_dependencies: Array[Dependency] = None,
        header_prefix: String = None,
        header_required: Union[Boolean, FeatureOption] = None,
        static: Boolean = None
    ) -> Library:
        ...

    def first_supported_argument(
        list_of_strings: Array[String]
    ) -> Union[String, Array]:
        ...

    def first_supported_link_argument(
        list_of_strings: Array[String]
    ) -> Union[String, Array]:
        ...

    def get_define(
        define_name: String,
        prefix: String = None,
        no_builtin_args: Boolean = None
    ) -> String:
        ...

    def get_id(
    ) -> String:
        ...

    def get_argument_syntax(
    ) -> String:
        ...

    def get_linker_id(
    ) -> String:
        ...

    def get_supported_arguments(
        list_of_string: Array[String]
    ) -> Array[String]:
        ...

    def get_supported_link_arguments(
        list_of_string: Array[String]
    ) -> Array[String]:
        ...
    
    def has_argument(
        argument_name: String
    ) -> Boolean:
        ...

    def has_link_argument(
        argument_name: String
    )-> Boolean:
        ...

    def has_function(
        func_name: String,
        prefix: String = None,
        no_builtin_args: Boolean = None,
        args: Array[Union[String, File]] = None
    ) -> Boolean:
        ...

    def check_header(
        header_name: String,
        dependencies: Array[Dependency] = None,
        prefix: String = None,
        required: Union[Boolean, FeatureOption] = None,
        no_builtin_args: Boolean = None,
        args: Array[Union[String, File]] = None,
        include_directories: Array[Union[IncludeDirectory, String]] = None
    ) -> Boolean:
        ...

    def has_header(
        header_name: String,
        dependencies: Array[Dependency] = None,
        prefix: String = None,
        required: Union[Boolean, FeatureOption] = None,
        no_builtin_args: Boolean = None,
        args: Array[Union[String, File]] = None,
        include_directories: Array[Union[IncludeDirectory, String]] = None
    ) -> Boolean:
        ...

    def has_header_symbol(
        header_name: String, # changed from headername to header_name for consistency with other functions
        symbol_name: String,
        dependencies: Array[Dependency] = None,
        prefix: String = None,
        required: Union[Boolean, FeatureOption] = None,
        no_builtin_args: Boolean = None,
        args: Array[Union[String, File]] = None
    ) -> Boolean:
        ...

    def has_member(
        type_name: String,
        member_name: String,
        dependencies: Array[Dependency] = None,
        prefix: String = None,
        no_builtin_args: Boolean = None,
        args: Array[Union[String, File]] = None
    ) -> Boolean:
        ...

    def has_members(
        type_name: String,
        *member_name: String,
        dependencies: Array[Dependency] = None,
        prefix: String = None,
        no_builtin_args: Boolean = None,
        args: Array[Union[String, File]] = None
    ) -> Boolean:
        ...

    def has_multi_arguments(
        *argument_names: String
    ) -> Boolean:
        ...

    def has_multi_link_arguments(
        *argument_names: String
    ) -> Boolean:
        ...

    def has_type(
        type_name: String,
        dependencies: Array[Dependency] = None,
        prefix: String = None,
        no_builtin_args: Boolean = None,
        args: Array[Union[String, File]] = None
    ) -> Boolean:
        ...

    def links(
        code: Union[String, File],
        dependencies: Array[Dependency] = None,
        no_builtin_args: Boolean = None,
        name: String = None,
        args: Array[Union[String, File]] = None
    ) -> Boolean:
        ...
    def run(
        code: Union[String, File],
        dependencies: Array[Dependency] = None,
        no_builtin_args: Boolean = None,
        name: String = None,
        args: Array[Union[String, File]] = None
    ) -> CompilationRunResult:
        ...

    def symbols_have_underscore_prefix(
    ) -> Boolean:
        ...

    def sizeof(
        type_name: String,
        prefix: String = None,
        dependencies: Array[Dependency] = None,
        no_builtin_args: Boolean = None,
        args: Array[Union[String, File]] = None
    ) -> Number:
        ...

    def version(
    ) -> String:
        ...

    def has_function_attribute(
        name: String
    ) -> Boolean:
        ...

    def get_supported_function_attributes(
        list_of_names: Array[String]
    ) -> Array[String]:
        ...

class BuildTarget(Target, metaclass=multimethod.multimeta):

    def extract_all_objects(
        recursive: Boolean = None
    ) -> Array[File]:
        ...
    
    def extract_objects(
        *sources: Union[String, ExternalFile]
    ) -> Array[File]:
        ...

    def private_dir_include(
    ) -> IncludeDirectory:
        ...

    def name(
    ) -> String:
        ...

    def found(
    ) -> Boolean:
        ...

class ConfigurationData(metaclass=multimethod.multimeta):
    
    def get(
        var_name: String,
        default_value: Optional[Union[Boolean, Number, String]]
    ) -> Union[Boolean, Number, String]:
        ...

    def get_unquoted(
        var_name: String,
        default_value: Optional[Union[Boolean, Number, String]]
    ) -> Union[Boolean, Number, String]:
        ...

    def has(
        var_name: String
    ) -> Boolean:
        ...

    def keys(
    ) -> Array[String]:
        ...

    def merge_from(
        other: ConfigurationData
    ) -> None:
        ...

    def set(
        var_name: String,
        value: Union[Boolean, Number, String],
        description: String = None
    ) -> None:
        ...

    def set10(
        var_name: String,
        boolean_value: Union[Boolean, Number, String],
        description: String = None
    )-> None:
        ...

    def set_quoted(
        var_name: String,
        value: String,
        description: String = None
    ) -> None:
        ...

class ConfiguredFile(File, metaclass=multimethod.multimeta):
    ...

class CustomTarget(Target, metaclass=multimethod.multimeta):
    
    def __getitem__(
        index: Number
    ) -> CustomTargetIndex:
        ...

    def to_list(
    ) -> Array[CustomTarget]:
        ...

# Created by indexing CustomTarget. Currently a separate class, because it behave differently in many places
class CustomTargetIndex(Target, metaclass=multimethod.multimeta):
    ...

class Dependency(metaclass=multimethod.multimeta):

    def found(
    ) -> Boolean:
        ...

    def name(
    ) -> String:
        ...

    # deprecated
    """
    def get_pkgconfig_variable(
        var_name: String,
        default: Any = None
    ) -> Any:
        ...
    """

    # deprecated
    """
    def get_configtool_variable(
        var_name: String
    ) -> Any:
        ...
    """

    def type_name(
    ) -> String:
        ...

    def version(
    ) -> String:
        ...

    def include_type(
    ) -> String:
        ...

    def as_system(
        value: Optional[String]
    ) -> Dependency:
        ...

    def as_link_whole(
    ) -> Dependency:
        ...
    
    def partial_dependency(
        compile_args: Boolean = None,
        link_args: Boolean = None,
        links: Boolean = None,
        includes: Boolean = None,
        sources: Boolean = None
    ) -> Dependency:
        ...

    def get_variable(
        var_name: String,
        cmake: String = None,
        pkgconfig: String = None,
        configtool: String = None,
        internal: String = None,
        default_value: String = None,
        pkgconfig_define: Array[String] = None
    ) -> String:
        ...

class Disabler(metaclass=multimethod.multimeta):

    def found(
    ) -> Boolean:
        ...

class ExternalProgram(File, metaclass=multimethod.multimeta):

    def found() -> Boolean:
        ...

class Environment(metaclass=multimethod.multimeta):

    def append(
        var_name: String,
        *args: String,
        separator: String = None
    ) -> None:
        ...

    def prepend(
        var_name: String,
        *args: String,
        separator: String = None
    ) -> None:
        ...

    def set(
        var_name: String,
        *args: String,
        separator: String = None
    ) -> None:
        ...

class ExternalLibrary(metaclass=multimethod.multimeta):

    def found(
    ) -> Boolean:
        ...

    def type_name(
    ) -> String:
        ...

    def partial_dependency(
        compile_args: Boolean = None,
        link_args: Boolean = None,
        links: Boolean = None,
        includes: Boolean = None,
        sources: Boolean = None
    ) -> Dependency:
        ...

class FeatureOption(metaclass=multimethod.multimeta):

    def enabled(
    ) -> Boolean:
        ...

    def disabled(
    ) -> Boolean:
        ...

    def auto(
    ) -> Boolean:
        ...

    def allowed(
    ) -> Boolean:
        ...

    def disable_auto_if(
        value: Boolean
    ) -> FeatureOption:
        ...

    def require(
        value: Boolean,
        error_message: String = None
    ) -> FeatureOption:
        ...

class Generator(metaclass=multimethod.multimeta):

    def process(
        list_of_files: Array[File],
        extra_args: Array[Union[String, File]] = None,
        preserve_path_from: String = None
    ) -> GeneratorTarget:
        ...

class GeneratorTarget(Target,metaclass=multimethod.multimeta):
    ...

class Subproject(metaclass=multimethod.multimeta):
    
    def found(
    ) -> Boolean:
        ...

    def get_variable(
        name: String,
        fallback: Any
    ) -> Any:
        ...

class RunResult(metaclass=multimethod.multimeta):

    def returncode(
    ) -> Number:
        ...

    def stderr(
    ) -> String:
        ...

    def stdout(
    ) -> String:
        ...

class CompilationRunResult(RunResult, metaclass=multimethod.multimeta):

    def compiled(
    ) -> Boolean:
        ...

class Module(metaclass=multimethod.multimeta):

    def found(
    ) -> Boolean:
        ...

class Range(metaclass=multimethod.multimeta):
    
    def __getitem__(
        index: Number
    ) -> Number:
        ...

class IncludeDirectory(metaclass=multimethod.multimeta):
    ...

class Library(BuildTarget, metaclass=multimethod.multimeta):
    ...

class SharedLibrary(Library, metaclass=multimethod.multimeta):
    ...

class StaticLibrary(Library, metaclass=multimethod.multimeta):
    ...

class Jar(BuildTarget, metaclass=multimethod.multimeta):
    ...

class Executable(BuildTarget, metaclass=multimethod.multimeta):
    ...

class RunTarget(Target, metaclass=multimethod.multimeta):
    ...

class BothLibraries(BuildTarget, metaclass=multimethod.multimeta):
    
    def get_shared_lib(
    ) -> Library:
        ...

    def get_static_lib(
    ) -> Library:
        ...

class SharedModule(BuildTarget, metaclass=multimethod.multimeta):
    ...