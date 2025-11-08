#pragma once

#include <algorithm>
#include <chrono>
#include <vector>

namespace random_walk
{
struct Model
{
    Model(const int N);

    auto update(const std::chrono::duration<double> dt) -> void;

    std::vector<double> x{};
    std::vector<double> y{};
    std::vector<double> vx{};
    std::vector<double> vy{};
};
} // namespace random_walk
