#include "gaz/gaz.hpp"
#include "gravity.hpp"
#include "random_walk.hpp"

#include <pybind11/chrono.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <map>
#include <string>
#include <vector>

struct Gaz
{
    Gaz(const int N) : model{N}
    {
    }

    auto update(const std::chrono::duration<double> dt) -> void
    {
        model.update(dt);
        time += dt;
    }

    auto get() -> pybind11::tuple
    {
        auto x_array = pybind11::array_t<double>({model.x.size()}, {sizeof(double)}, model.x.data(), pybind11::none());
        auto y_array = pybind11::array_t<double>({model.y.size()}, {sizeof(double)}, model.y.data(), pybind11::none());

        return pybind11::make_tuple(x_array, y_array);
    }

    random_walk::Model model;

    std::chrono::duration<double> time{};
};

PYBIND11_MODULE(gaz, m)
{
    pybind11::class_<Gaz>(m, "Gaz").def(pybind11::init<const int>()).def("update", &Gaz::update).def("get", &Gaz::get);
}
