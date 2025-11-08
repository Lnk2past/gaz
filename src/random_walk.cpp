#include "random_walk.hpp"

#include <algorithm>
#include <random>
#include <ranges>
#include <thread>

namespace random_walk
{
Model::Model(const int N) : x(N), y(N), vx(N), vy(N)
{
    auto eng = std::mt19937{1337};
    auto pos_dis = std::uniform_real_distribution{-500.0, 500.0};
    auto vel_dis = std::uniform_real_distribution{-10.0, 10.0};
    std::ranges::generate(x, [&] { return pos_dis(eng); });
    std::ranges::generate(y, [&] { return pos_dis(eng); });
    std::ranges::generate(vx, [&] { return vel_dis(eng); });
    std::ranges::generate(vy, [&] { return vel_dis(eng); });
}

auto Model::update(const std::chrono::duration<double> dt) -> void
{
    static constexpr auto n_threads = 8;
    auto threads = std::vector<std::jthread>{};
    threads.reserve(n_threads);

    auto slice = [&](auto start, auto end) {
        for (auto i = start; i < end; ++i)
        {
            x[i] += vx[i] * dt.count();
            y[i] += vy[i] * dt.count();
            if (x[i] < -500.0 || x[i] > 500.0)
            {
                vx[i] *= -1;
            }
            if (y[i] < -500.0 || y[i] > 500.0)
            {
                vy[i] *= -1;
            }
        }
    };

    auto s = x.size() / n_threads;
    for (auto i = std::size_t{}; i < n_threads; ++i)
    {
        auto start = i * s;
        auto end = start + s;
        end = end > x.size() ? x.size() - 1 : end;
        threads.emplace_back(slice, start, end);
    }
}
} // namespace random_walk