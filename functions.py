from multimethod import multimethod
from typing import Any, Dict, overload, Union, Literal, Optional
from merge_args import merge_args
import objects

def add_global_arguments(
    *args: objects.String,
    language: Union[objects.String,objects.Array[objects.String]] = None,
    native: objects.Boolean = None
) -> None:
    ...

def add_global_link_arguments(
    *args: objects.String,
    language: Union[objects.String,objects.Array[objects.String]] = None,
    native: objects.Boolean = None
) -> None:
    ...

def add_languages(
    *langs: Union[objects.String, objects.Array[objects.String]],
    required: Union[objects.Boolean, objects.FeatureOption] = None,
    native: objects.Boolean = None
) -> objects.Boolean:
    ...

def add_project_arguments(
    *args: objects.String,
    language: Union[objects.String,objects.Array[objects.String]] = None,
    native: objects.Boolean = None
) -> None:
    ...

def add_project_link_arguments(
    *args: objects.String,
    language: Union[objects.String,objects.Array[objects.String]] = None,
    native: objects.Boolean = None
) -> None:
    ...

def add_test_setup(
    name: objects.String,
    env: Union[objects.Array[objects.String], objects.Environment, objects.Dict] = None,
    exe_wrapper: objects.Array[objects.String] = None,
    gdb: objects.Boolean = None,
    timeout_multiplier: objects.Number = None,
    is_default: objects.Boolean = None,
    exclude_suites: objects.Array[objects.String] = None
) -> None:
    ...

def alias_target(
    target_name: objects.String,
    *depends: objects.Target
) -> objects.RunTarget:
    ...

def assert_(
    condition: objects.Boolean,
    message: Optional[objects.String]
) -> None:
    ...

def benchmark(
    name: objects.String,
    executable: Union[objects.Executable, objects.ExternalProgram, objects.Jar, objects.CustomTarget, objects.CustomTargetIndex, objects.GeneratorTarget, objects.ExternalFile],
    args: objects.Array[Union[objects.File, objects.String, objects.Target]] = None,
    env: Union[objects.Array[objects.String], objects.Environment, objects.Dict] = None,
    should_fail: objects.Boolean = None,
    suite: Union[objects.String, objects.Array[objects.String]] = None,
    timeout: objects.Number = None,
    workdir: objects.String = None,
    depends: objects.Array[objects.Target] = None,
    protocol: objects.String = None,
    priority: objects.Number = None
) -> None:
    ...

def executable(
    exe_name: objects.String,
    *sources: Union[objects.String, objects.Array[Union[objects.String, objects.File]]],
    build_by_default: objects.Boolean = None,
    build_rpath: objects.String = None,
    dependencies: objects.Array[objects.Dependency] = None,
    extra_files: objects.Array[objects.File] = None,
    link_args: objects.Array[objects.String] = None,
    link_depends: objects.Array[Union[objects.String, objects.File]] = None,
    link_language: objects.String = None,
    link_whole: objects.Boolean = None,
    link_with: objects.Array[Union[objects.Library, objects.CustomTarget, objects.CustomTargetIndex]] = None,
    export_dynamic: objects.Boolean = None,
    implib: Union[objects.Boolean, objects.String] = None,
    implicit_include_directories: objects.Boolean = None,
    include_directories: objects.Array[Union[objects.IncludeDirectory, objects.String]],
    install: objects.Boolean = None,
    install_dir: objects.String = None,
    install_mode: objects.String = None,
    install_rpath: objects.String = None,
    objects: objects.Array[objects.File] = None,
    name_suffix: objects.String = None,
    override_options: objects.Array[objects.String] = None,
    gnu_symbol_visibility: objects.String = None,
    d_import_dirs: Union[objects.Array[objects.IncludeDirectory], objects.Array[Union[objects.IncludeDirectory, objects.String]]] = None,
    d_unittest: objects.Boolean = None,
    d_module_versions: objects.Array[objects.String] = None,
    d_debug: objects.Array[objects.String] = None,
    pie: objects.Boolean = None,
    native: objects.Boolean = None,
    win_subsystem: objects.String = None
) -> objects.Executable:
    ...

