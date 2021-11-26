# SPDX-FileCopyrightText: 2021 Paul Aumann
#
# SPDX-License-Identifier: Apache-2.0

import tempfile, os, subprocess, shutil, re, errno, templates
from typing import List, Tuple
from util import red, varname, yellow

class MesonException(Exception):
    pass

# If an error line contains this substring, the error is skipped
IGNORE_STRING = "$IGNORE$"

class BuildFile:
    """Wrapper for the meson.build file. Provides methods for adding/removing lines and running checks."""

    # Buffer that is used to push/pop file contents
    push_buffer = ""

    def __init__(self, project_name: str = "generated",
                    project_languages: str = ["c"],
                    warnings: bool = False,
                    verbose: bool = False):
        self.warnings = warnings
        self.verbose = verbose

        self.src_folder = tempfile.TemporaryDirectory()
        print(f"Setting up directory: '{self.src_folder.name}'")
        self.buildfile = os.path.join(self.src_folder.name, "meson.build")
        
        # Creating and adding project information to meson.build file
        project_languages = [ f"'{lang}'" for lang in project_languages ]
        self.append_line(f"project('{project_name}', [{', '.join(project_languages)}])")

        # Generate meson structure
        print("Running meson setup ...")
        result = subprocess.run(["meson", "setup", "builddir"], cwd=self.src_folder.name, capture_output=True)
        if result.returncode != 0:
            print("Something went wrong:")
            print(result.stdout.decode("utf-8"))
            raise RuntimeError("Could not create buildfile.")

        print("Done!")

    def append_line(self, line: str = ""):
        """Appends a single line to the meson.build file. Removes linebreaks."""
        line = line.replace(templates.BUILDFILE_DIR, f"'{self.src_folder.name}'")
        escaped_line = line.replace("\n", "\\n")
        with open(self.buildfile, "a") as file:
            file.write(escaped_line + "\n")

    def append_lines(self, lines: List[str]):
        """Appends multiplie lines to the meson.build file. Removes linebreaks."""
        with open(self.buildfile, "a") as file:
            for line in lines:
                line = line.replace(templates.BUILDFILE_DIR, f"'{self.src_folder.name}'")
                escaped_line = line.replace("\n", "\\n")
                file.write(escaped_line + "\n")

    def remove_line(self, index: int):
        """Removes the line with the given index from the meson.build file."""
        # Read current lines from file
        with open(self.buildfile, "r") as readfile:
            lines = readfile.readlines()
        # Remove selected line
        del lines[index]
        # Write remaining lines back to file
        with open(self.buildfile, "w") as writefile:
            writefile.writelines(lines)

    def pop_line(self):
        """Removes the last line from the meson.build file."""
        self.remove_line(-1)

    def pop_lines(self, n: int):
        """Removes n lines from the meson.build file, starting at the last line."""
        if n < 0:
            raise ValueError(f"Cannot pop a negative number ({n}) of lines.")

        # Read current lines from file
        with open(self.buildfile, "r") as readfile:
            lines = readfile.readlines()

        if n > len(lines):
            raise ValueError(f"Can only pop {len(lines)} lines (not {n}).")

        # Remove selected lines
        for i in range(n):
            del lines[-1]

        # Write remaining lines back to file
        with open(self.buildfile, "w") as writefile:
            writefile.writelines(lines)

    def push_content(self):
        """Stores meson.build file content in a buffer. Can be restored via pop_content()"""
        # Store contents in buffer
        with open(self.buildfile, "r") as readfile:
            self.push_buffer = readfile.read()
        # Clear file contents
        open(self.buildfile, "w").close()
    
    def pop_content(self):
        """Retrieves file contents from the buffer and writes it to the meson.build file"""
        # Store buffer in file
        with open(self.buildfile, "w") as writefile:
            writefile.write(self.push_buffer)

    def line_count(self) -> int:
        """Returns the number of lines of the meson.build file"""
        with open(self.buildfile, "r") as readfile:
            return len(readfile.readlines())

    def get_line(self, index: int) -> str:
        """Returns the line with the given index."""
        with open(self.buildfile, "r") as file:
            lines = file.readlines
            return lines[index].rstrip("\n")

    def add_file(self, name: str, src_file: str):
        """Copies a file to the source folder of the buildfile."""
        dest_file= os.path.join(self.src_folder.name, name)
        try:
            shutil.copytree(src_file, dest_file)
        except OSError as exc:
            if exc.errno == errno.ENOTDIR:
                shutil.copy(src_file, dest_file)
            else:
                raise

    def error_line(self) -> str:
        """Returns the error line used to speed up checks."""
        return f"This error is produced to speed up checks and can be ignored ({IGNORE_STRING})"

    def check_lines(self, lines: List[str]) -> Tuple[int, str]:
        """Adds the given lines to the buildfile and runs a check. Returns error line and error message."""
        if not isinstance(lines, list) and not isinstance(lines, tuple):
            lines = (lines,)
        # Check how many lines are in the file before appending
        lines_before = self.line_count()

        # Add error line to lines. This makes meson run significantly faster, and doesn't change the result.
        lines.append(f"error('{self.error_line()}')")

        # Append lines to file
        self.append_lines(lines)

        # Check for errors
        builddir = os.path.join(self.src_folder.name, "builddir")
        result = subprocess.run(["meson", "--reconfigure"], cwd=builddir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        error_line = -1
        error_msg = ""
        for stdout_line in result.stdout.decode().split(os.linesep):
            # Ignore error line
            if IGNORE_STRING in stdout_line:
                continue
            # Check if line is error
            if re.match(r"\.\.[\\\/]meson\.build:\d+:\d+: ERROR: .*", stdout_line):
                error_msg = stdout_line.split("ERROR:")[1].strip()
                error_line = int(stdout_line.split(":")[1])
                break
            # Check if line is warning
            elif "WARNING" in stdout_line and self.warnings:
                error_msg = stdout_line.split("WARNING:")[1].strip() + yellow(" (WARNING)")
                error_line = lines_before + 1
                break
            # If line contains ERROR -> regex might be out of date
            elif "ERROR" in stdout_line:
                if "ERROR: First statement must be a call to project" in stdout_line:
                    print(f"{yellow('<INTERNAL>')} No project() call in meson.build file.")
                    error_line = lines_before + 1
                else:
                    print(f"{yellow('<INTERNAL>')} ERROR line found, but regex didn't match. Did the formatting change?")

        # 'meson --reconfigure' does not write to stderr, so if something was written, meson has crashed
        if len(result.stderr) > 0 and not self.verbose:
            error_msg = f"{red('<CRASH>')} Meson has crashed, re-run with --verbose to see stderr."
            error_line = lines_before + 1 # arbitrary number, so that test won't be re-run

        # If output is verbose, print stderr aswell
        elif len(result.stderr) > 0 and self.verbose:
            print(result.stderr.decode())
            error_msg = f"{red('<CRASH>')} Meson has crashed."
            error_line = lines_before + 1 # arbitrary number, so that test won't be re-run

        # if output is verbose, print buildfile contents and stdout
        if error_line >= 0 and self.verbose:
            print("######## MESON.BUILD CONTENTS ########")
            with open(self.buildfile, "r") as file:
                print(file.read())
            print("########## STDOUT CONTENTS ###########")
            print(result.stdout.decode())


        # Remove lines from file
        self.pop_lines(len(lines))
        
        # Return line number that failed, as well as the error message provided by meson
        return (error_line - lines_before - 1), error_msg

    def __dest__(self):
        """Destructor, removes temporary folder."""
        self.src_folder.cleanup()