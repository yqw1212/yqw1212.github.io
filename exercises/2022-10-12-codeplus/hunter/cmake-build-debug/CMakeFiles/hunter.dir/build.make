# CMAKE generated file: DO NOT EDIT!
# Generated by "MinGW Makefiles" Generator, CMake Version 3.17

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Disable VCS-based implicit rules.
% : %,v


# Disable VCS-based implicit rules.
% : RCS/%


# Disable VCS-based implicit rules.
% : RCS/%,v


# Disable VCS-based implicit rules.
% : SCCS/s.%


# Disable VCS-based implicit rules.
% : s.%


.SUFFIXES: .hpux_make_needs_suffix_list


# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

SHELL = cmd.exe

# The CMake executable.
CMAKE_COMMAND = "D:\Program Files\JetBrains\CLion 2020.2.4\bin\cmake\win\bin\cmake.exe"

# The command to remove a file.
RM = "D:\Program Files\JetBrains\CLion 2020.2.4\bin\cmake\win\bin\cmake.exe" -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = D:\yqw\Documents\c\hunter

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = D:\yqw\Documents\c\hunter\cmake-build-debug

# Include any dependencies generated for this target.
include CMakeFiles/hunter.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/hunter.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/hunter.dir/flags.make

CMakeFiles/hunter.dir/main.cpp.obj: CMakeFiles/hunter.dir/flags.make
CMakeFiles/hunter.dir/main.cpp.obj: ../main.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=D:\yqw\Documents\c\hunter\cmake-build-debug\CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/hunter.dir/main.cpp.obj"
	"D:\Program Files\MinGW\bin\g++.exe"  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles\hunter.dir\main.cpp.obj -c D:\yqw\Documents\c\hunter\main.cpp

CMakeFiles/hunter.dir/main.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/hunter.dir/main.cpp.i"
	"D:\Program Files\MinGW\bin\g++.exe" $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E D:\yqw\Documents\c\hunter\main.cpp > CMakeFiles\hunter.dir\main.cpp.i

CMakeFiles/hunter.dir/main.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/hunter.dir/main.cpp.s"
	"D:\Program Files\MinGW\bin\g++.exe" $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S D:\yqw\Documents\c\hunter\main.cpp -o CMakeFiles\hunter.dir\main.cpp.s

# Object files for target hunter
hunter_OBJECTS = \
"CMakeFiles/hunter.dir/main.cpp.obj"

# External object files for target hunter
hunter_EXTERNAL_OBJECTS =

hunter.exe: CMakeFiles/hunter.dir/main.cpp.obj
hunter.exe: CMakeFiles/hunter.dir/build.make
hunter.exe: CMakeFiles/hunter.dir/linklibs.rsp
hunter.exe: CMakeFiles/hunter.dir/objects1.rsp
hunter.exe: CMakeFiles/hunter.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=D:\yqw\Documents\c\hunter\cmake-build-debug\CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable hunter.exe"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles\hunter.dir\link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/hunter.dir/build: hunter.exe

.PHONY : CMakeFiles/hunter.dir/build

CMakeFiles/hunter.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles\hunter.dir\cmake_clean.cmake
.PHONY : CMakeFiles/hunter.dir/clean

CMakeFiles/hunter.dir/depend:
	$(CMAKE_COMMAND) -E cmake_depends "MinGW Makefiles" D:\yqw\Documents\c\hunter D:\yqw\Documents\c\hunter D:\yqw\Documents\c\hunter\cmake-build-debug D:\yqw\Documents\c\hunter\cmake-build-debug D:\yqw\Documents\c\hunter\cmake-build-debug\CMakeFiles\hunter.dir\DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/hunter.dir/depend