def both_libraries(
    library_name: objects.String,
    *sources: Union[objects.String, objects.Array[Union[objects.String, objects.File]]],
    build_by_default: objects.Boolean = None,
    build_rpath: objects.String = None,
    dependencies: objects.Array[objects.Dependency] = None,
    extra_files: objects.Array[objects.File] = None,
    link_args: objects.Array[objects.String] = None,
    link_depends: objects.Array[Union[objects.String, objects.File]] = None,
    link_language: objects.String = None,
    link_whole: objects.Array[Union[objects.Library, objects.CustomTarget, objects.CustomTargetIndex]] = None,
    link_with: objects.Array[Union[objects.Library, objects.CustomTarget, objects.CustomTargetIndex]] = None,
    implicit_include_directories: objects.Boolean = None,
    include_directories: objects.Array[Union[objects.IncludeDirectory, objects.String]],
    install: objects.Boolean = None,
    install_dir: objects.String = None,
    install_mode: objects.String = None,
    install_rpath: objects.String = None,
    objects: objects.Array[objects.File] = None,
    override_options: objects.Array[objects.String] = None,
    gnu_symbol_visibility: objects.String = None,
    d_import_dirs: Union[objects.Array[objects.IncludeDirectory], objects.Array[Union[objects.IncludeDirectory, objects.String]]] = None,
    d_unittest: objects.Boolean = None,
    d_module_versions: objects.Array[objects.String] = None,
    d_debug: objects.Array[objects.String] = None,
    native: objects.Boolean = None,
    # Additional kwargs
    name_prefix: objects.String = None,
    name_suffix: objects.String = None,
    rust_crate_type: objects.String = None
) -> objects.BothLibraries:
    ...

def build_target(
    name: objects.String,
    *sources: Union[objects.String, objects.Array[Union[objects.String, objects.File]]],
    build_by_default: objects.Boolean = None,
    build_rpath: objects.String = None,
    dependencies: objects.Array[objects.Dependency] = None,
    extra_files: objects.Array[objects.File] = None,
    link_args: objects.Array[objects.String] = None,
    link_depends: objects.Array[Union[objects.String, objects.File]] = None,
    link_language: objects.String = None,
    link_whole: objects.Boolean = None,
    link_with: objects.Array[Union[objects.Library, objects.CustomTarget, objects.CustomTargetIndex]] = None,
    export_dynamic: objects.Boolean = None,
    implib: Union[objects.Boolean, objects.String] = None,
    implicit_include_directories: objects.Boolean = None,
    include_directories: objects.Array[Union[objects.IncludeDirectory, objects.String]],
    install: objects.Boolean = None,
    install_dir: objects.String = None,
    install_mode: objects.String = None,
    install_rpath: objects.String = None,
    objects: objects.Array[objects.File] = None,
    name_suffix: objects.String = None,
    override_options: objects.Array[objects.String] = None,
    gnu_symbol_visibility: objects.String = None,
    d_import_dirs: Union[objects.Array[objects.IncludeDirectory], objects.Array[Union[objects.IncludeDirectory, objects.String]]] = None,
    d_unittest: objects.Boolean = None,
    d_module_versions: objects.Array[objects.String] = None,
    d_debug: objects.Array[objects.String] = None,
    pie: objects.Boolean = None,
    native: objects.Boolean = None,
    win_subsystem: objects.String = None,
    # Additional kwargs
    target_type: objects.String = None
) -> objects.BuildTarget:
    ...

def configuration_data(
    dict: Optional[objects.Dict]
) -> objects.ConfigurationData:
    ...

@multimethod
def configure_file(
    capture: objects.Boolean = None,
    command: objects.Array[Union[objects.String, objects.File]] = None,
    depfile: Union[objects.File, objects.String] = None,
    format: objects.String = None, 
    input: Union[objects.File, objects.String] = None,
    install: objects.Boolean = None,
    install_dir: objects.String = None,
    install_mode: objects.String = None,
    output: objects.String = None,
    output_format: objects.String = None,
    encoding: objects.String = None
) -> objects.ConfiguredFile:
    ...

