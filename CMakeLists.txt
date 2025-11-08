cmake_minimum_required(VERSION 3.25)
project(gaz LANGUAGES CXX)

# --- Settings ---
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

execute_process(
    COMMAND uv run --project ${CMAKE_SOURCE_DIR} python -c "import sysconfig; print(sysconfig.get_paths()['include'])"
    OUTPUT_VARIABLE Python_INCLUDE_DIR
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

execute_process(
    COMMAND uv run --project ${CMAKE_SOURCE_DIR} python -c "import sys; print(sys.prefix)"
    OUTPUT_VARIABLE Python_PREFIX
    OUTPUT_STRIP_TRAILING_WHITESPACE
)

find_package(pybind11 REQUIRED CONFIG)

include_directories(
    ${Python_INCLUDE_DIR}
    ${CMAKE_SOURCE_DIR}/include
)

add_subdirectory(src)
