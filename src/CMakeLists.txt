pybind11_add_module(gaz gaz.cpp)

target_sources(gaz PUBLIC gravity.cpp random_walk.cpp)