@configure_file.register
def configure_file(
    copy: objects.Boolean = None,
    depfile: Union[objects.File, objects.String] = None,
    format: objects.String = None,
    input: Union[objects.File, objects.String] = None,
    install: objects.Boolean = None,
    install_dir: objects.String = None,
    install_mode: objects.String = None,
    output: objects.String = None,
    output_format: objects.String = None,
    encoding: objects.String = None
) -> objects.ConfiguredFile:
    ...

def custom_target(
    name: objects.String,
    build_by_default: objects.Boolean = None,
    build_always_stale: objects.Boolean = None,
    capture: objects.Boolean = None,
    console: objects.Boolean = None,
    command: Union[objects.String, objects.ExternalProgram, objects.Array[objects.File]] = None,
    depend_files: objects.Array[Union[objects.File, objects.String]] = None,
    depends: objects.Boolean = None,
    depfile: objects.File = None,
    input: objects.Array[objects.File] = None,
    install: objects.Boolean = None,
    install_dir: objects.String = None,
    install_mode: objects.String = None,
    output: objects.Array[objects.File] = [],
    env: Union[objects.Array[objects.String], objects.Environment, objects.Dict] = None
) -> objects.CustomTarget:
    ...

def declare_dependency(
    compile_args: objects.Array[objects.String] = None,
    dependencies: objects.Array[objects.Dependency] = None,
    include_directories: objects.Array[Union[objects.IncludeDirectory, objects.String]] = None,
    link_args: objects.Array[objects.String] = None,
    link_with: objects.Array[objects.Library] = None,
    link_whole: objects.Array[objects.Library] = None,
    sources: objects.Array[objects.File] = None,
    version: objects.String = None,
    variables: Union[objects.Dict, objects.Array[objects.String]] = None
) -> objects.Dependency:
    ...

def dependency(
    dependency_name: objects.String,
    default_options: objects.Array[objects.String] = None,
    allow_fallback: objects.Boolean = None,
    fallback: Union[objects.String, objects.Array[objects.String]] = None,
    language: objects.String = None,
    method: objects.String = None,
    native: objects.Boolean = None,
    not_found_message: objects.String = None,
    required: Union[objects.Boolean, objects.FeatureOption] = None,
    static: objects.Boolean = None,
    version: objects.String = None,
    include_type: objects.String = None,
    disabler: objects.Boolean = None
) -> objects.Dependency:
    ...


def disabler(
) -> objects.Disabler:
    ...

def error(
    *message: objects.String
) -> None:
    ...

def environment(
    dict: Optional[objects.Dict]
) -> objects.Environment:
    ...

def find_program(
    *program_names: objects.String,
    required: Union[objects.Boolean, objects.FeatureOption] = None,
    native: objects.Boolean = None,
    disabler: objects.Boolean = None,
    version: objects.String = None,
    dirs: objects.Array[objects.String] = None
) -> objects.ExternalProgram:
    ...

def files(
    *list_of_files: objects.String
) -> objects.Array[objects.ExternalFile]:
    ...

def generator(
    executable: objects.Executable,
    arguments: objects.Array[Union[objects.String, objects.File]] = None,
    depends: objects.Array[objects.Target] = None,
    depend_files: objects.Array[Union[objects.File, objects.String]] = None,
    depfile: objects.String = None,
    output: objects.String = None,
    capture: objects.Boolean = None
) -> objects.Generator:
    ...

def get_option(
    option_name: objects.String
) -> Any:
    ...

def get_variable(
    variable_name: objects.String,
    fallback: Any
) -> Any:
    ...

def import_(
    name: objects.String,
    required: Union[objects.Boolean, objects.FeatureOption] = None,
    disabler: objects.Boolean = None
) -> objects.Module:
    ...

def include_directories(
    *directory_names: objects.String,
    is_system: objects.Boolean = None
) -> objects.IncludeDirectory:
    ...

def install_data(
    *list_of_files: Union[objects.ExternalFile, objects.String, objects.Target],
    install_dir: objects.String = None,
    install_mode: objects.String = None,
    rename: objects.Array[Union[objects.String, objects.File]] = None
) -> None:
    ...

