#pragma once

#include <algorithm>
#include <chrono>
#include <vector>

namespace gravity
{
struct Model
{
    Model(const int N);

    auto update(const std::chrono::duration<double> dt) -> void;

    std::vector<double> x{};
    std::vector<double> y{};
    std::vector<double> vx{};
    std::vector<double> vy{};
    std::vector<double> ax{};
    std::vector<double> ay{};
    std::vector<double> m{};
};
} // namespace gravity
