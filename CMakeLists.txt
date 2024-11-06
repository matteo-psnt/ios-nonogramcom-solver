cmake_minimum_required(VERSION 3.10)
project(nonogram_solver)

set(CMAKE_CXX_STANDARD 17)

find_package(pybind11 REQUIRED)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O3 -march=native -mtune=native -flto -ffast-math -funroll-loops -fomit-frame-pointer")

pybind11_add_module(line_solver line_solver.cpp)