def install_headers(
    *list_of_headers: objects.Array[objects.ExternalFile],
    install_mode: objects.String = None,
    subdir: objects.String = None
) -> None:
    ...

def install_man(
    *list_of_manpages: Union[objects.ExternalFile, objects.String, objects.CustomTarget, objects.CustomTargetIndex, objects.GeneratorTarget],
    install_mode: objects.String = None,
    locale: objects.String = None
) -> None:
    ...

def install_subdir(
    subdir_name: objects.String,
    exclude_files: objects.Array[Union[objects.String, objects.File]] = None,
    exclude_directories: objects.Array[objects.String] = None,
    install_dir: objects.String = None,
    install_mode: objects.String = None,
    strip_directory: objects.Boolean = None,
) -> None:
    ...

def is_disabler(
    var: Any
) -> objects.Boolean:
    ...

def is_variable(
    varname: objects.String
) -> objects.Boolean:
    ...

def jar(
    jar_name: objects.String,
    *sources: Union[objects.String, objects.Array[Union[objects.String, objects.File]]],
    build_by_default: objects.Boolean = None,
    build_rpath: objects.String = None,
    dependencies: objects.Array[objects.Dependency] = None,
    extra_files: objects.Array[objects.File] = None,
    link_args: objects.Array[objects.String] = None,
    link_depends: objects.Array[Union[objects.String, objects.File]] = None,
    link_language: objects.String = None,
    link_whole: objects.Boolean = None,
    link_with: objects.Array[Union[objects.Library, objects.CustomTarget, objects.CustomTargetIndex]] = None,
    export_dynamic: objects.Boolean = None,
    implicit_include_directories: objects.Boolean = None,
    include_directories: objects.Array[Union[objects.IncludeDirectory, objects.String]],
    install: objects.Boolean = None,
    install_dir: objects.String = None,
    install_mode: objects.String = None,
    install_rpath: objects.String = None,
    objects: objects.Array[objects.File] = None,
    name_suffix: objects.String = None,
    override_options: objects.Array[objects.String] = None,
    gnu_symbol_visibility: objects.String = None,
    d_import_dirs: Union[objects.Array[objects.IncludeDirectory], objects.Array[Union[objects.IncludeDirectory, objects.String]]] = None,
    d_unittest: objects.Boolean = None,
    d_module_versions: objects.Array[objects.String] = None,
    d_debug: objects.Array[objects.String] = None,
    native: objects.Boolean = None,
    # Additional kwargs
    main_class: objects.String
) -> objects.Jar:
    ...

def join_paths(
    *args: objects.String
) -> objects.String:
    ...

def library(
    library_name: objects.String,
    *sources: Union[objects.String, objects.Array[Union[objects.String, objects.File]]],
    build_by_default: objects.Boolean = None,
    build_rpath: objects.String = None,
    dependencies: objects.Array[objects.Dependency] = None,
    extra_files: objects.Array[objects.File] = None,
    link_args: objects.Array[objects.String] = None,
    link_depends: objects.Array[Union[objects.String, objects.File]] = None,
    link_language: objects.String = None,
    link_whole: objects.Boolean = None,
    link_with: objects.Array[Union[objects.Library, objects.CustomTarget, objects.CustomTargetIndex]] = None,
    implicit_include_directories: objects.Boolean = None,
    include_directories: objects.Array[Union[objects.IncludeDirectory, objects.String]],
    install: objects.Boolean = None,
    install_dir: objects.String = None,
    install_mode: objects.String = None,
    install_rpath: objects.String = None,
    objects: objects.Array[objects.File] = None,
    override_options: objects.Array[objects.String] = None,
    gnu_symbol_visibility: objects.String = None,
    d_import_dirs: Union[objects.Array[objects.IncludeDirectory], objects.Array[Union[objects.IncludeDirectory, objects.String]]] = None,
    d_unittest: objects.Boolean = None,
    d_module_versions: objects.Array[objects.String] = None,
    d_debug: objects.Array[objects.String] = None,
    native: objects.Boolean = None,
    # Additional kwargs
    name_prefix: objects.String = None,
    name_suffix: objects.String = None,
    rust_crate_type: objects.String = None
) -> objects.Library:
    ...

def message(
    text: Union[objects.String, objects.Number, objects.Array[Union[objects.String, objects.Number]], objects.Dict]
) -> None:
    ...

def warning(
    text: Union[objects.String, objects.Number, objects.Array[Union[objects.String, objects.Number]], objects.Dict]
) -> None:
    ...

@multimethod
def summary(
    key: objects.String,
    value: Union[objects.Number, objects.Boolean, objects.String, objects.ExternalProgram, objects.Dependency, objects.FeatureOption, objects.Array],
    section: objects.String = None,
    bool_yn: objects.Boolean = None,
    list_sep: objects.String = None
) -> None:
    ...

@summary.register
def summary(
    dictionary: objects.Dict,
    section: objects.String = None,
    bool_yn: objects.Boolean = None,
    list_sep: objects.String = None
) -> None:
    ...

def project(
    project_name: objects.String,
    *list_of_languages: objects.String,
    default_options: objects.Array[objects.String] = None,
    license: Union[objects.String, objects.Array[objects.String]] = None,
    meson_version: objects.String = None,
    subproject_dir: objects.String = None,
    version: objects.String = None
) -> None:
    ...

def run_command(
    command: Union[objects.String, objects.ExternalProgram, objects.Array[objects.File], objects.Compiler],
    check: objects.Boolean = None,
    env: Union[objects.Array[objects.String], objects.Environment, objects.Dict] = None
) -> objects.RunResult:
    ...

def run_target(
    target_name: objects.String,
    command: objects.Array[Union[objects.String, objects.Executable]] = None,
    depends: objects.Array[objects.Target] = None,
    env: Union[objects.Array[objects.String], objects.Environment, objects.Dict] = None
) -> objects.RunTarget:
    ...

def set_variable(
    variable_name: objects.String,
    value: Any
) -> None:
    ...

def shared_library(
    library_name: objects.String,
    *sources: Union[objects.String, objects.Array[Union[objects.String, objects.File]]],
    build_by_default: objects.Boolean = None,
    build_rpath: objects.String = None,
    dependencies: objects.Array[objects.Dependency] = None,
    extra_files: objects.Array[objects.File] = None,
    link_args: objects.Array[objects.String] = None,
    link_depends: objects.Array[Union[objects.String, objects.File]] = None,
    link_language: objects.String = None,
    link_whole: objects.Boolean = None,
    link_with: objects.Array[Union[objects.Library, objects.CustomTarget, objects.CustomTargetIndex]] = None,
    implicit_include_directories: objects.Boolean = None,
    include_directories: objects.Array[Union[objects.IncludeDirectory, objects.String]],
    install: objects.Boolean = None,
    install_dir: objects.String = None,
    install_mode: objects.String = None,
    install_rpath: objects.String = None,
    objects: objects.Array[objects.File] = None,
    name_suffix: objects.String = None,
    override_options: objects.Array[objects.String] = None,
    gnu_symbol_visibility: objects.String = None,
    d_import_dirs: Union[objects.Array[objects.IncludeDirectory], objects.Array[Union[objects.IncludeDirectory, objects.String]]] = None,
    d_unittest: objects.Boolean = None,
    d_module_versions: objects.Array[objects.String] = None,
    d_debug: objects.Array[objects.String] = None,
    native: objects.Boolean = None,
    # Additional kwargs
    name_prefix: objects.String = None,
    rust_crate_type: objects.String = None,
    soversion: objects.String = None,
    version: objects.String = None,
    darwin_versions: Union[objects.Number, objects.String, objects.Array[objects.String]] = None,
    vs_module_defs: Union[objects.String, objects.File, objects.CustomTarget, objects.CustomTargetIndex] = None
) -> objects.SharedLibrary:
    ...

def shared_module(
    module_name: objects.String,
    *sources: Union[objects.String, objects.Array[Union[objects.String, objects.File]]],
    build_by_default: objects.Boolean = None,
    build_rpath: objects.String = None,
    dependencies: objects.Array[objects.Dependency] = None,
    extra_files: objects.Array[objects.File] = None,
    link_args: objects.Array[objects.String] = None,
    link_depends: objects.Array[Union[objects.String, objects.File]] = None,
    link_language: objects.String = None,
    link_whole: objects.Boolean = None,
    link_with: objects.Array[Union[objects.Library, objects.CustomTarget, objects.CustomTargetIndex]] = None,
    implicit_include_directories: objects.Boolean = None,
    include_directories: objects.Array[Union[objects.IncludeDirectory, objects.String]],
    install: objects.Boolean = None,
    install_dir: objects.String = None,
    install_mode: objects.String = None,
    install_rpath: objects.String = None,
    objects: objects.Array[objects.File] = None,
    override_options: objects.Array[objects.String] = None,
    gnu_symbol_visibility: objects.String = None,
    d_import_dirs: Union[objects.Array[objects.IncludeDirectory], objects.Array[Union[objects.IncludeDirectory, objects.String]]] = None,
    d_unittest: objects.Boolean = None,
    d_module_versions: objects.Array[objects.String] = None,
    d_debug: objects.Array[objects.String] = None,
    native: objects.Boolean = None,
    # Additional kwargs
    name_prefix: objects.String = None,
    name_suffix: objects.String = None,
    rust_crate_type: objects.String = None,
    vs_module_defs: Union[objects.String, objects.File, objects.CustomTarget, objects.CustomTargetIndex] = None
) -> objects.SharedModule:
    ...

def static_library(
    library_name: objects.String,
    *sources: Union[objects.String, objects.Array[Union[objects.String, objects.File]]],
    build_by_default: objects.Boolean = None,
    build_rpath: objects.String = None,
    dependencies: objects.Array[objects.Dependency] = None,
    extra_files: objects.Array[objects.File] = None,
    link_args: objects.Array[objects.String] = None,
    link_depends: objects.Array[Union[objects.String, objects.File]] = None,
    link_language: objects.String = None,
    link_whole: objects.Boolean = None,
    link_with: objects.Array[Union[objects.Library, objects.CustomTarget, objects.CustomTargetIndex]] = None,
    implicit_include_directories: objects.Boolean = None,
    include_directories: objects.Array[Union[objects.IncludeDirectory, objects.String]],
    install: objects.Boolean = None,
    install_dir: objects.String = None,
    install_mode: objects.String = None,
    install_rpath: objects.String = None,
    objects: objects.Array[objects.File] = None,
    override_options: objects.Array[objects.String] = None,
    gnu_symbol_visibility: objects.String = None,
    d_import_dirs: Union[objects.Array[objects.IncludeDirectory], objects.Array[Union[objects.IncludeDirectory, objects.String]]] = None,
    d_unittest: objects.Boolean = None,
    d_module_versions: objects.Array[objects.String] = None,
    d_debug: objects.Array[objects.String] = None,
    native: objects.Boolean = None,
    # Additional kwargs
    name_prefix: objects.String = None,
    name_suffix: objects.String = None,
    rust_crate_type: objects.String = None,
    pic: objects.Boolean = None,
    prelink: objects.Boolean = None
) -> objects.StaticLibrary:
    ...

def subdir(
    dir_name: objects.String,
    if_found: objects.Array[objects.Dependency] = None
) -> None:
    ...

def subdir_done(
) -> None:
    ...

def subproject(
    subproject_name: objects.String,
    default_options: objects.Array[objects.String] = None,
    version: objects.String = None,
    required: Union[objects.Boolean, objects.FeatureOption] = None
) -> objects.Subproject:
    ...

@merge_args(benchmark)
def test(
    is_parallel: objects.Boolean = None
) -> None:
    ...

def unset_variable(
    var_name: objects.String
) -> None:
    ...

def vcs_tag(
    command: Union[objects.String, objects.ExternalProgram, objects.Array[objects.File]] = None,
    fallback: objects.String = None,
    input: objects.File = None,
    output: objects.File = None,
    replace_string: objects.String = None
) -> objects.CustomTarget:
    ...

@multimethod
def range(
    stop: objects.Number
) -> objects.Range:
    ...

@range.register
def range(
    start: objects.Number,
    stop: objects.Number,
    step: Optional[objects.Number]
) -> objects.Range:
    ...

